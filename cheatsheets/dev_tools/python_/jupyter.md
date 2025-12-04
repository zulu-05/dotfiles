# Cheatsheet: Jupyter Notebooks

**Jupyter** is an interactive computing environment that allows code, text (Markdown), and visualisations to be combined into a single document. It is the standard tool for Data Science and exploratory Python programming.

## 1. Installation & Start

While Jupyter can be installed globally, best practice dictates installing it within the project's virtual environment to ensure dependency isolation.

| Command | Description |
| :--- | :--- |
| `pip install jupyterlab` | **Install.** Installs the modern Jupyter Lab interface (and the classic notebook). |
| `jupyter lab` | **Launch.** Starts the local server and opens the interface in the default browser. |
| `jupyter notebook` | **Legacy Launch.** Starts the older, classic Notebook interface. |

## 2. Virtual Environments & Kernels

A common issue is launching Jupyter and realising it cannot import packages installed in the active virtual environment. This happens because Jupyter does not automatically see every venv; it needs a **Kernel** to be registered.

### The Workflow: connecting a venv to Jupyter

1. **Activate the venv:**
   `source .venv/bin/activate`

2. **Install the Kernel helper:**
   `pip install ipykernel`

3. **Register the Kernel:**
   This command tells the global (or local) Jupyter installation that this specific Python environment exists.
   `python -m ipykernel install --user --name=my_project_env`

4. **Select the Kernel:**
   In the Jupyter interface (top right corner), click the kernel name (usually "Python 3") and switch it to "my_project_env".

   ## 3. Interface Shortcuts

   Jupyter uses a modal editing system similar to Vim.
   *  **Command Mode (Esc):** For navigating and manipulating cells.
   *  **Edit Mode (Enter):** For typing code or text inside a cell.

   | Key (Command Mode) | Action |
   | :--- | :--- |
   | `Shift + Enter` | **Run.** Execute current cell and move focus to the next one. |
   | `Ctrl + Enter` | **Run In-Place.** Execute current cell and keep focus on it. |
   | `a` | **Above.** Insert a new cell *above* the current one. |
   | `b` | **Below.** Insert a new cell *below* the current one. |
   | `d, d` | **Delete.** Press `d` twice to delete the current cell. |
   | `m` | **Markdown.** Convert the cell to text/documentation mode. |
   | `y` | **Code.** Convert the cell back to Python code mode. |

   ## 4. Magic Commands

   "Magics" are special commands that start with `%` (line magic) or `%%` (cell magic) to provide extra functionality beyond standard Python.

   | Command | Description |
   | :--- | :--- |
   | `%pip install <pkg>` | **Install.** Installs a package into the *current* running kernel. Always use this instead of running `!pip install` to avoid path mismatches. |
   | `%timeit` | **Benchmark.** Runs the line of code multiple times and reports the average execution time. |
   | `%%time` | **Timer.** Measures the execution time of the entire cell (run once). |
   | `%%writefile <name>` | **Export.** Writes the contents of the cell to a file (e.g., `%%writefile script.py`). |
   | `%who` | **Inspect.** Lists all variables currently in the global namespace. |
   | `! <command>` | **Shell.** Runs a standard shell command (e.g., `!ls -la`). |

   ## 5. Version Control (Git) Tips

   Jupyter Notebooks (`.ipynb`) are JSON files containing code, metadata, and *output* (including images). This makes them notoriously difficult to diff and merge in Git.

   **Best Practices:**
   1.  **Clear Output:** Before committing, go to `Kernel -> Restart Kernel and Clear All Outputs`. This reduces the file size and diff noise significantly.
   2.  **Jupytext:** Consider using thee `jupytext` extension. It can automatically pair your `.ipynb` file with a light `.py` script, allowing you to version control the loic without the noise of the JSON structure.
