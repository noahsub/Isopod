from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Vertical, Center
from textual.widgets import Footer, OptionList, Static

from Managers.navigation_manager import NavigationManager


class HomePage(Screen):
    CSS_PATH = 'Styles/home_page.tcss'

    def compose(self) -> ComposeResult:
        yield Vertical(
            Static('Isopod'),
            OptionList(
                'Containers',
                'Images',
                'Networks',
                'Pods',
                'Volumes',
                'Exit'
            )
        )

    def on_option_list_option_selected(self, event: OptionList.OptionSelected):
        nav_manager = NavigationManager()
        selected = event.option.prompt
        match selected:
            case 'Containers':
                nav_manager.navigate('container_page')
            case 'Images':
                nav_manager.navigate('image_page')
            case 'Networks':
                nav_manager.navigate('network_page')
            case 'Pods':
                nav_manager.navigate('pod_page')
            case 'Volumes':
                nav_manager.navigate('volume_page')
            case 'Exit':
                exit(0)