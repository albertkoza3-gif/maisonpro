from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App

Builder.load_string("""
<RegisterScreen>:
    ScrollView:
        BoxLayout:
            orientation: "vertical"
            padding: dp(30)
            spacing: dp(12)
            size_hint_y: None
            height: self.minimum_height

            Label:
                text: "Créer un compte"
                font_size: "26sp"
                bold: True
                color: 0.1, 0.35, 0.75, 1
                size_hint_y: None
                height: dp(50)

            TextInput:
                id: last_name_input
                hint_text: "Nom"
                multiline: False
                size_hint_y: None
                height: dp(46)
                padding: [dp(10), dp(12)]

            TextInput:
                id: first_name_input
                hint_text: "Prénom"
                multiline: False
                size_hint_y: None
                height: dp(46)
                padding: [dp(10), dp(12)]

            TextInput:
                id: phone_input
                hint_text: "Numéro de téléphone"
                multiline: False
                input_type: "number"
                size_hint_y: None
                height: dp(46)
                padding: [dp(10), dp(12)]

            TextInput:
                id: email_input
                hint_text: "Adresse e-mail"
                multiline: False
                size_hint_y: None
                height: dp(46)
                padding: [dp(10), dp(12)]

            TextInput:
                id: password_input
                hint_text: "Mot de passe (6 caractères minimum)"
                password: True
                multiline: False
                size_hint_y: None
                height: dp(46)
                padding: [dp(10), dp(12)]

            TextInput:
                id: confirm_password_input
                hint_text: "Confirmer le mot de passe"
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
                height: dp(40)
                font_size: "12sp"
                text_size: self.width, None

            Button:
                text: "S'inscrire"
                size_hint_y: None
                height: dp(48)
                background_color: 0.1, 0.35, 0.75, 1
                on_release: root.do_register()

            Button:
                text: "J'ai déjà un compte"
                size_hint_y: None
                height: dp(44)
                background_color: 0.9, 0.9, 0.9, 1
                color: 0.1, 0.1, 0.1, 1
                on_release: root.go_to_login()
""")


class RegisterScreen(Screen):
    def do_register(self):
        app = App.get_running_app()

        first_name = self.ids.first_name_input.text.strip()
        last_name = self.ids.last_name_input.text.strip()
        phone = self.ids.phone_input.text.strip()
        email = self.ids.email_input.text.strip()
        password = self.ids.password_input.text
        confirm_password = self.ids.confirm_password_input.text

        if not all([first_name, last_name, phone, email, password, confirm_password]):
            self.ids.error_label.text = "Veuillez remplir tous les champs."
            return

        if password != confirm_password:
            self.ids.error_label.text = "Les mots de passe ne correspondent pas."
            return

        success, result = app.api_client.register(
            first_name, last_name, phone, email, password, confirm_password
        )
        if success:
            self.ids.error_label.text = ""
            app.on_login_success()
        else:
            self.ids.error_label.text = str(result)

    def go_to_login(self):
        self.manager.current = "login"