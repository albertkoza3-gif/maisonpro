from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp


Builder.load_string("""
<EditPropertyScreen>:

    BoxLayout:
        orientation: "vertical"

        BoxLayout:
            size_hint_y: None
            height: dp(65)
            padding: dp(15)

            canvas.before:
                Color:
                    rgba: 0.10, 0.35, 0.75, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: "MODIFIER L'ANNONCE"
                font_size: "21sp"
                bold: True
                color: 1, 1, 1, 1

        ScrollView:

            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(15)
                spacing: dp(8)

                Label:
                    text: "Titre"
                    size_hint_y: None
                    height: dp(25)

                TextInput:
                    id: title
                    multiline: False
                    size_hint_y: None
                    height: dp(48)

                Label:
                    text: "Description"
                    size_hint_y: None
                    height: dp(25)

                TextInput:
                    id: description
                    multiline: True
                    size_hint_y: None
                    height: dp(110)

                Label:
                    text: "Prix"
                    size_hint_y: None
                    height: dp(25)

                TextInput:
                    id: price
                    multiline: False
                    input_filter: "float"
                    size_hint_y: None
                    height: dp(48)

                Label:
                    text: "Ville"
                    size_hint_y: None
                    height: dp(25)

                TextInput:
                    id: city
                    multiline: False
                    size_hint_y: None
                    height: dp(48)

                Label:
                    text: "Commune"
                    size_hint_y: None
                    height: dp(25)

                TextInput:
                    id: commune
                    multiline: False
                    size_hint_y: None
                    height: dp(48)

                Label:
                    text: "Quartier"
                    size_hint_y: None
                    height: dp(25)

                TextInput:
                    id: quartier
                    multiline: False
                    size_hint_y: None
                    height: dp(48)

                Label:
                    text: "Téléphone de contact"
                    size_hint_y: None
                    height: dp(25)

                TextInput:
                    id: contact_phone
                    multiline: False
                    size_hint_y: None
                    height: dp(48)

                Button:
                    text: "Enregistrer les modifications"
                    size_hint_y: None
                    height: dp(52)
                    background_color: 0.10, 0.60, 0.30, 1
                    color: 1, 1, 1, 1
                    on_release: root.save_property()

                Button:
                    text: "Annuler"
                    size_hint_y: None
                    height: dp(48)
                    background_color: 0.75, 0.75, 0.75, 1
                    color: 0.1, 0.1, 0.1, 1
                    on_release: root.go_back()
""")


class EditPropertyScreen(Screen):

    property_data = None

    def on_pre_enter(self, *args):
        self.load_property()

    def load_property(self):

        if not self.property_data:
            return

        prop = self.property_data

        self.ids.title.text = str(
            prop.get("title", "")
        )

        self.ids.description.text = str(
            prop.get("description", "")
        )

        self.ids.price.text = str(
            prop.get("price", "")
        )

        self.ids.city.text = str(
            prop.get("city", "")
        )

        self.ids.commune.text = str(
            prop.get("commune", "")
        )

        self.ids.quartier.text = str(
            prop.get("quartier", "")
        )

        self.ids.contact_phone.text = str(
            prop.get("contact_phone", "")
        )

    def save_property(self):

        if not self.property_data:
            self.show_message(
                "Erreur",
                "Annonce introuvable."
            )
            return

        app = App.get_running_app()

        property_id = self.property_data.get("id")

        title = self.ids.title.text.strip()
        description = self.ids.description.text.strip()
        price = self.ids.price.text.strip()
        city = self.ids.city.text.strip()
        commune = self.ids.commune.text.strip()
        quartier = self.ids.quartier.text.strip()
        contact_phone = self.ids.contact_phone.text.strip()

        if not title:
            self.show_message(
                "Erreur",
                "Le titre est obligatoire."
            )
            return

        if not description:
            self.show_message(
                "Erreur",
                "La description est obligatoire."
            )
            return

        if not price:
            self.show_message(
                "Erreur",
                "Le prix est obligatoire."
            )
            return

        if not city:
            self.show_message(
                "Erreur",
                "La ville est obligatoire."
            )
            return

        try:
            price_value = float(price)
        except ValueError:
            self.show_message(
                "Erreur",
                "Le prix doit être un nombre."
            )
            return

        data = {
            "title": title,
            "description": description,
            "price": price_value,
            "city": city,
            "commune": commune,
            "quartier": quartier,
            "contact_phone": contact_phone
        }

        success, result = app.api_client.update_property(
            property_id,
            data
        )

        if success:

            self.show_message(
                "Succès",
                "Annonce modifiée avec succès."
            )

            self.property_data = None

            app.sm.current = "my_properties"

        else:

            error = "Impossible de modifier l'annonce."

            if isinstance(result, dict):
                error = result.get(
                    "error",
                    result.get("message", error)
                )

            self.show_message(
                "Erreur",
                error
            )

    def go_back(self):

        self.property_data = None

        app = App.get_running_app()
        app.sm.current = "my_properties"

    def show_message(self, title, message):

        Popup(
            title=title,
            content=Label(
                text=str(message),
                halign="center",
                valign="middle",
                text_size=(dp(280), None)
            ),
            size_hint=(0.85, 0.35)
        ).open()