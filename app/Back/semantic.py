# semantic.py

from typing import Dict, List, Optional, Any
from .parser import Node


class SymbolTable:
    def __init__(self):
        # classes[classname] = {fields: {name:type}, methods: {name: {ret, params: [(type,name)], locals:{}}}}
        self.classes: Dict[str, Dict[str, Any]] = {}
        self.errors: List[str] = []

    def analyze(self, root: Node):
        # root -> Prog -> ClassList
        if root.symbol != "Prog":
            self.errors.append("Root not Prog")
            return
        # traverse ClassList
        for cl in root.children:
            if cl.symbol == "ClassList":
                for c in cl.children:
                    self._process_classnode(c)

    def _process_classnode(self, node: Node):
        if node.symbol != "ClassDecl":
            # could be EPS or others
            for ch in node.children:
                if ch.symbol == "ClassDecl":
                    self._process_classnode(ch)
            return
        # find id
        ids = [c for c in node.children if c.symbol == "id"]
        if not ids:
            self.errors.append("Class with no id")
            return
        class_name = ids[0].token.value
        if class_name in self.classes:
            self.errors.append(f"Duplicate class {class_name}")
            return
        cls = {"fields": {}, "methods": {}}
        self.classes[class_name] = cls
        # MemberList is inside
        memberlist = next((c for c in node.children if c.symbol == "MemberList"), None)
        if memberlist:
            for mem in memberlist.children:
                if mem.symbol == "Member":
                    self._process_member(mem, cls, class_name)

    def _process_member(self, member: Node, cls: Dict, class_name: str):
        # Member -> FieldDecl | MethodDecl | ConstructorDecl
        if not member.children:
            return
        ch = member.children[0]
        if ch.symbol == "FieldDecl":
            # Type VarDeclList ;
            t = self._extract_type(ch)
            # find VarDecl children
            vardecls = [v for v in ch.children if v.symbol == "VarDecl"]
            if not vardecls:
                # VarDeclList nested structure
                for sub in ch.children:
                    if sub.symbol == "VarDeclList":
                        vardecls = [c for c in sub.children if c.symbol == "VarDecl"]
            for vd in vardecls:
                name_node = next((c for c in vd.children if c.symbol == "id"), None)
                if name_node:
                    name = name_node.token.value
                    if name in cls["fields"]:
                        self.errors.append(f"Duplicate field {name} in class {class_name}")
                    else:
                        cls["fields"][name] = t
        elif ch.symbol == "MethodDecl":
            mname = next((c.token.value for c in ch.children if c.symbol == "id" and c.token), None)
            rettype = self._extract_type(ch)
            if mname:
                if mname in cls["methods"]:
                    self.errors.append(f"Duplicate method {mname} in {class_name}")
                    return
                params = []
                paramlist = next((c for c in ch.children if c.symbol == "ParamList"), None)
                if paramlist:
                    params = self._collect_params(paramlist)
                cls["methods"][mname] = {"ret": rettype, "params": params, "locals": {}}
                # could analyze body: collect local vars and check types
                block = next((c for c in ch.children if c.symbol == "Block"), None)
                if block:
                    self._analyze_block(block, cls["methods"][mname], class_name, mname)
        elif ch.symbol == "ConstructorDecl":
            # similar handling: parameters and block
            pass

    def _collect_params(self, paramlist: Node):
        res = []
        def rec(n):
            for c in n.children:
                if c.symbol == "Param":
                    t = self._extract_type(c)
                    idnode = next((x for x in c.children if x.symbol == "id"), None)
                    name = idnode.token.value if idnode else None
                    res.append((t, name))
                else:
                    rec(c)
        rec(paramlist)
        return res

    def _extract_type(self, node: Node) -> Optional[str]:
        # node contains Type somewhere under its children
        tnode = None
        for c in node.children:
            if c.symbol == "Type":
                tnode = c
                break
        if not tnode:
            return None
        # Type -> token like 'int' or 'id' for class types or 'String'
        # find the terminal child in Type subtree
        for leaf in tnode.children:
            if leaf.token:
                return leaf.token.type  # 'int', 'String', 'id', 'void', 'boolean', 'char'
            else:
                # deeper
                for g in leaf.children:
                    if g.token:
                        return g.token.type
        return None

    def _analyze_block(self, block: Node, method_sym: Dict, class_name: str, method_name: str):
        # gather locals and perform basic checks inside method
        # For simplicity: find LocalVarDecl nodes and fill locals; check assignments/returns superficially
        def rec(n):
            for c in n.children:
                if c.symbol == "LocalVarDecl" or c.symbol == "FieldDecl":
                    t = self._extract_type(c)
                    varlist = [x for x in c.children if x.symbol == "VarDecl"]
                    for vd in varlist:
                        name_node = next((z for z in vd.children if z.symbol == "id"), None)
                        if name_node:
                            name = name_node.token.value
                            if name in method_sym["locals"]:
                                self.errors.append(f"Duplicate local {name} in {method_name} of class {class_name}")
                            else:
                                method_sym["locals"][name] = t
                elif c.symbol == "ReturnStmt":
                    # check return type compatibility (very simple)
                    pass
                rec(c)
        rec(block)

    # Additional helpers for expression type inference could be added:
    def infer_expr_type(self, expr_node: Node, cls_ctx: Dict=None, method_ctx: Dict=None) -> Optional[str]:
        # Very simple evaluator: numbers -> int, true/false -> boolean, string_literal -> String, char_literal -> char
        if not expr_node:
            return None
        # descend to find terminal
        if expr_node.token:
            if expr_node.token.type == "number":
                return "int"
            if expr_node.token.type == "string_literal":
                return "String"
            if expr_node.token.type == "char_literal":
                return "char"
            if expr_node.token.type in ("true","false"):
                return "boolean"
            if expr_node.token.type == "id":
                # look into locals, params, fields (not implemented here fully)
                return "id"
        # otherwise, naive cases
        for c in expr_node.children:
            t = self.infer_expr_type(c, cls_ctx, method_ctx)
            if t:
                return t
        return None

def run_semantic_on_tree(root: Node):
    st = SymbolTable()
    st.analyze(root)
    return st
