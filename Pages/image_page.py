import os
from pathlib import Path
from uuid import uuid4

from click import style
from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Vertical, Horizontal, Container, VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Static, Header, TabbedContent, TabPane, DataTable, Input, Button, Rule, TextArea

from Managers.file_manager import create_temp_directory, create_file
from Managers.image_manager import list_images, pull_image, search_docker_hub_images, fetch_top_docker_hub_images, \
    get_docker_hub_tags, remove_image, build_image
from Managers.navigation_manager import NavigationManager
from Managers.widget_manager import populate_table, get_selected_table_row


class ImagePage(Screen):
    BINDINGS = [
        Binding(key='ctrl+q', action='quit', description='Quit the application'),
        Binding(key='ctrl+l', action='logs', description='Display logs'),
    ]

    CSS_PATH = 'Styles/image_page.tcss'

    def compose(self) -> ComposeResult:
        with Vertical():
            yield Header(show_clock=True, time_format='%I:%M:%S %p')
            with Horizontal():
                with Container(id='strd_img_ctr'):
                    yield VerticalScroll(
                        DataTable(id='strd_img_tbl'),
                        Button('Remove', id='rm_img_btn')
                    )
                with Container(id='img_src_ctr'):
                    with TabbedContent(id='tabs'):
                        with TabPane('Docker Hub Images'):
                            yield VerticalScroll(
                                # Docker Hub Search Input
                                Input(placeholder='Keyword', id='dh_img_srch'),
                                # Docker Hub Image Table
                                DataTable(id='dh_img_tbl'),
                                # Docker Hub Tag Table
                                DataTable(id='dh_tag_tbl'),
                                Rule(),
                                Static(' Image Url'),
                                Input(placeholder='docker.io/library/alpine', id='dh_img_url'),
                                Static(' Tag'),
                                Input(placeholder='latest', id='hd_img_tag'),
                                Button('Download', id='dh_img_dl_btn'),
                                id='dh_img_tbl_ctr'
                            )
                        with TabPane('Distroless Images'):
                            yield Static('This feature will be available in a future release.')
                        with TabPane('GitHub Repository Image'):
                            yield Static('This feature will be available in a future release.')
                        with TabPane('Image Builder'):
                            yield Vertical(
                                Static(
                                    " Select a directory containing a Docker file and/or resources for image building, or create a temporary directory."),
                                Horizontal(
                                    Input(placeholder='Enter image directory',id='ib_dir'),
                                    Button("Load Directory", id="load_dir_btn"),
                                    Button("Create Temp Directory", id="create_tmp_dir_btn"),
                                    id='ib_dir_ctr'
                                ),
                                TextArea(id='ib_editor', show_line_numbers=True, soft_wrap=True),
                                Button('Build', id='ib_build_btn'),
                            )
        yield Footer()


    def on_mount(self):
        self.refresh_strd_img_tbl()
        self.display_top_docker_images()
        self.query_one('#strd_img_ctr').border_title = 'Stored Images'
        self.query_one('#img_src_ctr').border_title = 'Image Sources'

        path = create_temp_directory()
        self.query_one('#ib_dir', Input).value = str(path)

    def refresh_strd_img_tbl(self):
        data = list_images()
        populate_table(self, 'strd_img_tbl', data)

    def display_docker_images(self, query: str):
        data = search_docker_hub_images(query)
        populate_table(self, 'dh_img_tbl', data)

    def display_top_docker_images(self):
        data = fetch_top_docker_hub_images()
        populate_table(self, 'dh_img_tbl', data)

    def on_input_submitted(self, event: Input.Submitted):
        match event.input.id:
            case 'dh_img_srch':
                self.display_docker_images(event.input.value)

    def on_button_pressed(self, event: Button.Pressed):
        match event.button.id:
            case 'dh_img_dl_btn':
                repository = self.query_one('#dh_img_url', Input).value
                tag = self.query_one('#hd_img_tag', Input).value
                if pull_image('docker.io', repository, tag).returncode == 0:
                    self.refresh_strd_img_tbl()
            case 'rm_img_btn':
                img_id = get_selected_table_row(self, 'strd_img_tbl')[2]
                if remove_image(img_id):
                    self.refresh_strd_img_tbl()
            case 'create_tmp_dir_btn':
                path = create_temp_directory()
                self.query_one('#ib_dir', Input).value = str(path)
            case 'ib_build_btn':
                path = Path(self.query_one('#ib_dir', Input).value)
                if path.exists():
                    editor = self.query_one('#ib_editor', TextArea)
                    create_file(path, 'Dockerfile', editor.document.lines)
                if build_image(path, 'my_image').returncode == 0:
                    self.refresh_strd_img_tbl()



    def on_data_table_cell_selected(self, event: DataTable.CellSelected):
        match event.data_table.id:
            case 'dh_img_tbl':
                repository = get_selected_table_row(self, 'dh_img_tbl')[0]
                self.query_one('#dh_img_url', Input).value = repository
                tag_data = get_docker_hub_tags(repository)
                populate_table(self, 'dh_tag_tbl', tag_data)
            case 'dh_tag_tbl':
                tag = get_selected_table_row(self, 'dh_tag_tbl')[1]
                self.query_one('#hd_img_tag', Input).value = tag

    def action_logs(self):
        nav_manager = NavigationManager()
        nav_manager.navigate('log_page')
