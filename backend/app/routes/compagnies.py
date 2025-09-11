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

    @app.post("/compagnies")
    def add_compagnie():
        data = request.get_json() # Requiert du JSON en entrée

        nom = data.get("nom")
        code = data.get("code")

        with engine.begin() as conn:
            result = conn.execute(
                text("INSERT INTO compagnie (nom, code) VALUES (:nom, :code)"),
                {
                    "nom": nom,
                    "code": code
                }
            )

        return jsonify({
            "message": "Compagnie creee",
        })