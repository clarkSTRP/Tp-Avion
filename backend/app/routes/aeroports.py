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
        return jsonify(rows)

    @app.post("/aeroports") # Créer un aéroport
    @require_api_key
    def add_aeroports():
        return jsonify({"message": "to do"})