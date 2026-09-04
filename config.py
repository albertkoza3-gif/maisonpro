import os


# ============================================================
# CHEMIN DE BASE DU PROJET
# ============================================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# ============================================================
# ADRESSE DE L'API
# ============================================================

# En local : http://127.0.0.1:5000/api
# En production, cette variable sera fournie par le serveur.
API_BASE_URL = os.environ.get(
    "API_BASE_URL",
    "http://127.0.0.1:5000/api"
)

SERVER_ROOT_URL = API_BASE_URL.rstrip("/").removesuffix("/api")


# ============================================================
# CONFIGURATION FLASK
# ============================================================

class Config:
    """Configuration centrale de l'application MAISONPRO."""

    # Clé secrète
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "maisonpro-secret-key-a-changer"
    )

    # Base de données
    #
    # En local :
    #     SQLite -> maisonpro.db
    #
    # En production :
    #     DATABASE_URL sera fournie par l'hébergeur
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'maisonpro.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Dossier des photos
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    # Taille maximale : 16 Mo
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Extensions autorisées
    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "webp"
    }

    # Token valable 7 jours
    TOKEN_EXPIRATION_SECONDS = 60 * 60 * 24 * 7