from typing import Dict, List, Set, Tuple
from app.Back.grammar import GRAMMAR, START_SYMBOL, EPS, get_terminals

class ParserGenerator:
    def __init__(self, grammar=None):
        self.grammar = grammar if grammar is not None else GRAMMAR
        self.nonterms = list(self.grammar.keys())
        self.terminals = sorted(set(get_terminals() + ["$"]))
        self.first: Dict[str, Set[str]] = {nt: set() for nt in self.nonterms}
        self.follow: Dict[str, Set[str]] = {nt: set() for nt in self.nonterms}
        self.table: Dict[Tuple[str, str], List[str]] = {}
        self.conflicts: List[Tuple[str, str, List[str], List[str]]] = []

    def compute_first(self):
        changed = True
        while changed:
            changed = False
            for A, prods in self.grammar.items():
                for prod in prods:
                    if prod == [EPS]:
                        if EPS not in self.first[A]:
                            self.first[A].add(EPS)
                            changed = True
                        continue

                    add_eps = True
                    for X in prod:
                        if X in self.grammar:
                            before = len(self.first[A])
                            self.first[A].update(self.first[X] - {EPS})
                            if EPS not in self.first[X]:
                                add_eps = False
                                break
                            if len(self.first[A]) != before:
                                changed = True
                        else:
                            if X not in self.first[A]:
                                self.first[A].add(X)
                                changed = True
                            add_eps = False
                            break

                    if add_eps and EPS not in self.first[A]:
                        self.first[A].add(EPS)
                        changed = True

        stable = False
        while not stable:
            stable = True
            for A, prods in self.grammar.items():
                before = len(self.first[A])
                for prod in prods:
                    if prod and prod[0] in self.grammar:
                        self.first[A].update(self.first[prod[0]] - {EPS})
                if len(self.first[A]) != before:
                    stable = False

    def first_of_sequence(self, seq: List[str]) -> Set[str]:
        res: Set[str] = set()
        if not seq:
            res.add(EPS)
            return res
        for X in seq:
            if X in self.grammar:
                res.update(self.first[X] - {EPS})
                if EPS not in self.first[X]:
                    return res
            else:
                res.add(X)
                return res
        res.add(EPS)
        return res

    def compute_follow(self):
        self.follow[START_SYMBOL].add("$")
        changed = True
        while changed:
            changed = False
            for A, prods in self.grammar.items():
                for prod in prods:
                    for i, B in enumerate(prod):
                        if B in self.grammar:
                            beta = prod[i + 1 :]
                            first_beta = self.first_of_sequence(beta)
                            before = len(self.follow[B])
                            self.follow[B].update(first_beta - {EPS})
                            if EPS in first_beta or not beta:
                                self.follow[B].update(self.follow[A])
                            if len(self.follow[B]) != before:
                                changed = True

    # Aqui se construye la tabla LL
    def build_table(self):
        for A, prods in self.grammar.items():
            for prod in prods:
                firsts = self.first_of_sequence(prod)
                for a in (firsts - {EPS}):
                    key = (A, a)
                    if key in self.table:
                        self.conflicts.append((A, a, self.table[key], prod))
                    self.table[key] = prod
                if EPS in firsts:
                    for b in self.follow[A]:
                        key = (A, b)
                        if key in self.table:
                            self.conflicts.append((A, b, self.table[key], prod))
                        self.table[key] = prod
        self.table[("ElseOpt", "else")] = ["else", "Stmt"]

    # Aqui se genera la tabla
    def generate(self):
        self.compute_first()
        self.compute_follow()
        self.build_table()
        return {
            "first": self.first,
            "follow": self.follow,
            "table": self.table,
            "conflicts": self.conflicts,
        }