# grammar.py
from typing import Dict, List

EPS = "ε"

# Subconjunto ampliado de Java (factorizado para LL(1) en gran medida)
GRAMMAR: Dict[str, List[List[str]]] = {
    "Prog": [["ClassList"]],
    "ClassList": [["ClassDecl", "ClassList"], [EPS]],
    "ClassDecl": [["class", "id", "ClassExt", "{", "MemberList", "}"]],
    "ClassExt": [["extends", "id"], [EPS]],
    "MemberList": [["Member", "MemberList"], [EPS]],
    "Member": [["FieldDecl"], ["MethodDecl"], ["ConstructorDecl"]],
    "Modifiers": [["Modifier", "Modifiers"], [EPS]],
    "Modifier": [["public"], ["private"], ["protected"], ["static"], ["final"]],
    "FieldDecl": [["Modifiers", "Type", "VarDeclList", ";"]],
    "VarDeclList": [["VarDecl", "VarDeclRest"]],
    "VarDeclRest": [[",", "VarDecl", "VarDeclRest"], [EPS]],
    "VarDecl": [["id", "ArrayDeclOpt", "InitOpt"]],
    "ArrayDeclOpt": [["[", "]"], [EPS]],
    "InitOpt": [["=", "Expr"], [EPS]],
    "ConstructorDecl": [["Modifiers", "id", "(", "ParamList", ")", "Block"]],
    "MethodDecl": [["Modifiers", "Type", "id", "(", "ParamList", ")", "Block"]],
    "ParamList": [["Param", "ParamRest"], [EPS]],
    "ParamRest": [[",", "Param", "ParamRest"], [EPS]],
    "Param": [["Type", "id", "ArrayDeclOpt"]],
    "Type": [["int", "ArrayTypeOpt"], ["boolean"], ["char"], ["String", "ArrayTypeOpt"], ["id", "ArrayTypeOpt"], ["void"]],
    "ArrayTypeOpt": [["[", "]"], [EPS]],
    "Block": [["{", "StmtList", "}"]],
    "StmtList": [["Stmt", "StmtList"], [EPS]],
    "Stmt": [["LocalVarDecl"], ["IfStmt"], ["WhileStmt"], ["ForStmt"], ["ReturnStmt"], ["ExprStmt"], ["Block"], [";"]],
    "LocalVarDecl": [["Type", "VarDeclList", ";"]],
    "IfStmt": [["if", "(", "Expr", ")", "Stmt", "ElseOpt"]],
    "ElseOpt": [["else", "Stmt"], [EPS]],
    "WhileStmt": [["while", "(", "Expr", ")", "Stmt"]],
    "ForStmt": [["for", "(", "ForInit", "ForCond", "ForUpdate", ")", "Stmt"]],
    "ForInit": [["LocalVarDecl"], ["ExprStmt"], [";"]],
    "ForCond": [["Expr", ";"], [";"]],
    "ForUpdate": [["ExprList", ";"], [";"]],
    "ExprList": [["Expr", "ExprListRest"], [EPS]],
    "ExprListRest": [[",", "Expr", "ExprListRest"], [EPS]],
    "ReturnStmt": [["return", "ExprOpt", ";"]],
    "ExprOpt": [["Expr"], [EPS]],
    "ExprStmt": [["Expr", ";"]],
    "Expr": [["AssignExpr"]],
    "AssignExpr": [["CondOrExpr", "AssignTail"]],
    "AssignTail": [["=", "AssignExpr"], [EPS]],
    "CondOrExpr": [["CondAndExpr", "CondOrRest"]],
    "CondOrRest": [["||", "CondAndExpr", "CondOrRest"], [EPS]],
    "CondAndExpr": [["RelExpr", "CondAndRest"]],
    "CondAndRest": [["&&", "RelExpr", "CondAndRest"], [EPS]],
    "RelExpr": [["AddExpr", "RelRest"]],
    "RelRest": [["<", "AddExpr", "RelRest"], [">", "AddExpr", "RelRest"],
                ["<=", "AddExpr", "RelRest"], [">=", "AddExpr", "RelRest"],
                ["==", "AddExpr", "RelRest"], ["!=", "AddExpr", "RelRest"], [EPS]],
    "AddExpr": [["MulExpr", "AddRest"]],
    "AddRest": [["+", "MulExpr", "AddRest"], ["-", "MulExpr", "AddRest"], [EPS]],
    "MulExpr": [["UnaryExpr", "MulRest"]],
    "MulRest": [["*", "UnaryExpr", "MulRest"], ["/", "UnaryExpr", "MulRest"], [EPS]],
    "UnaryExpr": [["UnaryOp", "UnaryExpr"], ["PostfixExpr"]],
    "UnaryOp": [["+",], ["-"], ["!"], ["++"], ["--"]],
    "PostfixExpr": [["PrimaryExpr", "PostfixTail"]],
    "PostfixTail": [["++", "PostfixTail"], ["--", "PostfixTail"], [EPS]],
    "PrimaryExpr": [["literal"], ["id", "PrimarySuffix"], ["(", "Expr", ")"], ["new", "Creator"]],
    "PrimarySuffix": [[".", "id", "ArgsOpt"], ["[", "Expr", "]", "PrimarySuffix"], [EPS]],
    "Creator": [["id", "ArgsOpt"], ["Type", "ArrayCreatorRest"]],
    "ArgsOpt": [["(", "ArgList", ")"], [EPS]],
    "ArgList": [["Expr", "ArgRest"], [EPS]],
    "ArgRest": [[",", "Expr", "ArgRest"], [EPS]],
    "ArrayCreatorRest": [["[", "Expr", "]", "ArrayCreatorRest"], [EPS]],
    "literal": [["number"], ["char_literal"], ["string_literal"], ["true"], ["false"], ["null"]],
}

START_SYMBOL = "Prog"

def get_nonterminals():
    return list(GRAMMAR.keys())

def get_terminals():
    nonterms = set(GRAMMAR.keys())
    terms = set()
    for prods in GRAMMAR.values():
        for prod in prods:
            for sym in prod:
                if sym != EPS and sym not in nonterms:
                    terms.add(sym)
    return sorted(list(terms))
