from typing import List


def cut_string(line: str, letters: int = 15) -> str:
    if len(line) < letters:
        return line
    return line[:letters] + "…"


def break_string_into_lines(line: str, length: int) -> List[str]:
    result = []

    while len(line) > 0:
        result.append(line[:length])
        line = line[length:]

    return result
