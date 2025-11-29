#!/usr/bin/env python3
"""
System Provisioning Manager
---------------------------
Manages the installation, status checking, and documentation generation
of the software ecosystem.

Usage:
    system_manager.py status
    system_manager.py install [--exclude <tool>...]
    system_manager.py generate-docs
"""

import argparse
import subprocess
import shutil
import sys
import json
import re
from dataclasses import dataclass, field
from typing import List, Optional, Protocol, Dict, Any
from concurrent.futures import ThreadPoolExecutor

# Third-party imports (Assumed present in environment)
try:
    import requests
    from rich.console import Console
    from rich.table import Table
    from rich.progress import track
    from rich import print as rprint
except ImportError:
    print("Error: 'rich' and 'requests' libraries are required.")
    print("pip install rich requests")
    sys.exit(1)


# --- Configuration ---
DOCS_PATH = "PROVISIONING.md"


# --- Interfaces ---

class PackageManager(Protocol):
    def get_installed_version(self, package_name: str, binary_name: str) -> Optional[str]:
        # ...

    def get_latest_version(self, package_name: str) -> Optional[str]:
        # ...

    def install(self, package_name: str) -> bool:
        # ...


# --- Implementations ---

class AptManager:
    def get_installed_version(self, package_name; str, binary_name: str) -> Optional[str]:
        # Check via dpkg first as it's more reliable for exact version
        try:
            res = subprocess.run(
                ["dpkg-query", "-W", "-f=${Version}", package_name],
                capture_output=True, text=True
            )
            if res.returncode == 0 and res.stdout.strip():
                return res.stdout.strip()
        except FileNotFoundError:
            pass
        return None

    def get_latest_version(self, package_name: str) -> Optional[str]:
        # Check what version the repo is offering (Candidate)
        try:
            res = subprocess.run(
                ["apt-cache", "policy", package_name],
                capture_output=True, text=True
            )
            if res.returncode == 0:
                for line in res.stdout.splitlines():
                    if "Candidate:" in line:
                        return line.split("Candidate:")[-1].strip()
        except FileNotFoundError:
            pass
        return None

    def install(self, package_name: str) -> bool:
        print(f" [apt] Installing {package_name}...")
        res = subprocess.run(["sudo", "apt", "install", "-y", package_name])
        return res.returncode == 0


class SnapManager:
    def get_installed_version(self, package_name: str, binary_name: str) -> Optional[str]:
        try:
            res = subprocess.run(["snap", "list", package_name], capture_output=True, text=True)
                if res.returncode == 0:
                    lines = res.stdout.splitlines()
                    if len(lines) > 1:
                        # Parse columns. Snap output is fixed width, but split() usually works
                        parts = lines[1].split()
                        if len(parts) >= 2:
                            return parts[1]
        except FileNotFoundError:
            pass
        return None

    def get_latest_version(self, package_name: str) -> Optional[str]:
        try:
            res = subprocess.run(["snap", "info", package_name], capture_output=True, text=True)
            if res.returncode == 0:
                for line in res.stdout.splitlines():
                    if "latest/stable:" in line:
                    # Line looks like: "latest/stable:  1.2.3   2023-01-01 (123) 50MB -"
                    parts = line.split()
                    if len(parts) >= 2:
                        return parts[1]
        except FileNotFoundError:
            pass
        return None

    def install(self, package_name: str) -> bool:
        print(f" [snap] Installing {package_name}...")
        res = subprocess.run(["sudo", "snap", "install", package_name])
        return res.returncode == 0


class PipManager:
    def get_installed_version(self, package_name: str, binary_name: str) -> Optional[str]:
        try:
            # Use importlib logic via CLI for safety
            res = subprocess.run(
                [sys.executable, "-m", "pip", "show", package_name],
                capture_output=True, text=True
            )
            if res.returncode == 0:
                for line in res.stdout.splitlines():
                    if line.startswith("Version:"):
                        return line.split(":", 1)[1].strip()
        except FileNotFoundError:
            pass
        return None

    def get_latest_version(self, package_name: str) -> Optional[str]:
        try:
            url = f"https://pypi.org/pypi/{package_name}/json"
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                return resp.json()["info"]["version"]
        except Exception:
            pass
        return None

    def install(self, package_name: str) -> bool:
        print(f" [pip] Installing {package_name}...")
        res = subprocess.run([sys.executable, "-m", "pip", "install", package_name])
        return res.returncode == 0


