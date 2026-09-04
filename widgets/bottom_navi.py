from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.app import App

Builder.load_string("""
<BottomNav>:
    size_hint_y: None
    height: dp(56)
    canvas.before:
        Color:
            rgba: 0.95, 0.95, 0.97, 1
        Rectangle:
            pos: self.pos
            size: self.size

    Button:
        text: "Accueil"
        background_color: 0, 0, 0, 0
        color: 0.1, 0.35, 0.75, 1
        on_release: root.go("home")

    Button:
        text: "Recherche"
        background_color: 0, 0, 0, 0
        color: 0.1, 0.35, 0.75, 1
        on_release: root.go("search")

    Button:
        text: "Publier"
        background_color: 0, 0, 0, 0
        color: 0.1, 0.35, 0.75, 1
        on_release: root.go("publish")

    Button:
        text: "Favoris"
        background_color: 0, 0, 0, 0
        color: 0.1, 0.35, 0.75, 1
        on_release: root.go("favorites")

    Button:
        text: "Profil"
        background_color: 0, 0, 0, 0
        color: 0.1, 0.35, 0.75, 1
        on_release: root.go("profile")
""")


class BottomNav(BoxLayout):
    def go(self, screen_name):
        app = App.get_running_app()
        if screen_name in ("publish", "favorites", "profile") and not app.api_client.is_logged_in():
            app.sm.current = "login"
            return
        app.sm.current = screen_name