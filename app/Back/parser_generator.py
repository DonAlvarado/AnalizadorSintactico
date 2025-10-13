# parser_generator.py
from typing import Dict, List, Set, Tuple

from .grammar import GRAMMAR, START_SYMBOL, EPS, get_terminals, get_nonterminals


class ParserGenerator:
    def __init__(self, grammar=None):
        self.grammar = grammar if grammar is not None else GRAMMAR
        self.nonterms = list(self.grammar.keys())
        self.terminals = get_terminals()
        self.first: Dict[str, Set[str]] = {nt: set() for nt in self.nonterms}
        self.follow: Dict[str, Set[str]] = {nt: set() for nt in self.nonterms}
        self.table: Dict[Tuple[str,str], List[str]] = {}
        self.conflicts = []

    def compute_first(self):
        changed = True
        while changed:
            changed = False
            for A, prods in self.grammar.items():
                for prod in prods:
                    if prod == [EPS]:
                        if EPS not in self.first[A]:
                            self.first[A].add(EPS); changed = True
                        continue
                    add_eps = True
                    for X in prod:
                        if X in self.grammar:  # nonterminal
                            before = len(self.first[A])
                            # add FIRST(X) minus EPS
                            self.first[A].update(self.first[X] - {EPS})
                            if EPS not in self.first[X]:
                                add_eps = False
                                break
                            if len(self.first[A]) != before:
                                changed = True
                        else:
                            # terminal
                            if X not in self.first[A]:
                                self.first[A].add(X); changed = True
                            add_eps = False
                            break
                    if add_eps:
                        if EPS not in self.first[A]:
                            self.first[A].add(EPS); changed = True

    def first_of_sequence(self, seq: List[str]) -> Set[str]:
        res = set()
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
                            beta = prod[i+1:]
                            first_beta = self.first_of_sequence(beta)
                            before = len(self.follow[B])
                            self.follow[B].update(first_beta - {EPS})
                            if EPS in first_beta or not beta:
                                self.follow[B].update(self.follow[A])
                            if len(self.follow[B]) != before:
                                changed = True

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

    def generate(self):
        self.compute_first()
        self.compute_follow()
        self.build_table()
        return {
            "first": self.first,
            "follow": self.follow,
            "table": self.table,
            "conflicts": self.conflicts
        }

if __name__ == "__main__":
    pg = ParserGenerator()
    res = pg.generate()
    print("FIRST")
    for k,v in res["first"].items():
        print(k, "->", v)
    print("\nFOLLOW")
    for k,v in res["follow"].items():
        print(k, "->", v)
    if res["conflicts"]:
        print("\nConflicts found:", res["conflicts"])
    else:
        print("\nNo conflicts.")
