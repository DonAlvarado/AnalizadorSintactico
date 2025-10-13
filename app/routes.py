from flask import Blueprint, render_template, request, jsonify, send_from_directory
import os
from .Back.lexer import Lexer
from .Back.parser import Parser
from .Back.tree_viz import export_dot

bp = Blueprint("main", __name__, template_folder="Front/templates", static_folder="Front/static")
bp2 = Blueprint("api", __name__)

# Página principal (index opcional)
@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")  # bienvenida

# Panel principal / Analizador
@bp.route("/project", methods=["GET"])
def project_display():
    return render_template("ProjectDisplay.html")

# Endpoint para analizar código
@bp2.route("/api/analyze", methods=["POST"])
def analyze():
    code = request.json.get("code", "")
    
    lexer = Lexer(code)
    tokens = lexer.lex()
    if lexer.errors:
        return jsonify({"status": "lexer_error", "errors": lexer.errors})
    
    parser = Parser(tokens)
    tree, errs = parser.parse()  # <- desestructuramos correctamente
    if errs:
        return jsonify({"status": "parser_error", "errors": errs})
    
    dot_path = os.path.join("app/Front/static", "arbol.dot")
    export_dot(tree, dot_path)
    
    return jsonify({"status": "ok", "dot_path": dot_path})