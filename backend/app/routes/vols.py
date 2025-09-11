from flask import request, jsonify, abort
from sqlalchemy import text
from ..connect import engine

def vols_endpoint(app):
    
    @app.get("/vols") #Afficher tous les vols disponibles
    def list_vols():
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id, numero_vol, aeroport_depart_id, aeroport_arrivee_id, prix, places_disponibles FROM vol"))
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows)
    
    @app.get("/vols/<ref>") # Afficher détail d'un vol
    def get_vols_code(ref):
        with engine.connect() as conn:
            result = conn.execute(text("SELECT numero_vol, compagnie_id, aeroport_depart_id, aeroport_arrivee_id, heure_depart, heure_arrivee, prix, places_disponibles FROM vol Where LOWER(numero_vol) = LOWER(:ref)"),{"ref": ref})
            rows = [dict(r) for r in result.mappings()]
        return jsonify(rows)

    @app.put("/vols/<ref>") # Créer un vol
    def add_vols():
        return jsonify({"message": "to do"})