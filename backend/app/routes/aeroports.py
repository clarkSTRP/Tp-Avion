from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine

def aeroports_endpoint(app):
    
    @app.get("/aeroports") # Afficher la liste des aéroports
    def list_aeroports():
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, nom, code, ville FROM aeroport"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows)

    @app.post("/aeroports") # Créer un aéroport
    def add_aeroports():
        return jsonify({"message": "to do"})