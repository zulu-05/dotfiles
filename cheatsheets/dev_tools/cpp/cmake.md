# Cheatsheet: `CMake` (Cross-Platform Make)

This guide covers the fundamentals of using `CMake` to manage the build process for C/C++ projects.

## What is CMake?

CMake is **not a build system**—it doesn't compile or link code. Instead, CMake is a **build system generator**.

- **The Problem:** A C++ project needs a `Makefile` to be built on Linux, but a `Visual Studio Solution` (`.sln`) to be built on Windows. Maintaining both is difficult.
- **The Solution:** You write a single, cross-platform configuration file called `CMakeLists.txt`. You then run `cmake` on this file, and it automatically generates the native build files for your specific platform (e.g., it generates a `Makefile` on Linux).

This allows you to manage your project's build process from one source of truth.

## The Standard Workflow

The canonical way to build a CMake project is "out-of-source," which keeps all build artifacts separate from your source code.

Let's assume your project has a `CMakeLists.txt` file at its root.

**Step 1: Create and enter a build directory.** This keeps your main project directory clean.

```bash
mkdir build
cd build
```

**Step 2: Run `cmake` to configure the project and generate build files.** The `..` tells CMake to look for the `CMakeLists.txt` file in the parent directory.

```bash
cmake ..
```

**Step 3: Run the native build tool to compile and link your code.** On Linux, this is typically `make`. CMake generates a `Makefile` that `make` knows how to use.

```bash
make
```

**Step 4: Run your executable.** The compiled program will be located inside the `build` directory.

```bash
./my_program
```

## Anatomy of a `CMakeLists.txt`

This is the heart of CMake. It's a plain text file containing a series of commands that define your project's targets and dependencies.

Here is a heavily annotated example for a project with an executable (`main.cpp`) that uses a local library (`math_utils`).

**Project Structure:**

```bash
.
├── CMakeLists.txt
├── main.cpp
└── math_utils/
    ├── CMakeLists.txt
    ├── include/
    │   └── math_utils.h
    └── src/
        └── math_utils.cpp
```

**`./CMakeLists.txt` (Top-Level)**

```cmake
# Specify the minimum version of CMake required. This ensures compatibility.
cmake_minimum_required(VERSION 3.10)

# Define the project name, version, and language.
project(MyAwesomeApp VERSION 1.0 LANGUAGES CXX)

# Add the subdirectory containing our library. CMake will process the
# CMakeLists.txt file inside that directory.
add_subdirectory(math_utils)

# Define the executable target.
# The first argument is the name of the executable to create.
# Subsequent arguments are the source files needed to build it.
add_executable(my_program main.cpp)

# Link our executable against the library we defined in the subdirectory.
# This tells the linker that 'my_program' depends on 'math_utils'.
target_link_libraries(my_program PRIVATE math_utils)
```

**`./math_utils/CMakeLists.txt` (Library)**

```cmake
# Define the library target.
# 'math_utils' is the name we'll use to refer to this library.
# 'src/math_utils.cpp' is the source file for the library.
add_library(math_utils src/math_utils.cpp)

# Specify the include directories for this target.
# This tells CMake that any target linking against 'math_utils' should
# have the 'math_utils/include' directory in its include path.
# This is how #include "math_utils.h" will work.
target_include_directories(math_utils PUBLIC include)
```

## Common CMake Commands

|Command|Description|
|---|---|
|`cmake_minimum_required()`|Sets the minimum required version of CMake. Always the first line.|
|`project()`|Defines the name and other top-level properties of the project.|
|`add_executable(name sources...)`|Creates an executable target from the given source files.|
|`add_library(name sources...)`|Creates a library target from the given source files.|
|`target_include_directories(target visibility dirs...)`|Specifies the include directories for a target. `PUBLIC` means consumers of the library also get these include directories.|
|`target_link_libraries(target visibility libs...)`|Links a target against other libraries. This can be other CMake targets or system libraries.|

## Finding & Using External Libraries

A primary job of CMake is to find libraries already installed on the system. This is done with `find_package`.

**Example: Finding and using the system's Threads library.**

```cmake
# Tell CMake to find the built-in Threads package. The 'REQUIRED' keyword
# will cause CMake to fail if the package cannot be found.
find_package(Threads REQUIRED)

# Define our executable
add_executable(my_threaded_app main.cpp)

# Link our executable against the Threads library.
# CMake automatically creates an imported target (e.g., Threads::Threads)
# that we can link against. This handles all the necessary compiler and
# linker flags for us.
target_link_libraries(my_threaded_app PRIVATE Threads::Threads)
```