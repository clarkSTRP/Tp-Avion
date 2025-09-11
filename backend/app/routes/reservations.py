from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine

def reservations_endpoint(app):
    
    @app.get("/reservations") #Afficher tous les vols disponibles
    def list_reservations():
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, passager_id, vol_id, status, date_reservation FROM reservation"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows)

    @app.post("/reservations") # Créer une réservation
    def add_reservations():
        return jsonify({"message": "to do"})

    @app.delete("/reservations") # Supprimer une réservation
    def del_aeroports():
        return jsonify({"message": "to do (delete)"})