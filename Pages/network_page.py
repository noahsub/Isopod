from textual import events
from textual.app import Screen, ComposeResult, Binding
from textual.containers import Vertical, Horizontal, Container, VerticalScroll
from textual.widgets import Footer, Static, Header, DataTable, Button, Input

from Managers.navigation_manager import NavigationManager
from Managers.network_manager import list_networks, create_network, remove_network
from Managers.widget_manager import populate_table, get_selected_table_row


class NetworkPage(Screen):
    BINDINGS = [
        Binding(key='ctrl+q', action='quit', description='Quit the application'),
        Binding(key='ctrl+l', action='logs', description='Logs'),
        Binding(key='ctrl+o', action='home', description='Home'),
        Binding(key='ctrl+b', action='back', description='Back'),
    ]

    CSS_PATH = 'Styles/network_page.tcss'

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Header(show_clock=True, time_format='%I:%M:%S %p')
            with Horizontal():
                with Container(id='net_ctr'):
                    yield VerticalScroll(
                        DataTable(id='net_tbl'),
                        Button('Remove', id='rm_net_btn')
                    )
                with Container(id='crt_net_ctr'):
                    yield VerticalScroll(
                        Static(' Name'),
                        Input(placeholder='my-network', id='net_name'),
                        Static(' Subnet'),
                        Input(placeholder='192.168.1.0/24', id='net_subnet'),
                        Button('Create', id='crt_net_btn'),
                    )
        yield Footer()

    def on_mount(self, event: events.Mount) -> None:
        self.refresh_net_tbl()
        self.query_one('#net_ctr').border_title = 'Networks'
        self.query_one('#crt_net_ctr').border_title = 'Create Network'

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case 'crt_net_btn':
                name = self.query_one('#net_name', Input).value
                subnet = self.query_one('#net_subnet', Input).value
                if create_network(name, subnet).returncode == 0:
                    self.refresh_net_tbl()
            case 'rm_net_btn':
                selected_row = get_selected_table_row(self, 'net_tbl')
                if selected_row:
                    network_name = selected_row[0]
                    # Remove the selected network
                    remove_network(network_name)
                    # Refresh the table
                    self.refresh_net_tbl()


    def refresh_net_tbl(self):
        data = list_networks()
        populate_table(self, 'net_tbl', data)

    def action_logs(self):
        nav_manager = NavigationManager()
        nav_manager.navigate('log_page')

    def action_home(self):
        nav_manager = NavigationManager()
        nav_manager.navigate('home_page')

    def action_back(self):
        nav_manager = NavigationManager()
        nav_manager.navigate(nav_manager.previous_screen)