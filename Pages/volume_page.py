from textual import events
from textual.app import Screen, ComposeResult, Binding
from textual.containers import Vertical, Horizontal, Container, VerticalScroll
from textual.widgets import Footer, Static, Header, DataTable, Button, Input

from Managers.navigation_manager import NavigationManager
from Managers.volume_manager import create_volume, list_volumes, remove_volume
from Managers.widget_manager import populate_table, get_selected_table_row


class VolumePage(Screen):
    BINDINGS = [
        Binding(key='ctrl+q', action='quit', description='Quit the application'),
        Binding(key='ctrl+l', action='logs', description='Logs'),
        Binding(key='ctrl+o', action='home', description='Home'),
        Binding(key='ctrl+b', action='back', description='Back'),
    ]

    CSS_PATH = 'Styles/volume_page.tcss'

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Header(show_clock=True, time_format='%I:%M:%S %p')
            with Horizontal():
                with Container(id='volume_ctr'):
                    yield VerticalScroll(
                        DataTable(id='volume_tbl'),
                        Button('Remove', id='rm_volume_btn')
                    )
                with Container(id='crt_volume_ctr'):
                    yield VerticalScroll(
                        Static('Name'),
                        Input(placeholder='my-volume', id='volume_name'),
                        Button('Create', id='crt_volume_btn'),
                    )
        yield Footer()

    def on_mount(self, event: events.Mount) -> None:
        self.refresh_volume_tbl()
        self.query_one('#volume_ctr').border_title = 'Volumes'
        self.query_one('#crt_volume_ctr').border_title = 'Create Volume'

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case 'crt_volume_btn':
                name = self.query_one('#volume_name', Input).value
                if create_volume(name).returncode == 0:
                    self.refresh_volume_tbl()
            case 'rm_volume_btn':
                selected_row = get_selected_table_row(self, 'volume_tbl')
                if selected_row:
                    volume_name = selected_row[0]
                    remove_volume(volume_name)
                    self.refresh_volume_tbl()

    def refresh_volume_tbl(self):
        data = list_volumes()
        populate_table(self, 'volume_tbl', data)

    def action_logs(self):
        nav_manager = NavigationManager()
        nav_manager.navigate('log_page')

    def action_home(self):
        nav_manager = NavigationManager()
        nav_manager.navigate('home_page')

    def action_back(self):
        nav_manager = NavigationManager()
        nav_manager.navigate(nav_manager.previous_screen)
