from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine
from app.auth import require_api_key
from datetime import datetime, timezone, timedelta

def reservations_endpoint(app):
    
    @app.get("/reservations") #Afficher tous les vols disponibles
    @require_api_key
    def list_reservations():
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, passager_id, vol_id, status, date_reservation FROM reservation"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200


    @app.post("/reservations")
    @require_api_key
    def add_reservations():
        data = request.get_json() # Requiert du JSON en entrée

        # Date actuelle à UTC+2 :
        tz_utc2 = timezone(timedelta(hours=2))
        horaire_utc2 = datetime.now(tz_utc2)

        passager_id = data.get("passager_id")
        vol_id = data.get("vol_id")
        status = data.get("status", "confirmee")
        date_reservation = data.get("date_reservation", horaire_utc2)

        with engine.begin() as conn:
            result = conn.execute(
                text("INSERT INTO reservation (passager_id, vol_id, status, date_reservation) VALUES (:passager_id, :vol_id, :status, :date_reservation)"),
                {
                    "passager_id": passager_id,
                    "vol_id": vol_id,
                    "status": status,
                    "date_reservation": date_reservation
                }
            )

        return jsonify({"message": "Reservation creee"}), 201

    @app.delete("/reservations/<ref>") # Supprimer une réservation
    @require_api_key
    def del_aeroports(ref):
        with engine.begin() as conn:
            result = conn.execute(text("DELETE FROM reservation Where passager_id =:ref"),{"ref": ref})
        return jsonify({"mesage": "success"}), 202