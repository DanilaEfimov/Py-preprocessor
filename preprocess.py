import re

import parser
from parser import is_void_flag, is_value, parse_include_parameter, directive_in_line, parse_define_directive, is_define_directive, is_conditional_directive, VOID_FLAGS
from common import ERROR_MANUALS, MACRO_HANDLERS


def _endif(lines: list[str]) -> list[str]:
    ...


def _else(lines: list[str]) -> list[str]:
    ...


def _elif(lines: list[str]) -> list[str]:
    ...


def _if(lines: list[str]) -> list[str]:
    ...


def _debug_only(lines: list[str]) -> list[str]:
    ...


def _invisible(lines: list[str]) -> list[str]:
    ...


def _random(lines: list[str]) -> list[str]:
    ...


def _mirror(lines: list[str]) -> list[str]:
    ...


def _repeat(lines: list[str]) -> list[str]:
    ...


def expand_macros(path: str, symbols: dict) -> int:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        expanded_lines = []
        for line in lines:
            for macro, value in symbols.items():
                line = re.sub(rf'\b{re.escape(macro)}\b', value, line)
            expanded_lines.append(line)

        with open(path, "w", encoding="utf-8") as f:
            f.writelines(expanded_lines)
        return 0

    except OSError:
        return 1


def get_block_bounds(lines: list[str]) -> tuple[int, int]:
    # find ONLY open directive (not end before start)
    # find last closing directive in this scope
    # return numbers of start and end
    ...


def solve_block(lines: list[str]) -> list[str]:
    # split conditional branches
    # select condition instructions
    # find correct condition
    # return branch
    ...


def conditional_compile(lines: list[str], symbols: dict) -> list[str]:
    have_conditional_blocks = True
    while have_conditional_blocks:
        start, end = get_block_bounds(lines)    # find the boundaries of a conditional block
        if start == end:
            have_conditional_blocks = False

        branch = solve_block(lines[start:end])  # solve block (returns correct branch)
        lines[start:end] = branch               # replace all block to solution
    return lines
#TODO: вместо реккурсивного или итеративного решения со стеком можно просто
#TODO: смещать счетчил строк на начало выполненной ветви

def delete_comments(path: str) -> int:
    ...


def collect_includes(path: str, chain: list[str]) -> tuple[int, list[str]]:
    include_macro = MACRO_HANDLERS["include"]

    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            result = []

            for line in lines:
                if include_macro in line:
                    include_path = parse_include_parameter(line)
                    if include_path in chain:
                        return 104, []
                    else:
                        code, included_lines = collect_includes(include_path, chain + [include_path])

                        if code != 0:
                            return code, []
                        result.extend(included_lines)
                else:
                    result.append(line)

            return 0, result

    except OSError as e:
        return 103, [str(e)]


def include_files(_input: str, _output: str) -> int:
    try:
        with open(_input, "r", encoding="utf-8") as f:
            code, lines = collect_includes(_input, [])
            if code != 0:
                return code

        with open(_output, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return 0

    except OSError:
        return 103

def report_error(code: int):
    err = ERROR_MANUALS.get(code)
    if err:
        print(err["msg"])
        print("Hint:", err["hint"])
    else:
        print(f"Unknown error code: {code}")


def init_triggers(config: dict) -> dict:
    return {flag: config.get(flag, False) is True for flag in VOID_FLAGS}


def is_valid_config(config: dict) -> int:
    if "-i" not in config:
        return 100

    for flag, value in config.items():
        if is_void_flag(flag):
            if value is not True:
                return 101
        else:
            if not is_value(value):
                return 102

    return 0


def preprocess(config: dict) -> int:
    # noexcept(false)

    _input = config["-i"]
    _output = config["-o"]
    _symbol_table = config["-s"]

    code = include_files(_input, _output)
    if code != 0:
        return code

    symbols = parser.init_symbol_table(_symbol_table)
    with open(_output, "r", encoding="utf-8") as f:
        lines = f.readlines()
        lines = conditional_compile(lines, symbols)
        if code != 0:
            return code
    with open(_output, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return 0    # <-- breaker for testing