from flask import Blueprint, request, jsonify, current_app, render_template
from .Back.lexer import Lexer
from .Back.parser import Parser
from .Back.tree_viz import export_dot, render_dot_to_png
import os


bp = Blueprint("main", __name__, template_folder="Front/templates", static_folder="Front/static")
bp2 = Blueprint("api", __name__)

@bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@bp.route("/project", methods=["GET"])
def project_display():
    return render_template("ProjectDisplay.html")

@bp2.route("/api/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    code = data.get("code", "")

    lex = Lexer(code)
    tokens = lex.lex()
    token_list = [
        {"lexeme": t.value, "category": t.type, "line": t.line}
        for t in tokens if t.type not in ("$",)
    ]

    parser = Parser(tokens)
    tree, errors = parser.parse()

    static_dir = os.path.join(current_app.root_path, "Front", "static")
    os.makedirs(static_dir, exist_ok=True)

    dot_path = os.path.join(static_dir, "arbol.dot")
    png_path = os.path.join(static_dir, "Images", "arbol.png")

    export_dot(tree, dot_path)
    try:
        render_dot_to_png(dot_path, png_path)
        tree_image = f"static/Images/arbol.png"
    except Exception as e:
        tree_image = None
        errors.append(f"Error al generar árbol: {e}")

    return jsonify({
        "tokens": token_list,
        "errors": errors,
        "tree_image": tree_image
    })
