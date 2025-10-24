# tree_viz.py
from app.Back.parser import Node
from typing import Optional
import subprocess
import shutil
import os

def _node_label(n: Node) -> str:
    if n.token:
        val = str(n.token.value).replace('"', '\\"')
        return f"{n.symbol}:{val}"
    return n.symbol

def export_dot(root: Node, path: str) -> str:
    lines = ["digraph G {", '  node [shape=box, fontsize=10];', '  rankdir=TB;']
    id_map = {}
    counter = [0]

    def rec(node: Node):
        nid = counter[0]
        counter[0] += 1
        id_map[id(node)] = nid
        label = _node_label(node)
        lines.append(f'  {nid} [label="{label}"];')
        for child in getattr(node, "children", []):
            rec(child)
            lines.append(f'  {nid} -> {id_map[id(child)]};')

    rec(root)
    lines.append("}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path

def render_dot_to_png(dot_path: str, png_path: Optional[str] = None) -> str:
    if png_path is None:
        base, _ = os.path.splitext(dot_path)
        png_path = base + ".png"

    if shutil.which("dot") is None:
        raise RuntimeError(
            "Graphviz no encontrado. Instala Graphviz y asegúrate de que 'dot' esté en PATH."
        )

    subprocess.run(["dot", "-Tpng", dot_path, "-o", png_path], check=True)
    return png_path
