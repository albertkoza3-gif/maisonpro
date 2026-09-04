"""
Point d'entrée du serveur MAISONPRO.

Utilisation locale :
    python run.py

Pour la production :
    l'application est chargée par wsgi.py
"""

from app import create_app
from extensions import db

app = create_app()


with app.app_context():
    # Crée uniquement les tables manquantes.
    # Ne supprime aucune donnée existante.
    db.create_all()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )