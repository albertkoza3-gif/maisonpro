from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.app import App
from kivy.metrics import dp

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
                    text: "3. Photos"
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
                    height: dp(44)
                    background_color: 0.9, 0.9, 0.9, 1
                    color: 0.1, 0.1, 0.1, 1
                    on_release: root.open_photo_picker()

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
                    hint_text: "Ville (ex: Abidjan)"
                    multiline: False
                    size_hint_y: None
                    height: dp(44)

                TextInput:
                    id: commune_input
                    hint_text: "Commune (ex: Cocody)"
                    multiline: False
                    size_hint_y: None
                    height: dp(44)

                TextInput:
                    id: quartier_input
                    hint_text: "Quartier (ex: Riviera)"
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

                TextInput:
                    id: contact_phone_input
                    hint_text: "Numéro de contact pour cette annonce"
                    multiline: False
                    size_hint_y: None
                    height: dp(44)

                Label:
                    id: error_label
                    text: ""
                    color: 0.8, 0.1, 0.1, 1
                    size_hint_y: None
                    height: dp(40)
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
    selected_photos = None

    def on_pre_enter(self, *args):
        if self.selected_photos is None:
            self.selected_photos = []
        app = App.get_running_app()
        if not app.api_client.is_logged_in():
            app.sm.current = "login"

    def open_photo_picker(self):
        box = BoxLayout(orientation="vertical", spacing=dp(8), padding=dp(8))
        chooser = FileChooserIconView(multiselect=True, filters=["*.png", "*.jpg", "*.jpeg", "*.gif", "*.webp"])
        box.add_widget(chooser)

        popup = Popup(title="Choisissez une ou plusieurs photos", content=box, size_hint=(0.95, 0.9))

        buttons = BoxLayout(size_hint_y=None, height=dp(44), spacing=dp(6))

        def confirm(instance):
            self.selected_photos = list(chooser.selection)
            count = len(self.selected_photos)
            self.ids.photos_button.text = f"Ajouter des photos ({count} sélectionnée(s))"
            popup.dismiss()

        confirm_btn = Button(text="Valider la sélection")
        confirm_btn.bind(on_release=confirm)
        cancel_btn = Button(text="Annuler")
        cancel_btn.bind(on_release=lambda i: popup.dismiss())
        buttons.add_widget(cancel_btn)
        buttons.add_widget(confirm_btn)
        box.add_widget(buttons)

        popup.open()

    def do_publish(self):
        app = App.get_running_app()

        title = self.ids.title_input.text.strip()
        description = self.ids.description_input.text.strip()
        price = self.ids.price_input.text.strip()
        city = self.ids.city_input.text.strip()
        contact_phone = self.ids.contact_phone_input.text.strip()

        if not title or not description or not price or not city or not contact_phone:
            self.ids.error_label.text = "Titre, description, prix, ville et contact sont obligatoires."
            return

        fields = {
            "property_type": self.ids.type_spinner.text,
            "transaction_type": self.ids.transaction_spinner.text,
            "title": title,
            "description": description,
            "price": price,
            "city": city,
            "commune": self.ids.commune_input.text.strip(),
            "quartier": self.ids.quartier_input.text.strip(),
            "bedrooms": self.ids.bedrooms_input.text.strip(),
            "bathrooms": self.ids.bathrooms_input.text.strip(),
            "area": self.ids.area_input.text.strip(),
            "contact_phone": contact_phone,
        }

        success, result = app.api_client.create_property(fields, self.selected_photos or [])
        if success:
            self.ids.error_label.text = ""
            self._reset_form()
            app.sm.current = "home"
            home_screen = app.sm.get_screen("home")
            home_screen.load_listings()
        else:
            self.ids.error_label.text = str(result)

    def _reset_form(self):
        self.ids.title_input.text = ""
        self.ids.description_input.text = ""
        self.ids.price_input.text = ""
        self.ids.city_input.text = ""
        self.ids.commune_input.text = ""
        self.ids.quartier_input.text = ""
        self.ids.bedrooms_input.text = ""
        self.ids.bathrooms_input.text = ""
        self.ids.area_input.text = ""
        self.ids.contact_phone_input.text = ""
        self.selected_photos = []
        self.ids.photos_button.text = "Ajouter des photos (0 sélectionnée(s))"