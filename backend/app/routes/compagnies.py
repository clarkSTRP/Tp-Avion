from flask import request, jsonify, abort
from app.agents.log_agent import send_log
from sqlalchemy import text
from ..connect import engine
from app.agents.log_agent import send_log
from app.auth import require_api_key

def compagnies_endpoint(app):
    
    @app.get("/compagnies")
    @require_api_key
    def list_compagnies():
        with engine.connect() as conn:
            send_log("INFO", "Liste des compagnies demandée")
            res = conn.execute(text("SELECT id, nom, code FROM compagnie"))
            return jsonify([dict(r) for r in res.mappings()]), 200

    @app.get("/compagnies/<ref>")
    @require_api_key
    def get_compagnie_code(ref):
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, nom, code FROM compagnie Where LOWER(nom) = LOWER(:ref)"),{"ref": ref})
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200

    @app.post("/compagnies")
    @require_api_key
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
        return jsonify({"message": "Compagnie creee"}), 201