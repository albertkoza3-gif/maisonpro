import os

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from config import Config
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Autorise l'application mobile (autre origine) à appeler cette API
    CORS(app)

    # Crée le dossier des photos si nécessaire
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)

    # Import des modèles pour que db.create_all() les connaisse
    import models  # noqa: F401

    # Enregistrement des routes (blueprints)
    from routes.auth_routes import auth_bp
    from routes.property_routes import property_bp
    from routes.user_routes import user_bp
    from routes.favorite_routes import favorite_bp
    from routes.report_routes import report_bp
    from routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(property_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(favorite_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(admin_bp)

    @app.route("/uploads/<path:filename>")
    def serve_upload(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    @app.route("/")
    def index():
        return jsonify({
            "app": "MAISONPRO API",
            "status": "en ligne",
            "version": "1.0",
        })

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Route introuvable."}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Erreur interne du serveur."}), 500

    return app