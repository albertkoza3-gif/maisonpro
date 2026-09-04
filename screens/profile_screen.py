from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.metrics import dp

from widgets.bottom_nav import BottomNav


Builder.load_string('''
<ProfileScreen>:

    BoxLayout:
        orientation: "vertical"

        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: dp(150)
            padding: dp(15)
            spacing: dp(4)

            canvas.before:
                Color:
                    rgba: 0.10, 0.35, 0.75, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: "PROFIL"
                font_size: "24sp"
                bold: True
                color: 1, 1, 1, 1

            Label:
                id: avatar_label
                text: "USER"
                font_size: "24sp"
                bold: True
                color: 1, 1, 1, 1

            Label:
                id: name_label
                text: "Nom Prénom"
                font_size: "18sp"
                bold: True
                color: 1, 1, 1, 1

            Label:
                id: role_label
                text: "Utilisateur"
                font_size: "14sp"
                color: 1, 1, 1, 1

        ScrollView:

            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(15)
                spacing: dp(10)

                Button:
                    text: "Informations du compte"
                    size_hint_y: None
                    height: dp(52)
                    background_color: 0.92, 0.94, 0.98, 1
                    color: 0.10, 0.10, 0.10, 1
                    on_release: root.show_account_info()

                Button:
                    text: "Modifier mon profil"
                    size_hint_y: None
                    height: dp(52)
                    background_color: 0.92, 0.94, 0.98, 1
                    color: 0.10, 0.10, 0.10, 1
                    on_release: root.edit_profile()

                Button:
                    text: "Mes annonces"
                    size_hint_y: None
                    height: dp(52)
                    background_color: 0.92, 0.94, 0.98, 1
                    color: 0.10, 0.10, 0.10, 1
                    on_release: root.show_my_properties()

                Button:
                    text: "Mes favoris"
                    size_hint_y: None
                    height: dp(52)
                    background_color: 0.92, 0.94, 0.98, 1
                    color: 0.90, 0.15, 0.20, 1
                    on_release: root.show_favorites()

                Button:
                    id: admin_button
                    text: "Ouvrir l'administration"
                    size_hint_y: None
                    height: dp(52)
                    background_color: 0.10, 0.35, 0.75, 1
                    color: 1, 1, 1, 1
                    on_release: root.open_admin()

                Button:
                    text: "Déconnexion"
                    size_hint_y: None
                    height: dp(52)
                    background_color: 0.85, 0.15, 0.15, 1
                    color: 1, 1, 1, 1
                    on_release: root.logout()

        BottomNav:
''')


class ProfileScreen(Screen):

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

        first_name = str(user.get("first_name", ""))
        last_name = str(user.get("last_name", ""))

        full_name = f"{first_name} {last_name}".strip()

        if not full_name:
            full_name = "Utilisateur"

        self.ids.name_label.text = full_name

        roles = user.get("roles", [])

        if isinstance(roles, list):
            if "admin" in roles:
                role = "Administrateur"
            elif roles:
                role = ", ".join(roles)
            else:
                role = "Utilisateur"
        else:
            role = str(roles) if roles else "Utilisateur"

        self.ids.role_label.text = role

        is_admin = bool(user.get("is_admin", False))

        self.ids.admin_button.opacity = 1 if is_admin else 0
        self.ids.admin_button.disabled = not is_admin

    def show_account_info(self):

        app = App.get_running_app()
        user = app.api_client.current_user

        if not user:
            self.show_message(
                "Erreur",
                "Utilisateur non connecté."
            )
            return

        first_name = user.get("first_name", "")
        last_name = user.get("last_name", "")
        email = user.get("email", "")
        phone = user.get("phone", "")

        roles = user.get("roles", [])

        if isinstance(roles, list):
            role = ", ".join(roles)
        else:
            role = str(roles)

        admin = "Oui" if user.get("is_admin") else "Non"

        message = (
            f"Nom : {first_name} {last_name}\\n\\n"
            f"E-mail : {email}\\n\\n"
            f"Téléphone : {phone}\\n\\n"
            f"Rôle : {role}\\n\\n"
            f"Administrateur : {admin}"
        )

        self.show_message(
            "Informations du compte",
            message
        )

    def edit_profile(self):

        app = App.get_running_app()

        if "edit_profile" in app.sm.screen_names:
            app.sm.current = "edit_profile"
        else:
            self.show_message(
                "Information",
                "L'écran de modification du profil est indisponible."
            )

    def show_my_properties(self):

        app = App.get_running_app()

        if "my_properties" in app.sm.screen_names:
            app.sm.current = "my_properties"
        else:
            self.show_message(
                "Mes annonces",
                "Cette page sera ajoutée prochainement."
            )

    def show_favorites(self):

        app = App.get_running_app()

        if "favorites" in app.sm.screen_names:
            app.sm.current = "favorites"
        else:
            self.show_message(
                "Favoris",
                "La page des favoris est indisponible."
            )

    def open_admin(self):

        app = App.get_running_app()
        user = app.api_client.current_user

        if not user or not user.get("is_admin"):
            self.show_message(
                "Accès refusé",
                "Cette section est réservée à l'administrateur."
            )
            return

        if "admin" in app.sm.screen_names:
            app.sm.current = "admin"
        else:
            self.show_message(
                "Erreur",
                "L'écran administration est indisponible."
            )

    def logout(self):

        app = App.get_running_app()

        app.api_client.token = None
        app.api_client.current_user = None

        app.sm.current = "login"

    def go_home(self):

        app = App.get_running_app()
        app.sm.current = "home"

    def show_message(self, title, message):

        popup = Popup(
            title=title,
            content=Label(
                text=str(message),
                halign="center",
                valign="middle",
                text_size=(dp(280), None)
            ),
            size_hint=(0.85, 0.55)
        )

        popup.open()
