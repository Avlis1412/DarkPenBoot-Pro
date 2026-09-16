"""Temas mobile com contraste controlado."""

from kivy.utils import get_color_from_hex

THEMES = {
    "soft_dark": {
        "bg": "#1e1e24", "panel": "#242630", "fg": "#cdd6f4",
        "accent": "#789bd1", "accent2": "#aa8dce", "button": "#313244",
        "error": "#cf7890", "success": "#8fc88b", "info": "#789bd1",
    },
    "light": {
        "bg": "#eef1f5", "panel": "#ffffff", "fg": "#263241",
        "accent": "#3d6fb4", "accent2": "#765da3", "button": "#d9e0e9",
        "error": "#b84d57", "success": "#397d59", "info": "#3d6fb4",
    },
    "matrix": {
        "bg": "#08110c", "panel": "#112218", "fg": "#b8e8c3",
        "accent": "#38c978", "accent2": "#4ba8c7", "button": "#193825",
        "error": "#d06470", "success": "#65c58a", "info": "#4ba8c7",
    },
}


def colors(theme_key="soft_dark"):
    theme = THEMES.get(theme_key, THEMES["soft_dark"])
    return {key: get_color_from_hex(value) for key, value in theme.items()}
