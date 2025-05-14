from textual.app import ComposeResult
from textual.containers import Vertical, Container
from textual.widgets import Log
from textual.screen import Screen

from Managers.log_manager import LogManager


class LogPage(Screen):
    CSS_PATH = 'Styles/log_page.tcss'

    def compose(self) -> ComposeResult:
        yield Vertical(
            Container(
              Log(id='log'),
                id='log_container'
            )
        )

    def on_mount(self):
        log_manager = LogManager()
        logs = log_manager.get_logs()
        log_content = self.query_one('#log', Log)
        log_content.write_lines(logs)
