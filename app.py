from flask import Flask, render_template
import sqlite3
from database import crear_tabla

app = Flask(__name__)

# Creamos la tabla si no existe
crear_tabla()

# Función para obtener productos desde SQLite
def obtener_productos():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

# Página principal: solo bienvenida
@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

# Página de inventario: muestra la tabla
@app.route("/inventario")
def mostrar_inventario():
    productos = obtener_productos()
    return render_template("inventario.html", productos=productos)

if __name__ == "__main__":
    app.run(debug=True)