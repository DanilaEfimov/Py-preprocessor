ERROR_MANUALS = {
    -2: {
        "msg" : "undefined error",
        "hint": "it may be Python error: TypeError, ValueError and so on...\n"
                "advise to try debug"
    },
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
                "also path have not contains '@include'\n"
                "or file not exist"
    },
    104 : {
        "msg": "self-reference in included file's chain :: collect_includes(...)",
        "hint": "Check out how deep locate @include itself."
    },
    200 : {
        "msg" : "invalid directive's syntax.",
        "hint" : "for @define : @define 'name' 'value'\n"
                 "for @undef - same and so on\n"
                 "look at manuals"
    },
    201 : {
        "msg" : "undefined symbol directed as @undef parameter",
        "hint" : "check macro name and included files"
    },
    202 : {
        "msg" : "undefined directive",
        "hint" : "check directives in target and included files"
    },
    203 : {
        "msg" : "missed directive of the end of the conditional block or branch",
        "hint" : "for every opening of conditional block must be end-directive\n"
                 "end conditional directives: @elif @endif @else ..."
    },
    204 : {
        "msg" : "missed directive of the start of the conditional block or branch",
        "hint" : "for every closing of conditional block must be start-directive\n"
                 "start conditional directives: @ifdef, @ifndef"
    },
    205 : {
        "msg" : "cannot parse conditional block",
        "hint" : "check directives syntax in manuals"
    }
}

MACRO_HANDLERS = {
    "include" :     "@include",
    "define" :      "@define",
    "undef" :       "@undef",
    "ifdef" :       "@ifdef",
    "ifndef" :      "@ifndef",
    "else" :        "@else",
    "elif" :        "@elif",
    "endif" :       "@endif",
    "mirror" :      "@mirror",
    "repeat" :      "@repeat",
    "invisible" :   "@invisible",
    "debug_only" :  "@debug_only",
    "random" :      "@random"
}
