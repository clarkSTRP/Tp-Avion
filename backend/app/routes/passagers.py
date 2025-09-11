from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine
from app.auth import require_api_key

def passagers_endpoint(app):
    
    @app.get("/passager/<ref>") # Afficher détail d'un passager
    @require_api_key
    def get_passager_code(ref):
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM passager Where LOWER(passport_numero) = LOWER(:ref)"),{"ref": ref})
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows)

    @app.post("/passager") # Créer un passager
    @require_api_key
    def add_passager():
        return jsonify({"message": "to do"})