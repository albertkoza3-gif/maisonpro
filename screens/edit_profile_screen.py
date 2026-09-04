from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp

from widgets.bottom_nav import BottomNav


Builder.load_string('''
<EditProfileScreen>:

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
                text: "Modifier mon profil"
                font_size: "22sp"
                bold: True
                color: 1, 1, 1, 1

        ScrollView:

            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(20)
                spacing: dp(8)

                Label:
                    text: "Prenom"
                    size_hint_y: None
                    height: dp(25)
                    halign: "left"
                    text_size: self.width, None

                TextInput:
                    id: first_name
                    multiline: False
                    size_hint_y: None
                    height: dp(48)
                    padding: dp(10)

                Label:
                    text: "Nom"
                    size_hint_y: None
                    height: dp(25)
                    halign: "left"
                    text_size: self.width, None

                TextInput:
                    id: last_name
                    multiline: False
                    size_hint_y: None
                    height: dp(48)
                    padding: dp(10)

                Label:
                    text: "Telephone"
                    size_hint_y: None
                    height: dp(25)
                    halign: "left"
                    text_size: self.width, None

                TextInput:
                    id: phone
                    multiline: False
                    size_hint_y: None
                    height: dp(48)
                    padding: dp(10)

                Label:
                    text: "E-mail"
                    size_hint_y: None
                    height: dp(25)
                    halign: "left"
                    text_size: self.width, None

                TextInput:
                    id: email
                    multiline: False
                    size_hint_y: None
                    height: dp(48)
                    padding: dp(10)

                Label:
                    text: "Nouveau mot de passe"
                    size_hint_y: None
                    height: dp(25)
                    halign: "left"
                    text_size: self.width, None

                TextInput:
                    id: password
                    multiline: False
                    password: True
                    size_hint_y: None
                    height: dp(48)
                    padding: dp(10)

                Label:
                    text: "Laissez vide pour garder le mot de passe actuel."
                    font_size: "12sp"
                    color: 0.4, 0.4, 0.4, 1
                    size_hint_y: None
                    height: dp(35)
                    text_size: self.width, None

                Button:
                    text: "Enregistrer les modifications"
                    size_hint_y: None
                    height: dp(52)
                    background_color: 0.10, 0.60, 0.30, 1
                    color: 1, 1, 1, 1
                    on_release: root.save_profile()

                Button:
                    text: "Annuler"
                    size_hint_y: None
                    height: dp(48)
                    background_color: 0.75, 0.75, 0.75, 1
                    color: 0.1, 0.1, 0.1, 1
                    on_release: root.go_back()

        BottomNav:
''')


class EditProfileScreen(Screen):

    def on_pre_enter(self, *args):
        self.load_profile()

    def load_profile(self):

        app = App.get_running_app()

        if not app.api_client.is_logged_in():
            app.sm.current = "login"
            return

        user = app.api_client.current_user

        if not user:
            return

        self.ids.first_name.text = str(
            user.get("first_name", "")
        )

        self.ids.last_name.text = str(
            user.get("last_name", "")
        )

        self.ids.phone.text = str(
            user.get("phone", "")
        )

        self.ids.email.text = str(
            user.get("email", "")
        )

        self.ids.password.text = ""

    def save_profile(self):

        app = App.get_running_app()

        if not app.api_client.is_logged_in():
            app.sm.current = "login"
            return

        first_name = self.ids.first_name.text.strip()
        last_name = self.ids.last_name.text.strip()
        phone = self.ids.phone.text.strip()
        email = self.ids.email.text.strip()
        password = self.ids.password.text.strip()

        if not first_name:
            self.show_message(
                "Erreur",
                "Le prenom est obligatoire."
            )
            return

        if not last_name:
            self.show_message(
                "Erreur",
                "Le nom est obligatoire."
            )
            return

        if not phone:
            self.show_message(
                "Erreur",
                "Le telephone est obligatoire."
            )
            return

        if not email:
            self.show_message(
                "Erreur",
                "L'e-mail est obligatoire."
            )
            return

        data = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email
        }

        if password:
            data["password"] = password

        try:

            success, result = app.api_client.update_profile(data)

            print("Modification profil :", success)
            print("Reponse serveur :", result)

            if success:

                if isinstance(result, dict):

                    if "user" in result:
                        app.api_client.current_user = result["user"]
                    else:
                        app.api_client.current_user = result

                self.show_message(
                    "Succes",
                    "Votre profil a ete mis a jour."
                )

                profile_screen = app.sm.get_screen("profile")
                profile_screen.load_profile()

            else:

                error = "Impossible de modifier le profil."

                if isinstance(result, dict):
                    error = result.get(
                        "error",
                        result.get("message", error)
                    )

                self.show_message(
                    "Erreur",
                    error
                )

        except Exception as e:

            print("Erreur modification profil :", e)

            self.show_message(
                "Erreur",
                f"Une erreur est survenue : {e}"
            )

    def go_back(self):

        app = App.get_running_app()
        app.sm.current = "profile"

    def show_message(self, title, message):

        Popup(
            title=title,
            content=Label(
                text=str(message),
                halign="center",
                valign="middle",
                text_size=(dp(280), None)
            ),
            size_hint=(0.85, 0.50)
        ).open()
