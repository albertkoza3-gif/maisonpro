from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.utils import platform

import webbrowser
import re
from urllib.parse import quote


Builder.load_string("""
<PropertyDetailScreen>:

    BoxLayout:
        orientation: "vertical"

        # =====================================================
        # EN-TÊTE
        # =====================================================

        BoxLayout:
            size_hint_y: None
            height: dp(65)
            padding: dp(12)
            spacing: dp(8)

            canvas.before:
                Color:
                    rgba: 0.10, 0.35, 0.75, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Button:
                text: "< Retour"
                size_hint_x: None
                width: dp(85)
                background_color: 0, 0, 0, 0
                color: 1, 1, 1, 1
                on_release: root.go_back()

            Label:
                text: "DÉTAIL DE L'ANNONCE"
                font_size: "19sp"
                bold: True
                color: 1, 1, 1, 1


        # =====================================================
        # CONTENU
        # =====================================================

        ScrollView:

            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(12)
                spacing: dp(10)


                # =================================================
                # PHOTO
                # =================================================

                AsyncImage:
                    id: property_image
                    source: ""
                    size_hint_y: None
                    height: dp(220)
                    allow_stretch: True
                    keep_ratio: True


                # =================================================
                # TITRE
                # =================================================

                Label:
                    id: title_label
                    text: "Annonce"
                    font_size: "22sp"
                    bold: True
                    color: 0.08, 0.08, 0.08, 1
                    size_hint_y: None
                    height: dp(45)
                    text_size: self.width, None
                    halign: "left"
                    valign: "middle"


                # =================================================
                # PRIX
                # =================================================

                Label:
                    id: price_label
                    text: "0 FCFA"
                    font_size: "21sp"
                    bold: True
                    color: 0.10, 0.35, 0.75, 1
                    size_hint_y: None
                    height: dp(35)
                    text_size: self.width, None
                    halign: "left"


                # =================================================
                # LOCALISATION
                # =================================================

                Label:
                    id: location_label
                    text: "📍 Localisation"
                    font_size: "15sp"
                    color: 0.25, 0.25, 0.25, 1
                    size_hint_y: None
                    height: dp(30)
                    text_size: self.width, None
                    halign: "left"


                # =================================================
                # DETAILS
                # =================================================

                Label:
                    id: details_label
                    text: "Maison • Chambres • SDB • Surface"
                    font_size: "14sp"
                    color: 0.30, 0.30, 0.30, 1
                    size_hint_y: None
                    height: dp(35)
                    text_size: self.width, None
                    halign: "left"


                # =================================================
                # PROPRIETAIRE
                # =================================================

                Label:
                    text: "PROPRIÉTAIRE"
                    font_size: "17sp"
                    bold: True
                    color: 0.08, 0.08, 0.08, 1
                    size_hint_y: None
                    height: dp(30)
                    text_size: self.width, None
                    halign: "left"


                Label:
                    id: owner_name_label
                    text: "Propriétaire : Non disponible"
                    font_size: "15sp"
                    color: 0.25, 0.25, 0.25, 1
                    size_hint_y: None
                    height: dp(30)
                    text_size: self.width, None
                    halign: "left"


                # =================================================
                # CONTACT
                # =================================================

                Label:
                    text: "CONTACT DU PROPRIÉTAIRE"
                    font_size: "17sp"
                    bold: True
                    color: 0.08, 0.08, 0.08, 1
                    size_hint_y: None
                    height: dp(30)
                    text_size: self.width, None
                    halign: "left"


                Label:
                    id: phone_label
                    text: "Téléphone : Non disponible"
                    font_size: "15sp"
                    color: 0.25, 0.25, 0.25, 1
                    size_hint_y: None
                    height: dp(30)
                    text_size: self.width, None
                    halign: "left"


                # =================================================
                # BOUTONS CONTACT
                # =================================================

                BoxLayout:
                    size_hint_y: None
                    height: dp(52)
                    spacing: dp(8)

                    Button:
                        text: "📞 Appeler"
                        background_color: 0.10, 0.60, 0.30, 1
                        color: 1, 1, 1, 1
                        bold: True
                        on_release: root.call_owner()

                    Button:
                        text: "💬 WhatsApp"
                        background_color: 0.05, 0.65, 0.35, 1
                        color: 1, 1, 1, 1
                        bold: True
                        on_release: root.whatsapp_owner()


                # =================================================
                # DESCRIPTION
                # =================================================

                Label:
                    text: "DESCRIPTION"
                    font_size: "17sp"
                    bold: True
                    color: 0.08, 0.08, 0.08, 1
                    size_hint_y: None
                    height: dp(30)
                    text_size: self.width, None
                    halign: "left"


                Label:
                    id: description_label
                    text: ""
                    font_size: "14sp"
                    color: 0.20, 0.20, 0.20, 1
                    size_hint_y: None
                    text_size: self.width, None
                    halign: "left"
                    valign: "top"
                    padding: dp(5), dp(5)


                # =================================================
                # VUES
                # =================================================

                Label:
                    id: views_label
                    text: "👁 0 vue"
                    font_size: "13sp"
                    color: 0.45, 0.45, 0.45, 1
                    size_hint_y: None
                    height: dp(25)
                    text_size: self.width, None
                    halign: "left"


                Widget:
                    size_hint_y: None
                    height: dp(20)
""")


