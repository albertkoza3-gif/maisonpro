import os
import uuid

from flask import Blueprint, request, jsonify, g, current_app

from extensions import db
from models import Property, PropertyImage
from utils.security import token_required, allowed_file


property_bp = Blueprint(
    "properties",
    __name__,
    url_prefix="/api/properties"
)


VALID_PROPERTY_TYPES = {
    "maison",
    "appartement",
    "studio",
    "villa",
    "terrain",
    "magasin",
    "bureau",
    "chambre",
    "autre",
}

VALID_TRANSACTION_TYPES = {
    "vente",
    "location",
}


# =========================================================
# UTILITAIRES
# =========================================================

def _get_base_url():
    return request.host_url.rstrip("/")


def _get_whatsapp_url(phone):
    if not phone:
        return ""

    phone = str(phone).strip()

    phone = (
        phone
        .replace(" ", "")
        .replace("-", "")
        .replace("(", "")
        .replace(")", "")
    )

    if phone.startswith("+"):
        phone = phone[1:]
    elif phone.startswith("00"):
        phone = phone[2:]
    elif phone.startswith("0"):
        phone = "225" + phone[1:]

    return f"https://wa.me/{phone}"


def _build_image_url(filename):
    if not filename:
        return ""

    base_url = _get_base_url()

    if str(filename).startswith("http://"):
        return filename

    if str(filename).startswith("https://"):
        return filename

    return f"{base_url}/uploads/{filename}"


# =========================================================
# ENREGISTREMENT DES PHOTOS
# =========================================================

def _save_uploaded_photos(files, property_id):

    saved = []

    upload_folder = current_app.config["UPLOAD_FOLDER"]

    os.makedirs(upload_folder, exist_ok=True)

    print("")
    print("========================================")
    print("MAISONPRO - TRAITEMENT DES PHOTOS")
    print("Dossier :", upload_folder)
    print("Nombre de fichiers reçus :", len(files))
    print("========================================")

    for file in files:

        if file is None:
            print("Fichier ignoré : fichier vide")
            continue

        filename = (file.filename or "").strip()

        if not filename:
            print("Fichier ignoré : nom vide")
            continue

        print("")
        print("PHOTO REÇUE :", filename)

        # -------------------------------------------------
        # Vérifier l'extension
        # -------------------------------------------------

        if not allowed_file(
            filename,
            current_app.config["ALLOWED_EXTENSIONS"]
        ):
            print("PHOTO REFUSÉE :", filename)
            continue

        extension = (
            filename
            .rsplit(".", 1)[1]
            .lower()
        )

        # -------------------------------------------------
        # Nom unique
        # -------------------------------------------------

        unique_name = (
            f"{uuid.uuid4().hex}.{extension}"
        )

        filepath = os.path.join(
            upload_folder,
            unique_name
        )

        print("Nom final :", unique_name)
        print("Chemin :", filepath)

        # -------------------------------------------------
        # Sauvegarder physiquement le fichier
        # -------------------------------------------------

        try:

            file.save(filepath)

            # Vérifier que le fichier existe réellement
            if not os.path.isfile(filepath):

                print(
                    "ERREUR : fichier non créé :",
                    filepath
                )

                continue

            file_size = os.path.getsize(filepath)

            print(
                "PHOTO ENREGISTRÉE :",
                filepath
            )

            print(
                "Taille :",
                file_size,
                "octets"
            )

            # -------------------------------------------------
            # Créer l'entrée en base
            # -------------------------------------------------

            image = PropertyImage(
                property_id=property_id,
                filename=unique_name
            )

            db.session.add(image)

            saved.append(unique_name)

            print(
                "IMAGE AJOUTÉE À LA BASE :",
                unique_name
            )

        except Exception as e:

            print(
                "ERREUR ENREGISTREMENT PHOTO :",
                repr(e)
            )

            # Si le fichier a été créé mais que la base
            # échoue, essayer de supprimer le fichier.
            try:

                if os.path.exists(filepath):
                    os.remove(filepath)

            except Exception:
                pass

    print("")
    print("PHOTOS SAUVEGARDÉES :", saved)
    print("========================================")
    print("")

    return saved


# =========================================================
# LISTE DES ANNONCES
# =========================================================

