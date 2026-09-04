import os
import uuid

from flask import Blueprint, request, jsonify, g, current_app

from extensions import db
from models import User
from utils.security import token_required, allowed_file

user_bp = Blueprint("users", __name__, url_prefix="/api/users")


# =========================================================
# RECUPERER MON PROFIL
# =========================================================

@user_bp.route("/me", methods=["GET"])
@token_required
def get_me():

    return jsonify(
        g.current_user.to_dict(include_private=True)
    ), 200


# =========================================================
# MODIFIER MON PROFIL
# =========================================================

@user_bp.route("/me", methods=["PUT"])
@token_required
def update_me():

    user = g.current_user

    # Accepte JSON ou formulaire
    if request.form:
        form = request.form
    else:
        form = request.get_json(silent=True) or {}

    first_name = form.get("first_name")
    last_name = form.get("last_name")
    phone = form.get("phone")
    email = form.get("email")
    password = form.get("password")
    roles = form.get("roles")

    # -----------------------------------------------------
    # PRENOM
    # -----------------------------------------------------

    if first_name is not None:

        first_name = str(first_name).strip()

        if not first_name:
            return jsonify({
                "error": "Le prénom est obligatoire."
            }), 400

        user.first_name = first_name

    # -----------------------------------------------------
    # NOM
    # -----------------------------------------------------

    if last_name is not None:

        last_name = str(last_name).strip()

        if not last_name:
            return jsonify({
                "error": "Le nom est obligatoire."
            }), 400

        user.last_name = last_name

    # -----------------------------------------------------
    # TELEPHONE
    # -----------------------------------------------------

    if phone is not None:

        phone = str(phone).strip()

        if not phone:
            return jsonify({
                "error": "Le téléphone est obligatoire."
            }), 400

        existing = User.query.filter(
            User.phone == phone,
            User.id != user.id
        ).first()

        if existing:
            return jsonify({
                "error": "Ce numéro de téléphone est déjà utilisé."
            }), 409

        user.phone = phone

    # -----------------------------------------------------
    # EMAIL
    # -----------------------------------------------------

    if email is not None:

        email = str(email).strip().lower()

        if not email:
            return jsonify({
                "error": "L'e-mail est obligatoire."
            }), 400

        existing = User.query.filter(
            User.email == email,
            User.id != user.id
        ).first()

        if existing:
            return jsonify({
                "error": "Cette adresse e-mail est déjà utilisée."
            }), 409

        user.email = email

    # -----------------------------------------------------
    # MOT DE PASSE
    # -----------------------------------------------------

    if password is not None:

        password = str(password).strip()

        if password:

            if len(password) < 6:
                return jsonify({
                    "error": "Le nouveau mot de passe doit contenir au moins 6 caractères."
                }), 400

            user.set_password(password)

    # -----------------------------------------------------
    # ROLES
    # -----------------------------------------------------

    if roles is not None:

        roles = str(roles).strip()

        if roles:
            user.roles = roles

    # -----------------------------------------------------
    # PHOTO DE PROFIL
    # -----------------------------------------------------

    photo = (
        request.files.get("profile_photo")
        if request.files
        else None
    )

    if (
        photo
        and photo.filename
        and allowed_file(
            photo.filename,
            current_app.config["ALLOWED_EXTENSIONS"]
        )
    ):

        extension = photo.filename.rsplit(
            ".",
            1
        )[1].lower()

        unique_name = (
            f"{uuid.uuid4().hex}.{extension}"
        )

        photo.save(
            os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                unique_name
            )
        )

        user.profile_photo = unique_name

    # -----------------------------------------------------
    # SAUVEGARDE
    # -----------------------------------------------------

    try:

        db.session.commit()

    except Exception as e:

        db.session.rollback()

        print(
            "Erreur modification profil :",
            e
        )

        return jsonify({
            "error": "Impossible de modifier le profil."
        }), 500

    return jsonify({
        "message": "Profil mis à jour avec succès.",
        "user": user.to_dict(
            include_private=True
        )
    }), 200


# =========================================================
# PROFIL PUBLIC
# =========================================================

@user_bp.route("/<int:user_id>", methods=["GET"])
def get_public_profile(user_id):

    user = User.query.get(user_id)

    if not user:

        return jsonify({
            "error": "Utilisateur introuvable."
        }), 404

    return jsonify(
        user.to_dict(
            include_private=False
        )
    ), 200
