from parser import is_void_flag, is_value, parse_include_parameter, VOID_FLAGS
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


def define_macros(path: str) -> int:
    ...


def conditional_compile(path: str) -> int:
    ...


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
    return 0    # <-- breaker for testing
    code = delete_comments(path)
    if code != 0:
        return code

    code = define_macros(path)
    if code != 0:
        return code

    code = conditional_compile(path)
    return code