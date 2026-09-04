from flask import Blueprint, request, jsonify

from extensions import db
from models import User
from utils.security import generate_token

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    first_name = (data.get("first_name") or "").strip()
    last_name = (data.get("last_name") or "").strip()
    phone = (data.get("phone") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    confirm_password = data.get("confirm_password") or ""

    # --- Validation des données ---
    if not all([first_name, last_name, phone, email, password, confirm_password]):
        return jsonify({"error": "Tous les champs sont obligatoires."}), 400

    if password != confirm_password:
        return jsonify({"error": "Les mots de passe ne correspondent pas."}), 400

    if len(password) < 6:
        return jsonify({"error": "Le mot de passe doit contenir au moins 6 caractères."}), 400

    if "@" not in email or "." not in email:
        return jsonify({"error": "Adresse e-mail invalide."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Cet e-mail est déjà utilisé."}), 409

    if User.query.filter_by(phone=phone).first():
        return jsonify({"error": "Ce numéro de téléphone est déjà utilisé."}), 409

    user = User(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        email=email,
        roles="acheteur",
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    token = generate_token(user.id)
    return jsonify({"token": token, "user": user.to_dict(include_private=True)}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "E-mail et mot de passe requis."}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "E-mail ou mot de passe incorrect."}), 401

    if user.is_blocked:
        return jsonify({"error": "Ce compte a été bloqué par l'administrateur."}), 403

    token = generate_token(user.id)
    return jsonify({"token": token, "user": user.to_dict(include_private=True)}), 200