import re

from parser import is_void_flag, is_value, parse_include_parameter, is_define_directive, is_conditional_directive, init_symbol_table, VOID_FLAGS
from common import ERROR_MANUALS, MACRO_HANDLERS
from custom_directives import _debug_only, _mirror, _random, _repeat, _invisible


def is_directive(line: str) -> bool:
    return line in MACRO_HANDLERS.values()


def is_opening_of_block(line: str) -> bool:
    return line in {
        MACRO_HANDLERS["ifdef"],
        MACRO_HANDLERS["ifndef"]
    }


def is_branch_terminator(line: str) -> bool:
    return line in {
        MACRO_HANDLERS["endif"],
        MACRO_HANDLERS["elif"],
        MACRO_HANDLERS["else"]
    }


def is_defined_symbol(symbol: str, symbols: dict) -> bool:
    return symbol in symbols


def is_open_block_directive(line: str) -> bool:
    return line in {
        MACRO_HANDLERS["ifdef"],
        MACRO_HANDLERS["ifndef"]
    }



def is_define_directive(line: str) -> bool:
    return line in {
        MACRO_HANDLERS["define"],
        MACRO_HANDLERS["undef"]
    }


def solve_condition_directive(directive: str, symbols: dict) -> bool:
    words = directive.strip().split(' ')
    if words[0] == MACRO_HANDLERS["ifdef"] or words[0] == MACRO_HANDLERS["elif"]:
        if len(words) < 2:
            raise 200
        symbol = words[1]
        return is_defined_symbol(symbol, symbols)

    elif words[0] == MACRO_HANDLERS["ifndef"]:
        if len(words) < 2:
            raise 200
        symbol = words[1]
        return not is_defined_symbol(symbol, symbols)

    elif words[0] == MACRO_HANDLERS["else"]:
        return True


def solve_define_macros(directive: str, symbols: dict) -> None:
    words = directive.strip().split(' ')
    if words[0] == MACRO_HANDLERS["define"]:
        if len(words) < 3:
            raise 200
        var = words[1]
        val = words[2]
        symbols[var] = val
    elif words[0] == MACRO_HANDLERS["undef"]:
        if len(words) < 2:
            raise 200   # invalid syntax
        symbol = words[1]
        if is_defined_symbol(symbol, symbols):
            symbols.pop(symbol)
        else:
            raise 201   # undefined symbol under cursor


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
    except int as code:
        return code


def read_macros_defines(lines: list[str], symbols: dict) -> None:
    for line in lines:
        words = line.strip().split(' ')
        if is_define_directive(words[0]):
            solve_define_macros(line, symbols)


def get_conditional_branch(lines: list[str]) -> list[str]:
    end = 0
    flag = False
    staples = 1
    for i in range(1,len(lines)):
        line = lines[i].strip()
        words = line.split(' ')
        if is_branch_terminator(words[0]):
            staples -= 1
            if staples == 0:
                end = i
                flag = True
                break
        elif is_open_block_directive(words[0]):
            staples += 1

    if not flag:
        raise 203

    return lines[1:end]


def get_block_bounds(lines: list[str]) -> tuple[int, int]:
    # find ONLY open directive (not end before start)
    # find last closing directive in this scope
    # return numbers of start and end
    start, end = 0, 0
    flag = False
    for i in range(len(lines)):
        line = lines[i].strip()
        words = line.split(' ')
        if is_open_block_directive(words[0]):
            start = i
            flag = True
            break
        elif is_branch_terminator(words[0]):
            raise 204

    if not flag:
        return 0, 0

    staples = 1
    for i in range(start + 1,len(lines)):
        line = lines[i].strip()
        words = line.split(' ')
        if is_open_block_directive(words[0]):
            staples += 1
        elif words[0] == MACRO_HANDLERS["endif"]:
            staples -= 1
            if staples == 0:
                end = i
                break

    if end == 0:
        raise 203

    return start, end


def solve_block(lines: list[str], symbols: dict) -> list[str]:
    # split conditional branches
    # select condition instructions
    # find correct condition
    # return branch
    for i in range(len(lines)):
        line = lines[i].strip()
        words = line.split(' ')
        if is_conditional_directive(words[0]):
            solved = solve_condition_directive(line, symbols)
            if solved:
                remains = lines[i:]
                branch = get_conditional_branch(remains)
                return branch

    return []


def conditional_compiled_text(lines: list[str], symbols: dict) -> list[str]:
    while True:
        start, end = get_block_bounds(lines)    # find the boundaries of a conditional block

        read_macros_defines(lines[0:start], symbols)
        if start == end:
            break

        branch = solve_block(lines[start:], symbols)  # solve block (returns correct branch)
        lines[start:end+1] = branch               # replace all block to solution
    return lines


def conditional_compiling(_input: str, _output: str, symbols: dict) -> int:
    try:
        with open(_output, "r", encoding="utf-8") as f:
            lines = f.readlines()
            lines = conditional_compiled_text(lines, symbols)
        with open(_output, "w", encoding="utf-8") as f:
            f.writelines(lines)
    except OSError as e:
        print(str(e))
    except int as code:
        return code

    return 0


def delete_used_directives(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
            striped = lines[i].strip()
            words = striped.split(' ')
            if len(words) == 0:
                continue
            elif is_directive(words[0]):
                lines.pop(i)
                i = 0
            else:
                i += 1
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
    except OSError as e:
        print(str(e))
        return 1
    except int as code:
        return code

    return 0

#           vvv custom directives vvv

def custom_preprocessing(path: str) -> int:
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        lines = follow_custom_directives(lines)
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(lines)
        return 0

    except int as code:
        return code
    except OSError:
        return -1


def follow_custom_directives(lines: list[str]) -> list[str]:
    lines = _repeat(lines)
    lines = _invisible(lines)
    lines = _debug_only(lines)
    lines = _random(lines)
    return lines


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


def preprocessing(config: dict) -> int:
    # noexcept(false)

    _input = config["-i"]
    _output = config["-o"]
    _symbol_table = config["-s"]

    code = include_files(_input, _output)
    if code != 0:
        return code

    symbols = init_symbol_table(_symbol_table)
    code = conditional_compiling(_input, _output, symbols)
    if code != 0:
        return code

    code = custom_preprocessing(_output)
    if code != 0:
        return code

    code = delete_used_directives(_output)  # it must be followed before expanding, it's safer this way
    if code != 0:
        return code

    code = expand_macros(_output, symbols)
    if code != 0:
        return code
    return code