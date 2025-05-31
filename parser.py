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


def init_symbol_table(lines) -> dict:
    """ symbol table file parser """
    symbols = {}    # macros
    for line in lines:
        line = line.strip()
        if not line or '=' not in line:
            continue    # pass empty lines
        symbol, value = map(str.split, line.split('=', 1))
        symbols[symbol] = value
    return symbols

""" vvv preprocessor's parse utils vvv """

def parse_include_parameter(directive: str):
    return directive.replace(MACRO_HANDLERS["include"], '').strip()