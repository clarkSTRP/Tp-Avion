from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine
from app.auth import require_api_key
from app.agents.log_agent import send_log

def passagers_endpoint(app):
    
    @app.get("/passager/<ref>") # Afficher détail d'un passager
    @require_api_key
    def get_passager_code(ref):
        with engine.connect() as conn:
            send_log("INFO", f"detail du passagers {ref} demandée")
            result = conn.execute(text("SELECT * FROM passager Where LOWER(passport_numero) = LOWER(:ref)"),{"ref": ref})
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200

    @app.post("/passager")
    @require_api_key
    def add_passager():

        data = request.get_json() # Requiert du JSON en entrée

        nom = data.get("nom")
        email = data.get("email")
        tel = data.get("tel")
        passport_numero = data.get("passport_numero")

        with engine.begin() as conn:
            send_log("INFO", f"creation du passager {nom}{email}{tell}{passport_numero}")
            result = conn.execute(
                text("INSERT INTO passager (nom, email, tel, passport_numero) VALUES (:nom, :email, :tel, :passport_numero)"),
                {
                    "nom": nom,
                    "email": email,
                    "tel": tel,
                    "passport_numero": passport_numero
                }
            )

        return jsonify({"message": "Passager cree"}), 201