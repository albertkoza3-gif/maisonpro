from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp

from widgets.bottom_nav import BottomNav
from widgets.property_card import PropertyCard


Builder.load_string("""
<MyPropertiesScreen>:

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
                text: "MES ANNONCES"
                font_size: "22sp"
                bold: True
                color: 1, 1, 1, 1

        ScrollView:

            BoxLayout:
                id: listings_box
                orientation: "vertical"
                size_hint_y: None
                size_hint_x: 1
                height: self.minimum_height
                padding: dp(12)
                spacing: dp(12)

        BottomNav:
""")


class MyPropertiesScreen(Screen):

    def on_pre_enter(self, *args):
        self.load_properties()

    def load_properties(self):
        app = App.get_running_app()

        if not app.api_client.is_logged_in():
            app.sm.current = "login"
            return

        self.ids.listings_box.clear_widgets()

        success, properties = app.api_client.get_my_properties()

        if not success:
            self.show_message(
                "Erreur",
                "Impossible de charger vos annonces."
            )
            return

        if not properties:
            label = Label(
                text="Vous n'avez encore publié aucune annonce.",
                size_hint_y=None,
                height=dp(80),
                halign="center",
                valign="middle"
            )
            label.bind(
                size=lambda instance, value:
                setattr(instance, "text_size", value)
            )
            self.ids.listings_box.add_widget(label)
            return

        for prop in properties:
            self.add_property(prop)

    def add_property(self, prop):

        card_box = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            height=dp(230),
            spacing=dp(6)
        )

        card = PropertyCard()
        card.set_data(prop)
        card_box.add_widget(card)

        buttons = BoxLayout(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(45),
            spacing=dp(5)
        )

        property_id = prop.get("id")

        is_active = prop.get("is_active", True)

        status_button = Button(
            text="Désactiver" if is_active else "Activer",
            background_color=(
                (0.95, 0.55, 0.10, 1)
                if is_active
                else
                (0.10, 0.60, 0.30, 1)
            )
        )

        edit_button = Button(
            text="Modifier",
            background_color=(0.10, 0.35, 0.75, 1)
        )

        delete_button = Button(
            text="Supprimer",
            background_color=(0.85, 0.15, 0.15, 1)
        )

        status_button.bind(
            on_release=lambda instance, p=property_id, a=is_active:
            self.toggle_property(p, a)
        )

        edit_button.bind(
            on_release=lambda instance, p=prop:
            self.edit_property(p)
        )

        delete_button.bind(
            on_release=lambda instance, p=property_id:
            self.confirm_delete(p)
        )

        buttons.add_widget(status_button)
        buttons.add_widget(edit_button)
        buttons.add_widget(delete_button)

        card_box.add_widget(buttons)

        self.ids.listings_box.add_widget(card_box)

    def toggle_property(self, property_id, current_status):

        app = App.get_running_app()

        new_status = not current_status

        success, result = app.api_client.update_property(
            property_id,
            {
                "is_active": new_status
            }
        )

        if success:
            message = (
                "Annonce activée."
                if new_status
                else
                "Annonce désactivée."
            )

            self.show_message("Succès", message)
            self.load_properties()

        else:
            error = "Impossible de modifier le statut."

            if isinstance(result, dict):
                error = result.get(
                    "error",
                    result.get("message", error)
                )

            self.show_message("Erreur", error)

    def confirm_delete(self, property_id):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        content.add_widget(
            Label(
                text="Voulez-vous vraiment supprimer cette annonce ?"
            )
        )

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(10)
        )

        cancel_button = Button(
            text="Annuler"
        )

        delete_button = Button(
            text="Supprimer",
            background_color=(0.85, 0.15, 0.15, 1)
        )

        buttons.add_widget(cancel_button)
        buttons.add_widget(delete_button)

        content.add_widget(buttons)

        popup = Popup(
            title="Confirmation",
            content=content,
            size_hint=(0.85, 0.35)
        )

        cancel_button.bind(
            on_release=popup.dismiss
        )

        delete_button.bind(
            on_release=lambda instance:
            self.delete_property(property_id, popup)
        )

        popup.open()

    def delete_property(self, property_id, popup):

        app = App.get_running_app()

        success, result = app.api_client.delete_property(
            property_id
        )

        popup.dismiss()

        if success:
            self.show_message(
                "Succès",
                "Annonce supprimée avec succès."
            )
            self.load_properties()
        else:
            error = "Impossible de supprimer l'annonce."

            if isinstance(result, dict):
                error = result.get(
                    "error",
                    result.get("message", error)
                )

            self.show_message("Erreur", error)

    def edit_property(self, property_data):

        app = App.get_running_app()

        edit_screen = app.sm.get_screen(
            "edit_property"
        )

        edit_screen.property_data = property_data

        app.sm.current = "edit_property"

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