@property_bp.route("", methods=["GET"])
def list_properties():

    query = Property.query.filter_by(
        is_active=True
    )

    city = request.args.get("city")
    commune = request.args.get("commune")
    quartier = request.args.get("quartier")

    price_min = request.args.get(
        "price_min",
        type=float
    )

    price_max = request.args.get(
        "price_max",
        type=float
    )

    transaction_type = request.args.get(
        "transaction_type"
    )

    property_type = request.args.get(
        "property_type"
    )

    bedrooms = request.args.get(
        "bedrooms",
        type=int
    )

    search = request.args.get("search")

    if city:
        query = query.filter(
            Property.city.ilike(f"%{city}%")
        )

    if commune:
        query = query.filter(
            Property.commune.ilike(f"%{commune}%")
        )

    if quartier:
        query = query.filter(
            Property.quartier.ilike(f"%{quartier}%")
        )

    if price_min is not None:
        query = query.filter(
            Property.price >= price_min
        )

    if price_max is not None:
        query = query.filter(
            Property.price <= price_max
        )

    if transaction_type:
        query = query.filter(
            Property.transaction_type == transaction_type
        )

    if property_type:
        query = query.filter(
            Property.property_type == property_type
        )

    if bedrooms is not None:
        query = query.filter(
            Property.bedrooms >= bedrooms
        )

    if search:

        like = f"%{search}%"

        query = query.filter(
            db.or_(
                Property.title.ilike(like),
                Property.description.ilike(like),
                Property.city.ilike(like),
                Property.commune.ilike(like),
                Property.quartier.ilike(like)
            )
        )

    query = query.order_by(
        Property.created_at.desc()
    )

    page = request.args.get(
        "page",
        1,
        type=int
    )

    per_page = request.args.get(
        "per_page",
        20,
        type=int
    )

    if per_page > 100:
        per_page = 100

    if per_page < 1:
        per_page = 20

    pagination = query.paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    base_url = _get_base_url()

    return jsonify({
        "properties": [
            property_obj.to_dict(base_url)
            for property_obj in pagination.items
        ],
        "total": pagination.total,
        "page": page,
        "pages": pagination.pages,
        "per_page": per_page
    }), 200


# =========================================================
# ANNONCES RÉCENTES
# =========================================================

@property_bp.route("/recent", methods=["GET"])
def recent_properties():

    limit = request.args.get(
        "limit",
        10,
        type=int
    )

    if limit > 50:
        limit = 50

    if limit < 1:
        limit = 10

    props = (
        Property.query
        .filter_by(is_active=True)
        .order_by(Property.created_at.desc())
        .limit(limit)
        .all()
    )

    base_url = _get_base_url()

    return jsonify([
        property_obj.to_dict(base_url)
        for property_obj in props
    ]), 200


# =========================================================
# ANNONCES POPULAIRES
# =========================================================

@property_bp.route("/popular", methods=["GET"])
def popular_properties():

    limit = request.args.get(
        "limit",
        10,
        type=int
    )

    if limit > 50:
        limit = 50

    if limit < 1:
        limit = 10

    props = (
        Property.query
        .filter_by(is_active=True)
        .order_by(
            Property.views_count.desc()
        )
        .limit(limit)
        .all()
    )

    base_url = _get_base_url()

    return jsonify([
        property_obj.to_dict(base_url)
        for property_obj in props
    ]), 200


# =========================================================
# MES ANNONCES
# =========================================================

@property_bp.route("/mine", methods=["GET"])
@token_required
def my_properties():

    props = (
        Property.query
        .filter_by(
            owner_id=g.current_user.id
        )
        .order_by(
            Property.created_at.desc()
        )
        .all()
    )

    base_url = _get_base_url()

    return jsonify([
        property_obj.to_dict(base_url)
        for property_obj in props
    ]), 200


# =========================================================
# VOIR UNE ANNONCE
# =========================================================

@property_bp.route(
    "/<int:property_id>",
    methods=["GET"]
)
def get_property(property_id):

    prop = Property.query.get(
        property_id
    )

    if not prop or not prop.is_active:

        return jsonify({
            "error": "Annonce introuvable."
        }), 404

    prop.views_count = (
        prop.views_count or 0
    ) + 1

    db.session.commit()

    return jsonify(
        prop.to_dict(
            _get_base_url()
        )
    ), 200


# =========================================================
# CRÉER UNE ANNONCE
# =========================================================

