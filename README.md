
---

# Py-preprocessor ⚙️

**Py-preprocessor** is an experimental compile-time preprocessor for the hypothetical Py++ language, designed to enhance code expressiveness through meta-directives and conditional compilation.

---

## Features ✨

* `@repeat(n)` — repeats the following code block `n` times at compile time
* `@mirror` — generates a reversed version of a string or literal list
* `@random([...])` — selects a single statement randomly from a list at compile time
* `@invisible` — hides code from introspection and compiler output
* `@debug_only` — includes code only when compiled in debug mode
* Conditional compilation directives: `@if`, `@elif`, `@else`, `@endif`
* `@include` — inserts external source files inline, supports nested includes and detects circular dependencies

---

## Usage ▶️

Run the preprocessor via command line with parameters:

```bash
git clone https://github.com/DanilaEfimov/Py-preprocessor.git
cd Py-preprocessor
preprocessor.bat -i sample/script.py -o sample/target.py -v -s sample/symbols.ini -d 10

```

Parameters:

* `-i` — input Py++ source file
* `-o` — output file for preprocessed code (defaults to input file if omitted)
* `-v` — verbose output mode
* `-s` — path to symbols file
* `-d` — maximum include depth

---

## Example Directives 💡

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

@ifdef DEBUG
print("Only in debug mode")
@endif

@include utils.pyp
```

---

## Error Codes ⚠️

* `-1` — missing parameters
* `1` — file not found or cannot be opened
* `103` — failed to open file specified in `@include`
* `204` — missing start directive for conditional block

---

## Project Structure 📂

* `main.py` — entry point and main logic
* `parser.py` — command line parsing and validation
* `preprocess.py` — preprocessing engine
* `common.py` — common constants and error codes

---

## License

MIT License © 2025 Danila Efimov

---

## Contact

GitHub: [https://github.com/DanilaEfimov/Py-preprocessor](https://github.com/DanilaEfimov/Py-preprocessor)

---
