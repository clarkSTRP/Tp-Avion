from flask import Flask, request, jsonify
from sqlalchemy import text
from app.connect import engine

def create_app():
    app = Flask(__name__)

    @app.route("/logs", methods=["POST"])
    def receive_log():
        data = request.json
        service = data.get("service", "unknown")
        level = data.get("level", "INFO")
        message = data.get("message", "")
        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO logs (service, level, message) VALUES (:service, :level, :message)"),
                {"service": service, "level": level, "message": message}
            )
        return jsonify({"status": "ok"}), 201
        
    @app.route("/logs", methods=["GET"])
    def get_logs():
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM logs ORDER BY timestamp DESC"))
            logs = [dict(row) for row in result.mappings()]
        return jsonify(logs)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)