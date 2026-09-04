import os
import requests


# ============================================================
# MAISONPRO - API EN LIGNE
# ============================================================

BASE_URL = "https://maisonpro.onrender.com/api"


class APIClient:

    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url.rstrip("/")
        self.token = None
        self.user = None

    # ========================================================
    # UTILISATEUR CONNECTÉ
    # ========================================================

    @property
    def current_user(self):
        return self.user

    # ========================================================
    # AUTHENTIFICATION
    # ========================================================

    def set_token(self, token):
        self.token = token

    def clear_token(self):
        self.token = None
        self.user = None

    def is_logged_in(self):
        return bool(self.token)

    def _headers(self):
        headers = {
            "Accept": "application/json"
        }

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    # ========================================================
    # CONNEXION
    # ========================================================

    def login(self, email, password):

        try:
            response = requests.post(
                f"{self.base_url}/auth/login",
                json={
                    "email": email,
                    "password": password
                },
                timeout=30
            )

            if response.status_code == 200:

                data = response.json()

                self.token = data.get("token")
                self.user = data.get("user")

                return True, data

            try:
                data = response.json()

                return False, data.get(
                    "error",
                    "E-mail ou mot de passe incorrect."
                )

            except Exception:
                return False, "Erreur de connexion au serveur."

        except requests.RequestException as e:
            return False, f"Impossible de contacter le serveur : {e}"

    # ========================================================
    # INSCRIPTION
    # ========================================================

    def register(
        self,
        first_name,
        last_name,
        phone,
        email,
        password,
        confirm_password
    ):

        try:

            response = requests.post(
                f"{self.base_url}/auth/register",
                json={
                    "first_name": first_name,
                    "last_name": last_name,
                    "phone": phone,
                    "email": email,
                    "password": password,
                    "confirm_password": confirm_password
                },
                timeout=30
            )

            if response.status_code == 201:

                data = response.json()

                self.token = data.get("token")
                self.user = data.get("user")

                return True, data

            try:

                data = response.json()

                return False, data.get(
                    "error",
                    "Erreur lors de l'inscription."
                )

            except Exception:

                return False, "Erreur lors de l'inscription."

        except requests.RequestException as e:

            return False, f"Impossible de contacter le serveur : {e}"

    # ========================================================
    # GET
    # ========================================================

    def get(self, endpoint, params=None):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        return requests.get(
            url,
            params=params,
            headers=self._headers(),
            timeout=30
        )

    # ========================================================
    # POST JSON
    # ========================================================

    def post(self, endpoint, data=None):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        return requests.post(
            url,
            json=data or {},
            headers=self._headers(),
            timeout=30
        )

    # ========================================================
    # POST FORMULAIRE
    # ========================================================

    def post_form(self, endpoint, data=None, files=None):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        return requests.post(
            url,
            data=data or {},
            files=files,
            headers=self._headers(),
            timeout=30
        )

    # ========================================================
    # PUT JSON
    # ========================================================

    def put(self, endpoint, data=None):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        return requests.put(
            url,
            json=data or {},
            headers=self._headers(),
            timeout=30
        )

    # ========================================================
    # PUT FORMULAIRE
    # ========================================================

    def put_form(self, endpoint, data=None, files=None):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        return requests.put(
            url,
            data=data or {},
            files=files,
            headers=self._headers(),
            timeout=30
        )

    # ========================================================
    # DELETE
    # ========================================================

    def delete(self, endpoint):

        url = f"{self.base_url}/{endpoint.lstrip('/')}"

        return requests.delete(
            url,
            headers=self._headers(),
            timeout=30
        )

    # ========================================================
    # ANNONCES RÉCENTES
    # ========================================================

    def get_recent_properties(self, limit=8):

        try:

            response = self.get(
                "/properties/recent",
                params={
                    "limit": limit
                }
            )

            if response.status_code == 200:

                data = response.json()

                if isinstance(data, dict):
                    return True, data.get(
                        "properties",
                        []
                    )

                if isinstance(data, list):
                    return True, data

            return False, []

        except requests.RequestException:
            return False, []

    # ========================================================
    # ANNONCES POPULAIRES
    # ========================================================

    def get_popular_properties(self, limit=8):

        try:

            response = self.get(
                "/properties/popular",
                params={
                    "limit": limit
                }
            )

            if response.status_code == 200:

                data = response.json()

                if isinstance(data, dict):
                    return True, data.get(
                        "properties",
                        []
                    )

                if isinstance(data, list):
                    return True, data

            return False, []

        except requests.RequestException:
            return False, []

    # ========================================================
    # TOUTES LES ANNONCES
    # ========================================================

    def get_properties(self, params=None):

        try:

            response = self.get(
                "/properties",
                params=params
            )

            if response.status_code == 200:

                data = response.json()

                if isinstance(data, dict):
                    return True, data.get(
                        "properties",
                        []
                    )

                if isinstance(data, list):
                    return True, data

            return False, []

        except requests.RequestException:
            return False, []

    # ========================================================
    # RECHERCHE
    # ========================================================

    def search_properties(self, filters=None):

        try:

            filters = filters or {}

            response = self.get(
                "/properties",
                params=filters
            )

            if response.status_code == 200:

                data = response.json()

                if isinstance(data, dict):
                    return True, data.get(
                        "properties",
                        []
                    )

                if isinstance(data, list):
                    return True, data

            return False, []

        except requests.RequestException:
            return False, []

    # ========================================================
    # UNE ANNONCE
    # ========================================================

    def get_property(self, property_id):

        try:

            response = self.get(
                f"/properties/{property_id}"
            )

            if response.status_code == 200:
                return True, response.json()

            return False, None

        except requests.RequestException:
            return False, None

    # ========================================================
    # MON PROFIL
    # ========================================================

    def get_my_profile(self):

        try:

            response = self.get(
                "/users/me"
            )

            if response.status_code == 200:

                data = response.json()

                if isinstance(data, dict):
                    self.user = data.get(
                        "user",
                        data
                    )

                return True, self.user

            return False, None

        except requests.RequestException:
            return False, None

    # ========================================================
    # MODIFIER MON PROFIL
    # ========================================================

    def update_my_profile(
        self,
        data=None,
        files=None
    ):

        try:

            response = self.put_form(
                "/users/me",
                data=data or {},
                files=files
            )

            if response.status_code == 200:

                result = response.json()

                if isinstance(result, dict):
                    self.user = result.get(
                        "user",
                        result
                    )

                return True, result

            try:

                result = response.json()

                return False, result.get(
                    "error",
                    "Impossible de modifier le profil."
                )

            except Exception:

                return False, "Impossible de modifier le profil."

        except requests.RequestException as e:

            return False, str(e)

    # ========================================================
    # CRÉER UNE ANNONCE
    # ========================================================

    def create_property(
        self,
        fields=None,
        photos=None
    ):

        fields = fields or {}
        photos = photos or []

        opened_files = []
        files = []

        try:

            # ------------------------------------------------
            # Préparer les photos
            # ------------------------------------------------

            for photo in photos:

                if not photo:
                    continue

                photo_path = os.path.abspath(photo)

                if not os.path.isfile(photo_path):
                    print(
                        f"Photo introuvable : {photo_path}"
                    )
                    continue

                file_object = open(
                    photo_path,
                    "rb"
                )

                opened_files.append(file_object)

                filename = os.path.basename(
                    photo_path
                )

                extension = os.path.splitext(
                    filename
                )[1].lower()

                if extension == ".png":
                    mime_type = "image/png"

                elif extension == ".webp":
                    mime_type = "image/webp"

                elif extension == ".gif":
                    mime_type = "image/gif"

                else:
                    mime_type = "image/jpeg"

                files.append(
                    (
                        "images",
                        (
                            filename,
                            file_object,
                            mime_type
                        )
                    )
                )

            # ------------------------------------------------
            # Envoyer l'annonce
            # ------------------------------------------------

            response = self.post_form(
                "/properties",
                data=fields,
                files=files
            )

            if response.status_code in (200, 201):

                try:
                    return True, response.json()

                except Exception:
                    return True, {
                        "message": "Annonce publiée avec succès."
                    }

            # ------------------------------------------------
            # Erreur serveur
            # ------------------------------------------------

            try:

                data = response.json()

                return False, data.get(
                    "error",
                    f"Erreur serveur : {response.status_code}"
                )

            except Exception:

                return False, (
                    f"Erreur serveur : {response.status_code}"
                )

        except requests.RequestException as e:

            return False, (
                f"Impossible de contacter le serveur : {e}"
            )

        except Exception as e:

            return False, (
                f"Erreur lors de la publication : {e}"
            )

        finally:

            # ------------------------------------------------
            # Fermer toutes les photos
            # ------------------------------------------------

            for file_object in opened_files:

                try:
                    file_object.close()

                except Exception:
                    pass

    # ========================================================
    # PUBLIER UNE ANNONCE
    # Alias compatible avec d'autres écrans
    # ========================================================

    def publish_property(
        self,
        data=None,
        files=None
    ):

        try:

            response = self.post_form(
                "/properties",
                data=data or {},
                files=files
            )

            if response.status_code in (200, 201):

                return True, response.json()

            try:

                result = response.json()

                return False, result.get(
                    "error",
                    "Impossible de publier l'annonce."
                )

            except Exception:

                return False, (
                    f"Erreur serveur : {response.status_code}"
                )

        except requests.RequestException as e:

            return False, str(e)

    # ========================================================
    # MES ANNONCES
    # ========================================================

    def get_my_properties(self):

        try:

            response = self.get(
                "/properties/mine"
            )

            if response.status_code == 200:

                data = response.json()

                if isinstance(data, dict):
                    return True, data.get(
                        "properties",
                        []
                    )

                if isinstance(data, list):
                    return True, data

            return False, []

        except requests.RequestException:
            return False, []

    # ========================================================
    # MODIFIER UNE ANNONCE
    # ========================================================

    def update_property(
        self,
        property_id,
        data=None,
        files=None
    ):

        try:

            response = self.put_form(
                f"/properties/{property_id}",
                data=data or {},
                files=files
            )

            if response.status_code == 200:

                return True, response.json()

            try:

                result = response.json()

                return False, result.get(
                    "error",
                    "Impossible de modifier l'annonce."
                )

            except Exception:

                return False, (
                    f"Erreur serveur : {response.status_code}"
                )

        except requests.RequestException as e:

            return False, str(e)

    # ========================================================
    # SUPPRIMER UNE ANNONCE
    # ========================================================

    def delete_property(self, property_id):

        try:

            response = self.delete(
                f"/properties/{property_id}"
            )

            if response.status_code in (200, 204):

                return True, response

            try:

                data = response.json()

                return False, data.get(
                    "error",
                    "Impossible de supprimer l'annonce."
                )

            except Exception:

                return False, (
                    f"Erreur serveur : {response.status_code}"
                )

        except requests.RequestException as e:

            return False, str(e)

    # ========================================================
    # FAVORIS
    # ========================================================

    def get_favorites(self):

        try:

            response = self.get(
                "/favorites"
            )

            if response.status_code == 200:

                data = response.json()

                if isinstance(data, dict):
                    return True, data.get(
                        "favorites",
                        []
                    )

                if isinstance(data, list):
                    return True, data

            return False, []

        except requests.RequestException:
            return False, []

    # ========================================================
    # AJOUTER AUX FAVORIS
    # ========================================================

    def add_favorite(self, property_id):

        try:

            response = self.post(
                "/favorites",
                {
                    "property_id": property_id
                }
            )

            if response.status_code in (200, 201):

                return True, response.json()

            try:

                data = response.json()

                return False, data.get(
                    "error",
                    "Impossible d'ajouter aux favoris."
                )

            except Exception:

                return False, "Impossible d'ajouter aux favoris."

        except requests.RequestException as e:

            return False, str(e)

    # ========================================================
    # SUPPRIMER DES FAVORIS
    # ========================================================

    def remove_favorite(self, property_id):

        try:

            response = self.delete(
                f"/favorites/{property_id}"
            )

            if response.status_code in (200, 204):

                return True, response

            try:

                data = response.json()

                return False, data.get(
                    "error",
                    "Impossible de retirer des favoris."
                )

            except Exception:

                return False, "Impossible de retirer des favoris."

        except requests.RequestException as e:

            return False, str(e)

    # ========================================================
    # SIGNALER UNE ANNONCE
    # ========================================================

    def report_property(
        self,
        property_id,
        reason
    ):

        try:

            response = self.post(
                f"/reports/{property_id}",
                {
                    "reason": reason
                }
            )

            if response.status_code in (200, 201):

                return True, response.json()

            try:

                data = response.json()

                return False, data.get(
                    "error",
                    "Impossible de signaler l'annonce."
                )

            except Exception:

                return False, "Impossible de signaler l'annonce."

        except requests.RequestException as e:

            return False, str(e)


# ============================================================
# CLIENT GLOBAL
# ============================================================

api = APIClient()