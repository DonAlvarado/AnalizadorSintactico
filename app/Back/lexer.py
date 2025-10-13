from .tokenizer import tokenize_chars, RawToken
from dataclasses import dataclass
from typing import List

KEYWORDS = {
    "class","extends","public","private","protected","static","final",
    "int","void","boolean","char","String","if","else","while","for",
    "return","new","this","true","false","null"
}

@dataclass
class Token:
    type: str
    value: str
    line: int
    col: int

class Lexer:
    def __init__(self, text: str):
        self.src = text
        self.tokens: List[Token] = []
        self.errors: List[str] = []

    def lex(self) -> List[Token]:
        for rt in tokenize_chars(self.src):
            if rt.typ == "ILLEGAL":
                self.errors.append(f"Illegal character {rt.val!r} at {rt.line}:{rt.col}")
                continue
            if rt.typ == "ID":
                if rt.val in KEYWORDS:
                    self.tokens.append(Token(rt.val, rt.val, rt.line, rt.col))
                else:
                    self.tokens.append(Token("id", rt.val, rt.line, rt.col))
            elif rt.typ == "NUMBER":
                self.tokens.append(Token("number", rt.val, rt.line, rt.col))
            elif rt.typ == "STRING":
                self.tokens.append(Token("string_literal", rt.val, rt.line, rt.col))
            elif rt.typ == "CHAR":
                self.tokens.append(Token("char_literal", rt.val, rt.line, rt.col))
            elif rt.typ == "OP":
                self.tokens.append(Token(rt.val, rt.val, rt.line, rt.col))
            elif rt.typ == "SYMBOL":
                self.tokens.append(Token(rt.val, rt.val, rt.line, rt.col))
            else:
                pass
        self.tokens.append(Token("$", "$", -1, -1))
        return self.tokens
