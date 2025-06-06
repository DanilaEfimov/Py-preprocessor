ERROR_MANUALS = {
    -1: {
        "msg": "parameters nave not given",
        "hint": "try to use CLI and read manuals"
    },
    0: {
        "msg": "all is done",
        "hint": "no hints, don't worry"
    },
    1 : {
        "msg" : "failed to open file, or file not exist.",
        "hint" : "check it out, local paths and all that"
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
    },
    200 : {
        "msg" : "invalid define directive's syntax.",
        "hint" : "for @define : @define @arg@ (arg is name of macro)\n"
                 "for @undef - same"
    },
    201 : {
        "msg" : "undefined symbol directed as @undef parameter",
        "hint" : "check macro name and included files"
    },
    202 : {
        "mag" : "undefined directive",
        "hint" : "check directives in target and included files"
    }
}

MACRO_HANDLERS = {
    "include" :     "@include",
    "define" :      "@define",
    "undef" :       "@undef",
    "if" :          "@if",
    "else" :        "@else",
    "elif" :        "@elif",
    "endif" :       "@endif",
    "mirror" :      "@mirror",
    "repeat" :      "@repeat",
    "invisible" :   "@invisible",
    "debug_only" :  "@debug_only",
    "random" :      "@random"
}
