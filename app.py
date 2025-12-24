from flask import Flask, request, jsonify, render_template
import mysql.connector
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# ================== CONEXIÓN DB ==================
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="smashhub"
    )

# ================== PÁGINAS ==================
@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/proximos")
def proximos_page():
    return render_template("proximos.html")
@app.route("/jugadores")
def jugadores_page():
    return render_template("jugadores.html")

@app.route("/anteriores")
def anteriores_page():
    return render_template("anteriores.html")

@app.route("/torneo/<tipo>/<slug>")
def torneo_page(tipo, slug):
    try:
        if tipo == "proximos":
            carpeta = "Torneos proximos"
        elif tipo == "terminados":
            carpeta = "Torneos terminados"
        else:
            return "Tipo inválido", 404

        return render_template(f"{carpeta}/{slug}.html")

    except:
        return "Torneo no encontrado", 404

# ================== REGISTER ==================
@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)
    print("DATA:", data)

    if not data:
        return jsonify({"status": "no data"}), 400

    try:
        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute(
            "SELECT 1 FROM usuarios WHERE email=%s OR usuario=%s",
            (data["correo"], data["usuario"])
        )

        if cursor.fetchone():
            return jsonify({"status": "exists"}), 409

        password_hash = bcrypt.generate_password_hash(
            data["contrasena"]
        ).decode("utf-8")

        cursor.execute("""
            INSERT INTO usuarios
            (nombres, apellidos, email, nacimiento, genero, usuario, contrasena)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            data["nombres"],
            data["apellidos"],
            data["correo"],
            data["nacimiento"],
            data["genero"],
            data["usuario"],
            password_hash
        ))

        conexion.commit()
        return jsonify({"status": "ok"})

    except Exception as e:
        print("ERROR SQL:", e)
        return jsonify({"status": "error", "msg": str(e)}), 500

    finally:
        cursor.close()
        conexion.close()

# ================== LOGIN ==================
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json(force=True)

    if not data:
        return jsonify({"status": "bad request"}), 400

    user = data.get("usuario")
    password = data.get("contrasena")

    if not user or not password:
        return jsonify({"status": "missing data"}), 400

    conexion = conectar()
    cursor = conexion.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM usuarios
        WHERE email=%s OR usuario=%s
    """, (user, user))

    result = cursor.fetchone()

    cursor.close()
    conexion.close()

    if result and bcrypt.check_password_hash(result["contrasena"], password):
        return jsonify({"status": "ok"})
    else:
        return jsonify({"status": "error"}), 401

# ================== MAIN ==================
if __name__ == "__main__":
    app.run()