class CargoManager:
    def get_installed_version(self, package_name: str, binary_name: str) -> Optional[str]:
        # Cargo install list is slow, better to check the binary version if possible
        # Or parse `cargo install --list`
        try:
            res = subprocess.run(["cargo", "install", "--list"], capture_output=True, text=True)
            if res.returncode == 0:
                for line in res.stdout.splitlines():
                    if line.startswith(package_name):
                        # Line format: "package-name v1.2.3:"
                        match = re.search(r"v([\d.]+)", line)
                        if match:
                                return match.group(1)
        except FileNotFoundError:
            pass
        return None

    def get_latest_version(self, package_name: str) -> Optional[str]:
        try:
            url = f"https://crates.io/api/v1/crates/{package_name}"
            headers = {"User-Agent": "dotfiles-manager (contact@example.com)"}
            resp = requests.get(url, headers=headers, timeout=3)
            if resp.status_code == 200:
                return resp.json()["crate"]["max_version"]
        except Exception:
            pass
        return None

    def install(self, package_name: str) -> bool:
        print(f" [cargo] Installing {package_name}...")
        res = subprocess.run(["cargo", "install", package_name])
        return res.returncode == 0


class NpmManager:
    def get_installed_version(self, package_name: str, binary_name: str) -> Optional[str]:
        try:
            # Check global install list in JSON format
            res = subprocess.run(
                ["npm", "list", "-g", "--depth=0", "--json", package_name],
                capture_output=True, text=True
            )
            # npm returns non-zero if package is missing or tree is invalid
            # but we parse JSON regardless
            if res.stdout:
                data = json.loads(res.stdout)
                deps = data.get("dependencies", {})
                if package_name in deps:
                    return deps[package_name].get("version")
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        return None

    def get_latest_version(self, package_name: str) -> Optional[str]:
        try:
            res = subprocess.run(
                ["npm", "view", package_name, "version"],
                capture_output=True, text=True
            )
            if res.returncode == 0:
                return res.stdout.strip()
        except FileNotFoundError:
            pass
        return None

    def install(self, package_name: str) -> bool:
        print(f" [npm] Installing {package_name}...")
        res = subprocess.run(["sudo", "npm", "install", "-g", package_name])
        return res.returncode == 0


class LuaRocksManager:
    def get_installed_version(self, package_name: str, binary_name: str) -> Optional[str]:
        try:
            res = subprocess.run(["luarocks", "list", package_name], capture_output=True, text=True)
            for line in res.stdout.splitlines():
                # Output format usually: " 1.0.0-1 (installed) ..."
                if "(installed)" in line:
                    return line.strip().split()[0]
        except FileNotFoundError:
            pass
        return None

    def get_latest_version(self, package_name: str) -> Optional[str]:
        try:
            # --porcelain outputs: name \t version \t status \t path
            res = subprocess.run(
                ["luarocks", "search", "--porcelain", package_name],
                capture_output=True, text=True
            )
            versions = []
            for line in res.stdout.splitlines():
                parts = line.split("\t")
                if len(parts) >= 2 and parts[0] == package_name:
                    versions.append(parts[1])
            if versions:
                return versions[0] # Usually the first hit is the relevant one in search
        except FileNotFoundError:
            pass
        return None

    def install(self, package_name: str) -> bool:
        print(f" [luarocks] Installing {package_name}...")
        res = subprocess.run(["sudo", "luarocks", "install", package_name])
        return res.returncode == 0


