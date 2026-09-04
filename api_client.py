import os
import requests


class APIClient:

    def __init__(self, base_url=None):

        self.base_url = (
            base_url
            or os.environ.get(
                "API_BASE_URL",
                "http://127.0.0.1:5000/api"
            )
        ).rstrip("/")

        self.token = None
        self.current_user = None

    # =========================================================
    # UTILITAIRES
    # =========================================================

    def is_logged_in(self):
        return bool(self.token)

    def _headers(self):
        headers = {}

        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        return headers

    def request(
        self,
        method,
        endpoint,
        json=None,
        data=None,
        files=None,
        params=None
    ):
        """
        Effectue une requête vers l'API.

        Retourne toujours :
            (success, result)
        """

        url = f"{self.base_url}{endpoint}"

        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self._headers(),
                json=json,
                data=data,
                files=files,
                params=params,
                timeout=15
            )

            try:
                result = response.json()
            except ValueError:
                result = {
                    "message": response.text
                }

            if 200 <= response.status_code < 300:
                return True, result

            print(
                f"Erreur API {response.status_code} :",
                result
            )

            return False, result

        except requests.exceptions.ConnectionError:
            return False, {
                "error": "Impossible de contacter le serveur."
            }

        except requests.exceptions.Timeout:
            return False, {
                "error": "Le serveur met trop de temps à répondre."
            }

        except Exception as e:
            print("Erreur APIClient :", e)

            return False, {
                "error": str(e)
            }

    # =========================================================
    # AUTHENTIFICATION
    # =========================================================

    def register(
        self,
        first_name,
        last_name,
        phone,
        email,
        password
    ):
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "password": password
        }

        success, result = self.request(
            "POST",
            "/auth/register",
            json=data
        )

        if success and isinstance(result, dict):

            token = result.get("token")

            if token:
                self.token = token

            user = result.get("user")

            if user:
                self.current_user = user

        return success, result

    def login(self, email, password):

        data = {
            "email": email,
            "password": password
        }

        success, result = self.request(
            "POST",
            "/auth/login",
            json=data
        )

        if success and isinstance(result, dict):

            self.token = result.get("token")

            self.current_user = result.get("user")

        return success, result

    def logout(self):

        self.token = None
        self.current_user = None

    # =========================================================
    # PROFIL
    # =========================================================

    def get_profile(self):

        success, result = self.request(
            "GET",
            "/users/me"
        )

        if success and isinstance(result, dict):
            self.current_user = result

        return success, result

    def get_me(self):

        return self.get_profile()

    def update_profile(self, data):

        success, result = self.request(
            "PUT",
            "/users/me",
            data=data
        )

        if success and isinstance(result, dict):

            if "user" in result:
                self.current_user = result["user"]

            else:
                self.current_user = result

        return success, result

    def get_public_profile(self, user_id):

        return self.request(
            "GET",
            f"/users/{user_id}"
        )

    # =========================================================
    # ANNONCES - LISTE
    # =========================================================

    def get_properties(self, params=None):

        return self.request(
            "GET",
            "/properties",
            params=params
        )

    def get_recent_properties(self, limit=8):

        return self.request(
            "GET",
            "/properties/recent",
            params={
                "limit": limit
            }
        )

    def get_popular_properties(self, limit=8):

        return self.request(
            "GET",
            "/properties/popular",
            params={
                "limit": limit
            }
        )

    def get_property(self, property_id):

        return self.request(
            "GET",
            f"/properties/{property_id}"
        )

    # =========================================================
    # MES ANNONCES
    # =========================================================

    def get_my_properties(self):

        return self.request(
            "GET",
            "/properties/mine"
        )

    # =========================================================
    # PUBLIER UNE ANNONCE
    # =========================================================

    def publish_property(
        self,
        property_type,
        transaction_type,
        title,
        description,
        price,
        city,
        commune,
        quartier,
        bedrooms=None,
        bathrooms=None,
        area=None,
        contact_phone="",
        photos=None
    ):

        data = {
            "property_type": property_type,
            "transaction_type": transaction_type,
            "title": title,
            "description": description,
            "price": price,
            "city": city,
            "commune": commune,
            "quartier": quartier,
            "contact_phone": contact_phone
        }

        if bedrooms is not None:
            data["bedrooms"] = bedrooms

        if bathrooms is not None:
            data["bathrooms"] = bathrooms

        if area is not None:
            data["area"] = area

        files = []

        if photos:

            for photo_path in photos:

                if not photo_path:
                    continue

                if not os.path.exists(photo_path):
                    print(
                        "Photo introuvable :",
                        photo_path
                    )
                    continue

                try:

                    file_object = open(
                        photo_path,
                        "rb"
                    )

                    files.append(
                        (
                            "photos",
                            (
                                os.path.basename(photo_path),
                                file_object,
                                "image/jpeg"
                            )
                        )
                    )

                except Exception as e:

                    print(
                        "Erreur ouverture photo :",
                        e
                    )

        try:

            success, result = self.request(
                "POST",
                "/properties",
                data=data,
                files=files
            )

            return success, result

        finally:

            for _, (_, file_object, _) in files:

                try:
                    file_object.close()
                except Exception:
                    pass

    # =========================================================
    # MODIFIER UNE ANNONCE
    # =========================================================

    def update_property(
        self,
        property_id,
        data
    ):

        return self.request(
            "PUT",
            f"/properties/{property_id}",
            json=data
        )

    # =========================================================
    # SUPPRIMER UNE ANNONCE
    # =========================================================

    def delete_property(self, property_id):

        return self.request(
            "DELETE",
            f"/properties/{property_id}"
        )

    # =========================================================
    # FAVORIS
    # =========================================================

    def get_my_favorites(self):

        return self.request(
            "GET",
            "/favorites/mine"
        )

    def get_favorites(self):

        return self.get_my_favorites()

    def add_favorite(self, property_id):

        return self.request(
            "POST",
            f"/favorites/{property_id}"
        )

    def remove_favorite(self, property_id):

        return self.request(
            "DELETE",
            f"/favorites/{property_id}"
        )

    # =========================================================
    # SIGNALEMENT
    # =========================================================

    def report_property(
        self,
        property_id,
        reason
    ):

        data = {
            "reason": reason
        }

        return self.request(
            "POST",
            f"/reports/{property_id}",
            json=data
        )

    # =========================================================
    # ADMINISTRATION - UTILISATEURS
    # =========================================================

    def get_admin_users(self):

        return self.request(
            "GET",
            "/admin/users"
        )

    def block_user(self, user_id):

        return self.request(
            "POST",
            f"/admin/users/{user_id}/block"
        )

    def unblock_user(self, user_id):

        return self.request(
            "POST",
            f"/admin/users/{user_id}/unblock"
        )

    # =========================================================
    # ADMINISTRATION - ANNONCES
    # =========================================================

    def get_admin_properties(self):

        return self.request(
            "GET",
            "/admin/properties"
        )

    def admin_update_property(
        self,
        property_id,
        data
    ):

        return self.request(
            "PUT",
            f"/admin/properties/{property_id}",
            json=data
        )

    def admin_delete_property(
        self,
        property_id
    ):

        return self.request(
            "DELETE",
            f"/admin/properties/{property_id}"
        )

    # =========================================================
    # ADMINISTRATION - SIGNALEMENTS
    # =========================================================

    def get_admin_reports(self):

        return self.request(
            "GET",
            "/admin/reports"
        )