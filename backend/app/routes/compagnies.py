from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine
from app.auth import require_api_key

def compagnies_endpoint(app):
    
    @app.get("/compagnies")
    @require_api_key
    def list_compagnies():
        with engine.connect() as conn:
            res = conn.execute(text("SELECT id, nom, code FROM compagnie"))
            return jsonify([dict(r) for r in res.mappings()])

    @app.get("/compagnies/<ref>")
    @require_api_key
    def get_compagnie_code(ref):
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, nom, code FROM compagnie Where LOWER(nom) = LOWER(:ref)"),{"ref": ref})
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows)

    @app.post("/compagnie") # Créer une compagnie
    @require_api_key
    def add_acompagnie():
        return jsonify({"message": "to do"})
