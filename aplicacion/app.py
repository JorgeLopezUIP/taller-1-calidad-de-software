
from flask import Flask, render_template, request, redirect, url_for, session, flash
from conexion import obtener_conexion
from werkzeug.security import generate_password_hash, check_password_hash
import os, secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(31)  


@app.route("/")
def inicio():
    return redirect(url_for("login"))


# REGISTRAR ESTUDIANTES
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"].strip()
        email = request.form["email"].strip().lower()
        contrasena = request.form["contrasena"]

        if not nombre or not email or not contrasena:
            flash("Todos los campos son obligatorios")
            return redirect(url_for("registro"))

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "SELECT id FROM estudiantes WHERE email = %s",
                (email,)
            )

            if cursor.fetchone():
                flash("Este correo ya está registrado")
                return redirect(url_for("registro"))

            contrasena_hash = generate_password_hash(contrasena)

            cursor.execute("""
                INSERT INTO estudiantes (nombre, email, contrasena)
                VALUES (%s, %s, %s)
            """, (nombre, email, contrasena_hash))

            conexion.commit()
            flash("Registro exitoso. Ahora inicia sesión")
            return redirect(url_for("login"))

        finally:
            cursor.close()
            conexion.close()

    return render_template("registro.html")


# INICIAR SESIÓN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        contrasena = request.form["contrasena"]

        conexion = obtener_conexion()
        cursor = conexion.cursor()

        try:
            cursor.execute(
                "SELECT * FROM estudiantes WHERE email = %s",
                (email,)
            )
            estudiante = cursor.fetchone()

        finally:
            cursor.close()
            conexion.close()

        if estudiante and check_password_hash(
            estudiante["contrasena"], contrasena
        ):
            session.clear()
            session["id"] = estudiante["id"]
            session["nombre"] = estudiante["nombre"]

            return redirect(url_for("bienvenido"))

        flash("Correo o contraseña incorrectos")

    return render_template("login.html")


# PÁGINA DE BIENVENIDA
@app.route("/bienvenido")
def bienvenido():
    if "id" not in session:
        return redirect(url_for("login"))

    return render_template(
        "bienvenido.html",
        nombre=session["nombre"]
    )


# CERRAR SESIÓN
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
