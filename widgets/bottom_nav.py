from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App
from kivy.metrics import dp


Builder.load_string("""
<BottomNav>:

    orientation: "horizontal"
    size_hint_y: None
    height: dp(70)
    spacing: dp(1)
    padding: dp(2)

    canvas.before:
        Color:
            rgba: 0.92, 0.94, 0.98, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Button:
        text: "Accueil"
        font_size: "12sp"
        background_color: 0, 0, 0, 0
        color: 0.10, 0.35, 0.75, 1
        on_release: root.go("home")

    Button:
        text: "Recherche"
        font_size: "12sp"
        background_color: 0, 0, 0, 0
        color: 0.10, 0.35, 0.75, 1
        on_release: root.go("search")

    Button:
        text: "Publier"
        font_size: "12sp"
        background_color: 0, 0, 0, 0
        color: 0.10, 0.35, 0.75, 1
        on_release: root.go("publish")

    Button:
        text: "Favoris"
        font_size: "12sp"
        background_color: 0, 0, 0, 0
        color: 0.90, 0.15, 0.20, 1
        on_release: root.go("favorites")

    Button:
        text: "PROFIL"
        font_size: "13sp"
        bold: True
        background_color: 0.10, 0.35, 0.75, 1
        color: 1, 1, 1, 1
        on_release: root.go("profile")
""")


class BottomNav(BoxLayout):

    def go(self, screen_name):

        app = App.get_running_app()

        if not hasattr(app, "sm"):
            return

        if screen_name in (
            "publish",
            "favorites",
            "profile"
        ):

            if not app.api_client.is_logged_in():
                app.sm.current = "login"
                return

        if screen_name in app.sm.screen_names:
            app.sm.current = screen_name