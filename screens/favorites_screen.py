from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App

from widgets.property_card import PropertyCard
from widgets.bottom_nav import BottomNav  # noqa: F401


Builder.load_string("""
<FavoritesScreen>:
    BoxLayout:
        orientation: "vertical"

        Label:
            text: "Mes favoris"
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

        Label:
            id: empty_label
            text: ""
            color: 0.4, 0.4, 0.4, 1
            size_hint_y: None
            height: dp(30)

        ScrollView:
            GridLayout:
                id: favorites_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: dp(12)
                spacing: dp(10)

        BottomNav:
""")


class FavoritesScreen(Screen):

    def on_pre_enter(self, *args):
        app = App.get_running_app()

        if not app.api_client.is_logged_in():
            app.sm.current = "login"
            return

        self.load_favorites()

    def load_favorites(self):
        app = App.get_running_app()

        success, favorites = app.api_client.get_favorites()

        grid = self.ids.favorites_grid
        grid.clear_widgets()

        if not success:
            self.ids.empty_label.text = (
                "Impossible de charger les favoris."
            )
            return

        if not favorites:
            self.ids.empty_label.text = (
                "Vous n'avez aucun favori pour le moment."
            )
            return

        self.ids.empty_label.text = ""

        for prop in favorites:
            card = PropertyCard()
            card.set_data(prop)
            card.on_select = self.open_property
            grid.add_widget(card)

    def open_property(self, property_id):
        app = App.get_running_app()

        detail_screen = app.sm.get_screen("property_detail")
        detail_screen.property_id = property_id

        app.sm.current = "property_detail"