class GemManager:
    def get_installed_version(self, package_name: str, binary_name: str) -> Optional[str]:
        try:
            res = subprocess.run(["gem", "list", "-e", package_name], capture_output=True, text=True)
            # Output: name (version)
            if res.returncode == 0 and package_name in res.stdout:
                match = re.search(r"\(([\d.]+\)", res.stdout)
                if match:
                    return match.group(1)
        except FileNotFoundError:
            pass
        return None

    def get_latest_version(self, package_name: str) -> Optional[str]:
        try:
            # Query RubyGems API
            url = f"https://rubygems.org/api/v1/gems/{package_name}.json"
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                return resp.json()["version"]
        except Exception:
            pass
        return None

    def install(self, package_name: str) -> bool:
        print(f" [gem] Installing {package_name}...")
        res = subprocess.run(["sudo", "gem", "install", package_name])
        return res.returncode == 0


class ComposerManager:
    """PHP Package Manager (Global)"""
    def get_installed_version(self, package_name: str, binary_name: str) -> Optional[str]:
        try:
            # Composer global show outputs info about a specific package
            # We capture stdout to find 'versions : * 1.2.3'
            res = subprocess.run(
                ["composer", "global", "show", package_name],
                capture_output=True, text=True
            )
            if res.returncode == 0:
                for line in res.stdout.splitlines():
                    if line.strip().startswith("versions"):
                        # Line format: "versions : * 2.5.5"
                        parts = line.split(":")
                        if len(parts) > 1:
                            # Remove the asterisk if present
                            return parts[1].replace("*", "").strip()
        except FileNotFoundError:
            pass
        return None

    def get_latest_version(self, package_name: str) -> Optional[str]:
        try:
            # Query Packagist API
            url = f"https://packagist.org/packages/{package_name}.json"
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                # Packagist returns all versions. We need the latest stable.
                versions = data.get("package", {}).get("versions", {})

                # Filter out dev-master, beta, etc.
                stable_versions = [
                    v for v in versions.keys()
                    if "dev" not in v and "beta" not in v and "alpha" not in v
                ]

                if stable_versions:
                    # Sort implies relying on version strings (basic sort),
                    # but usually the first one in the structure is most relevant or we rely on 'dist'.
                    # A naive max(stable_versions) works reasonably well for standard semantic versioning
                    return list(versions.key())[0] # The API usually lists latest first or we pick specifically
                    # For better precision we'd use 'packaging.version.parse', but let's keep it simple:
                    # The Packagist API JSON usually structures keys such that we can iterate.
        except Exception:
            pass
        return None

    def install(self, package_name: str) -> bool:
        print(f" [composer] Installing {package_name}...")
        res = subprocess.run(["composer", "global", "require", package_name])
        return res.returncode == 0


class DotnetManager:
    """source: NuGet via .NET CLI Global Tools"""
    def get_installed_version(self, package_name: str, binary_name: str) -> Optional[str]:
        try:
            # 'dotnet tool list -g' lists all installed tools
            res = subprocess.run(
                ["dotnet", "tool", "list", "-g"],
                capture_output=True, text=True
            )
                if res.returncode == 0:
                    for line in res.stdout.splitlines():
                    # Output: package.id        1.0.0       commands
                    if line.lower().startswith(package_name.lower()):
                        parts = line.split()
                        if len(parts) >= 2:
                            return parts[1]
        except FileNotFoundError:
            pass
        return None

    def get_latest_version(self, package_name: str) -> Optional[str]:
        try:
            # Query NuGet API
            url = f"https://api.nuget.org/v3-flatcontainer/{package_name.lower()}/index.json"
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                data = resp.json()
                versions = data.get("versions", [])
                if versions:
                    return versions[-1] # List is sorted chronologically
        except Exception:
            pass
        return None

    def install(self, package_name: str) -> bool:
        print(f" [dotnet] Installing {package_name}...")
        res = subprocess.run(["dotnet", "tool", "install", "-g", package_name])
        return res.returncode == 0


