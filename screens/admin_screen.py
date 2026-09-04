from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.metrics import dp

from config import API_BASE_URL


Builder.load_string("""
<AdminScreen>:

    BoxLayout:
        orientation: "vertical"

        # ==================================================
        # HEADER
        # ==================================================

        BoxLayout:
            size_hint_y: None
            height: dp(58)

            canvas.before:
                Color:
                    rgba: 0.06, 0.22, 0.50, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: "MAISONPRO"
                color: 1, 1, 1, 1
                bold: True
                font_size: "19sp"

            Label:
                text: "ADMIN"
                color: 0.8, 0.9, 1, 1
                bold: True
                font_size: "14sp"

        # ==================================================
        # NAVIGATION ADMIN
        # ==================================================

        BoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(3)
            padding: dp(3)

            Button:
                text: "Tableau"
                on_release: root.show_dashboard()

            Button:
                text: "Utilisateurs"
                on_release: root.show_users()

            Button:
                text: "Annonces"
                on_release: root.show_properties()

            Button:
                text: "Signalements"
                on_release: root.show_reports()

        # ==================================================
        # MESSAGE
        # ==================================================

        Label:
            id: status_label
            text: "Administration MaisonPro"
            color: 0.25, 0.25, 0.25, 1
            size_hint_y: None
            height: dp(38)
            text_size: self.width - dp(10), None
            halign: "center"
            valign: "middle"

        # ==================================================
        # CONTENU
        # ==================================================

        ScrollView:

            GridLayout:
                id: content_grid
                cols: 1
                size_hint_y: None
                height: self.minimum_height
                padding: dp(10)
                spacing: dp(10)

        # ==================================================
        # RETOUR
        # ==================================================

        Button:
            text: "Retour à l'accueil"
            size_hint_y: None
            height: dp(50)
            background_color: 0.1, 0.35, 0.75, 1
            color: 1, 1, 1, 1
            on_release: root.go_home()
""")


