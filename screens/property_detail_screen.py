from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from urllib.parse import quote


SERVER_URL = "https://maisonpro.onrender.com"


Builder.load_string("""
<PropertyDetailScreen>:

    BoxLayout:
        orientation: "vertical"

        BoxLayout:
            size_hint_y: None
            height: dp(55)
            padding: dp(8)
            spacing: dp(8)

            Button:
                text: "← Retour"
                size_hint_x: None
                width: dp(90)
                on_release: root.go_back()

            Label:
                id: title_top
                text: "Détail de l'annonce"
                bold: True
                font_size: "18sp"
                color: 0.1, 0.1, 0.1, 1

        ScrollView:

            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(12)
                spacing: dp(12)

                Image:
                    id: property_image
                    source: ""
                    size_hint_y: None
                    height: dp(230)
                    allow_stretch: True
                    keep_ratio: True

                Label:
                    id: property_title
                    text: ""
                    font_size: "22sp"
                    bold: True
                    color: 0.05, 0.05, 0.05, 1
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None

                Label:
                    id: property_price
                    text: ""
                    font_size: "20sp"
                    bold: True
                    color: 0.1, 0.55, 0.2, 1
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None

                Label:
                    id: property_location
                    text: ""
                    font_size: "16sp"
                    color: 0.3, 0.3, 0.3, 1
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None

                Label:
                    id: property_description
                    text: ""
                    font_size: "16sp"
                    color: 0.15, 0.15, 0.15, 1
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None

                Label:
                    id: property_info
                    text: ""
                    font_size: "15sp"
                    color: 0.25, 0.25, 0.25, 1
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None

                Label:
                    id: owner_name
                    text: ""
                    font_size: "17sp"
                    bold: True
                    color: 0.1, 0.1, 0.1, 1
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None

                Label:
                    id: owner_phone
                    text: ""
                    font_size: "16sp"
                    color: 0.2, 0.2, 0.2, 1
                    size_hint_y: None
                    height: self.texture_size[1]
                    text_size: self.width, None

                BoxLayout:
                    size_hint_y: None
                    height: dp(50)
                    spacing: dp(8)

                    Button:
                        text: "📞 Appeler"
                        background_color: 0.1, 0.6, 0.25, 1
                        on_release: root.call_owner()

                    Button:
                        text: "WhatsApp"
                        background_color: 0.1, 0.7, 0.3, 1
                        on_release: root.open_whatsapp()

                BoxLayout:
                    size_hint_y: None
                    height: dp(50)
                    spacing: dp(8)

                    Button:
                        text: "❤️ Favoris"
                        background_color: 0.9, 0.2, 0.25, 1
                        on_release: root.add_to_favorites()

                    Button:
                        text: "⚠ Signaler"
                        background_color: 0.8, 0.5, 0.1, 1
                        on_release: root.report_property()
""")


class PropertyDetailScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.property_id = None
        self.property_data = None

    def on_pre_enter(self, *args):
        if self.property_id:
            self.load_property()

    def build_image_url(self, image_url):
        if not image_url:
            return ""

        image_url = str(image_url).strip()

        if image_url.startswith("http://") or image_url.startswith("https://"):
            return image_url

        if image_url.startswith("/"):
            return SERVER_URL + image_url

        if image_url.startswith("uploads/"):
            return SERVER_URL + "/" + image_url

        return SERVER_URL + "/uploads/" + image_url

    def load_property(self):
        app = App.get_running_app()

        success, data = app.api_client.get_property(self.property_id)

        if not success or not data:
            self.show_message("Erreur", "Impossible de charger l'annonce.")
            return

        self.property_data = data

        self.ids.property_title.text = data.get(
            "title",
            "Annonce"
        )

        price = data.get("price", 0)

        try:
            price_text = f"{float(price):,.0f}".replace(",", " ")
        except Exception:
            price_text = str(price)

        self.ids.property_price.text = price_text + " FCFA"

        city = data.get("city", "")
        commune = data.get("commune", "")
        quartier = data.get("quartier", "")

        location_parts = []

        if city:
            location_parts.append(str(city))

        if commune:
            location_parts.append(str(commune))

        if quartier:
            location_parts.append(str(quartier))

        location = ", ".join(location_parts)

        self.ids.property_location.text = (
            "📍 " + location
            if location
            else "📍 Localisation non renseignée"
        )

        description = data.get(
            "description",
            "Aucune description."
        )

        self.ids.property_description.text = (
            "Description\n\n" + str(description)
        )

        property_type = data.get("property_type", "")
        transaction_type = data.get("transaction_type", "")
        bedrooms = data.get("bedrooms", "")
        bathrooms = data.get("bathrooms", "")
        area = data.get("area", "")

        info = []

        if property_type:
            info.append("Type : " + str(property_type))

        if transaction_type:
            info.append("Transaction : " + str(transaction_type))

        if bedrooms:
            info.append("Chambres : " + str(bedrooms))

        if bathrooms:
            info.append("Salles de bain : " + str(bathrooms))

        if area:
            info.append("Surface : " + str(area) + " m²")

        self.ids.property_info.text = "\n".join(info)

        owner_name = data.get(
            "owner_name",
            "Propriétaire"
        )

        owner_phone = data.get(
            "owner_phone",
            data.get("contact_phone", "")
        )

        self.ids.owner_name.text = (
            "👤 Propriétaire : " + str(owner_name)
        )

        if owner_phone:
            self.ids.owner_phone.text = (
                "📞 Téléphone : " + str(owner_phone)
            )
        else:
            self.ids.owner_phone.text = (
                "📞 Téléphone non renseigné"
            )

        self.load_photo(data)

    def load_photo(self, data):
        images = data.get("images", [])

        if not images:
            self.ids.property_image.source = ""
            print("MAISONPRO : aucune photo dans l'annonce")
            return

        image = images[0]

        if isinstance(image, dict):
            image_url = (
                image.get("url")
                or image.get("filename")
                or image.get("image")
                or ""
            )
        else:
            image_url = str(image)

        final_url = self.build_image_url(image_url)

        print("MAISONPRO PHOTO :", final_url)

        self.ids.property_image.source = final_url
        self.ids.property_image.reload()

    def go_back(self):
        app = App.get_running_app()
        app.sm.current = "home"

    def call_owner(self):
        if not self.property_data:
            return

        phone = self.property_data.get(
            "owner_phone",
            self.property_data.get("contact_phone", "")
        )

        if not phone:
            self.show_message(
                "Téléphone",
                "Le numéro du propriétaire n'est pas disponible."
            )
            return

        try:
            import webbrowser

            phone_clean = str(phone).replace(
                " ",
                ""
            )

            webbrowser.open(
                "tel:" + phone_clean
            )

        except Exception as e:
            self.show_message(
                "Erreur",
                "Impossible d'ouvrir l'appel."
            )

    def open_whatsapp(self):
        if not self.property_data:
            return

        phone = self.property_data.get(
            "owner_phone",
            self.property_data.get("contact_phone", "")
        )

        if not phone:
            self.show_message(
                "WhatsApp",
                "Le numéro du propriétaire n'est pas disponible."
            )
            return

        phone = str(phone).strip()
        phone = phone.replace(" ", "")
        phone = phone.replace("+", "")

        if phone.startswith("0"):
            phone = "225" + phone[1:]

        message = (
            "Bonjour, je suis intéressé(e) "
            "par votre annonce sur MaisonPro."
        )

        whatsapp_url = (
            "https://wa.me/"
            + phone
            + "?text="
            + quote(message)
        )

        try:
            import webbrowser
            webbrowser.open(whatsapp_url)
        except Exception:
            self.show_message(
                "WhatsApp",
                "Impossible d'ouvrir WhatsApp."
            )

    def add_to_favorites(self):
        if not self.property_id:
            return

        app = App.get_running_app()

        if not app.api_client.is_logged_in():
            self.show_message(
                "Connexion",
                "Connectez-vous pour ajouter cette annonce aux favoris."
            )
            return

        success, result = app.api_client.add_favorite(
            self.property_id
        )

        if success:
            self.show_message(
                "Favoris",
                "Annonce ajoutée aux favoris."
            )
        else:
            self.show_message(
                "Favoris",
                str(result)
            )

    def report_property(self):
        if not self.property_id:
            return

        app = App.get_running_app()

        if not app.api_client.is_logged_in():
            self.show_message(
                "Connexion",
                "Connectez-vous pour signaler une annonce."
            )
            return

        success, result = app.api_client.report_property(
            self.property_id,
            "Annonce à vérifier"
        )

        if success:
            self.show_message(
                "Signalement",
                "Votre signalement a été envoyé."
            )
        else:
            self.show_message(
                "Signalement",
                str(result)
            )

    def show_message(self, title, message):
        content = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        label = Label(
            text=str(message),
            halign="center",
            valign="middle"
        )

        button = Button(
            text="OK",
            size_hint_y=None,
            height=dp(45)
        )

        content.add_widget(label)
        content.add_widget(button)

        popup = Popup(
            title=str(title),
            content=content,
            size_hint=(0.85, 0.4),
            auto_dismiss=False
        )

        button.bind(
            on_release=popup.dismiss
        )

        popup.open()