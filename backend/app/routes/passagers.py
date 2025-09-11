from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine

def passagers_endpoint(app):
    
    @app.get("/passager/<ref>") # Afficher détail d'un passager
    def get_passager_code(ref):
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM passager Where LOWER(passport_numero) = LOWER(:ref)"),{"ref": ref})
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows)