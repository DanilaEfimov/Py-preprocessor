
---

# Py-preprocessor

**Py-preprocessor** is an experimental preprocessor for the hypothetical Py++ language that adds powerful meta-directives and metaprogramming capabilities at compile time.
The project aims to enhance code expressiveness and simplify writing repetitive and conditional constructs.

---

## Features

* **@repeat(n)** — repeats the following code block `n` times at compile time
* **@mirror** — generates a mirrored (reversed) version of a string or list of literals
* **@random(\[...])** — selects one statement randomly from the provided list during compilation
* **@invisible** — hides code from introspection tools and compiler output
* **@debug\_only** — includes code only when compiling in debug mode
* **Conditional compilation:** `@if`, `@elif`, `@else`, `@endif` — allows writing code conditionally compiled based on compile-time expressions
* **@include** — inserts external source files inline during compilation, supports nested includes and prevents circular dependencies

---

## Quick Start

### Running

Run the preprocessor from the command line with required parameters:

```bash
preprocessor.bat -i sample/script.py -o sample/target.py -v -s sample/symbols.ini -d 10
```

Where:

* `-i` — input Py++ source file
* `-o` — output file for the preprocessed code (if omitted, input file is overwritten)
* `-v` — verbose output mode
* `-s` — path to symbols file
* `-d` — maximum include depth

---

## Directive Examples

```py++
@repeat(3)
print("Hello")

@mirror
print("abc")

@random(["print('A')", "print('B')", "print('C')"])

@invisible
_internal_boot()

@debug_only
print("Debug mode enabled")

@if DEBUG
print("Only in debug mode")
@endif

@include utils.pyp
```

---

## Error Handling

The preprocessor provides a detailed error code reference and hints to help quickly diagnose issues, such as:

* `-1`: missing parameters
* `1`: file not found or failed to open
* `103`: error opening file specified in `@include`
* `204`: missing directive at start of conditional block

---

## Project Structure

* `main.py` — entry point and main processing loop
* `parser.py` — command line argument parsing and validation
* `preprocess.py` — main preprocessing logic
* `common.py` — common structures, error codes, and constants

---

## License

MIT License © 2025 Danila Efimov

---

## Contacts

* GitHub: [https://github.com/DanilaEfimov/Py-preprocessor](https://github.com/DanilaEfimov/Py-preprocessor)
* Author: Danila Efimov

---
