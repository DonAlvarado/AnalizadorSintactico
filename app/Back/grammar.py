# grammar.py
from typing import Dict, List

EPS = "ε"

GRAMMAR: Dict[str, List[List[str]]] = {
    # Programa
    "Prog": [["ImportList", "ClassDecl"]],

    # Imports
    "ImportList": [["ImportDecl", "ImportList"], [EPS]],
    "ImportDecl": [["import", "ImportPath", ";"]],
    "ImportPath": [["id", "ImportPathTail"]],
    "ImportPathTail": [[".", "ImportPathSeg"], [EPS]],
    "ImportPathSeg": [["id", "ImportPathTail"], ["*"]],


    # Clase
    "ClassDecl": [["ModifiersOpt", "class", "id", "{", "MemberList", "}"]],
    "ModifiersOpt": [["Modifier", "ModifiersOpt"], [EPS]],
    "Modifier": [
        ["public"], ["private"], ["protected"],
        ["static"], ["final"], ["abstract"]
    ],

    # Miembros
    "MemberList": [["Member", "MemberList"], [EPS]],
    "Member": [["ModifiersOpt", "TypeOrVoid", "id", "MemberRest"]],

    "MemberRest": [
        ["(", "ParamList", ")", "Block"],
        ["FieldTail", ";"]
    ],

    "FieldTail": [["InitOpt", "FieldRest"]],
    "FieldRest": [[",", "id", "InitOpt", "FieldRest"], [EPS]],
    "InitOpt": [["=", "Expr"], [EPS]],

    # Tipos
    "TypeOrVoid": [["Type"], ["void"]],
    "Type": [["int"], ["double"], ["boolean"], ["char"], ["String"]],

    # Parametros
    "ParamList": [["Param", "ParamRest"], [EPS]],
    "ParamRest": [[",", "Param", "ParamRest"], [EPS]],
    "Param": [["Type", "id"]],

    # Bloques de Codigo y sus statements
    "Block": [["{", "StmtList", "}"]],
    "StmtList": [["Stmt", "StmtList"], [EPS]],

    "Stmt": [
        ["VarDeclStmt"],
        ["IfStmt"],
        ["WhileStmt"],
        ["ForStmt"],
        ["ReturnStmt"],
        ["BreakStmt"],
        ["ContinueStmt"],
        ["SimpleStmt"],
        ["Block"]
    ],

    "VarDeclStmt": [["Type", "VarDeclList", ";"]],
    "VarDeclList": [["VarDecl", "VarDeclRest"]],
    "VarDeclRest": [[",", "VarDecl", "VarDeclRest"], [EPS]],
    "VarDecl": [["id", "InitOpt"]],

    # Statements simples
    "SimpleStmt": [["AssignOrCall", ";"]],
    "AssignOrCall": [["PrimaryExpr", "AssignTail"]],
    "AssignTail": [
        ["=", "Expr"],
        [EPS]
    ],

    # Control de Bucles y Condicionales
    "IfStmt": [["if", "(", "Expr", ")", "Stmt", "ElseOpt"]],
    "ElseOpt": [["else", "Stmt"], [EPS]],
    "WhileStmt": [["while", "(", "Expr", ")", "Stmt"]],
    "ForStmt": [["for", "(", "ForInitOpt", ";", "ExprOpt", ";", "ForUpdateOpt", ")", "Stmt"]],
    "ForInitOpt": [["AssignOrCallList"], [EPS]],
    "ForUpdateOpt": [["AssignOrCallList"], [EPS]],
    "AssignOrCallList": [["AssignOrCall", "AssignOrCallListRest"]],
    "AssignOrCallListRest": [[",", "AssignOrCall", "AssignOrCallListRest"], [EPS]],

    "ExprOpt": [["Expr"], [EPS]],
    "ReturnStmt": [["return", "ReturnExprOpt", ";"]],
    "ReturnExprOpt": [["Expr"], [EPS]],
    "BreakStmt": [["break", ";"]],
    "ContinueStmt": [["continue", ";"]],

    # Expresiones
    "Expr": [["CondOrExpr"]],
    "CondOrExpr": [["CondAndExpr", "CondOrRest"]],
    "CondOrRest": [["||", "CondAndExpr", "CondOrRest"], [EPS]],
    "CondAndExpr": [["RelExpr", "CondAndRest"]],
    "CondAndRest": [["&&", "RelExpr", "CondAndRest"], [EPS]],
    "RelExpr": [["AddExpr", "RelRest"]],
    "RelRest": [
        ["<", "AddExpr", "RelRest"],
        [">", "AddExpr", "RelRest"],
        ["<=", "AddExpr", "RelRest"],
        [">=", "AddExpr", "RelRest"],
        ["==", "AddExpr", "RelRest"],
        ["!=", "AddExpr", "RelRest"],
        [EPS]
    ],
    "AddExpr": [["MulExpr", "AddRest"]],
    "AddRest": [
        ["+", "MulExpr", "AddRest"],
        ["-", "MulExpr", "AddRest"],
        [EPS]
    ],
    "MulExpr": [["UnaryExpr", "MulRest"]],
    "MulRest": [
        ["*", "UnaryExpr", "MulRest"],
        ["/", "UnaryExpr", "MulRest"],
        [EPS]
    ],
    "UnaryExpr": [["UnaryOp", "UnaryExpr"], ["PrimaryExpr"]],
    "UnaryOp": [["+"], ["-"], ["!"]],

    # Expresiones Iniciales
    "PrimaryExpr": [
        ["literal"],
        ["id", "PrimaryTail"],
        ["(", "Expr", ")"]
    ],
    "PrimaryTail": [
        ["(", "ArgList", ")", "PrimaryTail"],
        [".", "id", "PrimaryTail"],
        [EPS]
    ],

    # Argumentos en las funciomnes
    "ArgList": [["Expr", "ArgRest"], [EPS]],
    "ArgRest": [[",", "Expr", "ArgRest"], [EPS]],

    # Literales
    "literal": [
        ["number"], ["true"], ["false"],
        ["string_literal"], ["char_literal"]
    ]
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
