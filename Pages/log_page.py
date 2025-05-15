from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Container
from textual.widgets import Log, Header, Footer
from textual.screen import Screen

from Managers.log_manager import LogManager
from Managers.navigation_manager import NavigationManager


class LogPage(Screen):
    CSS_PATH = 'Styles/log_page.tcss'

    BINDINGS = [
        Binding(key='ctrl+q', action='quit', description='Quit the application'),
        Binding(key='ctrl+o', action='home', description='Home'),
        Binding(key='ctrl+b', action='back', description='Go back'),
    ]

    def compose(self) -> ComposeResult:
        yield Vertical(
            Header(),
            Container(
              Log(id='log_content'),
                id='log_container'
            ),
            Footer()
        )

    def on_show(self):
        log_manager = LogManager()
        logs = log_manager.get_logs()
        log_content = self.query_one('#log_content', Log)
        log_content.write_lines(logs)

    def on_mount(self):
        self.query_one('#log_container').border_title = 'Logs'

    def action_back(self):
        nav_manager = NavigationManager()
        nav_manager.navigate(nav_manager.previous_screen)

    def action_home(self):
        nav_manager = NavigationManager()
        nav_manager.navigate('home_page')