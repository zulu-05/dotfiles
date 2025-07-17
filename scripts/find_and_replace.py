#!/usr/bin/env python3
import os
import argparse

def find_replace(directory, find, replace, pattern="*"):
    from fnmatch import fnmatch
    for path, _, files in os.walk(directory):
        for name in files:
            if fnmatch(name, pattern):
                filepath = os.path.join(path, name)
                with open(filepath) as f:
                    s = f.read()
                if find in s:
                    print(f"Replacing in: {filepath}")
                    s = s.replace(find, replace)
                    with open(filepath, "w") as f:
                        f.write(s)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find and replace text in files.")
    parser.add_argument("find", help="The text to find.")
    parser.add_argument("replace", help="The text to replace with.")
    parser.add_argument("directory", help="The directory to search in.", default=".", nargs="?")
    parser.add_argument("--pattern", help="File pattern to search for (e.g., '*.py').", default="*")
    args = parser.parse_args()

    find_replace(args.directory, args.find, args.replace, args.pattern)
