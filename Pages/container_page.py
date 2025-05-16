from textual import events
from textual.app import Screen, ComposeResult, Binding
from textual.containers import Vertical, Horizontal, Container, VerticalScroll
from textual.widgets import Footer, Static, Header, DataTable, Button, Input, TabbedContent, TabPane, Switch, Rule

from Managers.image_manager import list_images
from Managers.navigation_manager import NavigationManager
from Managers.container_manager import create_container, list_containers, remove_container
from Managers.network_manager import list_networks
from Managers.pod_manager import list_pods
from Managers.volume_manager import list_volumes
from Managers.widget_manager import populate_table, get_selected_table_row

class ContainerPage(Screen):
    BINDINGS = [
        Binding(key='ctrl+q', action='quit', description='Quit the application'),
        Binding(key='ctrl+l', action='logs', description='Logs'),
        Binding(key='ctrl+o', action='home', description='Home'),
        Binding(key='ctrl+b', action='back', description='Back'),
    ]

    CSS_PATH = 'Styles/container_page.tcss'

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Header(show_clock=True, time_format='%I:%M:%S %p')
            with Horizontal():
                with Container(id='container_ctr'):
                    yield VerticalScroll(
                        DataTable(id='container_tbl'),
                        Button('Remove', id='rm_container_btn')
                    )
                with Container(id='crt_container_ctr'):
                    with TabbedContent(id='crt_container_tabs'):
                        with TabPane('General'):
                            yield VerticalScroll(
                                Static(' Container Name'),
                                Input(placeholder='my-container', id='crt_container_name'),
                                Static(" Detach | Interactive | TTY"),
                                Horizontal(
                                    Switch(animate=True, id='detach_switch'),
                                    Switch(animate=True, id='interactive_switch'),
                                    Switch(animate=True, id='tty_switch'),
                                    id='crt_container_switches'
                                ),
                                Static(' Start Command'),
                                Input(placeholder='command', id='crt_container_cmd'),
                            )
                        with TabPane('Image'):
                            yield VerticalScroll(
                                Static(' Selected Image'),
                                Input(placeholder='my-image', id='crt_container_selected_image'),
                                Static(' Stored Images'),
                                DataTable(id='crt_container_img_tbl'),
                                Rule(),
                                Static(' Desired image not listed? Search or create it'),
                                Button('Create / Find Image', id='crt_container_find_img_btn'),
                            )
                        with TabPane('Network'):
                            yield VerticalScroll(
                                Static(' Selected Network'),
                                Input(placeholder='my-image', id='crt_container_selected_network'),
                                Static(' Active Networks'),
                                DataTable(id='crt_container_network_tbl'),
                                Rule(),
                                Static(' Network not listed? Create a New Network'),
                                Button('Create Network', id='crt_container_new_network_btn'),
                                Rule(),
                                Static(' WARNING: Network will be ignored if a pod is specified as the network is inherited from the pod'),
                            )
                        with TabPane('Pod'):
                            yield VerticalScroll(
                                Static(' Selected Pod'),
                                Input(placeholder='my-pod', id='crt_container_selected_pod'),
                                Static(' Available Pods'),
                                DataTable(id='crt_container_pod_tbl'),
                                Rule(),
                                Static(' Pod not listed? Create a New Pod'),
                                Button('Create Pod', id='crt_container_new_pod_btn'),
                            )
                        with TabPane('Storage'):
                            yield VerticalScroll(
                                Static(' Selected Volume'),
                                Input(placeholder='my-volume', id='crt_container_selected_volume'),
                                Static(' Mount Path'),
                                Input(placeholder='/mnt/path', id='crt_container_mount_path'),
                                Static(' Available Volumes'),
                                DataTable(id='crt_container_vol_tbl'),
                                Rule(),
                                Static(' Volume not listed? Create a New Volume'),
                                Button('Create Volume', id='crt_container_new_vol_btn'),
                            )
                        with TabPane('Final'):
                            yield VerticalScroll(
                                Static(' Review Configuration', id='crt_container_review_config'),
                                DataTable(id='crt_container_summary_tbl'),
                                Rule(),
                                Button('Create Container', id='crt_container_btn'),
                            )
        yield Footer()

    def on_show(self, event: events.Show) -> None:
        self.refresh_container_tbl()
        self.refresh_strd_img_tbl()
        self.refresh_net_tbl()
        self.refresh_pod_tbl()
        self.refresh_volume_tbl()

    def on_mount(self, event: events.Mount) -> None:
        self.query_one('#container_ctr').border_title = 'Containers'
        self.query_one('#crt_container_ctr').border_title = 'Create Container'

    def on_button_pressed(self, event: Button.Pressed):
        nav_manager = NavigationManager()
        match event.button.id:
            case 'crt_container_btn':
                name = self.query_one('#crt_container_name', Input).value
                cmd = self.query_one('#crt_container_cmd', Input).value
                detach = self.query_one('#detach_switch', Switch).value
                interactive = self.query_one('#interactive_switch', Switch).value
                tty = self.query_one('#tty_switch', Switch).value
                network = self.query_one('#crt_container_selected_network', Input).value
                pod = self.query_one('#crt_container_selected_pod', Input).value
                volume = self.query_one('#crt_container_selected_volume', Input).value
                mount_path = self.query_one('#crt_container_mount_path', Input).value
                image = self.query_one('#crt_container_selected_image', Input).value

                if create_container(name=name,
                                    image=image,
                                    command=cmd,
                                    detached=detach,
                                    interactive=interactive,
                                    tty=tty,
                                    network=network,
                                    pod=pod,
                                    volume=volume,
                                    mount_path=mount_path).returncode == 0:
                    self.refresh_container_tbl()
            case 'rm_container_btn':
                selected_row = get_selected_table_row(self, 'container_tbl')
                if selected_row:
                    container_name = selected_row[0]
                    remove_container(container_name)
                    self.refresh_container_tbl()
            case 'crt_container_find_img_btn':
                nav_manager.navigate('image_page')
            case 'crt_container_new_pod_btn':
                nav_manager.navigate('pod_page')

    def refresh_container_tbl(self):
        data = list_containers()
        populate_table(self, 'container_tbl', data)

    def refresh_strd_img_tbl(self):
        data = list_images()
        populate_table(self, 'crt_container_img_tbl', data)

    def refresh_net_tbl(self):
        data = list_networks()
        populate_table(self, 'crt_container_network_tbl', data)

    def refresh_pod_tbl(self):
        data = list_pods()
        populate_table(self, 'crt_container_pod_tbl', data)

    def refresh_volume_tbl(self):
        data = list_volumes()
        populate_table(self, 'crt_container_vol_tbl', data)

    def on_data_table_cell_selected(self, event: DataTable.CellSelected):
        match event.data_table.id:
            case 'crt_container_img_tbl':
                repo, tag = get_selected_table_row(self, 'crt_container_img_tbl')[:2]
                self.query_one('#crt_container_selected_image', Input).value = f'{repo}:{tag}'
            case 'crt_container_network_tbl':
                name = get_selected_table_row(self, 'crt_container_network_tbl')[1]
                self.query_one('#crt_container_selected_network', Input).value = name
            case 'crt_container_pod_tbl':
                name = get_selected_table_row(self, 'crt_container_pod_tbl')[1]
                self.query_one('#crt_container_selected_pod', Input).value = name
            case 'crt_container_vol_tbl':
                name = get_selected_table_row(self, 'crt_container_vol_tbl')[0]
                self.query_one('#crt_container_selected_volume', Input).value = name
                self.query_one('#crt_container_mount_path', Input).value = f'/mnt/{name.replace(' ', '-')}'

    def action_logs(self):
        nav_manager = NavigationManager()
        nav_manager.navigate('log_page')

    def action_home(self):
        nav_manager = NavigationManager()
        nav_manager.navigate('home_page')

    def action_back(self):
        nav_manager = NavigationManager()
        nav_manager.navigate(nav_manager.previous_screen)


