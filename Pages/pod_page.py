from textual import events
from textual.app import Screen, ComposeResult, Binding
from textual.containers import Vertical, Horizontal, Container, VerticalScroll
from textual.widgets import Footer, Static, Header, DataTable, Button, Input

from Managers.navigation_manager import NavigationManager
from Managers.pod_manager import create_pod, list_pods, remove_pod
from Managers.widget_manager import populate_table, get_selected_table_row


class PodPage(Screen):
    BINDINGS = [
        Binding(key='ctrl+q', action='quit', description='Quit the application'),
        Binding(key='ctrl+l', action='logs', description='Logs'),
        Binding(key='ctrl+o', action='home', description='Home'),
        Binding(key='ctrl+b', action='back', description='Back'),
    ]

    CSS_PATH = 'Styles/pod_page.tcss'

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Header(show_clock=True, time_format='%I:%M:%S %p')
            with Horizontal():
                with Container(id='pod_ctr'):
                    yield VerticalScroll(
                        DataTable(id='pod_tbl'),
                        Button('Remove', id='rm_pod_btn')
                    )
                with Container(id='crt_pod_ctr'):
                    yield VerticalScroll(
                        Static(' Name'),
                        Input(placeholder='my-pod', id='pod_name'),
                        Static(' Network'),
                        Input(placeholder='my-network', id='pod_net'),
                        Button('Create', id='crt_pod_btn'),
                    )
        yield Footer()

    def on_mount(self, event: events.Mount) -> None:
        self.refresh_pod_tbl()
        self.query_one('#pod_ctr').border_title = 'Pods'
        self.query_one('#crt_pod_ctr').border_title = 'Create Pod'

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case 'crt_pod_btn':
                name = self.query_one('#pod_name', Input).value
                network = self.query_one('#pod_net', Input).value
                if create_pod(name, network).returncode == 0:
                    self.refresh_pod_tbl()
            case 'rm_pod_btn':
                selected_row = get_selected_table_row(self, 'pod_tbl')
                if selected_row:
                    pod_name = selected_row[0]
                    # Remove the selected network
                    remove_pod(pod_name)
                    # Refresh the table
                    self.refresh_pod_tbl()


    def refresh_pod_tbl(self):
        data = list_pods()
        populate_table(self, 'pod_tbl', data)

    def action_logs(self):
        nav_manager = NavigationManager()
        nav_manager.navigate('log_page')

    def action_home(self):
        nav_manager = NavigationManager()
        nav_manager.navigate('home_page')

    def action_back(self):
        nav_manager = NavigationManager()
        nav_manager.navigate(nav_manager.previous_screen)