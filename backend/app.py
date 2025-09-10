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

@app.get("/compagnies")
def list_compagnies():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, nom, code FROM compagnie"))
        rows = [dict(r) for r in result.mappings()]
    return jsonify(rows)

# c return the id of  a company
@app.get("/compagnies/<ref>")
def get_compagnie_code(ref):
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, nom, code FROM compagnie Where LOWER(nom) = LOWER(:ref)"),{"ref": ref})
        rows = [dict(r) for r in result.mappings()]
    return jsonify(rows)

@app.get("/aeroports")
def list_aeroports():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id, nom, code, ville FROM aeroport"))
        rows = [dict(r) for r in result.mappings()]
    return jsonify(rows)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
