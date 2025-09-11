from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine

def compagnies_endpoint(app):
    
    @app.get("/compagnies")
    def list_compagnies():
        with engine.connect() as conn:
            res = conn.execute(text("SELECT id, nom, code FROM compagnie"))
            return jsonify([dict(r) for r in res.mappings()])

    @app.get("/compagnies/<ref>")
    def get_compagnie_code(ref):
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, nom, code FROM compagnie Where LOWER(nom) = LOWER(:ref)"),{"ref": ref})
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows)

    @app.post("/compagnie") # Créer une compagnie
    def add_acompagnie():
        return jsonify({"message": "to do"})
