import ast
import random
import re

def _debug_only(lines: list[str]) -> list[str]:
    new_lines = []
    for line in lines:
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        words = stripped.split(maxsplit=1)

        if words and words[0] == CUSTOM_DIRECTIVES["debug_only"]:
            modified_line = ' ' * indent + "if __debug__:\n"
            new_lines.append(modified_line)
        else:
            new_lines.append(line)
    return new_lines


def _invisible(lines: list[str]) -> list[str]:
    i = 0
    while i < len(lines):
        if i + 1 == len(lines):
            break

        line = lines[i].strip()
        words = line.split(' ')
        if len(words) != 1:
            i += 1
            continue

        if CUSTOM_DIRECTIVES["invisible"] in words[0].strip():
            lines.pop(i)
            lines.pop(i)
        i += 1
    return lines


def _random(lines: list[str]) -> list[str]:
    new_lines = []
    pattern = re.compile(rf"{re.escape(CUSTOM_DIRECTIVES['random'])}\s*\((.+)\)")
    for line in lines:
        match = pattern.match(line.strip())
        if match:
            list_literal = match.group(1)
            try:
                options = ast.literal_eval(list_literal)
                if isinstance(options, list) and options:
                    chosen = str(random.choice(options)) + "\n"
                    new_lines.append(chosen)
                    continue
            except Exception:
                raise 200
        new_lines.append(line)
    return new_lines


def _mirror(lines: list[str]) -> list[str]:
    import ast, re

    literal_pattern = re.compile(r'(\[.*?\]|"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\')')

    i = 0
    while i < len(lines):
        if i + 1 >= len(lines):
            break

        if lines[i].strip() == CUSTOM_DIRECTIVES["mirror"]:
            line = lines[i + 1]

            def replace_literal(m):
                try:
                    val = ast.literal_eval(m.group(0))
                    if isinstance(val, str):
                        return repr(val[::-1])
                    elif isinstance(val, list):
                        return repr(val[::-1])
                except Exception:
                    pass
                return m.group(0)  # если не парсится — не меняем

            new_line = literal_pattern.sub(replace_literal, line)
            lines = lines[:i] + [new_line] + lines[i + 2:]
            continue

        i += 1

    return lines


def _repeat(lines: list[str]) -> list[str]:
    i = 0
    while i < len(lines):
        if i + 1 == len(lines):
            break

        line = lines[i].strip()
        words = line.split(' ')
        if len(words) != 1:
            i += 1
            continue

        if CUSTOM_DIRECTIVES["repeat"] in words[0].strip():
            expression = line
            pattern = fr"{CUSTOM_DIRECTIVES["repeat"]}\((\d+)\)"
            match = re.search(pattern, expression)
            if match:
                count = int(match.group(1))
                var = lines[i+1]
                extending = [var] * count
                lines = lines[:i] + extending + lines[i+2:]
                i += count
                continue
            else:
                raise 200
        i += 1

    return lines


def is_custom_directive(line: str) -> bool:
    return line in CUSTOM_DIRECTIVES.values()


CUSTOM_DIRECTIVES = {
    "debug_only" : "@debug_only",
    "invisible" : "@invisible",
    "random" : "@random",
    "mirror" : "@mirror",
    "repeat" : "@repeat",
}