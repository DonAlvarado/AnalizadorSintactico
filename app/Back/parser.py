from dataclasses import dataclass
from typing import Any, List, Optional, Tuple
from app.Back.lexer import Lexer, Token
from app.Back.parser_generator import ParserGenerator
from app.Back.grammar import GRAMMAR, START_SYMBOL, EPS

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
        gen = ParserGenerator().generate()
        self.table = gen["table"]
        self.follow = gen["follow"]
        self.errors: List[str] = []

    def advance(self):
        if self.pos < len(self.tokens) - 1:
            self.pos += 1
            self.curr = self.tokens[self.pos]

    def parse(self) -> Tuple[Node, List[str]]:
        root = Node(START_SYMBOL)
        self._parse_nonterm(START_SYMBOL, root)
        return root, self.errors

    def _parse_nonterm(self, A: str, parent: Node):
        a = self.curr.type
        prod = self.table.get((A, a))
        if not prod:
            self.errors.append(f"[Línea {self.curr.line}] Error sintáctico: token inesperado '{self.curr.value}'.")
            follow_set = self.follow.get(A, set())
            # Bug de mostrar mas errores en los errores
            if self.curr.type == "$":
                return

            while self.curr.type not in follow_set:
                self.advance()
                if self.curr.type == "$":
                    return
            return
        
        if prod == [EPS]:
            parent.children.append(Node(EPS))
            return

        for sym in prod:
            if sym in EPS:
                parent.children.append(Node(EPS))
                continue

            if sym in GRAMMAR:
                node = Node(sym)
                parent.children.append(node)
                self._parse_nonterm(sym, node)
            else:
                if self.curr.type == sym:
                    node = Node(sym, token=self.curr)
                    parent.children.append(node)
                    self.advance()
                else:
                    self.errors.append(f"[Línea {self.curr.line}] Falta '{sym}' antes de '{self.curr.value}'.")
                    if self.curr.type == "$":
                        parent.children.append(Node(sym))
                    else:
                        self.advance()
                        if self.curr.type == sym:
                            node = Node(sym, token=self.curr)
                            parent.children.append(node)
                            self.advance()
                        else:
                            parent.children.append(Node(sym))

def print_tree(node: Node, indent=0):
    pad = "  " * indent
    if node.token:
        print(f"{pad}{node.symbol} -> {node.token.value}")
    elif not node.children:
        print(f"{pad}{node.symbol}")
    else:
        print(f"{pad}{node.symbol}")
        for c in node.children:
            print_tree(c, indent + 1)


#Esto es para hacer pruebas con el parser en vez de andar levantando el servidor
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python -m app.Back.parser programa.txt")
        sys.exit(1)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        text = f.read()
    lex = Lexer(text)
    tokens = lex.lex()
    if lex.errors:
        print("Lexer errors:")
        for e in lex.errors:
            print("-", e)
    p = Parser(tokens)
    tree, errs = p.parse()
    print_tree(tree)
    if errs:
        print("\nSyntax errors:")
        for e in errs:
            print("-", e)
