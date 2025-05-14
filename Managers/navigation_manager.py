from textual.app import App
from textual.screen import Screen

# window = App()
# screens = dict()
#
# current_screen = ''
# previous_screen = ''
#
# def set_window(app: App):
#     global window
#     window = app
#
# def install(page: Screen, tag: str, title: str):
#     global window
#     global screens
#     window.install_screen(screen=page, name=tag)
#     screens[tag] = (page, title)
#
# def navigate(tag: str):
#     global screens
#     global window
#     global current_screen
#     global previous_screen
#     window.sub_title = screens[tag][1]
#     window.push_screen(tag)
#     previous_screen = current_screen
#     current_screen = tag

class NavigationManager:
    _instance = None

    def __new__(cls, app: App = None):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.app = app
            cls._instance.screens = {}
            cls._instance.current_screen = ''
            cls._instance.previous_screen = ''
        return cls._instance

    def set_app(self, app: App):
        self.app = app

    def install(self, page: Screen, tag: str, title: str):
        self.app.install_screen(screen=page, name=tag)
        self.screens[tag] = (page, title)

    def navigate(self, tag: str):
        self.app.sub_title = self.screens[tag][1]
        self.app.push_screen(tag)
        self.previous_screen = self.current_screen
        self.current_screen = tag
