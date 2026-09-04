from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp


Builder.load_string("""
<PropertyCard>:

    orientation: "vertical"
    size_hint_y: None
    height: dp(285)
    padding: dp(8)
    spacing: dp(6)

    canvas.before:
        Color:
            rgba: 0.96, 0.97, 0.99, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10), dp(10), dp(10), dp(10)]

    BoxLayout:
        size_hint_y: None
        height: dp(145)

        AsyncImage:
            id: property_image
            source: ""
            allow_stretch: True
            keep_ratio: True

    Label:
        id: title_label
        text: "Annonce"
        font_size: "18sp"
        bold: True
        color: 0.08, 0.08, 0.08, 1
        size_hint_y: None
        height: dp(28)
        text_size: self.width, None
        halign: "left"
        shorten: True

    Label:
        id: price_label
        text: "0 FCFA"
        font_size: "17sp"
        bold: True
        color: 0.10, 0.35, 0.75, 1
        size_hint_y: None
        height: dp(27)
        text_size: self.width, None
        halign: "left"

    Label:
        id: location_label
        text: "📍 Côte d'Ivoire"
        font_size: "13sp"
        color: 0.25, 0.25, 0.25, 1
        size_hint_y: None
        height: dp(25)
        text_size: self.width, None
        halign: "left"
        shorten: True

    Label:
        id: details_label
        text: "Maison • 0 chambre(s) • 0 SDB • 0 m²"
        font_size: "13sp"
        color: 0.35, 0.35, 0.35, 1
        size_hint_y: None
        height: dp(25)
        text_size: self.width, None
        halign: "left"
        shorten: True

    Button:
        text: "Voir l'annonce"
        size_hint_y: None
        height: dp(38)
        background_color: 0.10, 0.35, 0.75, 1
        color: 1, 1, 1, 1
        on_release: root.select_property()
""")


class PropertyCard(BoxLayout):

    property_data = None
    on_select = None

    # ========================================================
    # CONFIGURATION SERVEUR
    # ========================================================

    SERVER_URL = "https://maisonpro.onrender.com"

    # ========================================================
    # CHARGER LES DONNÉES
    # ========================================================

    def set_data(self, prop):

        self.property_data = prop or {}

        # ----------------------------------------------------
        # TITRE
        # ----------------------------------------------------

        title = self.property_data.get(
            "title",
            "Annonce immobilière"
        )

        self.ids.title_label.text = str(title)

        # ----------------------------------------------------
        # PRIX
        # ----------------------------------------------------

        price = self.property_data.get(
            "price",
            0
        )

        try:

            price_number = float(price)

            price_text = (
                f"{price_number:,.0f}"
                .replace(",", " ")
            )

            price_text = f"{price_text} FCFA"

        except (ValueError, TypeError):

            price_text = f"{price} FCFA"

        transaction_type = str(
            self.property_data.get(
                "transaction_type",
                ""
            )
        ).strip().lower()

        if transaction_type:

            price_text += (
                f" • {transaction_type.capitalize()}"
            )

        self.ids.price_label.text = price_text

        # ----------------------------------------------------
        # LOCALISATION
        # ----------------------------------------------------

        city = str(
            self.property_data.get(
                "city",
                ""
            )
        ).strip()

        commune = str(
            self.property_data.get(
                "commune",
                ""
            )
        ).strip()

        quartier = str(
            self.property_data.get(
                "quartier",
                ""
            )
        ).strip()

        location_parts = []

        if city:
            location_parts.append(city)

        if commune:
            location_parts.append(commune)

        if quartier:
            location_parts.append(quartier)

        if location_parts:

            location = " • ".join(
                location_parts
            )

            self.ids.location_label.text = (
                f"📍 {location}"
            )

        else:

            self.ids.location_label.text = (
                "📍 Localisation non précisée"
            )

        # ----------------------------------------------------
        # TYPE DE BIEN
        # ----------------------------------------------------

        property_type = str(
            self.property_data.get(
                "property_type",
                "Bien"
            )
        ).strip()

        if property_type:

            property_type = (
                property_type.capitalize()
            )

        else:

            property_type = "Bien"

        # ----------------------------------------------------
        # CHAMBRES
        # ----------------------------------------------------

        bedrooms = self.property_data.get(
            "bedrooms"
        )

        if bedrooms is None or bedrooms == "":

            bedrooms_text = "Chambres : -"

        else:

            bedrooms_text = (
                f"{bedrooms} chambre(s)"
            )

        # ----------------------------------------------------
        # SALLES DE BAIN
        # ----------------------------------------------------

        bathrooms = self.property_data.get(
            "bathrooms"
        )

        if bathrooms is None or bathrooms == "":

            bathrooms_text = "SDB : -"

        else:

            bathrooms_text = (
                f"{bathrooms} SDB"
            )

        # ----------------------------------------------------
        # SUPERFICIE
        # ----------------------------------------------------

        area = self.property_data.get(
            "area"
        )

        if area is None or area == "":

            area_text = "Surface : -"

        else:

            try:

                area_text = (
                    f"{float(area):,.0f}"
                    .replace(",", " ")
                )

                area_text = (
                    f"{area_text} m²"
                )

            except (ValueError, TypeError):

                area_text = f"{area} m²"

        self.ids.details_label.text = (
            f"{property_type} • "
            f"{bedrooms_text} • "
            f"{bathrooms_text} • "
            f"{area_text}"
        )

        # ----------------------------------------------------
        # PHOTO
        # ----------------------------------------------------

        self.load_property_image(
            self.property_data
        )

    # ========================================================
    # CHARGER LA PHOTO
    # ========================================================

    def load_property_image(self, prop):

        images = prop.get(
            "images",
            []
        )

        # ----------------------------------------------------
        # Aucune image
        # ----------------------------------------------------

        if not images:

            self.ids.property_image.source = ""

            return

        # ----------------------------------------------------
        # Vérifier le format
        # ----------------------------------------------------

        if not isinstance(images, list):

            images = [images]

        if len(images) == 0:

            self.ids.property_image.source = ""

            return

        image_url = images[0]

        if not image_url:

            self.ids.property_image.source = ""

            return

        image_url = str(
            image_url
        ).strip()

        # ----------------------------------------------------
        # URL complète
        # ----------------------------------------------------

        if image_url.startswith(
            "http://"
        ) or image_url.startswith(
            "https://"
        ):

            final_url = image_url

        # ----------------------------------------------------
        # Chemin /uploads/...
        # ----------------------------------------------------

        elif image_url.startswith(
            "/uploads/"
        ):

            final_url = (
                self.SERVER_URL
                + image_url
            )

        # ----------------------------------------------------
        # Chemin uploads/...
        # ----------------------------------------------------

        elif image_url.startswith(
            "uploads/"
        ):

            final_url = (
                self.SERVER_URL
                + "/"
                + image_url
            )

        # ----------------------------------------------------
        # Nom de fichier uniquement
        # ----------------------------------------------------

        else:

            final_url = (
                self.SERVER_URL
                + "/uploads/"
                + image_url.lstrip("/")
            )

        # ----------------------------------------------------
        # Afficher l'image
        # ----------------------------------------------------

        print(
            "PHOTO MAISONPRO :",
            final_url
        )

        self.ids.property_image.source = final_url

        self.ids.property_image.reload()

    # ========================================================
    # OUVRIR L'ANNONCE
    # ========================================================

    def select_property(self):

        if not self.property_data:

            return

        property_id = self.property_data.get(
            "id"
        )

        if property_id is None:

            return

        if self.on_select:

            self.on_select(
                property_id
            )