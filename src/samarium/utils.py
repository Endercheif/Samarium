import os
import sys

from contextlib import contextmanager, suppress
from typing import Callable, TypeVar

from .exceptions import (
    NotDefinedError,
    # SamariumTypeError,
    # SamariumSyntaxError
)
from .tokenizer import Tokenlike
from .tokens import Token, OPEN_TOKENS, CLOSE_TOKENS


T = TypeVar("T")

OPEN_TO_CLOSE = {
    Token.BRACKET_OPEN: Token.BRACKET_CLOSE,
    Token.BRACE_OPEN: Token.BRACE_CLOSE,
    Token.PAREN_OPEN: Token.PAREN_CLOSE,
    Token.TABLE_OPEN: Token.TABLE_CLOSE,
    Token.SLICE_OPEN: Token.SLICE_CLOSE
}


def match_brackets(tokens: list[Tokenlike]) -> tuple[int, Tokenlike]:
    stack = []
    for token in tokens:
        if token in OPEN_TOKENS:
            stack += [token]
        elif token in CLOSE_TOKENS:
            if OPEN_TO_CLOSE[stack[-1]] == token:
                stack.pop(-1)
            else:
                return 1, token
    if stack:
        return -1, stack[-1]
    return 0, 0


def readfile(path: str) -> str:
    with open(path) as f:
        return f.read()


def run_with_backup(
    main: Callable[..., T],
    backup: Callable[..., T],
    *args
) -> T:
    with suppress(NotDefinedError):
        return main(*args)
    return backup(*args)


@contextmanager
def silence_stdout():
    stdout = sys.stdout
    sys.stdout = open(os.devnull, "w")
    yield
    sys.stdout = stdout


def sysexit(code: int = 0):
    os._exit(code)
