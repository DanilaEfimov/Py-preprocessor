ERROR_MANUALS = {
    0: {
        "msg": "all is done",
        "hint": "no hints, don't worry"
    },
    100: {
        "msg": "missed argument: input file path was not given",
        "hint": "Use the -i flag followed by the input file path, e.g., -i file.txt"
    },
    101: {
        "msg": "invalid value for void flag",
        "hint": "Void flags should be passed without a value (just the flag itself)."
    },
    102: {
        "msg": "missing or invalid value for flag",
        "hint": "Make sure to provide a value after the flag, e.g., -o output.txt"
    },
    103 : {
        "msg": "failed to open file directed as @include parameter",
        "hint": "Check out local path. It have to be relative ./preprocessor\n"
                "also path have not contains \"@include\"\n"
                "or file not exist"
    },
    104 : {
        "msg": "self-reference in included file's chain :: collect_includes(...)",
        "hint": "Check out how deep locate @include itself."
    }
}

MACRO_HANDLERS = {
    "include" : "@include",
    "mirror" : "@mirror",
}
