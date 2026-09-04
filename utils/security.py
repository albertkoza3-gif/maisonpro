from functools import wraps

from flask import request, jsonify, g, current_app
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired


def generate_token(user_id):
    """Crée un token signé contenant l'identifiant de l'utilisateur."""
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps({"user_id": user_id})


def verify_token(token):
    """Vérifie un token et renvoie l'identifiant utilisateur, ou None si invalide."""
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        data = serializer.loads(
            token, max_age=current_app.config["TOKEN_EXPIRATION_SECONDS"]
        )
        return data.get("user_id")
    except (BadSignature, SignatureExpired):
        return None


def get_token_from_request():
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header.split(" ", 1)[1].strip()
    return None


def token_required(f):
    """Décorateur : protège une route, exige un utilisateur connecté."""

    @wraps(f)
    def decorated(*args, **kwargs):
        # Import ici pour éviter les imports circulaires avec models.py
        from models import User

        token = get_token_from_request()
        if not token:
            return jsonify({"error": "Authentification requise."}), 401

        user_id = verify_token(token)
        if not user_id:
            return jsonify({"error": "Token invalide ou expiré."}), 401

        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "Utilisateur introuvable."}), 401
        if user.is_blocked:
            return jsonify({"error": "Ce compte a été bloqué par l'administrateur."}), 403

        g.current_user = user
        return f(*args, **kwargs)

    return decorated


def admin_required(f):
    """Décorateur : protège une route, exige un utilisateur administrateur."""

    @wraps(f)
    @token_required
    def decorated(*args, **kwargs):
        if not g.current_user.is_admin:
            return jsonify({"error": "Accès réservé à l'administrateur."}), 403
        return f(*args, **kwargs)

    return decorated


def allowed_file(filename, allowed_extensions):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in allowed_extensions
    )