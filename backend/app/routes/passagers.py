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

    @app.post("/passager")
    def add_passager():
        data = request.get_json() # Requiert du JSON en entrée

        nom = data.get("nom")
        email = data.get("email")
        tel = data.get("tel")
        passport_numero = data.get("passport_numero")

        with engine.begin() as conn:
            result = conn.execute(
                text("INSERT INTO passager (nom, email, tel, passport_numero) VALUES (:nom, :email, :tel, :passport_numero)"),
                {
                    "nom": nom,
                    "email": email,
                    "tel": tel,
                    "passport_numero": passport_numero
                }
            )

        return jsonify({
            "message": "Passager cree",
        })