# table_gen.py
import csv
from parser_generator import ParserGenerator
from grammar import GRAMMAR, START_SYMBOL
from grammar import get_terminals

def export_table_csv(filename="parse_table.csv"):
    pg = ParserGenerator()
    res = pg.generate()
    table = res["table"]
    terminals = sorted(set(get_terminals() + ["$"]))
    nonterms = sorted(list(GRAMMAR.keys()))
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Nonterminal"] + terminals)
        for A in nonterms:
            row = [A]
            for t in terminals:
                prod = table.get((A, t))
                row.append(" ".join(prod) if prod else "")
            writer.writerow(row)
    return filename

if __name__ == "__main__":
    print("Generating parse_table.csv")
    export_table_csv()
