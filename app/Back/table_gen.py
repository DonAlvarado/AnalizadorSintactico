# table_gen.py
import csv
from typing import List
from app.Back.parser_generator import ParserGenerator
from app.Back.grammar import GRAMMAR, START_SYMBOL
from app.Back.grammar import get_terminals

def export_table_csv(filename: str = "tabla_transicion.csv") -> str:
    pg = ParserGenerator()
    res = pg.generate()
    table = res["table"]
    terminals = sorted(set(get_terminals() + ["$"]))
    nonterms = list(GRAMMAR.keys())

    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Nonterminal"] + terminals)
        for A in nonterms:
            row: List[str] = [A]
            for t in terminals:
                prod = table.get((A, t))
                row.append(" ".join(prod) if prod else "")
            w.writerow(row)
    return filename

def export_table_txt(filename: str = "tabla_transicion.txt") -> str:
    pg = ParserGenerator()
    res = pg.generate()
    table = res["table"]
    conflicts = res["conflicts"]
    terminals = sorted(set(get_terminals() + ["$"]))
    nonterms = list(GRAMMAR.keys())

    lines: List[str] = []
    lines.append("== Tabla LL(1) ==")
    lines.append("")
    lines.append("Columnas (terminales): " + ", ".join(terminals))
    lines.append("")

    for A in nonterms:
        lines.append(f"[{A}]")
        for t in terminals:
            prod = table.get((A, t))
            if prod:
                lines.append(f"  ({A}, {t}) -> {' '.join(prod)}")
        lines.append("")

    if conflicts:
        lines.append("== Conflictos ==")
        for (A, a, oldp, newp) in conflicts:
            lines.append(f"  Conflict ({A}, {a}): existing={' '.join(oldp)} vs new={' '.join(newp)}")
        lines.append("")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return filename

if __name__ == "__main__":
    #Se crean dos archivos para ver la tabla de transiciones del parser
    csv_path = export_table_csv()
    txt_path = export_table_txt()
    print("Tabla exportada a:", csv_path, "y", txt_path)
