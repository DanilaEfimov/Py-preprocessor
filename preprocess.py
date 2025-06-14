import re
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


def replace_conditional_block(lines: list[str], symbols: dict) -> list[str]:
    ...


def conditional_compile(lines: list[str], symbols: dict) -> (list[str], dict):
    _define =   MACRO_HANDLERS["define"]
    _undef =    MACRO_HANDLERS["undef"]
    _ifdef =    MACRO_HANDLERS["ifdef"]
    _ifndef =   MACRO_HANDLERS["ifndef"]
    _else =     MACRO_HANDLERS["else"]
    _elif =     MACRO_HANDLERS["elif"]
    _endif =    MACRO_HANDLERS["endif"]

    # TODO: debug conditional compiling stuff and select functional blocks for refactoring
    try:
        i = 0
        while i < (len(lines)):
            line = lines[i].strip()
            words = line.split(' ')
            count = len(words)
            if count > 0:
# conditional checking
                if (words[0] == _ifdef or words[0] == _ifndef) and count == 2:
                    opening = int(i)
                    i += 1  # next line
                    block = [line]
                    while line != _endif and i < len(lines):
                        line = lines[i].strip()
                        block.append(line)
                        i += 1  # next line
                    if i == len(lines):
                        raise 203
                    closing = int(i)
                    block = replace_conditional_block(block, symbols)
                    lines[opening:closing], symbols = conditional_compile(block, symbols)
# define checking
                elif words[0] == _define:
                    if count == 3:
                        symbol = words[1]
                        value = words[2]
                        symbols[symbol] = str(value)
                    else:
                        raise 200
# undef checking
                elif words[0] == _undef:
                    if count == 2:
                        symbol = words[1]
                        if symbol in symbols:
                            symbols.pop(symbol)
                        else:
                            raise 201
                    else:
                        raise 200
# undefined directive checking
                elif words[0][0] == '@':    # directive pattern
                    raise 202
        return 0
    except int as code:
        return code  # error


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


def include_files(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8") as f:
            code, lines = collect_includes(path, [])
            if code != 0:
                return code

        with open(path, "w", encoding="utf-8") as f:
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


def preprocess(path: str) -> int:
    code = include_files(path)
    if code != 0:
        return code

    code = conditional_compile(path, )
    if code != 0:
        return code

    return 0    # <-- breaker for testing
    code = delete_comments(path)
    if code != 0:
        return code

    return 0