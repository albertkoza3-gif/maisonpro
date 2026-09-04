from kivy.lang import Builder
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.app import App
from kivy.clock import Clock

from widgets.property_card import PropertyCard
from widgets.bottom_nav import BottomNav  # noqa: F401


Builder.load_string("""
<SearchScreen>:
    BoxLayout:
        orientation: "vertical"

        # =====================================================
        # EN-TÊTE
        # =====================================================

        Label:
            text: "Recherche de biens"
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


        # =====================================================
        # FILTRES
        # =====================================================

        ScrollView:
            size_hint_y: None
            height: dp(270)

            BoxLayout:
                orientation: "vertical"
                padding: dp(12)
                spacing: dp(8)
                size_hint_y: None
                height: self.minimum_height


                # Ville + Commune
                BoxLayout:
                    size_hint_y: None
                    height: dp(44)
                    spacing: dp(6)

                    TextInput:
                        id: city_input
                        hint_text: "Ville"
                        multiline: False

                    TextInput:
                        id: commune_input
                        hint_text: "Commune"
                        multiline: False


                # Quartier
                TextInput:
                    id: quartier_input
                    hint_text: "Quartier"
                    multiline: False
                    size_hint_y: None
                    height: dp(44)


                # Prix minimum + maximum
                BoxLayout:
                    size_hint_y: None
                    height: dp(44)
                    spacing: dp(6)

                    TextInput:
                        id: price_min_input
                        hint_text: "Prix minimum"
                        multiline: False
                        input_type: "number"

                    TextInput:
                        id: price_max_input
                        hint_text: "Prix maximum"
                        multiline: False
                        input_type: "number"


                # Vente / Location + Type
                BoxLayout:
                    size_hint_y: None
                    height: dp(44)
                    spacing: dp(6)

                    Spinner:
                        id: transaction_spinner
                        text: "Vente ou location"
                        values:
                            [
                            "Vente ou location",
                            "vente",
                            "location"
                            ]

                    Spinner:
                        id: type_spinner
                        text: "Type de bien"
                        values:
                            [
                            "Type de bien",
                            "maison",
                            "appartement",
                            "studio",
                            "villa",
                            "terrain",
                            "magasin",
                            "bureau",
                            "chambre",
                            "autre"
                            ]


                # Nombre de chambres
                Spinner:
                    id: bedrooms_spinner
                    text: "Chambres (min)"
                    values:
                        [
                        "Chambres (min)",
                        "1",
                        "2",
                        "3",
                        "4",
                        "5"
                        ]

                    size_hint_y: None
                    height: dp(44)


                # Bouton rechercher
                Button:
                    text: "Rechercher"
                    size_hint_y: None
                    height: dp(46)

                    background_color:
                        0.95, 0.65, 0.1, 1

                    color:
                        1, 1, 1, 1

                    bold: True

                    on_release:
                        root.do_search()


        # =====================================================
        # NOMBRE DE RÉSULTATS
        # =====================================================

        Label:
            id: results_label

            text:
                "Faites une recherche pour voir les résultats."

            color:
                0.3, 0.3, 0.3, 1

            size_hint_y: None
            height: dp(30)

            font_size:
                "12sp"


        # =====================================================
        # RÉSULTATS
        # =====================================================

        ScrollView:

            GridLayout:
                id: results_grid

                cols: 1

                size_hint_y: None
                height: self.minimum_height

                padding:
                    dp(12)

                spacing:
                    dp(10)


        # =====================================================
        # NAVIGATION
        # =====================================================

        BottomNav:
""")


class SearchScreen(Screen):

    # =========================================================
    # PRÉ-REMPLIR LES FILTRES
    # =========================================================

    def preset_filters(self, filters):
        """
        Pré-remplit les filtres depuis l'écran d'accueil.

        Exemple :
            {"city": "Abidjan"}

        ou :
            {"property_type": "villa"}
        """

        if "city" in filters:
            self.ids.city_input.text = str(filters["city"])

        if "commune" in filters:
            self.ids.commune_input.text = str(filters["commune"])

        if "quartier" in filters:
            self.ids.quartier_input.text = str(filters["quartier"])

        if "property_type" in filters:
            self.ids.type_spinner.text = str(filters["property_type"])

        if "transaction_type" in filters:
            self.ids.transaction_spinner.text = str(
                filters["transaction_type"]
            )

        if "bedrooms" in filters:
            self.ids.bedrooms_spinner.text = str(
                filters["bedrooms"]
            )

        if "price_min" in filters:
            self.ids.price_min_input.text = str(
                filters["price_min"]
            )

        if "price_max" in filters:
            self.ids.price_max_input.text = str(
                filters["price_max"]
            )

        # Lancer automatiquement la recherche
        Clock.schedule_once(
            lambda dt: self.do_search(),
            0
        )


    # =========================================================
    # RÉCUPÉRER LES FILTRES
    # =========================================================

    def _collect_filters(self):

        transaction = self.ids.transaction_spinner.text
        property_type = self.ids.type_spinner.text
        bedrooms = self.ids.bedrooms_spinner.text

        return {
            "city": self.ids.city_input.text.strip(),

            "commune":
                self.ids.commune_input.text.strip(),

            "quartier":
                self.ids.quartier_input.text.strip(),

            "price_min":
                self.ids.price_min_input.text.strip()
                or None,

            "price_max":
                self.ids.price_max_input.text.strip()
                or None,

            "transaction_type":
                transaction
                if transaction != "Vente ou location"
                else None,

            "property_type":
                property_type
                if property_type != "Type de bien"
                else None,

            "bedrooms":
                bedrooms
                if bedrooms != "Chambres (min)"
                else None,
        }


    # =========================================================
    # EFFECTUER LA RECHERCHE
    # =========================================================

    def do_search(self):

        app = App.get_running_app()

        filters = self._collect_filters()

        # Appel API
        success, results = (
            app.api_client.search_properties(filters)
        )

        grid = self.ids.results_grid

        # Nettoyer les anciens résultats
        grid.clear_widgets()


        # =====================================================
        # ERREUR SERVEUR
        # =====================================================

        if not success:

            self.ids.results_label.text = (
                "Impossible de contacter le serveur."
            )

            return


        # =====================================================
        # AUCUN RÉSULTAT
        # =====================================================

        if not results:

            self.ids.results_label.text = (
                "Aucun bien trouvé."
            )

            return


        # =====================================================
        # AFFICHER LE NOMBRE DE RÉSULTATS
        # =====================================================

        self.ids.results_label.text = (
            f"{len(results)} résultat(s) trouvé(s)."
        )


        # =====================================================
        # AFFICHER LES CARTES
        # =====================================================

        for prop in results:

            card = PropertyCard()

            card.set_data(prop)

            card.on_select = self.open_property

            grid.add_widget(card)


    # =========================================================
    # OUVRIR UN BIEN
    # =========================================================

    def open_property(self, property_id):

        app = App.get_running_app()

        detail_screen = app.sm.get_screen(
            "property_detail"
        )

        detail_screen.property_id = property_id

        app.sm.current = "property_detail"

