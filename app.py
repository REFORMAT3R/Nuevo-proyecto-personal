from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
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


# ======== INICIO DEL SERVIDOR =========
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)