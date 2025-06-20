"""
    valid input format : -i @file_to_preprocessing
    other flags:
    -s @symbols_table_file
    -o @target_file
    -v @verbose output
    -d @depth of directives including
"""

from common import MACRO_HANDLERS

""" vvv CLI interface flags and other definitions vvv """

VOID_FLAGS = {"-v"}
FLAGS_WITH_VALUES = {"-i", "-o", "-s", "-d"}
NUMERIC_FLAGS = {"-d"}

def is_value(pattern: str) -> bool:
    return pattern is not None and not is_flag(pattern)


def is_flag(pattern : str) -> bool:
    return pattern in VOID_FLAGS or pattern in FLAGS_WITH_VALUES


def is_void_flag(flag: str) -> bool:
    return flag in VOID_FLAGS


def is_num_flag(flag: str) -> bool:
    return flag in NUMERIC_FLAGS


def is_valid_void_value(flag: str, value) -> bool:
    return value is True


def is_valid_numeric_value(flag: str, value) -> bool:
    # noexcept(false)
    if flag == "-d":
        return int(value) > 0
    raise 106


def init_triggers(config: dict) -> dict:
    return {flag: config.get(flag, False) is True for flag in VOID_FLAGS}


def is_valid_config(config: dict) -> int:
    if "-i" not in config:
        return 100   # missed -input argument

    for flag, value in config.items():
        if is_void_flag(flag):
            if not is_valid_void_value(flag, value):
                return 101   # invalid value for void flag
        elif is_num_flag(flag):
            if not is_valid_numeric_value(flag, value):
                return 105
        elif not is_value(value):
                return 102   # invalid value for flag
    return 0    # valid config


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
    }


def parse_include_parameter(directive: str):
    return directive.replace(MACRO_HANDLERS["include"], '').strip()