@property_bp.route("", methods=["POST"])
@token_required
def create_property():

    # IMPORTANT :
    # Avec multipart/form-data, les champs sont dans request.form
    # et les photos sont dans request.files.

    form = request.form

    property_type = (
        form.get("property_type") or ""
    ).strip().lower()

    transaction_type = (
        form.get("transaction_type") or ""
    ).strip().lower()

    title = (
        form.get("title") or ""
    ).strip()

    description = (
        form.get("description") or ""
    ).strip()

    price = form.get(
        "price",
        type=float
    )

    city = (
        form.get("city") or ""
    ).strip()

    commune = (
        form.get("commune") or ""
    ).strip()

    quartier = (
        form.get("quartier") or ""
    ).strip()

    bedrooms = form.get(
        "bedrooms",
        type=int
    )

    bathrooms = form.get(
        "bathrooms",
        type=int
    )

    area = form.get(
        "area",
        type=float
    )

    # -----------------------------------------------------
    # TÉLÉPHONE DU COMPTE
    # -----------------------------------------------------

    owner_phone = (
        g.current_user.phone or ""
    ).strip()

    # -----------------------------------------------------
    # VALIDATION
    # -----------------------------------------------------

    if property_type not in VALID_PROPERTY_TYPES:

        return jsonify({
            "error": "Type de bien invalide."
        }), 400

    if transaction_type not in VALID_TRANSACTION_TYPES:

        return jsonify({
            "error": (
                "Le bien doit être 'vente' "
                "ou 'location'."
            )
        }), 400

    if not title:

        return jsonify({
            "error": "Le titre est obligatoire."
        }), 400

    if not description:

        return jsonify({
            "error": "La description est obligatoire."
        }), 400

    if not city:

        return jsonify({
            "error": "La ville est obligatoire."
        }), 400

    if not owner_phone:

        return jsonify({
            "error": (
                "Votre compte ne possède pas "
                "de numéro de téléphone."
            )
        }), 400

    if price is None or price <= 0:

        return jsonify({
            "error": (
                "Le prix doit être "
                "un nombre positif."
            )
        }), 400

    # =====================================================
    # PHOTOS REÇUES
    # =====================================================

    photos = request.files.getlist("images")

    print("")
    print("========================================")
    print("MAISONPRO - NOUVELLE ANNONCE")
    print("Propriétaire :", g.current_user.first_name)
    print("Téléphone :", owner_phone)
    print("NOMBRE DE PHOTOS REÇUES :", len(photos))
    print("========================================")

    for photo in photos:

        if photo and photo.filename:

            print(
                "FICHIER REÇU :",
                photo.filename
            )

    # -----------------------------------------------------
    # Création de l'annonce
    # -----------------------------------------------------

    prop = Property(
        owner_id=g.current_user.id,
        property_type=property_type,
        transaction_type=transaction_type,
        title=title,
        description=description,
        price=price,
        city=city,
        commune=commune or None,
        quartier=quartier or None,
        bedrooms=bedrooms,
        bathrooms=bathrooms,
        area=area,
        contact_phone=owner_phone,
        is_active=True,
        views_count=0
    )

    db.session.add(prop)

    try:

        # Obtenir l'ID de l'annonce avant
        # d'enregistrer les photos.

        db.session.flush()

        print(
            "ANNONCE CRÉÉE AVEC ID :",
            prop.id
        )

        # -------------------------------------------------
        # Enregistrer les photos
        # -------------------------------------------------

        saved_photos = _save_uploaded_photos(
            photos,
            prop.id
        )

        print(
            "TOTAL PHOTOS SAUVEGARDÉES :",
            len(saved_photos)
        )

        # -------------------------------------------------
        # Validation finale
        # -------------------------------------------------

        db.session.commit()

        print("")
        print("========================================")
        print("PUBLICATION TERMINÉE")
        print("Annonce ID :", prop.id)
        print("Photos :", saved_photos)
        print("========================================")
        print("")

    except Exception as e:

        db.session.rollback()

        print("")
        print(
            "ERREUR CRÉATION ANNONCE :",
            repr(e)
        )
        print("")

        return jsonify({
            "error": (
                "Impossible de créer "
                "l'annonce."
            )
        }), 500

    return jsonify(
        prop.to_dict(
            _get_base_url()
        )
    ), 201


# =========================================================
# MODIFIER UNE ANNONCE
# =========================================================