class AdminScreen(Screen):

    # ======================================================
    # ENTRÉE DANS L'ÉCRAN
    # ======================================================

    def on_pre_enter(self, *args):

        app = App.get_running_app()

        if not app.api_client.is_logged_in():
            app.sm.current = "login"
            return

        user = app.api_client.current_user or {}

        print("========================================")
        print("         ACCES ADMIN MAISONPRO")
        print("Utilisateur :", user)
        print("is_admin :", user.get("is_admin"))
        print("========================================")

        if not user.get("is_admin", False):
            self.show_access_denied()
            return

        self.show_dashboard()

    # ======================================================
    # LABEL
    # ======================================================

    def create_label(
        self,
        text,
        size=40,
        font_size="16sp",
        bold=False,
        color=(0.1, 0.1, 0.1, 1)
    ):

        label = Label(
            text=str(text),
            font_size=font_size,
            bold=bold,
            color=color,
            size_hint_y=None,
            height=dp(size),
            halign="center",
            valign="middle"
        )

        label.bind(
            width=lambda instance, width:
            setattr(
                instance,
                "text_size",
                (width - dp(10), None)
            )
        )

        return label

    # ======================================================
    # TABLEAU DE BORD
    # ======================================================

    def show_dashboard(self):

        app = App.get_running_app()

        self.ids.content_grid.clear_widgets()

        self.ids.status_label.text = (
            "Tableau de bord administrateur"
        )

        self.ids.content_grid.add_widget(
            self.create_label(
                "Tableau de bord",
                size=45,
                font_size="22sp",
                bold=True,
                color=(0.06, 0.22, 0.50, 1)
            )
        )

        # Utilisateurs
        users_success, users = (
            app.api_client.admin_get_users()
        )

        # Annonces
        properties_success, properties = (
            app.api_client.admin_get_properties()
        )

        # Signalements
        reports_success, reports = (
            app.api_client.admin_get_reports()
        )

        if not users_success:
            users = []

        if not properties_success:
            properties = []

        if not reports_success:
            reports = []

        total_users = len(users)
        total_properties = len(properties)

        active_properties = sum(
            1
            for prop in properties
            if prop.get("is_active", True)
        )

        inactive_properties = (
            total_properties - active_properties
        )

        total_reports = len(reports)

        pending_reports = sum(
            1
            for report in reports
            if report.get("status", "pending") == "pending"
        )

        # ==================================================
        # STATISTIQUES
        # ==================================================

        stats_grid = GridLayout(
            cols=2,
            size_hint_y=None,
            height=dp(250),
            spacing=dp(8)
        )

        stats = [
            ("Utilisateurs", total_users),
            ("Annonces", total_properties),
            ("Annonces actives", active_properties),
            ("Signalements", total_reports),
        ]

        for title, value in stats:

            card = BoxLayout(
                orientation="vertical",
                padding=dp(8),
                spacing=dp(3)
            )

            card.add_widget(
                self.create_label(
                    title,
                    size=35,
                    font_size="14sp",
                    bold=True
                )
            )

            card.add_widget(
                self.create_label(
                    value,
                    size=55,
                    font_size="25sp",
                    bold=True,
                    color=(0.06, 0.22, 0.50, 1)
                )
            )

            stats_grid.add_widget(card)

        self.ids.content_grid.add_widget(
            stats_grid
        )

        # ==================================================
        # RESUME
        # ==================================================

        summary = (
            f"Utilisateurs : {total_users}\n"
            f"Annonces : {total_properties}\n"
            f"Annonces actives : {active_properties}\n"
            f"Annonces masquées : {inactive_properties}\n"
            f"Signalements : {total_reports}\n"
            f"Signalements en attente : {pending_reports}"
        )

        self.ids.content_grid.add_widget(
            self.create_label(
                summary,
                size=150,
                font_size="15sp",
                color=(0.25, 0.25, 0.25, 1)
            )
        )

        # ==================================================
        # ACTIONS RAPIDES
        # ==================================================

        self.ids.content_grid.add_widget(
            self.create_label(
                "Actions rapides",
                size=40,
                font_size="18sp",
                bold=True,
                color=(0.06, 0.22, 0.50, 1)
            )
        )

        buttons = [
            ("Gérer les utilisateurs", self.show_users),
            ("Gérer les annonces", self.show_properties),
            ("Consulter les signalements", self.show_reports)
        ]

        for text, callback in buttons:

            button = Button(
                text=text,
                size_hint_y=None,
                height=dp(52)
            )

            button.bind(
                on_release=lambda instance,
                cb=callback: cb()
            )

            self.ids.content_grid.add_widget(button)

    # ======================================================
    # UTILISATEURS
    # ======================================================

    def show_users(self):

        app = App.get_running_app()

        self.ids.content_grid.clear_widgets()

        self.ids.status_label.text = (
            "Chargement des utilisateurs..."
        )

        print("")
        print("========================================")
        print("      CHARGEMENT DES UTILISATEURS")
        print("========================================")
        print("API :", API_BASE_URL)
        print("Token :", app.api_client.token)
        print("Utilisateur :", app.api_client.current_user)

        success, users = (
            app.api_client.admin_get_users()
        )

        print("Succès :", success)
        print("Résultat :", users)
        print("========================================")

        # ==================================================
        # ERREUR
        # ==================================================

        if not success:

            self.ids.status_label.text = (
                "Erreur de chargement"
            )

            self.ids.content_grid.add_widget(
                self.create_label(
                    "Impossible de charger les utilisateurs.",
                    size=60,
                    font_size="18sp",
                    bold=True,
                    color=(0.8, 0.1, 0.1, 1)
                )
            )

            self.ids.content_grid.add_widget(
                self.create_label(
                    str(users),
                    size=100,
                    font_size="14sp",
                    color=(0.6, 0.1, 0.1, 1)
                )
            )

            return

        # ==================================================
        # SECURITE
        # ==================================================

        if not isinstance(users, list):

            self.ids.status_label.text = (
                "Réponse serveur invalide."
            )

            self.ids.content_grid.add_widget(
                self.create_label(
                    str(users),
                    size=100,
                    font_size="14sp"
                )
            )

            return

        self.ids.status_label.text = (
            f"{len(users)} utilisateur(s)"
        )

        # ==================================================
        # TITRE
        # ==================================================

        self.ids.content_grid.add_widget(
            self.create_label(
                "Gestion des utilisateurs",
                size=50,
                font_size="20sp",
                bold=True,
                color=(0.06, 0.22, 0.50, 1)
            )
        )

        # ==================================================
        # AUCUN UTILISATEUR
        # ==================================================

        if not users:

            self.ids.content_grid.add_widget(
                self.create_label(
                    "Aucun utilisateur trouvé.",
                    size=80,
                    font_size="17sp"
                )
            )

            return

        # ==================================================
        # LISTE DES UTILISATEURS
        # ==================================================

        for user in users:

            user_id = user.get("id")

            first_name = user.get(
                "first_name",
                ""
            )

            last_name = user.get(
                "last_name",
                ""
            )

            email = user.get(
                "email",
                "Non renseigné"
            )

            phone = user.get(
                "phone",
                "Non renseigné"
            )

            roles = user.get(
                "roles",
                []
            )

            is_admin = bool(
                user.get(
                    "is_admin",
                    False
                )
            )

            is_blocked = bool(
                user.get(
                    "is_blocked",
                    False
                )
            )

            if isinstance(roles, list):
                role_text = ", ".join(roles)
            else:
                role_text = str(roles)

            if not role_text:
                role_text = "acheteur"

            if is_admin:
                role_label = "ADMINISTRATEUR"
            else:
                role_label = role_text.upper()

            if is_blocked:
                status_label = "BLOQUÉ"
            else:
                status_label = "ACTIF"

            # ==================================================
            # CARTE UTILISATEUR
            # ==================================================

            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(205),
                padding=dp(10),
                spacing=dp(5)
            )

            # --------------------------------------------------
            # INFORMATIONS
            # --------------------------------------------------

            info = (
                f"ID : {user_id}\n"
                f"Nom : {first_name} {last_name}\n"
                f"Email : {email}\n"
                f"Téléphone : {phone}\n"
                f"Rôle : {role_label}\n"
                f"Statut : {status_label}"
            )

            card.add_widget(
                self.create_label(
                    info,
                    size=135,
                    font_size="13sp",
                    bold=False
                )
            )

            # ==================================================
            # ADMIN
            # ==================================================

            if is_admin:

                admin_label = self.create_label(
                    "Compte administrateur protégé",
                    size=45,
                    font_size="12sp",
                    bold=True,
                    color=(0.06, 0.22, 0.50, 1)
                )

                card.add_widget(admin_label)

            # ==================================================
            # UTILISATEUR NORMAL
            # ==================================================

            else:

                button = Button(
                    text=(
                        "Débloquer l'utilisateur"
                        if is_blocked
                        else "Bloquer l'utilisateur"
                    ),
                    size_hint_y=None,
                    height=dp(45)
                )

                button.bind(
                    on_release=lambda instance,
                    uid=user_id,
                    blocked=is_blocked:
                    self.toggle_user(
                        uid,
                        not blocked
                    )
                )

                card.add_widget(button)

            self.ids.content_grid.add_widget(card)

    # ======================================================
    # BLOQUER / DEBLOQUER
    # ======================================================

    def toggle_user(
        self,
        user_id,
        block
    ):

        app = App.get_running_app()

        if not user_id:
            self.show_message(
                "ID utilisateur invalide."
            )
            return

        if block:

            action = "bloquer"

            success, result = (
                app.api_client.admin_block_user(
                    user_id
                )
            )

        else:

            action = "débloquer"

            success, result = (
                app.api_client.admin_unblock_user(
                    user_id
                )
            )

        print(
            f"Action {action} utilisateur {user_id}"
        )

        print(
            "Succès :",
            success
        )

        print(
            "Résultat :",
            result
        )

        if success:

            self.ids.status_label.text = (
                str(result)
            )

            self.show_users()

        else:

            self.ids.status_label.text = (
                "Échec : " + str(result)
            )

            self.show_message(
                str(result)
            )

    # ======================================================
    # ANNONCES
    # ======================================================

    def show_properties(self):

        app = App.get_running_app()

        self.ids.content_grid.clear_widgets()

        self.ids.status_label.text = (
            "Chargement des annonces..."
        )

        success, properties = (
            app.api_client.admin_get_properties()
        )

        if not success:

            self.ids.status_label.text = (
                "Erreur : " + str(properties)
            )

            return

        self.ids.status_label.text = (
            f"{len(properties)} annonce(s)"
        )

        self.ids.content_grid.add_widget(
            self.create_label(
                "Gestion des annonces",
                size=50,
                font_size="20sp",
                bold=True,
                color=(0.06, 0.22, 0.50, 1)
            )
        )

        if not properties:

            self.ids.content_grid.add_widget(
                self.create_label(
                    "Aucune annonce.",
                    size=60
                )
            )

            return

        for prop in properties:

            property_id = prop.get("id")

            title = prop.get(
                "title",
                "Sans titre"
            )

            price = prop.get(
                "price",
                0
            )

            city = prop.get(
                "city",
                ""
            )

            owner_name = prop.get(
                "owner_name",
                ""
            )

            is_active = prop.get(
                "is_active",
                True
            )

            status = (
                "ACTIVE"
                if is_active
                else "MASQUÉE"
            )

            try:

                price_text = (
                    f"{int(float(price)):,} FCFA"
                    .replace(",", " ")
                )

            except (
                TypeError,
                ValueError
            ):

                price_text = (
                    f"{price} FCFA"
                )

            card = BoxLayout(
                orientation="vertical",
                size_hint_y=None,
                height=dp(175),
                padding=dp(8),
                spacing=dp(4)
            )

            info = (
                f"{title}\n"
                f"{price_text}\n"
                f"{city}\n"
                f"Propriétaire : {owner_name}\n"
                f"Statut : {status}"
            )

            card.add_widget(
                self.create_label(
                    info,
                    size=110,
                    font_size="14sp"
                )
            )

            buttons = BoxLayout(
                size_hint_y=None,
                height=dp(42),
                spacing=dp(5)
            )

            edit_button = Button(
                text="Modifier"
            )

            edit_button.bind(
                on_release=lambda instance,
                p=prop:
                self.open_edit_property(p)
            )

            status_button = Button(
                text=(
                    "Masquer"
                    if is_active
                    else "Afficher"
                )
            )

            status_button.bind(
                on_release=lambda instance,
                pid=property_id,
                active=is_active:
                self.change_property_status(
                    pid,
                    not active
                )
            )

            delete_button = Button(
                text="Supprimer"
            )

            delete_button.bind(
                on_release=lambda instance,
                pid=property_id:
                self.confirm_delete_property(
                    pid
                )
            )

            buttons.add_widget(edit_button)
            buttons.add_widget(status_button)
            buttons.add_widget(delete_button)

            card.add_widget(buttons)

            self.ids.content_grid.add_widget(card)

    # ======================================================
    # STATUT ANNONCE
    # ======================================================

    def change_property_status(
        self,
        property_id,
        is_active
    ):

        app = App.get_running_app()

        success, result = (
            app.api_client.admin_update_property(
                property_id,
                is_active=is_active
            )
        )

        if success:

            self.ids.status_label.text = (
                "Annonce mise à jour."
            )

            self.show_properties()

        else:

            self.ids.status_label.text = (
                str(result)
            )

    # ======================================================
    # MODIFIER ANNONCE
    # ======================================================

    def open_edit_property(
        self,
        prop
    ):

        box = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(8)
        )

        title_input = TextInput(
            text=str(
                prop.get(
                    "title",
                    ""
                )
            ),
            hint_text="Titre",
            multiline=False
        )

        price_input = TextInput(
            text=str(
                prop.get(
                    "price",
                    ""
                )
            ),
            hint_text="Prix",
            multiline=False,
            input_type="number"
        )

        box.add_widget(title_input)
        box.add_widget(price_input)

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(5)
        )

        popup = Popup(
            title="Modifier l'annonce",
            content=box,
            size_hint=(0.9, 0.5)
        )

        cancel_button = Button(
            text="Annuler"
        )

        cancel_button.bind(
            on_release=lambda instance:
            popup.dismiss()
        )

        save_button = Button(
            text="Enregistrer"
        )

        def save(instance):

            title = title_input.text.strip()

            price_text = (
                price_input.text.strip()
            )

            if not title:

                self.show_message(
                    "Le titre est obligatoire."
                )

                return

            try:

                price = float(
                    price_text
                )

            except ValueError:

                self.show_message(
                    "Le prix doit être un nombre."
                )

                return

            app = App.get_running_app()

            success, result = (
                app.api_client.admin_update_property(
                    prop.get("id"),
                    title=title,
                    price=price
                )
            )

            if success:

                popup.dismiss()

                self.ids.status_label.text = (
                    "Annonce modifiée avec succès."
                )

                self.show_properties()

            else:

                self.show_message(
                    str(result)
                )

        save_button.bind(
            on_release=save
        )

        buttons.add_widget(
            cancel_button
        )

        buttons.add_widget(
            save_button
        )

        box.add_widget(buttons)

        popup.open()

    # ======================================================
    # SUPPRIMER ANNONCE
    # ======================================================

    def confirm_delete_property(
        self,
        property_id
    ):

        box = BoxLayout(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(10)
        )

        box.add_widget(
            self.create_label(
                "Voulez-vous vraiment supprimer cette annonce ?",
                size=70,
                font_size="15sp"
            )
        )

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(5)
        )

        popup = Popup(
            title="Confirmation",
            content=box,
            size_hint=(0.85, 0.35)
        )

        cancel_button = Button(
            text="Annuler"
        )

        cancel_button.bind(
            on_release=lambda instance:
            popup.dismiss()
        )

        delete_button = Button(
            text="Supprimer"
        )

        def delete(instance):

            app = App.get_running_app()

            success, message = (
                app.api_client.admin_delete_property(
                    property_id
                )
            )

            popup.dismiss()

            self.ids.status_label.text = (
                str(message)
            )

            if success:
                self.show_properties()

        delete_button.bind(
            on_release=delete
        )

        buttons.add_widget(
            cancel_button
        )

        buttons.add_widget(
            delete_button
        )

        box.add_widget(buttons)

        popup.open()

    # ======================================================
    # SIGNALEMENTS
    # ======================================================

    def show_reports(self):

        app = App.get_running_app()

        self.ids.content_grid.clear_widgets()

        self.ids.status_label.text = (
            "Chargement des signalements..."
        )

        success, reports = (
            app.api_client.admin_get_reports()
        )

        if not success:

            self.ids.status_label.text = (
                "Erreur : " + str(reports)
            )

            return

        self.ids.status_label.text = (
            f"{len(reports)} signalement(s)"
        )

        self.ids.content_grid.add_widget(
            self.create_label(
                "Signalements",
                size=50,
                font_size="20sp",
                bold=True,
                color=(0.06, 0.22, 0.50, 1)
            )
        )

        if not reports:

            self.ids.content_grid.add_widget(
                self.create_label(
                    "Aucun signalement.",
                    size=70,
                    color=(0.1, 0.55, 0.25, 1)
                )
            )

            return

        for report in reports:

            property_id = report.get(
                "property_id"
            )

            property_title = report.get(
                "property_title",
                "Annonce inconnue"
            )

            reporter_email = report.get(
                "reporter_email",
                "Utilisateur inconnu"
            )

            reason = report.get(
                "reason",
                ""
            )

            status = report.get(
                "status",
                "pending"
            )

            text = (
                f"Annonce : {property_title}\n"
                f"ID annonce : {property_id}\n"
                f"Signalé par : {reporter_email}\n"
                f"Motif : {reason}\n"
                f"Statut : {status}"
            )

            self.ids.content_grid.add_widget(
                self.create_label(
                    text,
                    size=140,
                    font_size="14sp"
                )
            )

    # ======================================================
    # ACCÈS REFUSÉ
    # ======================================================

    def show_access_denied(self):

        self.ids.content_grid.clear_widgets()

        self.ids.status_label.text = (
            "Accès refusé."
        )

        self.ids.content_grid.add_widget(
            self.create_label(
                "Accès réservé à l'administrateur.",
                size=100,
                font_size="18sp",
                bold=True,
                color=(0.8, 0.1, 0.1, 1)
            )
        )

    # ======================================================
    # MESSAGE POPUP
    # ======================================================

    def show_message(
        self,
        message
    ):

        content = BoxLayout(
            orientation="vertical",
            padding=dp(10),
            spacing=dp(10)
        )

        content.add_widget(
            self.create_label(
                str(message),
                size=90,
                font_size="14sp"
            )
        )

        close_button = Button(
            text="Fermer",
            size_hint_y=None,
            height=dp(45)
        )

        content.add_widget(close_button)

        popup = Popup(
            title="MAISONPRO",
            content=content,
            size_hint=(0.85, 0.4)
        )

        close_button.bind(
            on_release=lambda instance:
            popup.dismiss()
        )

        popup.open()

    # ======================================================
    # RETOUR ACCUEIL
    # ======================================================

    def go_home(self):

        app = App.get_running_app()

        app.sm.current = "home"