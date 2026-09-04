from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window

from api_client import APIClient

from screens.login_screen import LoginScreen
from screens.register_screen import RegisterScreen
from screens.home_screen import HomeScreen
from screens.search_screen import SearchScreen
from screens.property_detail_screen import PropertyDetailScreen
from screens.publish_screen import PublishScreen
from screens.profile_screen import ProfileScreen
from screens.edit_profile_screen import EditProfileScreen
from screens.favorites_screen import FavoritesScreen
from screens.admin_screen import AdminScreen
from screens.my_properties_screen import MyPropertiesScreen
from screens.edit_property_screen import EditPropertyScreen


Window.size = (380, 700)


class MaisonProApp(App):

    title = "MAISONPRO"

    def build(self):

        self.api_client = APIClient()

        self.sm = ScreenManager(
            transition=FadeTransition()
        )

        self.sm.add_widget(
            LoginScreen(name="login")
        )

        self.sm.add_widget(
            RegisterScreen(name="register")
        )

        self.sm.add_widget(
            HomeScreen(name="home")
        )

        self.sm.add_widget(
            SearchScreen(name="search")
        )

        self.sm.add_widget(
            PropertyDetailScreen(name="property_detail")
        )

        self.sm.add_widget(
            PublishScreen(name="publish")
        )

        self.sm.add_widget(
            ProfileScreen(name="profile")
        )

        self.sm.add_widget(
            EditProfileScreen(name="edit_profile")
        )

        self.sm.add_widget(
            FavoritesScreen(name="favorites")
        )

        self.sm.add_widget(
            AdminScreen(name="admin")
        )

        self.sm.add_widget(
            MyPropertiesScreen(name="my_properties")
        )

        self.sm.add_widget(
            EditPropertyScreen(name="edit_property")
        )

        self.sm.current = "home"

        return self.sm

    def on_login_success(self):

        self.sm.current = "home"

        home_screen = self.sm.get_screen("home")

        home_screen.load_listings()


if __name__ == "__main__":
    MaisonProApp().run()