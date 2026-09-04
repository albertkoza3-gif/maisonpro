from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.app import App
from kivy.metrics import dp
from kivy.clock import Clock
import os

from widgets.bottom_nav import BottomNav  # noqa: F401


Builder.load_string("""
<PublishScreen>:
    BoxLayout:
        orientation: "vertical"

        Label:
            text: "Publier une annonce"
            bold: True
            font_size: "20sp"
            color: 1, 1, 1, 1
            size_hint_y: None
            height: dp(50)
            canvas.before:
                Color:
                    rgba: 0.1, 0.35, 0.75, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

        ScrollView:
            do_scroll_x: False

            BoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(10)
                size_hint_y: None
                height: self.minimum_height

                Label:
                    text: "1. Type de bien"
                    bold: True
                    size_hint_y: None
                    height: dp(22)
                    text_size: self.width, None
                    halign: "left"
                    color: 0.1, 0.1, 0.1, 1

                Spinner:
                    id: type_spinner
                    text: "maison"
                    values: ["maison", "appartement", "studio", "villa", "terrain", "magasin", "bureau", "chambre", "autre"]
                    size_hint_y: None
                    height: dp(44)

                Label:
                    text: "2. Vente ou location"
                    bold: True
                    size_hint_y: None
                    height: dp(22)
                    text_size: self.width, None
                    halign: "left"
                    color: 0.1, 0.1, 0.1, 1

                Spinner:
                    id: transaction_spinner
                    text: "vente"
                    values: ["vente", "location"]
                    size_hint_y: None
                    height: dp(44)

                Label:
                    text: "3. Photos du bien"
                    bold: True
                    size_hint_y: None
                    height: dp(22)
                    text_size: self.width, None
                    halign: "left"
                    color: 0.1, 0.1, 0.1, 1

                Button:
                    id: photos_button
                    text: "Ajouter des photos (0 sélectionnée(s))"
                    size_hint_y: None
                    height: dp(50)
                    background_color: 0.9, 0.9, 0.9, 1
                    color: 0.1, 0.1, 0.1, 1
                    on_release: root.open_photo_picker()

                Label:
                    id: photos_info
                    text: "Aucune photo sélectionnée"
                    size_hint_y: None
                    height: dp(30)
                    color: 0.2, 0.4, 0.2, 1
                    text_size: self.width, None
                    halign: "left"

                Label:
                    text: "4. Titre de l'annonce"
                    bold: True
                    size_hint_y: None
                    height: dp(22)
                    text_size: self.width, None
                    halign: "left"
                    color: 0.1, 0.1, 0.1, 1

                TextInput:
                    id: title_input
                    hint_text: "Ex : Belle villa 4 chambres à Cocody"
                    multiline: False
                    size_hint_y: None
                    height: dp(44)

                Label:
                    text: "5. Description"
                    bold: True
                    size_hint_y: None
                    height: dp(22)
                    text_size: self.width, None
                    halign: "left"
                    color: 0.1, 0.1, 0.1, 1

                TextInput:
                    id: description_input
                    hint_text: "Décrivez le bien en détail..."
                    multiline: True
                    size_hint_y: None
                    height: dp(100)

                Label:
                    text: "Prix (FCFA)"
                    bold: True
                    size_hint_y: None
                    height: dp(22)
                    text_size: self.width, None
                    halign: "left"
                    color: 0.1, 0.1, 0.1, 1

                TextInput:
                    id: price_input
                    hint_text: "Ex : 25000000"
                    input_type: "number"
                    multiline: False
                    size_hint_y: None
                    height: dp(44)

                Label:
                    text: "6. Localisation"
                    bold: True
                    size_hint_y: None
                    height: dp(22)
                    text_size: self.width, None
                    halign: "left"
                    color: 0.1, 0.1, 0.1, 1

                TextInput:
                    id: city_input
                    hint_text: "Ville (ex : Abidjan)"
                    multiline: False
                    size_hint_y: None
                    height: dp(44)

                TextInput:
                    id: commune_input
                    hint_text: "Commune (ex : Cocody)"
                    multiline: False
                    size_hint_y: None
                    height: dp(44)

                TextInput:
                    id: quartier_input
                    hint_text: "Quartier (ex : Riviera)"
                    multiline: False
                    size_hint_y: None
                    height: dp(44)

                Label:
                    text: "7. Caractéristiques"
                    bold: True
                    size_hint_y: None
                    height: dp(22)
                    text_size: self.width, None
                    halign: "left"
                    color: 0.1, 0.1, 0.1, 1

                BoxLayout:
                    size_hint_y: None
                    height: dp(44)
                    spacing: dp(6)

                    TextInput:
                        id: bedrooms_input
                        hint_text: "Chambres"
                        input_type: "number"
                        multiline: False

                    TextInput:
                        id: bathrooms_input
                        hint_text: "Salles de bain"
                        input_type: "number"
                        multiline: False

                TextInput:
                    id: area_input
                    hint_text: "Superficie (m²)"
                    input_type: "number"
                    multiline: False
                    size_hint_y: None
                    height: dp(44)

                Label:
                    text: "Le numéro du propriétaire sera automatiquement utilisé."
                    size_hint_y: None
                    height: dp(35)
                    color: 0.3, 0.3, 0.3, 1
                    text_size: self.width, None
                    halign: "left"

                Label:
                    id: error_label
                    text: ""
                    color: 0.8, 0.1, 0.1, 1
                    size_hint_y: None
                    height: dp(50)
                    text_size: self.width, None

                Button:
                    text: "8. Publier l'annonce"
                    size_hint_y: None
                    height: dp(50)
                    background_color: 0.1, 0.6, 0.3, 1
                    on_release: root.do_publish()

        BottomNav:
""")


class PublishScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.selected_photos = []

    def on_pre_enter(self, *args):
        app = App.get_running_app()

        if not app.api_client.is_logged_in():
            app.sm.current = "login"
            return

        # Vérifier le profil de l'utilisateur
        if not app.api_client.current_user:
            success, user = app.api_client.get_my_profile()

            if not success:
                self.ids.error_label.text = (
                    "Impossible de récupérer les informations de votre compte."
                )
                return

        # Réinitialiser le message
        self.ids.error_label.text = ""

    def open_photo_picker(self):

        box = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            padding=dp(8)
        )

        chooser = FileChooserIconView(
            multiselect=True,
            filters=[
                "*.png",
                "*.jpg",
                "*.jpeg",
                "*.gif",
                "*.webp"
            ]
        )

        box.add_widget(chooser)

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(8)
        )

        cancel_btn = Button(
            text="Annuler"
        )

        confirm_btn = Button(
            text="Valider"
        )

        buttons.add_widget(cancel_btn)
        buttons.add_widget(confirm_btn)

        box.add_widget(buttons)

        popup = Popup(
            title="Choisir les photos du bien",
            content=box,
            size_hint=(0.95, 0.90)
        )

        cancel_btn.bind(
            on_release=lambda instance: popup.dismiss()
        )

        def confirm_selection(instance):

            selections = list(chooser.selection)

            print("")
            print("========================================")
            print("MAISONPRO - SÉLECTION DES PHOTOS")
            print("Nombre sélectionné :", len(selections))

            for photo in selections:
                print("PHOTO :", photo)

            print("========================================")
            print("")

            # Garder uniquement les vrais fichiers
            valid_photos = []

            for photo in selections:

                if os.path.isfile(photo):

                    extension = os.path.splitext(photo)[1].lower()

                    if extension in [
                        ".jpg",
                        ".jpeg",
                        ".png",
                        ".gif",
                        ".webp"
                    ]:
                        valid_photos.append(
                            os.path.abspath(photo)
                        )

            self.selected_photos = valid_photos

            count = len(self.selected_photos)

            self.ids.photos_button.text = (
                f"Ajouter des photos ({count} sélectionnée(s))"
            )

            if count == 0:

                self.ids.photos_info.text = (
                    "Aucune photo valide sélectionnée."
                )

            elif count == 1:

                self.ids.photos_info.text = (
                    "1 photo prête à être envoyée."
                )

            else:

                self.ids.photos_info.text = (
                    f"{count} photos prêtes à être envoyées."
                )

            print("PHOTOS VALIDES :", self.selected_photos)

            popup.dismiss()

        confirm_btn.bind(
            on_release=confirm_selection
        )

        popup.open()

    def do_publish(self):

        app = App.get_running_app()

        self.ids.error_label.text = ""

        # -----------------------------------------
        # VÉRIFICATION CONNEXION
        # -----------------------------------------

        if not app.api_client.is_logged_in():

            self.ids.error_label.text = (
                "Vous devez être connecté pour publier."
            )

            app.sm.current = "login"
            return

        # -----------------------------------------
        # RÉCUPÉRER LES INFORMATIONS DU COMPTE
        # -----------------------------------------

        user = app.api_client.current_user

        if not user:

            success, user = app.api_client.get_my_profile()

            if not success or not user:

                self.ids.error_label.text = (
                    "Impossible de récupérer votre compte."
                )

                return

        owner_phone = (
            user.get("phone")
            if isinstance(user, dict)
            else None
        )

        if not owner_phone:

            self.ids.error_label.text = (
                "Votre numéro de téléphone n'est pas enregistré dans votre compte."
            )

            return

        print("")
        print("========================================")
        print("MAISONPRO - PUBLICATION")
        print("Propriétaire :", user.get("first_name", ""))
        print("Téléphone :", owner_phone)
        print("Nombre de photos :", len(self.selected_photos))
        print("========================================")
        print("")

        # -----------------------------------------
        # RÉCUPÉRER LES CHAMPS
        # -----------------------------------------

        title = self.ids.title_input.text.strip()
        description = self.ids.description_input.text.strip()
        price = self.ids.price_input.text.strip()
        city = self.ids.city_input.text.strip()

        commune = self.ids.commune_input.text.strip()
        quartier = self.ids.quartier_input.text.strip()

        bedrooms = self.ids.bedrooms_input.text.strip()
        bathrooms = self.ids.bathrooms_input.text.strip()
        area = self.ids.area_input.text.strip()

        # -----------------------------------------
        # VÉRIFICATIONS
        # -----------------------------------------

        if not title:

            self.ids.error_label.text = (
                "Le titre de l'annonce est obligatoire."
            )

            return

        if not description:

            self.ids.error_label.text = (
                "La description est obligatoire."
            )

            return

        if not price:

            self.ids.error_label.text = (
                "Le prix est obligatoire."
            )

            return

        if not city:

            self.ids.error_label.text = (
                "La ville est obligatoire."
            )

            return

        # -----------------------------------------
        # VÉRIFICATION DES PHOTOS
        # -----------------------------------------

        if not self.selected_photos:

            self.ids.error_label.text = (
                "Sélectionne au moins une photo du bien."
            )

            return

        for photo in self.selected_photos:

            if not os.path.isfile(photo):

                self.ids.error_label.text = (
                    f"Photo introuvable : {photo}"
                )

                return

        # -----------------------------------------
        # PRÉPARATION DES DONNÉES
        # -----------------------------------------

        fields = {

            "property_type":
                self.ids.type_spinner.text,

            "transaction_type":
                self.ids.transaction_spinner.text,

            "title":
                title,

            "description":
                description,

            "price":
                price,

            "city":
                city,

            "commune":
                commune,

            "quartier":
                quartier,

            "bedrooms":
                bedrooms,

            "bathrooms":
                bathrooms,

            "area":
                area,

            # Le backend récupère également
            # automatiquement le téléphone du compte.
            "contact_phone":
                owner_phone,
        }

        print("")
        print("DONNÉES ENVOYÉES :")
        print(fields)

        print("")
        print("PHOTOS ENVOYÉES :")

        for photo in self.selected_photos:
            print(photo)

        print("")

        # -----------------------------------------
        # ENVOI AU SERVEUR
        # -----------------------------------------

        self.ids.error_label.color = (
            0.1, 0.35, 0.75, 1
        )

        self.ids.error_label.text = (
            "Publication en cours..."
        )

        success, result = app.api_client.create_property(
            fields,
            self.selected_photos
        )

        # -----------------------------------------
        # SUCCÈS
        # -----------------------------------------

        if success:

            print("")
            print("========================================")
            print("ANNONCE PUBLIÉE AVEC SUCCÈS")
            print("========================================")
            print("")

            self.ids.error_label.text = ""

            self._reset_form()

            app.sm.current = "home"

            home_screen = app.sm.get_screen("home")

            Clock.schedule_once(
                lambda dt: home_screen.load_listings(),
                0.2
            )

        # -----------------------------------------
        # ERREUR
        # -----------------------------------------

        else:

            self.ids.error_label.color = (
                0.8, 0.1, 0.1, 1
            )

            self.ids.error_label.text = str(result)

            print("")
            print("ERREUR PUBLICATION :", result)
            print("")

    def _reset_form(self):

        self.ids.type_spinner.text = "maison"
        self.ids.transaction_spinner.text = "vente"

        self.ids.title_input.text = ""
        self.ids.description_input.text = ""
        self.ids.price_input.text = ""

        self.ids.city_input.text = ""
        self.ids.commune_input.text = ""
        self.ids.quartier_input.text = ""

        self.ids.bedrooms_input.text = ""
        self.ids.bathrooms_input.text = ""
        self.ids.area_input.text = ""

        self.selected_photos = []

        self.ids.photos_button.text = (
            "Ajouter des photos (0 sélectionnée(s))"
        )

        self.ids.photos_info.text = (
            "Aucune photo sélectionnée"
        )

        self.ids.error_label.text = ""