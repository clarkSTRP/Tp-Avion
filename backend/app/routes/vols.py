from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine
from app.auth import require_api_key

def vols_endpoint(app):
    
    @app.get("/vols") #Afficher tous les vols disponibles
    @require_api_key
    def list_vols():
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, aeroport_depart_id, aeroport_arrivee_id, prix, places_disponibles FROM vol"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows)
    
    @app.get("/vols/<ref>") # Afficher détail d'un vol
    @require_api_key
    def get_vols_code(ref):
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM vol Where LOWER(numero_vol) = LOWER(:ref)"),{"ref": ref})
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows)

    @app.post("/vols") # Créer un vol
    @require_api_key
    def add_vols():
        return jsonify({"message": "to do"})