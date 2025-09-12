from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine
from app.auth import require_api_key

def aeroports_endpoint(app):
    
    @app.get("/aeroports") # Afficher la liste des aéroports
    @require_api_key
    def list_aeroports():
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, nom, code, ville FROM aeroport"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200

    @app.post("/aeroports")
    @require_api_key
    def add_aeroports():
        data = request.get_json() # Requiert du JSON en entrée

        nom = data.get("nom")
        code = data.get("code")
        ville = data.get("ville")

        with engine.begin() as conn:
            result = conn.execute(
                text("INSERT INTO aeroport (nom, code, ville) VALUES (:nom, :code, :ville)"),
                {
                    "nom": nom,
                    "code": code,
                    "ville": ville
                }
            )
        return jsonify({"message": "Aeroport cree"}), 201