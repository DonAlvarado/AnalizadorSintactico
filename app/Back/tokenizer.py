# tokenizer.py
import re
from dataclasses import dataclass
from typing import Iterator

@dataclass
class RawToken:
    typ: str
    val: str
    line: int
    col: int

_token_spec = [
    ("WHITESPACE", r"[ \t\r]+"),
    ("NEWLINE",    r"\n"),
    ("LINE_COMMENT", r"//[^\n]*"),
    ("BLOCK_COMMENT", r"/\*.*?\*/"),
    ("NUMBER",     r"\d+(?:\.\d+)?"),
    ("ID",         r"[A-Za-z_][A-Za-z0-9_]*"),
    ("STRING",     r"\"(\\.|[^\"\\])*\""),
    ("CHAR",       r"\'(\\.|[^\'\\])\'"),
    ("OP",         r"==|!=|<=|>=|&&|\|\||[+\-*/=<>]"),
    ("SYMBOL",     r"[(){}\[\],;.]"),
    ("MISMATCH",   r"."),
]


_token_regex = re.compile("|".join(f"(?P<{n}>{p})" for n, p in _token_spec), re.DOTALL)

def tokenize_chars(text: str) -> Iterator[RawToken]:
    pos = 0
    line = 1
    line_start = 0
    L = len(text)
    while pos < L:
        m = _token_regex.match(text, pos)
        if not m:
            break
        typ = m.lastgroup
        val = m.group(typ)
        start = m.start()
        col = start - line_start + 1

        if typ == "NEWLINE":
            line += 1
            line_start = m.end()

        elif typ in ("WHITESPACE", "LINE_COMMENT"):
            # Ignorar los tokens con espacios en blanco
            pass

        elif typ == "BLOCK_COMMENT":
            line += val.count("\n")
            line_start = m.end()

        elif typ == "MISMATCH":
            yield RawToken("ILLEGAL", val, line, col)

        else:
            yield RawToken(typ, val, line, col)

        pos = m.end()
