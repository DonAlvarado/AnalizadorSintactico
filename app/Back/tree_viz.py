# tree_viz.py
from .parser import Node

def node_label(n: Node) -> str:
    if n.token:
        val = str(n.token.value).replace('"', '\\"')
        return f"{n.symbol}:{val}"
    return n.symbol

def export_dot(root: Node, path: str):
    lines = ["digraph G {"]
    id_map = {}
    counter = [0]

    def rec(node: Node):
        nid = counter[0]
        counter[0] += 1
        id_map[id(node)] = nid
        label = node_label(node)  # usamos la función node_label
        lines.append(f'  {nid} [label="{label}"];')
        for child in getattr(node, "children", []):
            rec(child)
            lines.append(f'  {nid} -> {id_map[id(child)]};')

    rec(root)
    lines.append("}")
    
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