class SdkmanManager:
    """Java/JVM Environment Manager (SDKMAN!)"""
    # Note: SDKMAN is a shell function, so we must run it via bash -c with sourcing.

    SDK_INIT = "$HOME/.sdkman/bin/sdkman-init.sh"

    def _run_sdk(self, args: List[str]) -> subprocess.CompletedProcess:
        # Helper to source sdkman before running command
        cmd = f"source {self.SDK_INIT} && sdk {' '.join(args)}"
        return subprocess.run(cmd, shell=True, executable="/bin/bash", capture_output=True, text=True)

    def get_installed_version(self, package_name: str, binary_name: str) -> Optional[str]:
        # To check installed, we look at the 'current' output
        try:
            # Check filesystem directly to avoid slow shell spawning if possible
            # ~/.sdkman/candidates/<<candidate>/current -> points to version
            import os
            home = os.path.expanduser("~")
            link_path = os.path.join(home, ".sdkman", "candidates", package_name, "current")
            if os.path.islink(link_path):
                return os.path.basename(os.readlink(link_path))
        except Exception:
            pass
        return None

    def get_latest_version(self, package_name: str) -> Optional[str]:
        try:
            # SDKMAN has an undocumented API for default versions
            url = f"https://api.sdkman.io/2/candidates/{package_name}/default"
            resp = requests.get(url, timeout=3)
            if resp.status_code == 200:
                return resp.text.strip()
        except Exception:
            pass
        return None

    def install(self, package_name: str) -> bool:
        print(f" [sdkman] Installing {package_name}...")
        # Force bash to run the install
        res = self._run_sdk(["install", package_name])
        return res.returncode == 0


# add Java, PHP and .NET package managers

# --- Registry ---

MANAGERS = {
    "apt": AptManager(),
    "snap": SnapManager(),
    "pip": PipManager(),
    "cargo": CargoManager(),
    "npm": NpmManager(),
    "luarocks": LuaRocksManager(),
    "gem": GemManager(),
    "composer": ComposerManager(),
    "dotnet": DotnetManager(),
    "sdk": SdkmanManager(),
}

@dataclass
class Tool:
    name: str
    manager: str
    description: str
    binary: str = "" # If different from name
    context: str = "General"

    @property
    def binary_name(self):
        return self.binary if self.binary else self.name

TOOLS = [
    # Core Utilities
    Tool("git", "apt", "Version control", context="Core"),
    Tool("curl", "apt", "URL transfer tool", context="Core"),
    Tool("ripgrep", "apt", "Fast search (rg)", binary="rg", context="Core"),
    Tool("inotify-tools", "apt", "Filesystem monitoring", context="Core"),
    Tool("pass", "apt", "Password manager", context="Core"),
    Tool("wl-clipboard", "apt", "Wayland clipboard", context="Core"),

    # Python Environment 
    Tool("python3-venv", "apt", "Virtual environments", context="Python"),
    Tool("rich", "pip", "Terminal formatting", context="Python"),
    Tool("requests", "pip", "HTTP library", context="Python"),
    Tool("pynvim", "pip", "Neovim Python client", context="Python"),

    # Editor 
    Tool("neovim", "apt", "Text Editor", binary="nvim", context="Editor"),
    Tool("tree-sitter-cli", "cargo", "Parser generator", context="Editor"),
    Tool("glow", "apt", "Markdown renderer", context="Editor"),

    # Languages/Build
    Tool("build-essential", "apt", "GCC/Make", context="Languages"),
    Tool("cmake", "apt", "Build system", context="Languages"),
    Tool("nodejs", "apt", "JS Runtime", context="Languages"),
    Tool("npm", "apt", "JS Package Manager", context="Languages"),
    Tool("luarocks", "apt", "Lua Package Manager", context="Languages"),

    # Apps
    Tool("typora", "snap", "Markdown Editor", context="Apps"),
    Tool("docker", "snap", "Container Engine", context="Apps"),
    Tool("tree", "snap", "Directory visualizer", context="Apps"),

    # PHP Environment
    # Tool("laravel/installer", "composer", "Laravel CLI", binary="laravel", context="Languages"),
    
    # .NET Environment
    # Tool("dotnet-ef", "dotnet", "Entity Framework Core CLI", context="Languages"),
    # Tool("powershell", "dotnet", "PowerShell Core", binary-"pwsh", context="Core"),

    # JVM Environment
    # Tool("java", "sdk", "Java JDK", context="Languages"),
    # Tool("maven", "sdk", "Maven Build Tool", binary="mvn", context="Languages"),
    # Tool("gradle", "sdk", "Gradle Build Tool", context="Languages"),
]


# --- Core Logic ---

