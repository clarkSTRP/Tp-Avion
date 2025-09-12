from flask import Flask, jsonify
from app.routes.compagnies import compagnies_endpoint
from app.routes.aeroports   import aeroports_endpoint
from app.routes.vols        import vols_endpoint
from app.routes.passagers   import passagers_endpoint
from app.routes.reservations import reservations_endpoint

def create_app():
    app = Flask(__name__)

    @app.get("/")
    def index():
     return jsonify({"message": "Tp-Avion"})
   
    compagnies_endpoint(app)
    vols_endpoint(app)
    passagers_endpoint(app)
    reservations_endpoint(app)
    aeroports_endpoint(app) 

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
