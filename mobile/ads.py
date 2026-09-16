"""Slot de anuncios exclusivo da interface mobile.

Nenhum componente deste modulo e importado pelo desktop Tkinter.
A integracao com uma rede de anuncios pode ser adicionada aqui sem alterar
as telas desktop; por padrao exibimos apenas um slot discreto e opt-in.
"""

import os
from kivy.metrics import dp, sp
from kivy.uix.label import Label

MOBILE_ADS_ENABLED = os.environ.get("DARKPENBOOT_MOBILE_ADS", "1") == "1"


def ad_banner(palette):
    if not MOBILE_ADS_ENABLED:
        return None
    return Label(
        text="Publicidade mobile",
        color=palette["info"],
        font_size=sp(10),
        size_hint_y=None,
        height=dp(24),
        halign="center",
        valign="middle",
    )
