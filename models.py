from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)

    phone = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)

    password_hash = db.Column(db.String(255), nullable=False)

    roles = db.Column(db.String(200), default="acheteur")

    profile_photo = db.Column(db.String(255), nullable=True)

    # IMPORTANT :
    # Cette colonne existe déjà dans ta base de données.
    is_admin = db.Column(db.Boolean, default=False)

    is_blocked = db.Column(db.Boolean, default=False)

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relations
    properties = db.relationship(
        "Property",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    favorites = db.relationship(
        "Favorite",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    reports = db.relationship(
        "Report",
        back_populates="user",
        cascade="all, delete-orphan"
    )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(
            self.password_hash,
            password
        )

    def to_dict(self, include_private=False):
        data = {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "email": self.email,
            "roles": self.roles or "",
            "profile_photo": self.profile_photo or "",
            "is_admin": bool(self.is_admin),
            "is_blocked": bool(self.is_blocked),
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
        }

        if not include_private:
            data.pop("email", None)
            data.pop("is_admin", None)
            data.pop("is_blocked", None)

        return data


class Property(db.Model):
    __tablename__ = "properties"

    id = db.Column(db.Integer, primary_key=True)

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    property_type = db.Column(
        db.String(50),
        nullable=False
    )

    transaction_type = db.Column(
        db.String(20),
        nullable=False
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    city = db.Column(
        db.String(100),
        nullable=False
    )

    commune = db.Column(
        db.String(100),
        nullable=True
    )

    quartier = db.Column(
        db.String(100),
        nullable=True
    )

    bedrooms = db.Column(
        db.Integer,
        nullable=True
    )

    bathrooms = db.Column(
        db.Integer,
        nullable=True
    )

    area = db.Column(
        db.Float,
        nullable=True
    )

    # Conservé pour compatibilité avec ta base existante.
    # Le numéro affiché sera prioritairement celui
    # du compte du propriétaire.
    contact_phone = db.Column(
        db.String(30),
        nullable=False
    )

    is_active = db.Column(
        db.Boolean,
        default=True
    )

    views_count = db.Column(
        db.Integer,
        default=0
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Relation propriétaire
    owner = db.relationship(
        "User",
        back_populates="properties"
    )

    # Images
    images = db.relationship(
        "PropertyImage",
        back_populates="property",
        cascade="all, delete-orphan"
    )

    # Favoris
    favorites = db.relationship(
        "Favorite",
        back_populates="property",
        cascade="all, delete-orphan"
    )

    # Signalements
    reports = db.relationship(
        "Report",
        back_populates="property",
        cascade="all, delete-orphan"
    )

    def to_dict(self, base_url=""):
        """
        Convertit l'annonce en dictionnaire.

        Le numéro du propriétaire est récupéré
        automatiquement depuis son compte utilisateur.
        """

        owner_phone = ""

        # PRIORITÉ AU NUMÉRO DU COMPTE
        if self.owner:
            owner_phone = (self.owner.phone or "").strip()

        # Secours pour les anciennes annonces
        if not owner_phone:
            owner_phone = (self.contact_phone or "").strip()

        owner_name = ""

        if self.owner:
            owner_name = (
                f"{self.owner.first_name or ''} "
                f"{self.owner.last_name or ''}"
            ).strip()

        owner_profile_photo = ""

        if self.owner and self.owner.profile_photo:
            if base_url:
                owner_profile_photo = (
                    f"{base_url}/uploads/"
                    f"{self.owner.profile_photo}"
                )
            else:
                owner_profile_photo = self.owner.profile_photo

        # Préparation du numéro WhatsApp
        whatsapp_url = ""

        if owner_phone:
            whatsapp_number = (
                owner_phone
                .replace(" ", "")
                .replace("-", "")
                .replace("(", "")
                .replace(")", "")
            )

            # Côte d'Ivoire :
            # 07xxxxxxxx -> 22507xxxxxxxx
            # 05xxxxxxxx -> 22505xxxxxxxx
            # 01xxxxxxxx -> 22501xxxxxxxx
            if whatsapp_number.startswith("0"):
                whatsapp_number = "225" + whatsapp_number[1:]

            elif whatsapp_number.startswith("+"):
                whatsapp_number = whatsapp_number[1:]

            whatsapp_url = (
                f"https://wa.me/{whatsapp_number}"
                "?text=Bonjour%2C%20je%20suis%20int%C3%A9ress%C3%A9"
                "%28e%29%20par%20votre%20annonce."
            )

        return {
            "id": self.id,

            "owner_id": self.owner_id,

            "owner_name": owner_name,

            "owner_phone": owner_phone,

            "owner_profile_photo": owner_profile_photo,

            "property_type": self.property_type,

            "transaction_type": self.transaction_type,

            "title": self.title,

            "description": self.description,

            "price": self.price,

            "city": self.city,

            "commune": self.commune,

            "quartier": self.quartier,

            "bedrooms": self.bedrooms,

            "bathrooms": self.bathrooms,

            "area": self.area,

            # Pour compatibilité avec l'application mobile
            "contact_phone": owner_phone,

            "whatsapp_url": whatsapp_url,

            "is_active": bool(self.is_active),

            "views_count": self.views_count or 0,

            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),

            "images": [
                f"{base_url}/uploads/{image.filename}"
                if base_url
                else image.filename
                for image in self.images
            ],
        }


class PropertyImage(db.Model):
    __tablename__ = "property_images"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    filename = db.Column(
        db.String(255),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    property = db.relationship(
        "Property",
        back_populates="images"
    )


class Favorite(db.Model):
    __tablename__ = "favorites"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        back_populates="favorites"
    )

    property = db.relationship(
        "Property",
        back_populates="favorites"
    )

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "property_id",
            name="unique_user_property_favorite"
        ),
    )


class Report(db.Model):
    __tablename__ = "reports"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    property_id = db.Column(
        db.Integer,
        db.ForeignKey("properties.id"),
        nullable=False
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    reason = db.Column(
        db.String(500),
        nullable=False
    )

    # Cette colonne existe déjà dans ta base.
    status = db.Column(
        db.String(20),
        default="pending"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    property = db.relationship(
        "Property",
        back_populates="reports"
    )

    user = db.relationship(
        "User",
        back_populates="reports"
    )

    def to_dict(self):
        return {
            "id": self.id,
            "property_id": self.property_id,
            "user_id": self.user_id,
            "reason": self.reason,
            "status": self.status or "pending",
            "created_at": (
                self.created_at.isoformat()
                if self.created_at
                else None
            ),
        }