class PropertyDetailScreen(Screen):

    property_id = None
    property_data = None

    # =========================================================
    # ENTREE SUR LA PAGE
    # =========================================================

    def on_pre_enter(self, *args):
        self.load_property()

    # =========================================================
    # CHARGER L'ANNONCE
    # =========================================================

    def load_property(self):

        if not self.property_id:
            self.show_message(
                "Erreur",
                "Annonce introuvable."
            )
            return

        app = App.get_running_app()

        try:

            success, result = app.api_client.get_property(
                self.property_id
            )

        except Exception as e:

            print("Erreur chargement annonce :", e)

            self.show_message(
                "Erreur",
                "Impossible de contacter le serveur."
            )

            return

        if not success:

            error = "Impossible de charger l'annonce."

            if isinstance(result, dict):

                error = result.get(
                    "error",
                    result.get(
                        "message",
                        error
                    )
                )

            self.show_message(
                "Erreur",
                error
            )

            return

        self.property_data = result

        self.display_property(result)

    # =========================================================
    # AFFICHER L'ANNONCE
    # =========================================================

    def display_property(self, prop):

        if not isinstance(prop, dict):
            self.show_message(
                "Erreur",
                "Les données de l'annonce sont invalides."
            )
            return

        # =====================================================
        # TITRE
        # =====================================================

        self.ids.title_label.text = str(
            prop.get(
                "title",
                "Annonce immobilière"
            )
        )

        # =====================================================
        # PRIX
        # =====================================================

        price = prop.get(
            "price",
            0
        )

        try:

            price_text = f"{float(price):,.0f}".replace(
                ",",
                " "
            )

            price_text += " FCFA"

        except (ValueError, TypeError):

            price_text = f"{price} FCFA"

        transaction_type = str(
            prop.get(
                "transaction_type",
                ""
            )
        ).strip()

        if transaction_type:

            price_text += (
                " • "
                + transaction_type.capitalize()
            )

        self.ids.price_label.text = price_text

        # =====================================================
        # LOCALISATION
        # =====================================================

        city = str(
            prop.get(
                "city",
                ""
            )
        ).strip()

        commune = str(
            prop.get(
                "commune",
                ""
            )
        ).strip()

        quartier = str(
            prop.get(
                "quartier",
                ""
            )
        ).strip()

        location = []

        if city:
            location.append(city)

        if commune:
            location.append(commune)

        if quartier:
            location.append(quartier)

        if location:

            self.ids.location_label.text = (
                "📍 "
                + " • ".join(location)
            )

        else:

            self.ids.location_label.text = (
                "📍 Localisation non précisée"
            )

        # =====================================================
        # TYPE
        # =====================================================

        property_type = str(
            prop.get(
                "property_type",
                "Bien"
            )
        ).capitalize()

        # =====================================================
        # CHAMBRES
        # =====================================================

        bedrooms = prop.get(
            "bedrooms"
        )

        if bedrooms is None or bedrooms == "":

            bedrooms_text = "Chambres : -"

        else:

            bedrooms_text = (
                f"{bedrooms} chambre(s)"
            )

        # =====================================================
        # SALLES DE BAIN
        # =====================================================

        bathrooms = prop.get(
            "bathrooms"
        )

        if bathrooms is None or bathrooms == "":

            bathrooms_text = "SDB : -"

        else:

            bathrooms_text = (
                f"{bathrooms} SDB"
            )

        # =====================================================
        # SURFACE
        # =====================================================

        area = prop.get(
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

                area_text += " m²"

            except (ValueError, TypeError):

                area_text = f"{area} m²"

        self.ids.details_label.text = (
            f"{property_type} • "
            f"{bedrooms_text} • "
            f"{bathrooms_text} • "
            f"{area_text}"
        )

        # =====================================================
        # PROPRIETAIRE
        # =====================================================

        owner_name = str(
            prop.get(
                "owner_name",
                ""
            )
        ).strip()

        if owner_name:

            self.ids.owner_name_label.text = (
                "Propriétaire : "
                + owner_name
            )

        else:

            self.ids.owner_name_label.text = (
                "Propriétaire : Non disponible"
            )

        # =====================================================
        # DESCRIPTION
        # =====================================================

        description = prop.get(
            "description",
            ""
        )

        if not description:

            description = (
                "Aucune description disponible."
            )

        self.ids.description_label.text = str(
            description
        )

        # =====================================================
        # TELEPHONE DU PROPRIETAIRE
        # =====================================================

        phone = self.get_owner_phone()

        if phone:

            self.ids.phone_label.text = (
                "Téléphone : "
                + phone
            )

        else:

            self.ids.phone_label.text = (
                "Téléphone : Non disponible"
            )

        # =====================================================
        # VUES
        # =====================================================

        views = prop.get(
            "views_count",
            0
        )

        self.ids.views_label.text = (
            f"👁 {views} vue(s)"
        )

        # =====================================================
        # PHOTO
        # =====================================================

        images = prop.get(
            "images",
            []
        )

        self.ids.property_image.source = ""

        if images and isinstance(
            images,
            list
        ):

            image_url = images[0]

            if image_url:

                image_url = str(
                    image_url
                ).strip()

                if image_url.startswith(
                    "http://"
                ) or image_url.startswith(
                    "https://"
                ):

                    self.ids.property_image.source = (
                        image_url
                    )

                else:

                    self.ids.property_image.source = (
                        "http://127.0.0.1:5000/"
                        + image_url.lstrip("/")
                    )

                self.ids.property_image.reload()

    # =========================================================
    # RECUPERER LE TELEPHONE DU PROPRIETAIRE
    # =========================================================

    def get_owner_phone(self):

        if not self.property_data:
            return None

        # =====================================================
        # PRIORITE 1 : owner_phone
        # =====================================================

        phone = self.property_data.get(
            "owner_phone",
            ""
        )

        # =====================================================
        # PRIORITE 2 : contact_phone
        # =====================================================

        if not phone:

            phone = self.property_data.get(
                "contact_phone",
                ""
            )

        if not phone:
            return None

        phone = str(phone).strip()

        if not phone:
            return None

        return phone

    # =========================================================
    # NETTOYER UN NUMERO
    # =========================================================

    def clean_phone(self, phone):

        if not phone:
            return ""

        return re.sub(
            r"[^0-9+]",
            "",
            str(phone)
        ).strip()

    # =========================================================
    # CONVERTIR NUMERO POUR WHATSAPP
    # =========================================================

    def get_whatsapp_phone(self, phone):

        clean_phone = re.sub(
            r"[^0-9]",
            "",
            str(phone)
        )

        if not clean_phone:
            return ""

        # =====================================================
        # Numéro déjà au format international
        # =====================================================

        if clean_phone.startswith("225"):

            return clean_phone

        # =====================================================
        # Numéro ivoirien local
        #
        # 0714333357
        # devient
        # 225714333357
        # =====================================================

        if clean_phone.startswith("0"):

            return (
                "225"
                + clean_phone[1:]
            )

        # =====================================================
        # Autre numéro
        # =====================================================

        return (
            "225"
            + clean_phone
        )

    # =========================================================
    # APPELER LE PROPRIETAIRE
    # =========================================================

    def call_owner(self):

        phone = self.get_owner_phone()

        if not phone:

            self.show_message(
                "Téléphone indisponible",
                "Le propriétaire n'a pas renseigné de numéro."
            )

            return

        clean_phone = self.clean_phone(
            phone
        )

        if not clean_phone:

            self.show_message(
                "Numéro invalide",
                "Le numéro du propriétaire est invalide."
            )

            return

        # =====================================================
        # ANDROID
        # =====================================================

        if platform == "android":

            try:

                from jnius import autoclass

                Intent = autoclass(
                    "android.content.Intent"
                )

                Uri = autoclass(
                    "android.net.Uri"
                )

                PythonActivity = autoclass(
                    "org.kivy.android.PythonActivity"
                )

                intent = Intent(
                    Intent.ACTION_DIAL
                )

                intent.setData(
                    Uri.parse(
                        "tel:" + clean_phone
                    )
                )

                PythonActivity.mActivity.startActivity(
                    intent
                )

                return

            except Exception as e:

                print(
                    "Erreur appel Android :",
                    e
                )

        # =====================================================
        # WINDOWS / PC
        # =====================================================

        try:

            webbrowser.open(
                "tel:" + clean_phone
            )

            return

        except Exception as e:

            print(
                "Erreur ouverture téléphone :",
                e
            )

        self.show_message(
            "Appeler",
            f"Numéro du propriétaire : {phone}"
        )

    # =========================================================
    # WHATSAPP
    # =========================================================

    def whatsapp_owner(self):

        phone = self.get_owner_phone()

        if not phone:

            self.show_message(
                "WhatsApp indisponible",
                "Le propriétaire n'a pas renseigné de numéro."
            )

            return

        # =====================================================
        # PRIORITE :
        # Utiliser directement l'URL créée par le backend
        # =====================================================

        backend_whatsapp_url = self.property_data.get(
            "whatsapp_url",
            ""
        )

        if backend_whatsapp_url:

            try:

                webbrowser.open(
                    str(backend_whatsapp_url)
                )

                return

            except Exception as e:

                print(
                    "Erreur ouverture WhatsApp backend :",
                    e
                )

        # =====================================================
        # Sinon, créer nous-mêmes l'URL
        # =====================================================

        whatsapp_phone = self.get_whatsapp_phone(
            phone
        )

        if not whatsapp_phone:

            self.show_message(
                "Numéro invalide",
                "Le numéro WhatsApp du propriétaire est invalide."
            )

            return

        # =====================================================
        # TITRE DE L'ANNONCE
        # =====================================================

        title = self.property_data.get(
            "title",
            "cette annonce"
        )

        # =====================================================
        # MESSAGE AUTOMATIQUE
        # =====================================================

        message = (
            "Bonjour, je suis intéressé(e) "
            "par votre annonce sur MaisonPro : "
            + str(title)
        )

        whatsapp_url = (
            "https://wa.me/"
            + whatsapp_phone
            + "?text="
            + quote(message)
        )

        try:

            webbrowser.open(
                whatsapp_url
            )

        except Exception as e:

            print(
                "Erreur WhatsApp :",
                e
            )

            self.show_message(
                "WhatsApp",
                f"Numéro : {phone}"
            )

    # =========================================================
    # RETOUR
    # =========================================================

    def go_back(self):

        app = App.get_running_app()

        if "home" in app.sm.screen_names:

            app.sm.current = "home"

        elif "search" in app.sm.screen_names:

            app.sm.current = "search"

        else:

            app.sm.current = app.sm.previous()

    # =========================================================
    # MESSAGE
    # =========================================================

    def show_message(
        self,
        title,
        message
    ):

        Popup(
            title=str(title),
            content=Label(
                text=str(message),
                halign="center",
                valign="middle",
                text_size=(
                    dp(280),
                    None
                )
            ),
            size_hint=(
                0.85,
                0.40
            )
        ).open()