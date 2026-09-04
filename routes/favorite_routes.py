from flask import Blueprint, jsonify, g

from extensions import db
from models import Favorite, Property
from utils.security import token_required


favorite_bp = Blueprint(
    "favorites",
    __name__,
    url_prefix="/api/favorites"
)


# =========================================================
# LISTE DES FAVORIS
# =========================================================

def _get_user_favorites():

    favorites = (
        Favorite.query
        .filter_by(
            user_id=g.current_user.id
        )
        .order_by(
            Favorite.created_at.desc()
        )
        .all()
    )

    return [
        favorite.property.to_dict()
        for favorite in favorites
        if favorite.property
        and favorite.property.is_active
    ]


# =========================================================
# GET /api/favorites
# =========================================================

@favorite_bp.route("", methods=["GET"])
@token_required
def list_favorites():

    return jsonify(
        _get_user_favorites()
    ), 200


# =========================================================
# GET /api/favorites/mine
# =========================================================

@favorite_bp.route("/mine", methods=["GET"])
@token_required
def my_favorites():

    return jsonify(
        _get_user_favorites()
    ), 200


# =========================================================
# AJOUTER AUX FAVORIS
# POST /api/favorites/<property_id>
# =========================================================

@favorite_bp.route(
    "/<int:property_id>",
    methods=["POST"]
)
@token_required
def add_favorite(property_id):

    property_obj = Property.query.get(
        property_id
    )

    if not property_obj:
        return jsonify({
            "error": "Annonce introuvable."
        }), 404

    if not property_obj.is_active:
        return jsonify({
            "error": "Cette annonce n'est plus disponible."
        }), 404

    existing = Favorite.query.filter_by(
        user_id=g.current_user.id,
        property_id=property_id
    ).first()

    if existing:

        return jsonify({
            "message": "Cette annonce est déjà dans vos favoris.",
            "property_id": property_id
        }), 200

    favorite = Favorite(
        user_id=g.current_user.id,
        property_id=property_id
    )

    try:

        db.session.add(favorite)
        db.session.commit()

    except Exception as e:

        db.session.rollback()

        print(
            "Erreur ajout favori :",
            e
        )

        return jsonify({
            "error": "Impossible d'ajouter cette annonce aux favoris."
        }), 500

    return jsonify({
        "message": "Annonce ajoutée aux favoris.",
        "property_id": property_id
    }), 201


# =========================================================
# RETIRER DES FAVORIS
# DELETE /api/favorites/<property_id>
# =========================================================

@favorite_bp.route(
    "/<int:property_id>",
    methods=["DELETE"]
)
@token_required
def remove_favorite(property_id):

    favorite = Favorite.query.filter_by(
        user_id=g.current_user.id,
        property_id=property_id
    ).first()

    if not favorite:

        return jsonify({
            "error": "Cette annonce n'est pas dans vos favoris."
        }), 404

    try:

        db.session.delete(favorite)
        db.session.commit()

    except Exception as e:

        db.session.rollback()

        print(
            "Erreur suppression favori :",
            e
        )

        return jsonify({
            "error": "Impossible de retirer cette annonce des favoris."
        }), 500

    return jsonify({
        "message": "Annonce retirée des favoris.",
        "property_id": property_id
    }), 200