def get_tool_status(tool: Tool) -> Dict[str, Any]:
    mgr = MANAGERS.get(tool.manager)
    if not mgr:
        return {"tool": tool, "current": "Err", "latest": "Err", "status": "Error"}

    current = mgr.get_installed_version(tool.name, tool.binary_name)
    latest = mgr.get_latest_version(tool.name)

    # Determine status symbol
    status = "❌" # Not installed
    if current:
        if latest and current != latest:
            # Simple string comparison isn't perfect for semver but often sufficient
            # Real semver parsing would go here
            if current == latest:
                status = "✅"
            else:
                status = "🔄" # Update available
        else:
            status = "✅" # Installed, unknown latest, or match

    return {
        "tool": tool,
        "current": current if current else "Not Installed",
        "latest": latest if latest else "Unknown",
        "status_icon": status
    }


def cmd_status():
    console = Console()
    table = Table(title="System Software Status")

    table.add_column("Status", justify="center")
    table.add_column("Tool", style="cyan")
    table.add_column("Manager", style="magenta")
    table.add_column("Current Version", style="green")
    table.add_column("Latest Version", style="yellow")
    table.add_column("Description")

    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(track(executor.map(get_tool_status, TOOLS), total=len(TOOLS), description="Checking versions..."))

    for res in results:
        table.add_row(
            res["status_icon"],
            res["tool"].name,
            res["tool"].manager,
            res["current"],
            res["latest"],
            res["tool"].description
        )

    console.print(table)
    console.print("\n[dim]Legend: ✅ Up-to-date  🔄 Update available  ❌ Not installed  ❓ Unknown Manager[/dim]")


def cmd_install(exclude_list: List[str]):
    console = Console()
    to_install = [t for t in TOOLS if t.name not in exclude_list]

    console.print(f"[bold]Starting installation for {len(to_install)} tools...[/bold]")

    for tool in to_install:
        mgr = MANAGERS.get(tool.manager)
        if not mgr:
            console.print(f"[red]Error: No manager found for {tool.manager}[/red]")
            continue

        current = mgr.get_installed_version(tool.name, tool.binary_name)

        if current:
            console.print(f"[dim]Skipping {tool.name} (already installed: {current})[/dim]")
            continue

        if mgr.install(tool.name):
            console.print(f"[green]Successfully installed {tool.name}[/green]")
        else:
            console.print(f"[red]Failed to install {tool.name}[/red]")


def cmd_generate_docs():
    with open(DOCS_PATH, "w") as f:
        f.write("# System Provisioning & Ecosystem\n\n")
        f.write("This file is **automatically generated** by `bin/system_manager.py`.\n")
        f.write("Do not edit this file manually. Update the registry in the Python script instead.\n\n")

        # Group by context
        contexts = sorted(list(set(t.context for t in TOOLS)))

        for ctx in contexts:
            f.write(f"## {ctx}\n\n")
            f.write("| Software | Source | Description | Binary |\n")
            f.write("| :--- | :--- | :--- | :--- |\n")

            ctx_tools = [t for t in TOOLS if t.context == ctx]
            for t in ctx_tools:
                bin_display = f"`{t.binary}`" if t.binary else "*(Same)*"
                f.write(f"| **`{t.name}`** | `{t.manager}` | {t.description} | {bin_display} |\n")

            f.write("\n")

    print(f"Successfully generated {DOCS_PATH}")


# --- Main Entrypoint ---

def main():
    parser = argparse.ArgumentParser(description="Manage system software.")
    subparsers = parser.add_subparsers(dest="command")

    # Status Command
    subparsers.add_parser("status", help="Check versions of all tools")

    # Install Command
    install_parser = subparsers.add_parser("install", help="Install missing tools")
    install_parser.add_argument("--exclude", nargs="+", default=[], help="List of tools to skip")
    
    # Docs Command
    subparsers.add_parser("generate-docs", help="Regenerate PROVISIONING.md")

    args = parser.parse_args()

    if args.command == "status":
        cmd_status()
    elif args.command == "install":
        cmd_install(args.exclude)
    elif args.command == "generate-docs":
        cmd_generate_docs()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
