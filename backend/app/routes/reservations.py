from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine
from app.auth import require_api_key

def reservations_endpoint(app):
    
    @app.get("/reservations") #Afficher tous les vols disponibles
    @require_api_key
    def list_reservations():
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, passager_id, vol_id, status, date_reservation FROM reservation"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows)

    @app.post("/reservations") # Créer une réservation
    @require_api_key
    def add_reservations():
        return jsonify({"message": "to do"})

    @app.delete("/reservations") # Supprimer une réservation
    @require_api_key
    def del_aeroports():
        return jsonify({"message": "to do (delete)"})