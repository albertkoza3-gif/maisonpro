import os


# ============================================================
# CHEMIN PRINCIPAL DU PROJET
# ============================================================

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# ============================================================
# SERVEUR MAISONPRO
# ============================================================

# Serveur en ligne Render
DEFAULT_API_BASE_URL = "https://maisonpro.onrender.com/api"

# Tu peux éventuellement définir API_BASE_URL dans les
# variables d'environnement pour changer de serveur.
API_BASE_URL = os.environ.get(
    "API_BASE_URL",
    DEFAULT_API_BASE_URL
).rstrip("/")


# URL de base du serveur sans /api
SERVER_ROOT_URL = API_BASE_URL.removesuffix("/api")


# ============================================================
# CONFIGURATION FLASK
# ============================================================

class Config:

    # --------------------------------------------------------
    # Sécurité
    # --------------------------------------------------------

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "maisonpro-secret-key-a-changer"
    )

    # --------------------------------------------------------
    # Base de données
    # --------------------------------------------------------

    # En ligne : Render pourra fournir DATABASE_URL.
    # En local : utilisation de SQLite.
    DATABASE_URL = os.environ.get("DATABASE_URL")

    if DATABASE_URL:
        # Render/PostgreSQL peut parfois fournir postgres://
        # SQLAlchemy utilise postgresql://
        if DATABASE_URL.startswith("postgres://"):
            DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1
            )

        SQLALCHEMY_DATABASE_URI = DATABASE_URL
    else:
        SQLALCHEMY_DATABASE_URI = (
            "sqlite:///"
            + os.path.join(BASE_DIR, "maisonpro.db")
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False


    # --------------------------------------------------------
    # Uploads
    # --------------------------------------------------------

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024


    # --------------------------------------------------------
    # Extensions de fichiers autorisées
    # --------------------------------------------------------

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "webp"
    }


    # --------------------------------------------------------
    # Token
    # --------------------------------------------------------

    TOKEN_EXPIRATION_SECONDS = 7 * 24 * 60 * 60


# ============================================================
# INFORMATIONS UTILISABLES PAR L'APPLICATION
# ============================================================

API_URL = API_BASE_URL