@property_bp.route(
    "/<int:property_id>",
    methods=["PUT"]
)
@token_required
def update_property(property_id):

    prop = Property.query.get(
        property_id
    )

    if not prop:

        return jsonify({
            "error": "Annonce introuvable."
        }), 404

    if (
        prop.owner_id != g.current_user.id
        and not g.current_user.is_admin
    ):

        return jsonify({
            "error": (
                "Vous n'êtes pas autorisé "
                "à modifier cette annonce."
            )
        }), 403

    form = request.form

    # -----------------------------------------------------
    # CHAMPS TEXTE
    # -----------------------------------------------------

    text_fields = [
        "title",
        "description",
        "city",
        "commune",
        "quartier"
    ]

    for field in text_fields:

        value = form.get(field)

        if value is not None:

            value = str(value).strip()

            if field in [
                "title",
                "description",
                "city"
            ] and not value:

                continue

            setattr(
                prop,
                field,
                value or None
            )

    # -----------------------------------------------------
    # PRIX
    # -----------------------------------------------------

    price = form.get(
        "price",
        type=float
    )

    if price is not None:

        if price <= 0:

            return jsonify({
                "error": (
                    "Le prix doit être "
                    "un nombre positif."
                )
            }), 400

        prop.price = price

    # -----------------------------------------------------
    # SURFACE
    # -----------------------------------------------------

    area = form.get(
        "area",
        type=float
    )

    if area is not None:
        prop.area = area

    # -----------------------------------------------------
    # CHAMBRES
    # -----------------------------------------------------

    bedrooms = form.get(
        "bedrooms",
        type=int
    )

    if bedrooms is not None:
        prop.bedrooms = bedrooms

    # -----------------------------------------------------
    # SALLES DE BAIN
    # -----------------------------------------------------

    bathrooms = form.get(
        "bathrooms",
        type=int
    )

    if bathrooms is not None:
        prop.bathrooms = bathrooms

    # -----------------------------------------------------
    # TYPE DE BIEN
    # -----------------------------------------------------

    new_property_type = form.get(
        "property_type"
    )

    if new_property_type:

        new_property_type = (
            new_property_type
            .strip()
            .lower()
        )

        if new_property_type in VALID_PROPERTY_TYPES:

            prop.property_type = (
                new_property_type
            )

    # -----------------------------------------------------
    # TYPE DE TRANSACTION
    # -----------------------------------------------------

    new_transaction_type = form.get(
        "transaction_type"
    )

    if new_transaction_type:

        new_transaction_type = (
            new_transaction_type
            .strip()
            .lower()
        )

        if new_transaction_type in VALID_TRANSACTION_TYPES:

            prop.transaction_type = (
                new_transaction_type
            )

    # -----------------------------------------------------
    # TÉLÉPHONE AUTOMATIQUE
    # -----------------------------------------------------

    if g.current_user.phone:

        prop.contact_phone = (
            g.current_user.phone
        )

    # =====================================================
    # NOUVELLES PHOTOS
    # =====================================================

    photos = request.files.getlist(
        "images"
    )

    print("")
    print("========================================")
    print("MODIFICATION ANNONCE :", prop.id)
    print("NOMBRE DE NOUVELLES PHOTOS :",
          len(photos))
    print("========================================")

    if photos:

        saved_photos = _save_uploaded_photos(
            photos,
            prop.id
        )

        print(
            "NOUVELLES PHOTOS SAUVEGARDÉES :",
            saved_photos
        )

    # -----------------------------------------------------
    # SAUVEGARDE
    # -----------------------------------------------------

    try:

        db.session.commit()

    except Exception as e:

        db.session.rollback()

        print(
            "ERREUR MODIFICATION ANNONCE :",
            repr(e)
        )

        return jsonify({
            "error": (
                "Impossible de modifier "
                "l'annonce."
            )
        }), 500

    return jsonify(
        prop.to_dict(
            _get_base_url()
        )
    ), 200


# =========================================================
# SUPPRIMER UNE ANNONCE
# =========================================================

@property_bp.route(
    "/<int:property_id>",
    methods=["DELETE"]
)
@token_required
def delete_property(property_id):

    prop = Property.query.get(
        property_id
    )

    if not prop:

        return jsonify({
            "error": "Annonce introuvable."
        }), 404

    if (
        prop.owner_id != g.current_user.id
        and not g.current_user.is_admin
    ):

        return jsonify({
            "error": (
                "Vous n'êtes pas autorisé "
                "à supprimer cette annonce."
            )
        }), 403

    # -----------------------------------------------------
    # SUPPRIMER LES FICHIERS PHOTOS
    # -----------------------------------------------------

    for image in prop.images:

        filepath = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            image.filename
        )

        if os.path.exists(filepath):

            try:

                os.remove(filepath)

            except Exception as e:

                print(
                    "Impossible de supprimer "
                    "l'image :",
                    repr(e)
                )

    # -----------------------------------------------------
    # SUPPRIMER L'ANNONCE
    # -----------------------------------------------------

    try:

        db.session.delete(prop)

        db.session.commit()

    except Exception as e:

        db.session.rollback()

        print(
            "ERREUR SUPPRESSION ANNONCE :",
            repr(e)
        )

        return jsonify({
            "error": (
                "Impossible de supprimer "
                "l'annonce."
            )
        }), 500

    return jsonify({
        "message": "Annonce supprimée.",
        "property_id": property_id
    }), 200
