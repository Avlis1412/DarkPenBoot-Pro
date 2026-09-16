"""Aplicacao Kivy mobile modular do DarkPenBoot Pro."""

import webbrowser
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from .config import DEFAULT_CONFIG
from .screens import AboutScreen, HelpScreen, HomeScreen
from .theme import colors


class DarkPenBootMobileApp(App):
    def build(self):
        palette = colors(DEFAULT_CONFIG["theme"])
        manager = ScreenManager(transition=FadeTransition(duration=0.12))
        go = lambda name: setattr(manager, "current", name)
        manager.add_widget(HomeScreen(palette, go, name="home"))
        manager.add_widget(HelpScreen(palette, go, name="help"))
        manager.add_widget(AboutScreen(palette, go, webbrowser.open, name="about"))
        return manager


if __name__ == "__main__":
    DarkPenBootMobileApp().run()
