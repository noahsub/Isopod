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
        selected = event.option.prompt
        match selected:
            case 'Containers':
                ...
            case 'Images':
                nav_manager = NavigationManager()
                nav_manager.navigate('image_page')
            case 'Networks':
                ...
            case 'Pods':
                ...
            case 'Volumes':
                ...
            case 'Exit':
                exit(0)