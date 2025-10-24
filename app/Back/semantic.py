from typing import Dict, List, Optional, Any
from app.Back.parser import Node

class SymbolTable:
    def __init__(self):
        self.classes: Dict[str, Dict[str, Any]] = {}
        self.errors: List[str] = []

    def analyze(self, root: Node):
        if root.symbol != "Prog":
            self.errors.append("Root is not Prog")
            return
        for ch in getattr(root, "children", []):
            self._walk(ch)

    def _walk(self, node: Node):
        if node.symbol == "ClassDecl":
            self._class_decl(node)
            return
        for c in getattr(node, "children", []):
            self._walk(c)

    def _class_decl(self, node: Node):
        idnode = next((c for c in node.children if c.symbol == "id" and c.token), None)
        if not idnode:
            self.errors.append("Class without id")
            return
        cname = idnode.token.value
        if cname in self.classes:
            self.errors.append(f"Duplicate class {cname}")
            return
        cls = {"fields": {}, "methods": {}}
        self.classes[cname] = cls

        mlist = next((c for c in node.children if c.symbol == "MemberList"), None)
        if mlist:
            self._members(mlist, cls, cname)

    def _members(self, node: Node, cls: Dict, cname: str):
        def rec(n: Node):
            for ch in getattr(n, "children", []):
                if ch.symbol == "Member":
                    self._member(ch, cls, cname)
                rec(ch)
        rec(node)

    def _member(self, node: Node, cls: Dict, cname: str):
        if not node.children:
            return
        inner = node.children[0]
        if inner.symbol == "VarDecl":
            t = self._extract_type(inner)
            idnode = next((c for c in inner.children if c.symbol == "id" and c.token), None)
            if idnode:
                name = idnode.token.value
                if name in cls["fields"]:
                    self.errors.append(f"Duplicate field {name} in {cname}")
                else:
                    cls["fields"][name] = t

        elif inner.symbol == "MethodDecl":
            rettype = self._extract_rettype(inner)
            mname_node = next((c for c in inner.children if c.symbol == "id" and c.token), None)
            mname = mname_node.token.value if mname_node else None
            if not mname:
                self.errors.append(f"Method without name in {cname}")
                return
            if mname in cls["methods"]:
                self.errors.append(f"Duplicate method {mname} in {cname}")
                return

            params = self._collect_params(next((c for c in inner.children if c.symbol == "ParamList"), None))
            data = {"ret": rettype, "params": params, "locals": {}}
            cls["methods"][mname] = data

            block = next((c for c in inner.children if c.symbol == "Block"), None)
            if block:
                self._collect_locals(block, data)

    def _collect_params(self, plist: Optional[Node]):
        res = []
        if not plist:
            return res
        def rec(n: Node):
            for c in getattr(n, "children", []):
                if c.symbol == "Param":
                    t = self._extract_type(c)
                    idnode = next((x for x in c.children if x.symbol == "id" and x.token), None)
                    name = idnode.token.value if idnode else None
                    res.append((t, name))
                else:
                    rec(c)
        rec(plist)
        return res

    def _collect_locals(self, block: Node, method_sym: Dict):
        def rec(n: Node):
            for c in getattr(n, "children", []):
                if c.symbol == "VarDecl":
                    t = self._extract_type(c)
                    idnode = next((x for x in c.children if x.symbol == "id" and x.token), None)
                    if idnode:
                        name = idnode.token.value
                        if name in method_sym["locals"]:
                            self.errors.append(f"Duplicate local {name} in method")
                        else:
                            method_sym["locals"][name] = t
                rec(c)
        rec(block)

    def _extract_type(self, node: Node) -> Optional[str]:
        tnode = next((c for c in node.children if c.symbol == "Type"), None)
        if not tnode:
            return None
        leaf = next((c for c in tnode.children if c.token), None)
        return leaf.token.type if leaf and leaf.token else None

    def _extract_rettype(self, node: Node) -> Optional[str]:
        tov = next((c for c in node.children if c.symbol == "TypeOrVoid"), None)
        if not tov:
            return None
        v = next((c for c in tov.children if c.token and c.token.type == "void"), None)
        if v:
            return "void"
        return self._extract_type(tov)

def run_semantic_on_tree(root: Node):
    st = SymbolTable()
    st.analyze(root)
    return st
