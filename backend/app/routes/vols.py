from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine
from app.auth import require_api_key
from app.agents.log_agent import send_log

def vols_endpoint(app):
    
    @app.get("/vols") #Afficher tous les vols disponibles
    @require_api_key
    def list_vols():
        with engine.connect() as conn:
            send_log("INFO", "Liste des vols demandée")
            result = conn.execute(text("SELECT id, numero_vol, aeroport_depart_id, aeroport_arrivee_id, prix, places_disponibles FROM vol"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200
    
    @app.get("/vols/<ref>") # Afficher détail d'un vol
    @require_api_key
    def get_vols_code(ref):
        with engine.connect() as conn:
            send_log("INFO", f"Detail du vol {ref} demandée")
            result = conn.execute(text("SELECT numero_vol, compagnie_id, aeroport_depart_id, aeroport_arrivee_id, heure_depart, heure_arrivee, prix, places_disponibles FROM vol Where LOWER(numero_vol) = LOWER(:ref)"),{"ref": ref})
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows), 200

    @app.put("/vols/<ref>") # Modifier un vol
    @require_api_key
    def modify_vols(ref):
        data = request.get_json()

        allowed_fields = [
            "numero_vol",
            "compagnie_id",
            "aeroport_depart_id",
            "aeroport_arrivee_id",
            "heure_depart",
            "heure_arrivee",
            "prix",
            "places_disponibles"
        ]
        fields = {k: v for k, v in data.items() if k in allowed_fields and v is not None}

        set_clause = ", ".join([f"{col} = :{col}" for col in fields.keys()])

        fields["idVol"] = ref

        with engine.begin() as conn:
            send_log("INFO", f"modification de la reservation {ref}")
            result = conn.execute(
                text(f"UPDATE vol SET {set_clause} WHERE id = :idVol"),
                fields
            )
        if result.rowcount == 0:
            return jsonify({"error": "Vol non trouve"}), 404

        return jsonify({"message": "Vol mis a jour"}), 200

    @app.post("/vols")
    @require_api_key
    def add_vols():
        data = request.get_json() # Requiert du JSON en entrée

        numero_vol = data.get("numero_vol")
        compagnie_id = data.get("compagnie_id")
        aeroport_depart_id = data.get("aeroport_depart_id")
        aeroport_arrivee_id = data.get("aeroport_arrivee_id")
        heure_depart = data.get("heure_depart")
        heure_arrivee = data.get("heure_arrivee")
        prix = data.get("prix")
        places_disponibles = data.get("places_disponibles")

        with engine.begin() as conn:
            send_log("INFO", f"creation du vol {numero_vol}{compagnie_id}{aeroport_depart_id}{aeroport_arrivee_id}{heure_depart}{heure_arrivee}{prix}{places_disponibles}")
            result = conn.execute(
                text("INSERT INTO vol (numero_vol, compagnie_id, aeroport_depart_id, aeroport_arrivee_id, heure_depart, heure_arrivee, prix, places_disponibles) VALUES (:numero_vol, :compagnie_id, :aeroport_depart_id, :aeroport_arrivee_id, :heure_depart, :heure_arrivee, :prix, :places_disponibles)"),
                {
                    "numero_vol": numero_vol,
                    "compagnie_id": compagnie_id,
                    "aeroport_depart_id": aeroport_depart_id,
                    "aeroport_arrivee_id": aeroport_arrivee_id,
                    "heure_depart": heure_depart,
                    "heure_arrivee": heure_arrivee,
                    "prix": prix,
                    "places_disponibles": places_disponibles
                }
            )

        return jsonify({"message": "vol cree"}), 201
