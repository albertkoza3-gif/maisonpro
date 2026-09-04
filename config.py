import os


# ============================================================
# CHEMIN PRINCIPAL DU PROJET
# ============================================================

BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


# ============================================================
# SERVEUR MAISONPRO
# ============================================================

DEFAULT_API_BASE_URL = (
    "https://maisonpro.onrender.com/api"
)

API_BASE_URL = os.environ.get(
    "API_BASE_URL",
    DEFAULT_API_BASE_URL
).rstrip("/")


SERVER_ROOT_URL = (
    API_BASE_URL.removesuffix("/api")
)


# ============================================================
# CONFIGURATION FLASK
# ============================================================

class Config:

    # --------------------------------------------------------
    # SÉCURITÉ
    # --------------------------------------------------------

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "maisonpro-secret-key-a-changer"
    )

    # --------------------------------------------------------
    # BASE DE DONNÉES
    # --------------------------------------------------------

    DATABASE_URL = os.environ.get(
        "DATABASE_URL"
    )

    if DATABASE_URL:

        if DATABASE_URL.startswith(
            "postgres://"
        ):

            DATABASE_URL = DATABASE_URL.replace(
                "postgres://",
                "postgresql://",
                1
            )

        SQLALCHEMY_DATABASE_URI = (
            DATABASE_URL
        )

    else:

        SQLALCHEMY_DATABASE_URI = (
            "sqlite:///"
            + os.path.join(
                BASE_DIR,
                "maisonpro.db"
            )
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --------------------------------------------------------
    # ANCIEN DOSSIER UPLOAD
    # Conservé pour compatibilité
    # --------------------------------------------------------

    UPLOAD_FOLDER = os.path.join(
        BASE_DIR,
        "uploads"
    )

    # --------------------------------------------------------
    # LIMITE DES FICHIERS
    # --------------------------------------------------------

    MAX_CONTENT_LENGTH = (
        16 * 1024 * 1024
    )

    # --------------------------------------------------------
    # EXTENSIONS AUTORISÉES
    # --------------------------------------------------------

    ALLOWED_EXTENSIONS = {
        "png",
        "jpg",
        "jpeg",
        "gif",
        "webp"
    }

    # --------------------------------------------------------
    # CLOUDINARY
    # --------------------------------------------------------

    CLOUDINARY_CLOUD_NAME = os.environ.get(
        "CLOUDINARY_CLOUD_NAME"
    )

    CLOUDINARY_API_KEY = os.environ.get(
        "CLOUDINARY_API_KEY"
    )

    CLOUDINARY_API_SECRET = os.environ.get(
        "CLOUDINARY_API_SECRET"
    )

    # --------------------------------------------------------
    # TOKEN
    # --------------------------------------------------------

    TOKEN_EXPIRATION_SECONDS = (
        7 * 24 * 60 * 60
    )


# ============================================================
# INFORMATIONS POUR L'APPLICATION
# ============================================================

API_URL = API_BASE_URL