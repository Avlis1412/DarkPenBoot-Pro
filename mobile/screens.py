"""Telas mobile de Ajuda, Sobre e navegacao basica."""

from kivy.metrics import sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from .config import (
    APP_AUTHOR, APP_NAME, APP_VERSION, GITHUB_URL, LEGAL_NOTICE,
    NIXOS_CONSTITUTION_URL, NIXOS_DOWNLOAD_URL, NIXOS_GOVERNANCE_URL,
)
from .ads import ad_banner
from .widgets import MobileButton, ScrollPage


class HomeScreen(Screen):
    def __init__(self, palette, go, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=16, spacing=10)
        root.add_widget(Label(text=APP_NAME, color=palette["accent"],
                              font_size=sp(24), bold=True, size_hint_y=None,
                              height=56))
        root.add_widget(MobileButton(palette, text="Download", on_release=lambda *_: go("download")))
        root.add_widget(MobileButton(palette, text="Ajuda", on_release=lambda *_: go("help")))
        root.add_widget(MobileButton(palette, text="Sobre", on_release=lambda *_: go("about")))
        banner = ad_banner(palette)
        if banner is not None:
            root.add_widget(banner)
        root.add_widget(Label(text=LEGAL_NOTICE, color=palette["info"],
                              font_size=sp(11), halign="left", valign="top"))
        self.add_widget(root)


class HelpScreen(Screen):
    def __init__(self, palette, go, **kwargs):
        super().__init__(**kwargs)
        page = ScrollPage(palette, "Ajuda", lambda *_: go("home"))
        page.add_text(
            "FLUXO MOBILE\n\n"
            "1. Abra Download e escolha uma distro.\n"
            "2. Aguarde a validacao do arquivo.\n"
            "3. Selecione a ISO local na tela ISO.\n"
            "4. Para OTG/DD, use ROOT e confirme o dispositivo.\n\n"
            "O botao Voltar permanece fixo e todas as paginas usam scroll vertical.\n\n"
            "A gravacao raw destrói os dados do dispositivo escolhido. Confirme o caminho antes de prosseguir.")
        self.add_widget(page)


class AboutScreen(Screen):
    def __init__(self, palette, go, open_url, **kwargs):
        super().__init__(**kwargs)
        page = ScrollPage(palette, "Sobre", lambda *_: go("home"))
        page.add_text(
            f"{APP_NAME} v{APP_VERSION}\n\n"
            f"Criador de pendrives bootaveis para Windows, Linux, macOS e Android.\n"
            f"Autor: {APP_AUTHOR}\n\n"
            "NixOS® é marca da NixOS Foundation. Este projeto não é afiliado, endossado ou patrocinado pela fundação.\n\n"
            "As imagens NixOS e seus links devem ser consultados nos canais oficiais.\n\n"
            "Licencas, governanca e atribuicoes permanecem sob responsabilidade dos respectivos projetos.")
        page.add_action("GitHub", lambda *_: open_url(GITHUB_URL))
        page.add_action("NixOS: Governanca", lambda *_: open_url(NIXOS_GOVERNANCE_URL))
        page.add_action("NixOS: Download", lambda *_: open_url(NIXOS_DOWNLOAD_URL))
        page.add_action("NixOS: Constituicao", lambda *_: open_url(NIXOS_CONSTITUTION_URL))
        self.add_widget(page)
