from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App

Builder.load_string("""
<LoginScreen>:
    BoxLayout:
        orientation: "vertical"
        padding: dp(30)
        spacing: dp(14)
        canvas.before:
            Color:
                rgba: 1, 1, 1, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Widget:
            size_hint_y: 0.15

        Label:
            text: "MAISONPRO"
            font_size: "34sp"
            bold: True
            color: 0.1, 0.35, 0.75, 1
            size_hint_y: None
            height: dp(60)

        Label:
            text: "Trouvez ou publiez un bien immobilier en Côte d'Ivoire"
            color: 0.4, 0.4, 0.4, 1
            font_size: "13sp"
            size_hint_y: None
            height: dp(30)

        Widget:
            size_hint_y: 0.08

        TextInput:
            id: email_input
            hint_text: "Adresse e-mail"
            multiline: False
            size_hint_y: None
            height: dp(46)
            padding: [dp(10), dp(12)]

        TextInput:
            id: password_input
            hint_text: "Mot de passe"
            password: True
            multiline: False
            size_hint_y: None
            height: dp(46)
            padding: [dp(10), dp(12)]

        Label:
            id: error_label
            text: ""
            color: 0.8, 0.1, 0.1, 1
            size_hint_y: None
            height: dp(24)
            font_size: "12sp"

        Button:
            text: "Se connecter"
            size_hint_y: None
            height: dp(48)
            background_color: 0.1, 0.35, 0.75, 1
            on_release: root.do_login()

        Button:
            text: "Créer un compte"
            size_hint_y: None
            height: dp(44)
            background_color: 0.9, 0.9, 0.9, 1
            color: 0.1, 0.1, 0.1, 1
            on_release: root.go_to_register()

        Widget:
""")


class LoginScreen(Screen):
    def do_login(self):
        app = App.get_running_app()
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text

        if not email or not password:
            self.ids.error_label.text = "Veuillez remplir tous les champs."
            return

        success, result = app.api_client.login(email, password)
        if success:
            self.ids.error_label.text = ""
            self.ids.password_input.text = ""
            app.on_login_success()
        else:
            self.ids.error_label.text = str(result)

    def go_to_register(self):
        self.manager.current = "register"