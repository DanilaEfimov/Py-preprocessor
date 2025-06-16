"""
    valid input format : -i @file_to_preprocessing
    other flags:
    -s @symbols_table_file
    -o @target_file
    -v @verbose output
"""

from common import MACRO_HANDLERS

""" vvv CLI interface flags and other definitions vvv """
VOID_FLAGS = {"-v"}
FLAGS_WITH_VALUES = {"-i", "-o", "-s"}


def is_value(pattern: str) -> bool:
    return pattern is not None and not is_flag(pattern)


def is_flag(pattern : str) -> bool:
    return pattern in VOID_FLAGS or pattern in FLAGS_WITH_VALUES


def is_void_flag(flag: str) -> bool:
    return flag in VOID_FLAGS


def parse_main_input(argv) -> dict:
    config = {}     # [arg, val] pairs dict
    argc = len(argv)
    i = 0
    while i < argc:
        arg = argv[i]

        if is_flag(arg):    # every patter is flag or value
            flag = arg

            if not is_void_flag(flag):          # read value
                if i + 1 < argc:
                    i += 1
                    token = argv[i]
                    if is_value(token):
                        config[flag] = token    # set flag in config
                        i += 1
                    else:
                        config[flag] = None     # missed value | fatal error
                        i += 1
                else:
                    config[flag] = None         # missed value | fatal error
                    i += 1

            else:
                config[flag] = True         # set void flag in config
                i += 1
        else:
            # TODO soon here will able be macro parse part
            # ignore undefined args
            i += 1
    return config


def init_symbol_table(path: str) -> dict:
    """ symbol table file parser """
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except OSError:
        return {}

    symbols = {}    # macros
    for line in lines:
        line = line.strip()
        if not line or '=' not in line:
            continue    # pass empty lines
        symbol, value = map(str.strip, line.split('=', 1))
        symbols[symbol] = value
    return symbols

""" vvv preprocessor's parse utils vvv """

def parse_conditional_blocks(path: str) -> list[str]:
    ...


def is_directive(line: str) -> bool:
    return line in MACRO_HANDLERS


def parse_define_directive(line: str) -> tuple[int, str, str, str]:
    line = line.strip()
    define = MACRO_HANDLERS["define"]
    undef = MACRO_HANDLERS["undef"]

    if line.startswith(define):
        parts = line.split(maxsplit=2)
        if len(parts) < 2:
            return 200, define, "", ""
        symbol = parts[1]
        value = parts[2] if len(parts) > 2 else ""
        return 0, define, symbol, value

    elif line.startswith(undef):
        parts = line.split(maxsplit=2)
        if len(parts) < 2:
            return 200, undef, "", ""
        symbol = parts[1]
        return 0, undef, symbol, ""

    else:
        return 200, "", "", ""


def is_define_directive(directive : str) -> bool:
    return directive in {
        MACRO_HANDLERS["define"],
        MACRO_HANDLERS["undef"]
    }


def is_conditional_directive(directive: str) -> bool:
    return directive in {
        MACRO_HANDLERS["ifdef"],
        MACRO_HANDLERS["ifndef"],
        MACRO_HANDLERS["else"],
        MACRO_HANDLERS["elif"],
        MACRO_HANDLERS["endif"],
    }


def directive_in_line(line: str) -> bool:
    stripped = line.strip().split(maxsplit=1)
    return stripped and stripped[0] in MACRO_HANDLERS.values()


def parse_include_parameter(directive: str):
    return directive.replace(MACRO_HANDLERS["include"], '').strip()
