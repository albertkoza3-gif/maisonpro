from flask import Blueprint, request, jsonify

from extensions import db
from models import User, Property, Report
from utils.security import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


def _base_url():
    return request.host_url.rstrip("/")


@admin_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([u.to_dict(include_private=True) for u in users]), 200


@admin_bp.route("/users/<int:user_id>/block", methods=["POST"])
@admin_required
def block_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable."}), 404
    user.is_blocked = True
    db.session.commit()
    return jsonify({"message": "Utilisateur bloqué."}), 200


@admin_bp.route("/users/<int:user_id>/unblock", methods=["POST"])
@admin_required
def unblock_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Utilisateur introuvable."}), 404
    user.is_blocked = False
    db.session.commit()
    return jsonify({"message": "Utilisateur débloqué."}), 200


@admin_bp.route("/properties", methods=["GET"])
@admin_required
def list_all_properties():
    props = Property.query.order_by(Property.created_at.desc()).all()
    return jsonify([p.to_dict(_base_url()) for p in props]), 200


@admin_bp.route("/properties/<int:property_id>", methods=["PUT"])
@admin_required
def admin_update_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"error": "Annonce introuvable."}), 404

    data = request.get_json(silent=True) or {}
    if "is_active" in data:
        prop.is_active = bool(data["is_active"])
    if "title" in data:
        prop.title = data["title"]
    if "price" in data:
        prop.price = float(data["price"])

    db.session.commit()
    return jsonify(prop.to_dict(_base_url())), 200


@admin_bp.route("/properties/<int:property_id>", methods=["DELETE"])
@admin_required
def admin_delete_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"error": "Annonce introuvable."}), 404
    db.session.delete(prop)
    db.session.commit()
    return jsonify({"message": "Annonce supprimée par l'administrateur."}), 200


@admin_bp.route("/reports", methods=["GET"])
@admin_required
def list_reports():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    result = []
    for r in reports:
        d = r.to_dict()
        d["property_title"] = r.property.title if r.property else None
        d["reporter_email"] = r.user.email if r.user else None
        result.append(d)
    return jsonify(result), 200