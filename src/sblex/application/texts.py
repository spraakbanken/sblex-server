from typing import Tuple


def inits(s: str) -> list[Tuple[str, str]]:
    return [(s[:i], s[i:]) for i in range(1, len(s) + 1)]
