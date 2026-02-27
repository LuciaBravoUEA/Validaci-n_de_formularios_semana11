from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Función para obtener productos desde la base de datos
def obtener_productos():
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM productos")
    productos = cursor.fetchall()
    conn.close()
    return productos

# Ruta principal
@app.route("/")
def inicio():
    return render_template("index.html")

# Ruta acerca de
@app.route("/about")
def about():
    return render_template("about.html")

# Ruta inventario
@app.route("/inventario")
def inventario():
    productos = obtener_productos()
    return render_template("inventario.html", productos=productos)

# Ruta eliminar producto
@app.route("/eliminar/<int:id>")
def eliminar(id):
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM productos WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("inventario"))

# Ruta editar producto
@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = sqlite3.connect("inventario.db")
    cursor = conn.cursor()
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        cantidad = request.form["cantidad"]
        cursor.execute("UPDATE productos SET nombre=?, precio=?, cantidad=? WHERE id=?",
                       (nombre, precio, cantidad, id))
        conn.commit()
        conn.close()
        return redirect(url_for("inventario"))
    else:
        cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
        producto = cursor.fetchone()
        conn.close()
        return render_template("editar.html", producto=producto)

# Ruta agregar producto
@app.route("/agregar", methods=["GET", "POST"])
def agregar():
    if request.method == "POST":
        nombre = request.form["nombre"]
        precio = request.form["precio"]
        cantidad = request.form["cantidad"]
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO productos (nombre, precio, cantidad) VALUES (?, ?, ?)",
                       (nombre, precio, cantidad))
        conn.commit()
        conn.close()
        return redirect(url_for("inventario"))
    return render_template("agregar.html")

# Ruta buscar producto
@app.route("/buscar", methods=["GET", "POST"])
def buscar():
    productos = []
    if request.method == "POST":
        termino = request.form["termino"]
        conn = sqlite3.connect("inventario.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + termino + '%',))
        productos = cursor.fetchall()
        conn.close()
    return render_template("buscar.html", productos=productos)

# Bloque principal para arrancar Flask
if __name__ == "__main__":
    app.run(debug=True)