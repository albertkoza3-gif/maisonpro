"""
Configuration de MAISONPRO
"""

import os


# ============================================================
# CHEMIN DU PROJET
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ============================================================
# API FLASK
# ============================================================

API_BASE_URL = "http://127.0.0.1:5000/api"

SERVER_ROOT_URL = API_BASE_URL.replace("/api", "")


# ============================================================
# SÉCURITÉ
# ============================================================

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "maisonpro-secret-key-a-changer"
)


# ============================================================
# BASE DE DONNÉES
# ============================================================

SQLALCHEMY_DATABASE_URI = os.environ.get(
    "DATABASE_URL",
    f"sqlite:///{os.path.join(BASE_DIR, 'maisonpro.db')}"
)

SQLALCHEMY_TRACK_MODIFICATIONS = False


# ============================================================
# UPLOADS
# ============================================================

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

MAX_CONTENT_LENGTH = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = {
    "png",
    "jpg",
    "jpeg",
    "gif",
    "webp"
}


# ============================================================
# TOKEN
# ============================================================

TOKEN_EXPIRATION_SECONDS = 60 * 60 * 24 * 7