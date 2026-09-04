from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock
from kivy.metrics import dp

from widgets.property_card import PropertyCard
from widgets.bottom_nav import BottomNav  # noqa: F401 (nécessaire pour enregistrer le widget KV)

Builder.load_string("""
<HomeScreen>:
    BoxLayout:
        orientation: "vertical"

        BoxLayout:
            orientation: "vertical"
            size_hint_y: None
            height: dp(120)
            padding: dp(16), dp(10)
            spacing: dp(8)
            canvas.before:
                Color:
                    rgba: 0.1, 0.35, 0.75, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: "MAISONPRO"
                font_size: "24sp"
                bold: True
                color: 1, 1, 1, 1
                size_hint_y: None
                height: dp(34)

            BoxLayout:
                size_hint_y: None
                height: dp(44)
                spacing: dp(6)

                TextInput:
                    id: search_input
                    hint_text: "Ville, commune, quartier..."
                    multiline: False
                    padding: [dp(10), dp(12)]

                Button:
                    text: "Rechercher"
                    size_hint_x: None
                    width: dp(110)
                    background_color: 0.95, 0.65, 0.1, 1
                    on_release: root.do_quick_search()

        ScrollView:
            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                padding: dp(12)
                spacing: dp(14)

                Button:
                    text: "+ Publier une annonce"
                    size_hint_y: None
                    height: dp(46)
                    background_color: 0.1, 0.6, 0.3, 1
                    on_release: root.go_to_publish()

                Label:
                    text: "Catégories"
                    bold: True
                    color: 0.1, 0.1, 0.1, 1
                    size_hint_y: None
                    height: dp(26)
                    text_size: self.width, None
                    halign: "left"

                GridLayout:
                    id: categories_grid
                    cols: 3
                    size_hint_y: None
                    height: dp(90)
                    spacing: dp(6)

                Label:
                    text: "Annonces récentes"
                    bold: True
                    color: 0.1, 0.1, 0.1, 1
                    size_hint_y: None
                    height: dp(26)
                    text_size: self.width, None
                    halign: "left"

                GridLayout:
                    id: recent_grid
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(10)

                Label:
                    text: "Biens populaires"
                    bold: True
                    color: 0.1, 0.1, 0.1, 1
                    size_hint_y: None
                    height: dp(26)
                    text_size: self.width, None
                    halign: "left"

                GridLayout:
                    id: popular_grid
                    cols: 1
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(10)

        BottomNav:
""")

CATEGORIES = ["maison", "appartement", "studio", "villa", "terrain", "bureau"]


class HomeScreen(Screen):
    _categories_built = False

    def on_pre_enter(self, *args):
        if not self._categories_built:
            self._build_categories()
            self._categories_built = True
        Clock.schedule_once(lambda dt: self.load_listings(), 0)

    def _build_categories(self):
        grid = self.ids.categories_grid
        grid.clear_widgets()
        from kivy.uix.button import Button

        for category in CATEGORIES:
            btn = Button(text=category.capitalize(), background_color=(0.9, 0.93, 0.98, 1), color=(0.1, 0.1, 0.1, 1))
            btn.bind(on_release=lambda instance, c=category: self.go_to_category(c))
            grid.add_widget(btn)

    def go_to_category(self, category):
        app = App.get_running_app()
        search_screen = app.sm.get_screen("search")
        search_screen.preset_filters({"property_type": category})
        app.sm.current = "search"

    def do_quick_search(self):
        app = App.get_running_app()
        query = self.ids.search_input.text.strip()
        search_screen = app.sm.get_screen("search")
        search_screen.preset_filters({"city": query})
        app.sm.current = "search"

    def go_to_publish(self):
        app = App.get_running_app()
        if not app.api_client.is_logged_in():
            app.sm.current = "login"
            return
        app.sm.current = "publish"

    def load_listings(self):
        app = App.get_running_app()

        success, recent = app.api_client.get_recent_properties(limit=8)
        self._fill_grid(self.ids.recent_grid, recent if success else [])

        success, popular = app.api_client.get_popular_properties(limit=8)
        self._fill_grid(self.ids.popular_grid, popular if success else [])

    def _fill_grid(self, grid, properties):
        grid.clear_widgets()
        for prop in properties:
            card = PropertyCard()
            card.set_data(prop)
            card.on_select = self.open_property
            grid.add_widget(card)

    def open_property(self, property_id):
        app = App.get_running_app()
        detail_screen = app.sm.get_screen("property_detail")
        detail_screen.property_id = property_id
        app.sm.current = "property_detail"