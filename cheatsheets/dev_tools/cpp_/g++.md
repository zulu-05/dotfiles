# Cheatsheet: `g++` (GNU C++ Compiler)

This guide covers the basics of compiling C++ programs from the command line using `g++`.

## The Compilation Process

Compiling a C++ program is typically a two-stage process that `g++` handles for you:

1. **Compilation:** `g++` takes your human-readable source code (e.g., `hello.cpp`) and compiles it into machine-readable **object code** (`hello.o`). This object code contains the translated instructions but isn't a runnable program yet.
2. **Linking:** The **linker** (which `g++` also runs) takes one or more object files and "links" them together with any necessary system libraries to produce a final, runnable **executable** file.

## Basic Compilation (Single File)

This is the most common use case for simple programs.

### Common Usage

```bash
# Compile my_program.cpp and create an executable named 'my_program'
g++ my_program.cpp -o my_program

# Compile with all recommended warnings enabled (highly recommended)
g++ -Wall my_program.cpp -o my_program
```

If you omit the `-o` flag, `g++` will create an executable with the default name `a.out`.

## Compiling & Linking Multiple Files

For any non-trivial program, you will have your code split across multiple `.cpp` files. The standard workflow is to compile each source file into an object file first, and then link all the object files together.

### The Workflow

Let's say you have `main.cpp`, `utils.cpp`, and `utils.h`.

**Step 1: Compile each `.cpp` file into an object file (`.o`) using the `-c` flag.** The `-c` flag tells `g++` to compile _only_ and not run the linker.

```bash
g++ -Wall -c main.cpp -o main.o
g++ -Wall -c utils.cpp -o utils.o
```

You will now have `main.o` and `utils.o` in your directory.

**Step 2: Link the object files together to create the final executable.** Now you run `g++` on the object files. Since it doesn't see any `.cpp` files, it knows its only job is to link.

```bash
g++ main.o utils.o -o my_program
```

This creates the final `my_program` executable.

This modular approach saves time on large projects because you only need to recompile files that have changed.

## Common `g++` Flags

|Flag|Name|Description|
|---|---|---|
|**-o [file]**|**Output**|Specifies the name of the output file. If not supplied, the default is `a.out`.|
|**-Wall**|**Warnings (All)**|**Highly recommended.** Enables all the compiler's warning messages about questionable code. This will help you find many bugs before you even run your program.|
|**-g**|**Debug**|Includes debugging information in the executable. This is essential for using a debugger like `gdb` to step through your code and inspect variables.|
|**-c**|**Compile Only**|Compiles the source file into an object file (`.o`) but does not run the linker. This is the key to compiling multi-file projects.|
|**-I[dir]**|**Include Path**|Adds the directory `[dir]` to the list of places to search for header files (`#include <...>` files). For example, `-I/usr/local/include`.|
|**-L[dir]**|**Library Path**|Adds the directory `[dir]` to the list of places to search for library files.|
|**-l[lib]**|**Link Library**|Tells the linker to link against a specific library. For example, `-lm` links the math library.|

### `g++` Flag Demonstrations

Here are practical examples showing how to use the common `gcc` flags.

#### **-o (Output File)**

This flag lets you name your executable. Without it, the name defaults to `a.out`.

- **`hello.cpp`**

```cpp
#include <iostream>

int main() {
    std::cout << "Hello, C++!" << std::endl;
    return 0;
}
```

- **Compilation**:

```bash
# Compile hello.c and name the executable 'hello_world'
g++ hello.cpp -o hello_world

# Run the program
./hello_world
# Output: Hello, world!
```

#### **-Wall (All Warnings)**

This flag is crucial for catching potential bugs. It enables all standard compiler warnings.

- **`warning.cpp`**
 
```cpp
#include <iostream>

int main() {
    int x = 10; // This variable is initialised but never used
    std::cout << "This program has a warning." << std::endl;
    return 0;
}
    ```

- **Compilation**:

```bash
# Compile with -Wall to see the warning
gcc -Wall warning.cpp -o warning
# Output:
# warning.c: In function ‘main’:
# warning.c:4:9: warning: unused variable ‘x’ [-Wunused-variable]
#     4 |     int x = 10;
#       |         ^
```

#### **-g (Debug Information)**

Include this flag to prepare your executable for debugging with a tool like `gdb`. It adds necessary metadata to the file.

- **Compilation**:

```bash
# Compile a program with debugging symbols
g++ -Wall -g my_program.cpp -o my_program_debug

# You can now run the debugger on the output file
gdb ./my_program_debug
```

#### **-c (Compile Only)**

This flag creates an object file (`.o`) without running the linker. This is fundamental for building projects with multiple source files.

- **The Workflow**:

```bash
# 1. Compile main.cpp into main.o
g++ -Wall -c main.cpp -o main.o

# 2. Compile utils.cpp into utils.o
g++ -Wall -c utils.cpp -o utils.o

# 3. Link the object files into the final program
g++ main.o utils.o -o my_app
```

#### **-I (Include Path)**

Use this when your own header files are in a different directory.

- **Project Structure**:

```bash
my_project/
├── include/
│   └── my_header.h
└── src/
    └── main.cpp
```

- **Compilation**:

```bash
# Tell gcc to also look for headers in the 'include' directory
gcc -Wall -Iinclude src/main.c -o my_app
```

#### **-l and -L (Link Library and Library Path)**

Use `-l` to link against a shared library (like the math library, `libm`). Use `-L` to tell `g++` where to find that library if it's not in a standard location.

- **`math_program.cpp`**

```cpp
#include <iostream>
#include <cmath> // C++ header for maths functions
   
int main() {
    double val = pow(2, 10); // pow() is in the math library
    std::cout << "2 to the power of 10 is " << val << std::endl;
    return 0;
}
```

- **Compilation**:

```bash
# Link the math library using -lm
# The 'lib' prefix and '.so' or '.a' suffix are assumed by the linker
g++ -Wall math_program.c -o math_app -lm
```