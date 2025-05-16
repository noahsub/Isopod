from textual.app import App

from Managers.navigation_manager import NavigationManager
from Pages.container_page import ContainerPage
from Pages.home_page import HomePage
from Pages.image_page import ImagePage
from Pages.log_page import LogPage
from Pages.network_page import NetworkPage
from Pages.pod_page import PodPage
from Pages.volume_page import VolumePage
from Themes.themes import LAVENDER


class IsopodApp(App):
    # CSS = f'$primary: {LAVENDER.primary}'

    def on_mount(self):
        self.register_theme(LAVENDER)
        self.theme = 'lavender'
        self.CSS = f'$primary: {LAVENDER.primary}'

        self.title = 'Isopod'
        nav_manager = NavigationManager(self)
        nav_manager.install(HomePage(), 'home_page', 'Home')
        nav_manager.install(ImagePage(), 'image_page', 'Image Manager')
        nav_manager.install(LogPage(), 'log_page', 'Logs')
        nav_manager.install(NetworkPage(), 'network_page', 'Network Manager')
        nav_manager.install(PodPage(), 'pod_page', 'Pod Manager')
        nav_manager.install(VolumePage(), 'volume_page', 'Volume Manager')
        nav_manager.install(ContainerPage(), 'container_page', 'Container Manager')
        nav_manager.navigate('home_page')


if __name__ == '__main__':
    app = IsopodApp()
    app.run()