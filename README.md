# 🧠 Analizador Sintáctico Avanzado para Java

Proyecto académico de la asignatura **Lenguajes Formales y Autómatas**, cuyo objetivo es construir un **analizador sintáctico predictivo LL(1)** capaz de procesar programas escritos en un **subconjunto de Java**.  
El sistema fue desarrollado desde cero en **Python + Flask**, integrando componentes de **análisis léxico**, **análisis sintáctico**, **clasificación semántica** y **visualización de árboles de derivación**.

---

## 📚 Descripción General

El sistema analiza el código fuente de un programa Java contenido en un archivo `programa.txt` o ingresado desde la interfaz web.  
Durante el análisis se generan:
- Lista de **tokens** detectados (identificadores, literales, operadores, símbolos).
- **Errores léxicos y sintácticos** con línea y descripción.
- **Árbol de derivación**, exportado en formato `.dot` y `.png`.
- Archivos de reporte:  
  - `errores.txt`  
  - `tabla_transicion.txt`  
  - `arbol.dot`  

Además, cuenta con una **interfaz gráfica Flask** que permite al usuario:
1. Cargar o escribir código Java.
2. Visualizar tokens, errores y el árbol de derivación.
3. Consultar el manual de usuario y el diagrama de arquitectura del sistema.

---

## ⚙️ Arquitectura del Proyecto

El proyecto se compone de tres capas principales:

Front-end (Flask + HTML/CSS/Bootstrap)
│
▼
Servidor Flask (routes.py / run.py)
│
▼
Back-end (Analizador: lexer, parser, semantic, etc.)

---

## 📂 Estructura de Carpetas

app/
├── Back/
│ ├── lexer.py
│ ├── parser.py
│ ├── parser_generator.py
│ ├── semantic.py
│ ├── grammar.py
│ ├── tokenizer.py
│ ├── tree_viz.py
│ └── table_gen.py
│
├── Front/
│ ├── templates/
│ │ ├── index.html
│ │ └── ProjectDisplay.html
│ ├── static/
│ │ ├── dashboard.css
│ │ ├── cover.css
│ │ ├── boostrap.min.css
│ │ ├── manual.pdf
│ │ |── Images/
│ │ | ├── JavaLogo.png
│ │ | └── arbol.png
│ │ |── arquitectura.drawio.svg
│ │ |
│ │──── icons/
│     └── arbol.png
├── routes.py
├── run.py
└── init.py

---

## 🔍 Funcionamiento

1. El usuario ingresa código Java desde la interfaz web.
2. Flask envía el texto al **endpoint `/api/analyze`**.
3. El módulo `lexer.py` tokeniza la entrada.
4. El módulo `parser.py` valida la estructura sintáctica usando la **tabla LL(1)**.
5. `tree_viz.py` genera la imagen del árbol de derivación.
6. El servidor devuelve los resultados en formato JSON.
7. La interfaz muestra los **tokens**, **errores** y el **árbol generado**.

---

## 🧩 Características técnicas

- **Lenguaje:** Python 3.11  
- **Framework:** Flask  
- **Visualización:** Graphviz (`.dot → .png`)  
- **Análisis sintáctico:** Predictivo descendente no recursivo  
- **Tabla:** LL(1) generada automáticamente  
- **Soporte de gramática:** Clases, variables, métodos, expresiones y retornos  
- **Tipos reconocidos:** `int`, `double`, `boolean`, `char`, `string`, `void`  
- **Errores detectados:** Léxicos (caracteres ilegales) y sintácticos (tokens inesperados)

---

## 🧾 Archivos generados

| Archivo | Descripción |
|----------|-------------|
| `errores.txt` | Detalle de errores léxicos y sintácticos con línea y descripción. |
| `tabla_transicion.txt` | Tabla LL(1) generada automáticamente. |
| `arbol.dot / arbol.png` | Árbol de derivación visualizable. |

---

## 🧭 Documentación adicional

- 📘 **Manual de usuario:** [Front/static/manual.pdf](app/Front/static/manual.pdf)  
- 🏗️ **Diagrama de arquitectura:** visible desde la vista *"Diagrama de arquitectura"* en el panel web.  
- 📜 **Enunciado oficial:** disponible en `Enunciado del Proyecto 2.pdf`.

---

## 🧪 Ejemplo de entrada

```java
class Demo {
  int x;
  int y;

  int suma(int a, int b) {
    return a + b;
  }

  void main() {
    x = 2 + 3 * (4 + 5);
    y = suma(x, 10);
    return;
  }
}
```

---

## 🧑‍💻 Ejecucion local

# Crear entorno virtual
python -m venv venv
venv\Scripts\activate

# Instalar dependencias
pip install flask graphviz

# Ejecutar servidor
python -m app.run

## 🧩 Creditos

Desarrollado por Axel Alvarado
Curso: Lenguajes Formales y Autómatas
Fecha: Jueves 23 de octubre del 2025