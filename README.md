# RASM

RASM (Readable Assembly) is a simple assembly-like language that compiles into NASM assembly.  
The transpiler is written in Python.

---

## Why RASM?

RASM was created to make assembly easier to read and understand, especially for beginners.

Traditional assembly languages are powerful but often difficult to learn due to:
- low-level syntax
- minimal readability
- historical design constraints from early CPUs

RASM aims to provide a more readable abstraction while still compiling down to real assembly.

---

## How it works

The compiler reads a `.rasm` file and processes it in several steps:

1. Reads the file line by line  
2. Removes comments  
3. Tokenizes each line  
4. Detects the current section (`.data` or `.text`)  
5. Applies the appropriate parsing rules  

---

## Text section

The text section translates RASM instructions into their NASM equivalents.

It also handles:
- user-defined labels
- external symbols (`extern`)
- data symbols from the `.data` section

---

## Data section

The data section defines variables and constants.

Each line follows this format:

[name] [type] [value]

e.g:
```asm
    num byte 1
    msg string "Hello, world!"
```

## Example:
```asm
section data
    num byte 1
    msg string "Hello"

section text

global _start

_start:
    move reg_A_64, reg_C_64
    add reg_A_64, num
    return
```

**Output**:
```asm
section .data
num db 1
msg db "Hello", 0

section .text

global _start

_start:
mov rax, rcx
add rax, num
ret
```

## Goals
- Improve readability of assembly for beginners
- Provie a simple compilation pipeline in Python
- Serve as a learning project for compilers and low-level programming