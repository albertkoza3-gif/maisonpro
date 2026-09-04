from flask import Blueprint, request, jsonify, g

from extensions import db
from models import Report, Property
from utils.security import token_required

report_bp = Blueprint("reports", __name__, url_prefix="/api/reports")


@report_bp.route("/<int:property_id>", methods=["POST"])
@token_required
def report_property(property_id):
    prop = Property.query.get(property_id)
    if not prop:
        return jsonify({"error": "Annonce introuvable."}), 404

    data = request.get_json(silent=True) or {}
    reason = (data.get("reason") or "").strip()
    if not reason:
        return jsonify({"error": "Veuillez préciser la raison du signalement."}), 400

    report = Report(property_id=property_id, user_id=g.current_user.id, reason=reason)
    db.session.add(report)
    db.session.commit()

    return jsonify({"message": "Signalement envoyé. Merci pour votre vigilance."}), 201