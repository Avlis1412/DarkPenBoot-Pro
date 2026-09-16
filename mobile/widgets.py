"""Widgets mobile: botoes, paginas rolaveis e navegacao consistente."""

from kivy.metrics import dp, sp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


class MobileButton(Button):
    def __init__(self, palette, **kwargs):
        kwargs.setdefault("size_hint_y", None)
        kwargs.setdefault("height", dp(48))
        kwargs.setdefault("font_size", sp(14))
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = palette["button"]
        self.color = palette["fg"]
        self.bold = True


class ScrollPage(BoxLayout):
    """Pagina com scroll vertical e rodape fixo para navegacao."""

    def __init__(self, palette, title, on_back, **kwargs):
        super().__init__(orientation="vertical", padding=dp(12), spacing=dp(8), **kwargs)
        self.palette = palette
        header = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(8))
        header.add_widget(MobileButton(palette, text="<-", size_hint_x=None,
                                       width=dp(54), on_release=on_back))
        header.add_widget(Label(text=title, color=palette["accent"],
                                font_size=sp(18), bold=True, halign="left"))
        self.add_widget(header)
        self.body = ScrollView(do_scroll_x=False, bar_width=dp(8),
                               scroll_type=["bars", "content"])
        self.content = BoxLayout(orientation="vertical", spacing=dp(10),
                                 padding=(0, 0, 0, dp(16)), size_hint_y=None)
        self.content.bind(minimum_height=self.content.setter("height"))
        self.body.add_widget(self.content)
        self.add_widget(self.body)

    def add_text(self, text, size=13):
        label = Label(text=text, color=self.palette["fg"], font_size=sp(size),
                      halign="left", valign="top", size_hint_y=None)
        label.bind(width=lambda *_: setattr(label, "text_size", (label.width, None)))
        label.bind(texture_size=lambda *_: setattr(label, "height", label.texture_size[1]))
        self.content.add_widget(label)
        return label

    def add_action(self, text, callback):
        button = MobileButton(self.palette, text=text, on_release=callback)
        self.content.add_widget(button)
        return button
