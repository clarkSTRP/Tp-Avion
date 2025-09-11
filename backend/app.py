import os
from flask import Flask, jsonify
from sqlalchemy import create_engine, text

DB_USER = os.getenv("DB_USER", "tp_user")
DB_PASS = os.getenv("DB_PASS", "tp_pass")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "tp_avion")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Tp-Avion"})

# Routes des compagnies
@app.get("/compagnies")
def list_compagnies():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, nom, code FROM compagnie"))
        rows = [dict(r) for r in result.mappings()]
    return jsonify(rows)

@app.get("/compagnies/<ref>") #Afficher compagnie spécifique
def get_compagnie_code(ref):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, nom, code FROM compagnie Where LOWER(nom) = LOWER(:ref)"),{"ref": ref})
        rows = [dict(r) for r in result.mappings()]
    return jsonify(rows)


@app.post("/compagnies")
def post_compagnie_code():
    with engine.connect() as conn:
        result = conn.execute(text("INSERT INTO compagnie (nom, code) VALUES ('Compagnie test', 'TT')"))
        rows = [dict(r) for r in result.mappings()]
    return jsonify(rows)

# Routes des aeroports
@app.get("/aeroports") # Afficher la liste des aéroports
def list_aeroports():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, nom, code, ville FROM aeroport"))
        rows = [dict(r) for r in result.mappings()]
    return jsonify(rows)

# Routes des vols
@app.get("/vols") #Afficher tous les vols disponibles
def list_vols():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, aeroport_depart_id, aeroport_arrivee_id, prix, places_disponibles FROM vol"))
        rows = [dict(r) for r in result.mappings()]
    return jsonify(rows)

@app.get("/vols/<ref>") # Afficher détail d'un vol
def get_vols_code(ref):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM vol Where LOWER(numero_vol) = LOWER(:ref)"),{"ref": ref})
        rows = [dict(r) for r in result.mappings()]
    return jsonify(rows)

# Route des passagers
@app.get("/passager/<ref>") # Afficher détail d'un passager
def get_passager_code(ref):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM passager Where LOWER(passport_numero) = LOWER(:ref)"),{"ref": ref})
        rows = [dict(r) for r in result.mappings()]
    return jsonify(rows)

# Route de réservations
@app.get("/reservations") #Afficher tous les vols disponibles
def list_reservations():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, passager_id, vol_id, status, date_reservation FROM reservation"))
        rows = [dict(r) for r in result.mappings()]
    return jsonify(rows)
 