from parser import is_void_flag, is_value, VOID_FLAGS


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


def conditional_compile(path: str) -> None:
    ...


def delete_comments(path: str) -> None:
    ...


def include_files(path: str) -> None:
    ...


def init_triggers(config: dict) -> dict:
    return {flag: config.get(flag, False) is True for flag in VOID_FLAGS}


def is_valid_config(config: dict) -> tuple[bool, str]:
    if "-i" not in config:
        return False, "missed argument: input file path was not given\n"

    for flag, value in config.items():
        if is_void_flag(flag):
            if value is not True:
                return False, f"invalid value for void flag {flag}\n"
        else:
            if not is_value(value):
                return False, f"missing or invalid value for flag {flag}\n"

    return True, "ready to preprocessing"