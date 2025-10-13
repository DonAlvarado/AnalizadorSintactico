# parser.py
from dataclasses import dataclass
from typing import Any, List, Optional

from .lexer import Lexer, Token
from .parser_generator import ParserGenerator
from .grammar import GRAMMAR, START_SYMBOL, EPS

@dataclass
class Node:
    symbol: str
    token: Optional[Token] = None
    children: List[Any] = None
    def __post_init__(self):
        if self.children is None:
            self.children = []

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0
        self.curr = tokens[0]
        self.pg = ParserGenerator()
        gen = self.pg.generate()
        self.table = gen["table"]
        self.follow = gen["follow"]
        self.errors: List[str] = []

    def advance(self):
        if self.pos < len(self.tokens)-1:
            self.pos += 1
            self.curr = self.tokens[self.pos]

    def parse(self):
        root = Node(START_SYMBOL)
        self._parse_nonterm(START_SYMBOL, root)
        return root, self.errors

    def _parse_nonterm(self, A: str, parent: Node):
        a = self.curr.type
        key = (A, a)
        prod = None
        if key in self.table:
            prod = self.table[key]
        else:
            # try special-case: if token is 'id' and table has entries for (A, '(') etc. attempt to map by value
            # fallback to panic-mode
            self.errors.append(f"Syntax error: no rule for ({A}, {a}) at {self.curr.line}:{self.curr.col}")
            follow_set = self.follow.get(A, set())
            while self.curr.type not in follow_set and self.curr.type != "$":
                self.advance()
            return

        if prod == [EPS]:
            parent.children.append(Node(EPS))
            return

        for sym in prod:
            if sym in GRAMMAR:  # nonterminal
                node = Node(sym)
                parent.children.append(node)
                self._parse_nonterm(sym, node)
            else:
                # terminal expected
                if sym == self.curr.type:
                    node = Node(sym, token=self.curr)
                    parent.children.append(node)
                    self.advance()
                else:
                    # special: many grammar terminals are literal strings and sometimes token types match value
                    # attempt match by value (e.g., token type '+' has type '+')
                    if self.curr.type == sym:
                        node = Node(sym, token=self.curr)
                        parent.children.append(node)
                        self.advance()
                    else:
                        # mismatch: report and attempt single-token delete recovery
                        self.errors.append(f"Syntax error: expected '{sym}', found '{self.curr.type}' at {self.curr.line}:{self.curr.col}")
                        if self.curr.type == "$":
                            parent.children.append(Node(sym))
                        else:
                            self.advance()
                            # try to match again
                            if self.curr.type == sym:
                                node = Node(sym, token=self.curr)
                                parent.children.append(node)
                                self.advance()
                            else:
                                parent.children.append(Node(sym))
        return

def print_tree(node: Node, indent=0):
    pad = "  " * indent
    if node.token:
        print(f"{pad}{node.symbol} -> {node.token.value}")
    elif not node.children:
        print(f"{pad}{node.symbol}")
    else:
        print(f"{pad}{node.symbol}")
        for c in node.children:
            print_tree(c, indent+1)

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python parser.py archivo.java")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        text = f.read()
    lex = Lexer(text)
    tokens = lex.lex()
    if lex.errors:
        print("Lexer errors:", lex.errors)
    p = Parser(tokens)
    tree, errs = p.parse()
    print_tree(tree)
    if errs:
        print("\nErrors:")
        for e in errs:
            print("-", e)
