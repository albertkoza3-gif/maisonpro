from app import create_app
from extensions import db

app = create_app()

# Crée les tables manquantes au démarrage.
# Cela ne supprime aucune donnée existante.
with app.app_context():
    db.create_all()