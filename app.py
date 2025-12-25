from flask import Flask, render_template, request, jsonify
from werkzeug.security import generate_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)

# ================== BASE DE DATOS ==================
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL and "sslmode" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ======== TABLA USUARIOS REAL =========
class Usuario(db.Model):
    __tablename__ = "usuarios"
  
    nombres = db.Column(db.String(100), nullable=False)
    apellidos = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nacimiento = db.Column(db.Date, nullable=False)
    genero = db.Column(db.String(20), nullable=False)
    usuario = db.Column(db.String(50), primary_key=True)
    contrasena = db.Column(db.String(200), nullable=False)   

# ======== PÁGINAS =========
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


# ======== TORNEO DINÁMICO =========
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


# ======== CREAR TABLAS EN LA DB =========
with app.app_context():
    db.create_all()

@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json()

    usuario = data.get("usuario")
    nombres = data.get("nombres")
    apellidos = data.get("apellidos")
    email = data.get("correo")
    nacimiento = data.get("nacimiento")
    genero = data.get("genero")
    contrasena = data.get("contrasena")

    # Validar si ya existe
    existe = Usuario.query.filter(
        (Usuario.usuario == usuario) | (Usuario.email == email)
    ).first()

    if existe:
        return jsonify({"error": "usuario_o_email_repetido"}), 409

    nuevo = Usuario(
        usuario=usuario,
        nombres=nombres,
        apellidos=apellidos,
        email=email,
        nacimiento=datetime.strptime(nacimiento, "%Y-%m-%d"),
        genero=genero,
        contrasena=generate_password_hash(contrasena)
    )

    db.session.add(nuevo)
    db.session.commit()

    return jsonify({"message": "creado"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    usuario = data.get("usuario")
    contrasena = data.get("contrasena")

    if not usuario or not contrasena:
        return jsonify({"error": "Faltan datos"}), 400

    # Buscar usuario por username o email
    user = Usuario.query.filter(
        (Usuario.usuario == usuario) | (Usuario.email == usuario)
    ).first()

    if not user:
        return jsonify({"error": "Usuario no existe"}), 401

    if check_password_hash(user.contrasena, contrasena):
        return jsonify({"ok": True}), 200

    return jsonify({"error": "Contraseña incorrecta"}), 401

# ======== INICIO DEL SERVIDOR =========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)