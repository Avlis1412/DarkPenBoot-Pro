#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
â•‘    DARKPENBOOT PRO v3.5.0 â€” MOBILE (KIVY / ANDROID)                      â•‘
â•‘                                                                          â•‘
â•‘  Autor: Adriano Rodrigues da Silva                                       â•‘
â•‘  GitHub: https://github.com/Avlis1412                                    â•‘
â•‘                                                                          â•‘
â•‘  VERSÃƒO MOBILE â€” Android/iOS via Kivy + Buildozer                        â•‘
â•‘                                                                          â•‘
â•‘  â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”  â•‘
â•‘  â”‚ INSPIRAÃ‡ÃƒO NIXOS â€” Build reprodutÃ­vel via Buildozer                 â”‚  â•‘
â•‘  â”‚ NixOSÂ® Ã© marca da NixOS Foundation (sem afiliaÃ§Ã£o)                  â”‚  â•‘
â•‘  â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜  â•‘
â•‘                                                                          â•‘
â•‘  FUNCIONALIDADES:                                                        â•‘
â•‘   âœ… Download de distros Linux (com SHA256)                              â•‘
â•‘   âœ… Download de ISOs Windows (link direto navegador)                    â•‘
â•‘   âœ… VerificaÃ§Ã£o SHA256 automÃ¡tica                                       â•‘
â•‘   âœ… SeleÃ§Ã£o de ISO local (/sdcard/Download)                             â•‘
â•‘   âœ… DetecÃ§Ã£o de pendrive OTG                                            â•‘
â•‘   âœ… GravaÃ§Ã£o via DD (requer ROOT)                                       â•‘
â•‘   âœ… Log em tempo real                                                   â•‘
â•‘   âœ… 7 temas (Matrix, Dracula, Nord, Cyberpunk, Monokai, Light, Soft)    â•‘
â•‘                                                                          â•‘
â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
"""

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# IMPORTS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
import os
import sys
import time
import json
import shutil
import hashlib
import threading
import webbrowser
import subprocess
from pathlib import Path
from datetime import datetime

# â”€â”€â”€ Kivy â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.metrics import dp, sp
from kivy.utils import platform, get_color_from_hex
from kivy.graphics import Color, RoundedRectangle, Rectangle, Ellipse, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.switch import Switch
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.properties import (
    StringProperty, NumericProperty, BooleanProperty, ObjectProperty
)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# DETECÃ‡ÃƒO DE PLATAFORMA
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
IS_ANDROID = platform == 'android'
IS_IOS = platform == 'ios'
IS_MOBILE = IS_ANDROID or IS_IOS

# â”€â”€ v3.6.1: pulso neon global â”€â”€
GLOBAL_PULSE_STATE = {
    "active": False,
    "phase": 0,
    "interval_ms": 80,
    "color_cycle_phase": 0,
    "color_cycle_index": 0,
    "_event": None,
}
REACTIVE_PULSE_STATE = {
    "active": False,
    "intensity": 0,
    "until_ts": 0.0,
    "phase": 0,
}
_PULSE_SUBSCRIBERS = []

def _trigger_reactive_pulse(intensity=2, duration_ms=1200):
    try:
        intensity = max(0, min(3, int(intensity)))
    except Exception:
        intensity = 2
    REACTIVE_PULSE_STATE["active"] = True
    REACTIVE_PULSE_STATE["intensity"] = intensity
    REACTIVE_PULSE_STATE["until_ts"] = (
        time.time() * 1000 + max(200, int(duration_ms)))
    REACTIVE_PULSE_STATE["phase"] = 0

def _start_global_pulse():
    if GLOBAL_PULSE_STATE["active"]:
        return
    GLOBAL_PULSE_STATE["active"] = True
    GLOBAL_PULSE_STATE["phase"] = 0
    GLOBAL_PULSE_STATE["color_cycle_phase"] = 0
    GLOBAL_PULSE_STATE["color_cycle_index"] = 0
    GLOBAL_PULSE_STATE["_event"] = Clock.schedule_interval(
        _pulse_tick, GLOBAL_PULSE_STATE["interval_ms"] / 1000.0)

def _stop_global_pulse():
    if not GLOBAL_PULSE_STATE["active"]:
        return
    GLOBAL_PULSE_STATE["active"] = False
    ev = GLOBAL_PULSE_STATE.get("_event")
    if ev is not None:
        try: ev.cancel()
        except Exception: pass
    GLOBAL_PULSE_STATE["_event"] = None

def _pulse_tick(dt):
    reactive = REACTIVE_PULSE_STATE["active"]
    if reactive and time.time() * 1000 > REACTIVE_PULSE_STATE["until_ts"]:
        REACTIVE_PULSE_STATE["active"] = False
        REACTIVE_PULSE_STATE["intensity"] = 0
        reactive = False
    if not GLOBAL_PULSE_STATE["active"] and not reactive:
        return False
    if GLOBAL_PULSE_STATE["active"]:
        GLOBAL_PULSE_STATE["phase"] = (
            GLOBAL_PULSE_STATE["phase"] + 1) % 16
        GLOBAL_PULSE_STATE["color_cycle_phase"] = (
            GLOBAL_PULSE_STATE.get("color_cycle_phase", 0) + 1) % 16
        if GLOBAL_PULSE_STATE["color_cycle_phase"] == 0:
            total = max(1, len(THEMES))
            GLOBAL_PULSE_STATE["color_cycle_index"] = (
                GLOBAL_PULSE_STATE.get("color_cycle_index", 0) + 1) % total
    if reactive:
        REACTIVE_PULSE_STATE["phase"] = (
            REACTIVE_PULSE_STATE["phase"] + 1) % 16
    for w in list(_PULSE_SUBSCRIBERS):
        try:
            if hasattr(w, "_redraw"): w._redraw()
            elif hasattr(w, "_draw"): w._draw()
        except Exception:
            pass
    return True
IS_TERMUX = os.environ.get('TERMUX_VERSION') is not None
IS_WINDOWS = platform == 'win'
IS_LINUX = platform == 'linux'
IS_MAC = platform == 'macosx'

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CONSTANTES
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
APP_NAME = "DarkPenBoot Pro"
APP_VERSION = "3.6.1"
APP_AUTHOR = "Adriano Rodrigues da Silva"
GITHUB_URL = "https://github.com/Avlis1412"

# â”€â”€â”€ NixOS (inspiraÃ§Ã£o) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
NIXOS_URL = "https://nixos.org"
NIXOS_GOVERNANCE_URL = "https://nixos.org/governance/"
NIXOS_DOWNLOAD_URL = "https://nixos.org/download/"
NIXOS_CONSTITUTION_URL = "https://github.com/NixOS/org/blob/main/doc/constitution.md"

PREMIUM_PRICE_BRL = "R$ 10,00"
PREMIUM_CHECKOUT_URL = "https://github.com/Avlis1412/DarkPenBoot-Pro#premium"

# â”€â”€â”€ PIX â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
PIX_KEY = "cc473489-9842-4fce-97e4-5a1b697aa4f3"
PIX_RECEIVER_NAME = "ADRIANO RODRIGUES DA SILVA"
PIX_BANK_NAME = "Santander"

# â”€â”€â”€ DiretÃ³rios (mobile) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
if IS_ANDROID:
    # Android: usa armazenamento externo
    BASE_DIR = Path("/sdcard/DarkPenBootPro")
elif IS_IOS:
    BASE_DIR = Path.home() / "Documents" / "DarkPenBootPro"
else:
    # Desktop (Termux/Windows/Linux/Mac)
    BASE_DIR = Path.home() / ".darkpenboot"

CONFIG_FILE = BASE_DIR / "config.json"
DOWNLOAD_DIR = BASE_DIR / "downloads"
LOG_DIR = BASE_DIR / "logs"
RECENT_FILE = BASE_DIR / "recent.json"

for _d in (BASE_DIR, DOWNLOAD_DIR, LOG_DIR):
    try:
        _d.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

# â”€â”€â”€ Tamanhos mÃ­nimos â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
MIN_ISO_SIZE = 100 * 1024 * 1024  # 100 MB

# â”€â”€â”€ User-Agent â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
BROWSER_UA = (
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TEMAS (mesmos do desktop)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
THEMES = {
    "matrix": {
        "label": "ðŸŸ¢ Matrix",
        "bg": "#040805", "fg": "#00ff41",
        "panel": "#0a1610", "border": "#00b833",
        "accent": "#00ff41", "accent2": "#00ccff",
        "error": "#ff2233", "warning": "#ffdd00",
        "success": "#00ff88", "info": "#00ccff",
        "button": "#0f2418", "button_hover": "#1a3a24",
    },
    "dracula": {
        "label": "ðŸ©¸ Crimson",
        "bg": "#0a0205", "fg": "#ff8095",
        "panel": "#1a0810", "border": "#ff2d55",
        "accent": "#ff4466", "accent2": "#e066ff",
        "error": "#ff2255", "warning": "#ffcc44",
        "success": "#00ffa3", "info": "#cc99ff",
        "button": "#22091a", "button_hover": "#3a1028",
    },
    "nord": {
        "label": "â„ï¸ Nord",
        "bg": "#2e3440", "fg": "#eceff4",
        "panel": "#3b4252", "border": "#4c566a",
        "accent": "#88c0d0", "accent2": "#b48ead",
        "error": "#bf616a", "warning": "#ebcb8b",
        "success": "#a3be8c", "info": "#81a1c1",
        "button": "#434c5e", "button_hover": "#4c566a",
    },
    "cyberpunk": {
        "label": "âš¡ Cyberpunk",
        "bg": "#08060f", "fg": "#f7e600",
        "panel": "#130d2b", "border": "#e6d800",
        "accent": "#f7e600", "accent2": "#ff007f",
        "error": "#ff0066", "warning": "#ffaa00",
        "success": "#00ff88", "info": "#00d4ff",
        "button": "#1f1240", "button_hover": "#2d1c5c",
    },
    "monokai": {
        "label": "ðŸŸ  Monokai",
        "bg": "#1e1f1c", "fg": "#f8f8f2",
        "panel": "#272822", "border": "#75715e",
        "accent": "#fd971f", "accent2": "#ae81ff",
        "error": "#f92672", "warning": "#e6db74",
        "success": "#a6e22e", "info": "#66d9ef",
        "button": "#3e3d32", "button_hover": "#4d4c3d",
    },
    "light": {
        "label": "â˜€ï¸ Light",
        "bg": "#f4f6f8", "fg": "#1a1a1a",
        "panel": "#ffffff", "border": "#d1d5db",
        "accent": "#2563eb", "accent2": "#7c3aed",
        "error": "#dc2626", "warning": "#d97706",
        "success": "#059669", "info": "#2563eb",
        "button": "#e5e7eb", "button_hover": "#d1d5db",
    },
    "soft_dark": {
        "label": "ðŸŒ™ Soft Dark",
        "bg": "#1e1e24", "fg": "#cdd6f4",
        "panel": "#242630", "border": "#45475a",
        "accent": "#89b4fa", "accent2": "#cba6f7",
        "error": "#f38ba8", "warning": "#f9e2af",
        "success": "#a6e3a1", "info": "#89b4fa",
        "button": "#313244", "button_hover": "#45475a",
    },
}

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# DISTROS (idÃªnticas ao desktop â€” versÃµes atualizadas 2025)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
DISTRO_INFO = {
    # ðŸŸ£ NIXOS â€” PRIORIDADE MÃXIMA
    "NixOS 25.05 GNOME": {
        "url": "https://releases.nixos.org/nixos/25.05/latest-nixos-gnome-x86_64-linux.iso",
        "docs": NIXOS_DOWNLOAD_URL,
        "license": "MIT + LGPL-2.1",
        "sha256": "",
        "homepage": NIXOS_URL,
        "foundation": "NixOS Foundation",
    },
    "NixOS 25.05 KDE": {
        "url": "https://releases.nixos.org/nixos/25.05/latest-nixos-plasma6-x86_64-linux.iso",
        "docs": NIXOS_DOWNLOAD_URL,
        "license": "MIT + LGPL-2.1",
        "sha256": "",
        "homepage": NIXOS_URL,
        "foundation": "NixOS Foundation",
    },
    "NixOS 25.05 Minimal": {
        "url": "https://releases.nixos.org/nixos/25.05/latest-nixos-minimal-x86_64-linux.iso",
        "docs": NIXOS_DOWNLOAD_URL,
        "license": "MIT + LGPL-2.1",
        "sha256": "",
        "homepage": NIXOS_URL,
        "foundation": "NixOS Foundation",
    },
    "NixOS 24.11 GNOME": {
        "url": "https://releases.nixos.org/nixos/24.11/latest-nixos-gnome-x86_64-linux.iso",
        "docs": NIXOS_DOWNLOAD_URL,
        "license": "MIT + LGPL-2.1",
        "sha256": "",
        "homepage": NIXOS_URL,
        "foundation": "NixOS Foundation",
    },
    # ðŸ§ UBUNTU
    "Ubuntu 24.04.1 LTS": {
        "url": "https://releases.ubuntu.com/24.04.1/ubuntu-24.04.1-desktop-amd64.iso",
        "docs": "https://ubuntu.com/download/desktop",
        "license": "GPL-3.0",
        "sha256": "",
    },
    # ðŸ§ DEBIAN
    "Debian 12.9 NetInst": {
        "url": "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.9.0-amd64-netinst.iso",
        "docs": "https://www.debian.org/CD/http-ftp/",
        "license": "DFSG-compliant",
        "sha256": "",
    },
    # ðŸ§ LINUX MINT
    "Linux Mint 22 Cinnamon": {
        "url": "https://mirrors.kernel.org/linuxmint/stable/22/linuxmint-22-cinnamon-64bit.iso",
        "docs": "https://linuxmint.com/download.php",
        "license": "GPL-3.0",
        "sha256": "",
    },
    # ðŸ§ FEDORA
    "Fedora Workstation 41": {
        "url": "https://download.fedoraproject.org/pub/fedora/linux/releases/41/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-41-1.4.iso",
        "docs": "https://fedoraproject.org/workstation/download/",
        "license": "GPL-2.0 + MIT + Apache 2.0",
        "sha256": "",
    },
    # ðŸ§ KALI
    "Kali Linux 2025.1": {
        "url": "https://cdimage.kali.org/kali-2025.1/kali-linux-2025.1-installer-amd64.iso",
        "docs": "https://www.kali.org/get-kali/",
        "license": "GPL-3.0",
        "sha256": "",
    },
    # ðŸ§ PARROT
    "Parrot OS 7.0 Home": {
        "url": "https://parrot.elhacker.net/iso/7.0/Parrot-home-7.0_amd64.iso",
        "docs": "https://parrotsec.org/download/",
        "license": "GPL-3.0",
        "sha256": "",
    },
    # ðŸ§ POP!_OS
    "Pop!_OS 22.04 LTS": {
        "url": "https://iso.pop-os.org/22.04/amd64/intel/32/pop-os_22.04_amd64_intel_32.iso",
        "docs": "https://pop.system76.com/",
        "license": "GPL-3.0",
        "sha256": "",
    },
    # ðŸ§ MANJARO
    "Manjaro KDE 24.2": {
        "url": "https://download.manjaro.org/kde/24.2.0/manjaro-kde-24.2.0-241210-linux612.iso",
        "docs": "https://manjaro.org/download/",
        "license": "GPL-3.0",
        "sha256": "",
    },
    # ðŸ§ openSUSE
    "openSUSE Leap 15.6": {
        "url": "https://download.opensuse.org/distribution/leap/15.6/iso/openSUSE-Leap-15.6-DVD-x86_64-Media.iso",
        "docs": "https://get.opensuse.org/leap/",
        "license": "GPL-2.0 / GPL-3.0",
        "sha256": "",
    },
    # ðŸ§ ARCH
    "Arch Linux Latest": {
        "url": "https://mirror.rackspace.com/archlinux/iso/latest/archlinux-x86_64.iso",
        "docs": "https://archlinux.org/download/",
        "license": "GPL-2.0",
        "sha256": "",
    },
    # ðŸ§ ZORIN
    "Zorin OS 17.2 Core": {
        "url": "https://mirrors.edge.kernel.org/zorinos/17/Zorin-OS-17.2-Core-64-bit.iso",
        "docs": "https://zorin.com/os/download/",
        "license": "GPL-3.0",
        "sha256": "",
    },
}

LINUX_DISTROS = {k: v["url"] for k, v in DISTRO_INFO.items()}

WINDOWS_OPTIONS = {
    "Windows 11": "https://www.microsoft.com/software-download/windows11",
    "Windows 10": "https://www.microsoft.com/software-download/windows10",
    "Windows Server 2025": "https://www.microsoft.com/en-us/evalcenter/download-windows-server-2025",
    "Windows Server 2022": "https://www.microsoft.com/en-us/evalcenter/download-windows-server-2022",
}

MACOS_DOWNLOAD_URL = "https://github.com/Comp-Labs/Download-macOS"

FS_LIST = ['NTFS', 'FAT32', 'exFAT', 'ext4', 'ext3', 'ext2']
HASH_ALGOS = ['SHA256', 'SHA512', 'SHA1', 'MD5']

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# UTILITÃRIOS CORE (mesmos do desktop)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def _format_bytes(n: int) -> str:
    if n <= 0:
        return "0 B"
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} PB"

def _format_eta(seconds: float) -> str:
    if seconds <= 0:
        return "0s"
    s = int(seconds)
    if s >= 3600:
        return f"{s // 3600}h {(s % 3600) // 60}m"
    if s >= 60:
        return f"{s // 60}m {s % 60}s"
    return f"{s}s"

def _sha256_file(filepath, progress_cb=None, cancel_flag=None):
    """Calcula SHA256 em blocos."""
    try:
        h = hashlib.sha256()
        total = os.path.getsize(filepath)
        done = 0
        last = 0.0
        with open(filepath, 'rb') as f:
            while True:
                if cancel_flag and cancel_flag():
                    return None
                chunk = f.read(1024 * 1024)
                if not chunk:
                    break
                h.update(chunk)
                done += len(chunk)
                now = time.time()
                if progress_cb and (now - last >= 1.0):
                    pct = int((done / total) * 100) if total > 0 else 0
                    progress_cb(pct, f"SHA256... {pct}%")
                    last = now
        return h.hexdigest()
    except Exception:
        return None

def _is_admin() -> bool:
    """Verifica se tem root."""
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# CONFIG (JSON persistente)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def load_config() -> dict:
    default = {
        'theme': 'soft_dark',
        'last_iso': '',
        'last_distro': 'NixOS 25.05 Minimal',
        'filesystem': 'FAT32',
        'mode': 'extract',
        'verify': True,
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                default.update(json.load(f))
        except Exception:
            pass
    return default

def save_config(cfg: dict):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def load_recent() -> list:
    if RECENT_FILE.exists():
        try:
            with open(RECENT_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                if isinstance(data, list):
                    return data
        except Exception:
            pass
    return []

def add_recent_iso(path: str):
    recent = load_recent()
    recent = [p for p in recent if p != path]
    recent.insert(0, path)
    try:
        with open(RECENT_FILE, 'w', encoding='utf-8') as f:
            json.dump(recent[:5], f, indent=2)
    except Exception:
        pass

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# DOWNLOADER (5 camadas de fallback)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def download_with_fallback(url, destino, progress_cb, cancel_flag, log_cb):
    """
    Downloader resiliente com mÃºltiplas camadas.
    Camadas: curl â†’ wget â†’ urllib
    """
    log_cb(f"â¬‡ï¸ Iniciando: {url}", "info")

    # Camada 1: curl
    if shutil.which('curl'):
        log_cb("ðŸ”§ Tentando via curl...", "info")
        if _download_curl(url, destino, progress_cb, cancel_flag, log_cb):
            return _post_download(destino, url, log_cb)
        if cancel_flag():
            return False

    # Camada 2: wget
    if shutil.which('wget'):
        log_cb("ðŸ”§ Tentando via wget...", "info")
        if _download_wget(url, destino, progress_cb, cancel_flag, log_cb):
            return _post_download(destino, url, log_cb)
        if cancel_flag():
            return False

    # Camada 3: urllib
    log_cb("ðŸ”§ Tentando via urllib...", "info")
    if _download_urllib(url, destino, progress_cb, cancel_flag, log_cb):
        return _post_download(destino, url, log_cb)

    log_cb("âŒ Todos os mÃ©todos falharam", "error")
    return False

def _download_curl(url, destino, progress_cb, cancel_flag, log_cb):
    try:
        if os.path.exists(destino):
            try:
                os.remove(destino)
            except Exception:
                pass
        cmd = [
            'curl', '-L', '--retry', '3', '--retry-delay', '3',
            '--max-redirs', '10', '--connect-timeout', '30',
            '--fail', '-A', BROWSER_UA,
            '-o', destino, url
        ]
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        last = -1
        stalled = 0
        while proc.poll() is None:
            if cancel_flag():
                try:
                    proc.kill()
                    proc.wait(timeout=5)
                except Exception:
                    pass
                try:
                    if os.path.exists(destino):
                        os.remove(destino)
                except Exception:
                    pass
                return False
            if os.path.exists(destino):
                cur = os.path.getsize(destino)
                if cur == last:
                    stalled += 1
                else:
                    stalled = 0
                    last = cur
                progress_cb(0, f"Baixando... {_format_bytes(cur)}")
                if stalled > 180:
                    try:
                        proc.kill()
                    except Exception:
                        pass
                    return False
            time.sleep(1)
        ok = (proc.returncode == 0
              and os.path.exists(destino)
              and os.path.getsize(destino) > MIN_ISO_SIZE)
        return ok
    except Exception as e:
        log_cb(f"âš ï¸ curl: {e}", "warning")
        return False

def _download_wget(url, destino, progress_cb, cancel_flag, log_cb):
    try:
        if os.path.exists(destino):
            try:
                os.remove(destino)
            except Exception:
                pass
        cmd = [
            'wget', '--tries=3', '--timeout=30', '--waitretry=5',
            '--no-check-certificate', '--max-redirect=10',
            f'--user-agent={BROWSER_UA}',
            '-O', destino, url
        ]
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        last = -1
        stalled = 0
        while proc.poll() is None:
            if cancel_flag():
                try:
                    proc.kill()
                    proc.wait(timeout=5)
                except Exception:
                    pass
                try:
                    if os.path.exists(destino):
                        os.remove(destino)
                except Exception:
                    pass
                return False
            if os.path.exists(destino):
                cur = os.path.getsize(destino)
                if cur == last:
                    stalled += 1
                else:
                    stalled = 0
                    last = cur
                progress_cb(0, f"Baixando... {_format_bytes(cur)}")
                if stalled > 180:
                    try:
                        proc.kill()
                    except Exception:
                        pass
                    return False
            time.sleep(1)
        ok = (proc.returncode == 0
              and os.path.exists(destino)
              and os.path.getsize(destino) > MIN_ISO_SIZE)
        return ok
    except Exception as e:
        log_cb(f"âš ï¸ wget: {e}", "warning")
        return False

def _download_urllib(url, destino, progress_cb, cancel_flag, log_cb):
    import urllib.request
    try:
        if os.path.exists(destino):
            try:
                os.remove(destino)
            except Exception:
                pass
        req = urllib.request.Request(url, headers={
            'User-Agent': BROWSER_UA,
            'Accept': '*/*',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
        })
        with urllib.request.urlopen(req, timeout=60) as resp:
            total = int(resp.headers.get('Content-Length', 0))
            done = 0
            last = 0
            with open(destino, 'wb') as f:
                while True:
                    if cancel_flag():
                        try:
                            f.close()
                        except Exception:
                            pass
                        if os.path.exists(destino):
                            try:
                                os.remove(destino)
                            except Exception:
                                pass
                        return False
                    chunk = resp.read(1024 * 1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    done += len(chunk)
                    now = time.time()
                    if now - last >= 1:
                        if total > 0:
                            pct = int((done / total) * 100)
                            progress_cb(pct,
                                f"Baixando... {pct}% "
                                f"({_format_bytes(done)}/{_format_bytes(total)})")
                        else:
                            progress_cb(0, f"Baixando... {_format_bytes(done)}")
                        last = now
        return os.path.exists(destino) and os.path.getsize(destino) > MIN_ISO_SIZE
    except Exception as e:
        log_cb(f"âš ï¸ urllib: {e}", "warning")
        return False

def _post_download(destino, url, log_cb):
    """Verifica se o arquivo Ã© HTML (erro) em vez de ISO."""
    try:
        size = os.path.getsize(destino)
        if size < 1024 * 1024:
            with open(destino, 'rb') as f:
                head = f.read(512).lower()
            if b'<html' in head or b'<!doc' in head:
                log_cb("âŒ Download retornou HTML (pÃ¡gina de erro)", "error")
                try:
                    os.rename(destino, destino + ".html_error")
                except Exception:
                    pass
                return False
        log_cb(f"âœ… Download OK: {_format_bytes(size)}", "success")
        return True
    except Exception:
        return False

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# KIVY UI â€” WIDGETS CUSTOMIZADOS
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def _ensure_linux_mkfs_tools(log_func=None):
    """Garante que as ferramentas mkfs estejam disponÃ­veis (Android/Termux)."""
    needed = {
        'mkfs.vfat':  ['mkfs.fat', 'mkdosfs'],
        'mkfs.ntfs':  ['mkntfs', 'ntfs-3g'],
        'mkfs.exfat': ['mkexfatfs', 'exfatprogs'],
        'mkfs.ext4':  ['mke2fs'],
    }
    import shutil as _sh
    missing = []
    for tool, alts in needed.items():
        if _sh.which(tool):
            continue
        if not any(_sh.which(a) for a in alts):
            missing.append(tool)
    if missing and log_func:
        log_func("âš ï¸ mkfs ausentes (Termux): " + ", ".join(missing),
                 is_warning=True)
        log_func("   ðŸ’¡ pkg install dosfstools ntfs-3g exfatprogs e2fsprogs",
                 is_info=True)
    return missing


def _scan_shell_all_platforms(log_func=None):
    """Varredura universal via shell (Android/Termux)."""
    import subprocess as _sp
    found = []
    try:
        r = _sp.run(["lsblk", "-J", "-o",
                     "NAME,TYPE,SIZE,MODEL,TRAN,SERIAL,RM"],
                    capture_output=True, text=True, timeout=15)
        if r.returncode == 0 and r.stdout.strip():
            import json as _j
            data = _j.loads(r.stdout)
            for dev in data.get("blockdevices", []):
                if dev.get("type") != "disk":
                    continue
                name = dev.get("name", "")
                if not name:
                    continue
                is_usb = (str(dev.get("tran") or "").lower() == "usb"
                          or dev.get("rm") in (True, "1", 1))
                if not is_usb:
                    continue
                found.append({
                    "DiskNumber": name,
                    "Model": (dev.get("model") or "USB").strip(),
                    "Size": 0,
                    "Letters": "",
                    "BusType": "USB",
                    "DevicePath": "/dev/block/" + name,
                    "SerialNumber": (dev.get("serial") or "").strip(),
                    "PNPDeviceID": "",
                })
    except Exception:
        pass
    if log_func:
        log_func("Varredura shell: " + str(len(found)) + " disp.",
                 is_info=True)
    return found



# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
# v3.6.1 â€” HeartPulseButton (Kivy)
# CoraÃ§Ã£o multicolor animado com anÃ©is pulsantes
# â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
class HeartPulseButton(Widget):
    def __init__(self, command=None, theme_key_getter=None, **kwargs):
        super().__init__(**kwargs)
        self._command = command
        self._theme_key_getter = theme_key_getter
        self._phase = 0
        self._pressed = False
        self.size_hint = (None, None)
        self.size = (dp(54), dp(40))
        # Label interno com o emoji
        self._label = Label(
            text='\u2764\ufe0f',
            font_size=sp(20),
            bold=True,
            halign='center',
            valign='middle',
            color=(1, 0.4, 0.6, 1),
        )
        self.add_widget(self._label)
        self.bind(pos=self._redraw, size=self._redraw)
        self._event = Clock.schedule_interval(self._tick, 1 / 30.0)
        _PULSE_SUBSCRIBERS.append(self)

    def _palette(self):
        try:
            tk = self._theme_key_getter() if self._theme_key_getter else 'soft_dark'
            t = THEMES.get(tk, THEMES.get('soft_dark', {}))
            return [
                get_color_from_hex(t.get('accent', '#ff5252')),
                get_color_from_hex(t.get('accent2', '#ff79c6')),
                get_color_from_hex(t.get('info', '#89b4fa')),
                get_color_from_hex(t.get('success', '#a6e3a1')),
                get_color_from_hex(t.get('warning', '#f9e2af')),
            ]
        except Exception:
            return [(1, 0.3, 0.4, 1)]

    def _tick(self, dt):
        self._phase = (self._phase + 1) % 64
        self._redraw()
        return True

    def _redraw(self, *args):
        try:
            self.canvas.before.clear()
            self.canvas.after.clear()
        except Exception:
            return
        palette = self._palette()
        idx = (self._phase // 12) % len(palette)
        col = palette[idx]
        cx, cy = self.center_x, self.center_y
        with self.canvas.before:
            # AnÃ©is pulsantes
            for i in range(6):
                rr = dp(14) + i * dp(2.2) + dp(3) * abs(3 - (self._phase % 8))
                Color(col[0], col[1], col[2], max(0.15, 0.7 - i * 0.1))
                Line(circle=(cx, cy, rr), width=1.2)
        # Atualiza cor do label
        try:
            self._label.color = col
            sz = 18 + int(2 * abs(3 - (self._phase % 8)))
            if self._pressed:
                sz -= 2
            self._label.font_size = sp(sz)
        except Exception:
            pass

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self._pressed = True
            if self._command:
                try: self._command()
                except Exception: pass
            return True
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self._pressed:
            self._pressed = False
            return True
        return super().on_touch_up(touch)


class RoundedButton(Button):
    """BotÃ£o com cantos arredondados e cores do tema."""

    def __init__(self, bg_color="#313244", text_color="#cdd6f4",
                 radius=12, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ''
        self.background_color = (0, 0, 0, 0)
        self.color = get_color_from_hex(text_color)
        self.font_size = sp(15)
        self.bold = True
        self._bg_color = get_color_from_hex(bg_color)
        self._radius = dp(radius)
        with self.canvas.before:
            self._color_instruction = Color(*self._bg_color)
            self._rect = RoundedRectangle(
                pos=self.pos, size=self.size, radius=[self._radius])
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _glassify(self, hex_color):
        """v3.6.1: mistura a cor com o fundo (efeito translÃºcido)."""
        try:
            h = hex_color.lstrip('#')
            r = int(h[0:2], 16); g = int(h[2:4], 16); b = int(h[4:6], 16)
            try:
                bg = self.parent.bg_color if hasattr(self.parent, 'bg_color') else None
                if bg and len(bg) >= 3:
                    pr, pg, pb = int(bg[0]*255), int(bg[1]*255), int(bg[2]*255)
                else:
                    pr, pg, pb = 20, 22, 30
            except Exception:
                pr, pg, pb = 20, 22, 30
            nr = int(r * 0.65 + pr * 0.35)
            ng = int(g * 0.65 + pg * 0.35)
            nb = int(b * 0.65 + pb * 0.35)
            return f"#{nr:02x}{ng:02x}{nb:02x}"
        except Exception:
            return hex_color

    def _update_rect(self, *args):
        self._rect.pos = self.pos
        self._rect.size = self.size

    def set_theme(self, bg_color, text_color):
        self._bg_color = get_color_from_hex(bg_color)
        self._color_instruction.rgba = self._bg_color
        self.color = get_color_from_hex(text_color)

# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# TELAS (SCREENS)
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•

class HomeScreen(Screen):
    """Tela inicial com menu principal."""
    pass


class DownloadScreen(Screen):
    """Tela de download de distros."""
    pass


class ISOScreen(Screen):
    """Tela de seleÃ§Ã£o de ISO local."""
    pass


class USBScreen(Screen):
    """Tela de detecÃ§Ã£o e gravaÃ§Ã£o em pendrive."""
    pass


class LogScreen(Screen):
    """Tela de log."""
    pass


class AboutScreen(Screen):
    """Tela Sobre + NixOS + PIX."""
    pass


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# APP PRINCIPAL
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
class DarkPenBootKivyApp(App):
    """Aplicativo Kivy principal."""

    # â”€â”€â”€ Propriedades reativas â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    theme_key = StringProperty('soft_dark')
    log_text = StringProperty('')
    download_progress = NumericProperty(0)
    download_status = StringProperty('Pronto')
    is_downloading = BooleanProperty(False)
    selected_iso = StringProperty('')
    selected_distro = StringProperty('NixOS 25.05 Minimal')
    detected_drives = StringProperty('')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_config = load_config()
        self.theme_key = self.user_config.get('theme', 'soft_dark')
        self._cancel_download = False
        self._download_thread = None
        self._log_lines = []
        # â”€â”€ v3.6.1: PgUp/PgDown â”€â”€
        try:
            Window.bind(on_key_down=self._on_key_down)
        except Exception:
            pass

    # â”€â”€â”€ Helpers de tema â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def get_theme(self) -> dict:
        return THEMES.get(self.theme_key, THEMES['soft_dark'])

    def hex(self, key: str) -> str:
        t = self.get_theme()
        return t.get(key, '#ffffff')

    def kivy_color(self, key: str):
        return get_color_from_hex(self.hex(key))

    # â”€â”€â”€ Log â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def log(self, msg: str, level: str = "info"):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        self._log_lines.append(line)
        if len(self._log_lines) > 500:
            self._log_lines = self._log_lines[-500:]
        self.log_text = "\n".join(self._log_lines[-200:])

    # â”€â”€â”€ Build UI â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€


    def _toggle_favorite(self):
        """v3.6.1: Favorita a ISO atual."""
        try:
            if not self.selected_iso:
                self._show_info("Favoritos",
                                "Nenhuma ISO selecionada.")
                return
            nome = Path(self.selected_iso).name
            self.log(f"\u2764\ufe0f Favoritado: {nome}", "success")
            _trigger_reactive_pulse(2, 800)
            self._show_info("\u2764\ufe0f Favorito",
                            f"ISO marcada como favorita:\n{nome}")
        except Exception as e:
            self.log(f"\u26a0\ufe0f {e}", "warning")

    def _open_donate(self):
        """v3.6.1: Abre pagina de doacao PIX."""
        try:
            self.log("\u2764\ufe0f Abrindo pagina de doacao...", "info")
            try:
                webbrowser.open(GITHUB_URL)
            except Exception:
                pass
            self._show_info("\u2764\ufe0f Doacao",
                            "Apoie o projeto:\n" + GITHUB_URL)
        except Exception as e:
            self.log(f"\u26a0\ufe0f {e}", "warning")

    def _open_ads_settings(self):
        """v3.6.1: Preferencias de anuncios."""
        try:
            self._show_info("\U0001f4e2 Anuncios",
                            "Versao gratuita contem anuncios.\n\n"
                            f"Assine o PREMIUM ({PREMIUM_PRICE_BRL}) "
                            f"para remove-los.")
        except Exception as e:
            self.log(f"\u26a0\ufe0f {e}", "warning")
    def _on_key_down(self, window, key, scancode, codepoint, modifier):
        """v3.6.1: PgUp=280, PgDown=281 (SDL2)."""
        try:
            if key == 280:  # PgUp
                self._scroll_current(-8)
                return True
            if key == 281:  # PgDn
                self._scroll_current(8)
                return True
        except Exception:
            pass
        return False

    def _scroll_current(self, delta):
        """v3.6.1: Rola o ScrollView da tela atual."""
        try:
            cur = self.sm.current_screen
            for child in cur.walk():
                if isinstance(child, ScrollView):
                    child.scroll_y = max(
                        0.0, min(1.0, child.scroll_y + delta * 0.03))
                    return
        except Exception:
            pass
    def build(self):
        Window.clearcolor = self.kivy_color('bg')

        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(self._build_home())
        self.sm.add_widget(self._build_download())
        self.sm.add_widget(self._build_iso())
        self.sm.add_widget(self._build_usb())
        self.sm.add_widget(self._build_log())
        self.sm.add_widget(self._build_about())

        self.log(f"ðŸš€ {APP_NAME} v{APP_VERSION} (Kivy Mobile)", "success")
        self.log(f"ðŸ“± Plataforma: {platform}", "info")
        self.log("ðŸŸ£ Inspirado em NixOS â€” build reprodutÃ­vel", "info")
        self.log("ðŸŸ£ NixOSÂ® Ã© marca da NixOS Foundation (sem afiliaÃ§Ã£o)", "info")

        # Aviso se nÃ£o for root
        if not _is_admin():
            self.log("âš ï¸ Sem ROOT â€” gravaÃ§Ã£o em pendrive desabilitada", "warning")
            self.log("ðŸ’¡ Use Termux com 'tsu' para ganhar root", "info")

        return self.sm

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # TELA HOME
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    def _build_home(self) -> Screen:
        s = HomeScreen(name='home')

        root = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))
        with root.canvas.before:
            Color(*self.kivy_color('bg'))
            bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(bg, 'pos', root.pos),
                  size=lambda *a: setattr(bg, 'size', root.size))

        # â”€â”€â”€ Header â”€â”€â”€
        title = Label(
            text=f"ðŸ”Œ DARKPENBOOT\n[color={self.hex('accent')}]PRO v{APP_VERSION}[/color]",
            markup=True,
            font_size=sp(24),
            bold=True,
            size_hint_y=None,
            height=dp(80),
            color=self.kivy_color('fg'),
        )
        root.add_widget(title)

        subtitle = Label(
            text=f"[color={self.hex('info')}]Criador de Pendrives BootÃ¡veis â€” Mobile[/color]",
            markup=True,
            font_size=sp(11),
            size_hint_y=None,
            height=dp(24),
        )
        root.add_widget(subtitle)

        # â”€â”€â”€ BotÃµes principais â”€â”€â”€
        buttons = [
            ("â¬‡ï¸  Baixar Distro Linux", 'download', 'accent'),
            ("ðŸ’¿  Selecionar ISO Local", 'iso', 'accent2'),
            ("ðŸ”Œ  Gravar no Pendrive", 'usb', 'warning'),
            ("ðŸ“‹  Ver Log", 'log', 'info'),
            ("â„¹ï¸  Sobre + NixOS + PIX", 'about', 'success'),
        ]

        for text, screen, color_key in buttons:
            btn = RoundedButton(
                text=text,
                bg_color=self.hex('button'),
                text_color=self.hex('fg'),
                size_hint_y=None,
                height=dp(58),
                radius=14,
            )
            btn.bind(on_release=lambda b, scr=screen: self.go_to(scr))
            root.add_widget(btn)

        # â”€â”€â”€ Seletor de tema â”€â”€â”€
        theme_row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        theme_row.add_widget(Label(
            text="ðŸŽ¨ Tema:", size_hint_x=0.3,
            color=self.kivy_color('fg'), font_size=sp(13), bold=True,
        ))
        theme_spinner = Spinner(
            text=THEMES[self.theme_key]['label'],
            values=[t['label'] for t in THEMES.values()],
            size_hint_x=0.7,
            background_normal='',
            background_color=self.kivy_color('button'),
            color=self.kivy_color('fg'),
        )
        theme_spinner.bind(text=self._on_theme_change)
        theme_row.add_widget(theme_spinner)
        root.add_widget(theme_row)

        # â”€â”€â”€ RodapÃ© â”€â”€â”€
        footer = Label(
            text=f"[color={self.hex('info')}]ðŸŸ£ nixos.org  â€¢  "
                 f"github.com/Avlis1412[/color]",
            markup=True,
            font_size=sp(10),
            size_hint_y=None,
            height=dp(24),
        )
        root.add_widget(footer)
        if os.environ.get("DARKPENBOOT_MOBILE_ADS", "1") == "1":
            root.add_widget(Label(
                text="Publicidade mobile",
                color=self.kivy_color('info'),
                font_size=sp(10), size_hint_y=None, height=dp(24),
                halign='center'))


        # â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€ v3.6.1: rodapÃ© com coraÃ§Ã£o + doaÃ§Ã£o â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
        try:
            footer_row = BoxLayout(
                orientation='horizontal',
                size_hint_y=None, height=dp(52), spacing=dp(6))
            # DoaÃ§Ã£o
            donate = RoundedButton(
                text="\U0001f496  DOAR VIA PIX",
                bg_color=self.hex('button'),
                text_color=self.hex('fg'),
                size_hint_x=0.5, height=dp(44),
            )
            donate.bind(on_release=lambda b: self._open_donate())
            footer_row.add_widget(donate)
            # CoraÃ§Ã£o pulsante
            heart = HeartPulseButton(
                command=self._toggle_favorite,
                theme_key_getter=lambda: self.theme_key,
            )
            footer_row.add_widget(heart)
            # AnÃºncios
            ads_btn = RoundedButton(
                text="\U0001f4e2  An\u00fancios",
                bg_color=self.hex('button'),
                text_color=self.hex('fg'),
                size_hint_x=0.5, height=dp(44),
            )
            ads_btn.bind(on_release=lambda b: self._open_ads_settings())
            footer_row.add_widget(ads_btn)
            root.add_widget(footer_row)
        except Exception as e:
            self.log(f"\u26a0\ufe0f Rodap\u00e9: {e}", "warning")

        s.add_widget(root)
        return s

    def _on_theme_change(self, spinner, text):
        for key, t in THEMES.items():
            if t['label'] == text:
                self.theme_key = key
                self.user_config['theme'] = key
                save_config(self.user_config)
                break

    def go_to(self, screen_name: str):
        self.sm.current = screen_name

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # TELA DOWNLOAD
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    def _build_download(self) -> Screen:
        s = DownloadScreen(name='download')

        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))

        # Header
        header = self._make_header("â¬‡ï¸ Download de ISOs", 'home')
        root.add_widget(header)

        # Info NixOS
        nixos_info = Label(
            text=f"[color={self.hex('accent2')}]ðŸŸ£ NixOS 24.11 + 25.05 "
                 f"com GOVERNANÃ‡A oficial[/color]",
            markup=True, font_size=sp(11),
            size_hint_y=None, height=dp(24),
        )
        root.add_widget(nixos_info)

        # Spinner de distros
        distro_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(6))
        distro_row.add_widget(Label(
            text="ðŸ§ Distro:", size_hint_x=0.3,
            color=self.kivy_color('fg'), font_size=sp(13), bold=True,
        ))
        self.distro_spinner = Spinner(
            text=self.selected_distro,
            values=list(DISTRO_INFO.keys()),
            size_hint_x=0.7,
            background_normal='',
            background_color=self.kivy_color('button'),
            color=self.kivy_color('fg'),
        )
        self.distro_spinner.bind(text=self._on_distro_change)
        distro_row.add_widget(self.distro_spinner)
        root.add_widget(distro_row)

        # BotÃ£o baixar
        self.btn_download = RoundedButton(
            text="â¬‡ï¸  Baixar Distro",
            bg_color=self.hex('accent'),
            text_color='#000000',
            size_hint_y=None, height=dp(56), radius=14,
        )
        self.btn_download.bind(on_release=self._start_download)
        root.add_widget(self.btn_download)
        # â”€â”€ v3.6.1: botao Site Oficial â”€â”€
        btn_site = RoundedButton(
            text="ðŸŒ  Site Oficial",
            bg_color=self.hex('button'),
            text_color=self.hex('fg'),
            size_hint_y=None, height=dp(48),
        )
        btn_site.bind(on_release=lambda b: self._open_distro_site())
        root.add_widget(btn_site)

        # Progress bar
        self.download_pb = ProgressBar(
            max=100, value=0,
            size_hint_y=None, height=dp(24),
        )
        root.add_widget(self.download_pb)

        # Status
        self.lbl_status = Label(
            text="Status: Pronto",
            size_hint_y=None, height=dp(28),
            color=self.kivy_color('info'), font_size=sp(11),
        )
        root.add_widget(self.lbl_status)

        # Log pequeno
        scroll = ScrollView()
        self.dl_log = Label(
            text="", size_hint_y=None,
            color=self.kivy_color('fg'), font_size=sp(9),
            halign='left', valign='top',
        )
        self.dl_log.bind(width=lambda *a: setattr(self.dl_log, 'text_size', (self.dl_log.width, None)))
        scroll.add_widget(self.dl_log)
        root.add_widget(scroll)

        # BotÃ£o voltar
        back = RoundedButton(
            text="âŒ Cancelar / Voltar",
            bg_color=self.hex('button'),
            text_color=self.hex('fg'),
            size_hint_y=None, height=dp(48),
        )
        back.bind(on_release=lambda b: self.go_to('home'))
        root.add_widget(back)

        s.add_widget(root)
        return s

    def _on_distro_change(self, spinner, text):
        self.selected_distro = text
        self.user_config['last_distro'] = text
        save_config(self.user_config)

    def _open_distro_site(self):
        """Abre o site oficial da distro selecionada (v3.6.1)."""
        try:
            distro = self.selected_distro
            info = DISTRO_INFO.get(distro, {})
            url = info.get("homepage") or info.get("docs")
            if not url:
                self._show_info("Sem URL",
                    f"A distro '{distro}' nao tem site cadastrado.")
                return
            webbrowser.open(url)
            self.log(f"ðŸŒ Site oficial: {url}", "success")
        except Exception as e:
            self.log(f"âš ï¸ Erro ao abrir site: {e}", "warning")

    def _start_download(self, *args):
        if self.is_downloading:
            return
        distro = self.distro_spinner.text
        url = LINUX_DISTROS.get(distro)
        if not url:
            self.log(f"âŒ Distro nÃ£o encontrada: {distro}", "error")
            return

        # Nome do arquivo
        filename = distro.replace(" ", "_").replace("/", "_") + ".iso"
        destino = DOWNLOAD_DIR / filename

        # Verifica se jÃ¡ existe
        if destino.exists() and os.path.getsize(destino) > MIN_ISO_SIZE:
            self.log(f"âœ… ISO jÃ¡ existe: {destino}", "success")
            self.selected_iso = str(destino)
            self.user_config['last_iso'] = str(destino)
            save_config(self.user_config)
            add_recent_iso(str(destino))
            self._show_info("Download", f"ISO jÃ¡ existe:\n{filename}")
            return

        self.is_downloading = True
        self._cancel_download = False
        self.btn_download.disabled = True
        self.btn_download.text = "â³ Baixando..."

        if "NixOS" in distro:
            self.log("ðŸŸ£ NixOS â€” GovernanÃ§a: nixos.org/governance/", "info")
            self.log("ðŸŸ£ NixOSÂ® marca da NixOS Foundation â€” sem afiliaÃ§Ã£o", "info")

        self.log(f"â¬‡ï¸ Baixando {distro}...", "info")
        self.log(f"ðŸ“¥ {url}", "info")

        def worker():
            def progress(pct, msg):
                Clock.schedule_once(lambda dt: self._update_progress(pct, msg), 0)

            def log_cb(msg, level="info"):
                Clock.schedule_once(lambda dt: self.log(msg, level), 0)

            def cancel():
                return self._cancel_download

            ok = download_with_fallback(url, str(destino), progress, cancel, log_cb)

            Clock.schedule_once(
                lambda dt: self._download_finished(ok, destino), 0)

        self._download_thread = threading.Thread(target=worker, daemon=True)
        self._download_thread.start()

    @mainthread
    def _update_progress(self, pct, msg):
        self.download_pb.value = pct
        self.lbl_status.text = f"Status: {msg}"
        self.dl_log.text = "\n".join(self._log_lines[-15:])

    @mainthread
    def _download_finished(self, ok, destino):
        self.is_downloading = False
        self.btn_download.disabled = False
        self.btn_download.text = "â¬‡ï¸  Baixar Distro"

        if ok:
            self.log(f"âœ… Download concluÃ­do: {destino}", "success")
            self.selected_iso = str(destino)
            self.user_config['last_iso'] = str(destino)
            save_config(self.user_config)
            add_recent_iso(str(destino))
            self.download_pb.value = 100
            self.lbl_status.text = "âœ… Download concluÃ­do!"
            self._show_info("Sucesso", f"ISO baixada:\n{destino.name}\n\n"
                                       f"VÃ¡ em ðŸ’¿ para usar.")
        else:
            if self._cancel_download:
                self.log("â¹ï¸ Download cancelado", "warning")
                self.lbl_status.text = "â¹ï¸ Cancelado"
            else:
                self.log("âŒ Download falhou", "error")
                self.lbl_status.text = "âŒ Falhou"
                self._show_info("Falha", "NÃ£o foi possÃ­vel baixar.\n"
                                          "Verifique a conexÃ£o.")

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # TELA ISO
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    def _build_iso(self) -> Screen:
        s = ISOScreen(name='iso')
        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))

        header = self._make_header("ðŸ’¿ Selecionar ISO", 'home')
        root.add_widget(header)

        # InstruÃ§Ãµes
        info = Label(
            text=f"[color={self.hex('info')}]Coloque ISOs em:\n"
                 f"{DOWNLOAD_DIR}[/color]",
            markup=True, font_size=sp(10),
            size_hint_y=None, height=dp(40),
        )
        root.add_widget(info)

        # BotÃ£o refresh
        btn_refresh = RoundedButton(
            text="ðŸ”„  Atualizar lista de ISOs",
            bg_color=self.hex('accent'),
            text_color='#000000',
            size_hint_y=None, height=dp(48),
        )
        btn_refresh.bind(on_release=self._refresh_iso_list)
        root.add_widget(btn_refresh)

        # Lista scrollÃ¡vel de ISOs
        scroll = ScrollView()
        self.iso_list = BoxLayout(
            orientation='vertical', size_hint_y=None, spacing=dp(4),
            padding=dp(4),
        )
        self.iso_list.bind(minimum_height=self.iso_list.setter('height'))
        scroll.add_widget(self.iso_list)
        root.add_widget(scroll)

        # ISO selecionada
        self.lbl_iso = Label(
            text="Nenhuma ISO selecionada",
            size_hint_y=None, height=dp(40),
            color=self.kivy_color('warning'), font_size=sp(11),
        )
        root.add_widget(self.lbl_iso)

        # BotÃ£o gravar
        btn_use = RoundedButton(
            text="ðŸ”Œ  Usar esta ISO â†’ Pendrive",
            bg_color=self.hex('warning'),
            text_color='#000000',
            size_hint_y=None, height=dp(48),
        )
        btn_use.bind(on_release=lambda b: self.go_to('usb'))
        root.add_widget(btn_use)

        # Voltar
        back = RoundedButton(
            text="â† Voltar",
            bg_color=self.hex('button'),
            text_color=self.hex('fg'),
            size_hint_y=None, height=dp(44),
        )
        back.bind(on_release=lambda b: self.go_to('home'))
        root.add_widget(back)

        s.add_widget(root)
        Clock.schedule_once(lambda dt: self._refresh_iso_list(), 0.5)
        return s

    def _refresh_iso_list(self, *args):
        self.iso_list.clear_widgets()
        isos = []
        for d in (DOWNLOAD_DIR, Path('/sdcard/Download'),
                  Path('/sdcard/Downloads'),
                  Path('/storage/emulated/0/Download')):
            try:
                if d.exists():
                    for f in d.iterdir():
                        if f.suffix.lower() in ('.iso', '.img'):
                            isos.append(f)
            except Exception:
                pass

        # Recentes
        for p in load_recent():
            try:
                pf = Path(p)
                if pf.exists() and pf not in isos:
                    isos.append(pf)
            except Exception:
                pass

        if not isos:
            lbl = Label(
                text="âŒ Nenhuma ISO encontrada",
                color=self.kivy_color('error'),
                size_hint_y=None, height=dp(40),
            )
            self.iso_list.add_widget(lbl)
            return

        for iso in isos:
            try:
                size = iso.stat().st_size
                btn = RoundedButton(
                    text=f"ðŸ’¿ {iso.name}\n"
                         f"   {_format_bytes(size)}  â€¢  {iso.parent}",
                    bg_color=self.hex('button'),
                    text_color=self.hex('fg'),
                    size_hint_y=None, height=dp(60),
                    halign='left',
                )
                btn.bind(on_release=lambda b, p=str(iso): self._select_iso(p))
                self.iso_list.add_widget(btn)
            except Exception:
                pass

    def _select_iso(self, path: str):
        self.selected_iso = path
        self.user_config['last_iso'] = path
        save_config(self.user_config)
        add_recent_iso(path)
        try:
            size = os.path.getsize(path)
            self.lbl_iso.text = f"âœ… {Path(path).name}\n{_format_bytes(size)}"
        except Exception:
            self.lbl_iso.text = f"âœ… {Path(path).name}"
        self.log(f"ðŸ’¿ ISO selecionada: {path}", "success")

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # TELA USB
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    def _build_usb(self) -> Screen:
        s = USBScreen(name='usb')
        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))

        header = self._make_header("ðŸ”Œ Pendrive USB", 'home')
        root.add_widget(header)

        # Aviso de ROOT
        root_warn = Label(
            text=f"[color={self.hex('warning')}]âš ï¸ GravaÃ§Ã£o requer ROOT "
                 f"(Termux com tsu)[/color]",
            markup=True, font_size=sp(10),
            size_hint_y=None, height=dp(24),
        )
        root.add_widget(root_warn)

        # BotÃ£o detectar
        btn_detect = RoundedButton(
            text="ðŸ”„  Detectar Pendrives",
            bg_color=self.hex('accent'),
            text_color='#000000',
            size_hint_y=None, height=dp(52),
        )
        btn_detect.bind(on_release=self._detect_drives)
        root.add_widget(btn_detect)

        # Lista
        scroll = ScrollView()
        self.usb_list = BoxLayout(
            orientation='vertical', size_hint_y=None, spacing=dp(4),
            padding=dp(4),
        )
        self.usb_list.bind(minimum_height=self.usb_list.setter('height'))
        scroll.add_widget(self.usb_list)
        root.add_widget(scroll)

        # Info ISO selecionada
        self.usb_iso_lbl = Label(
            text="", size_hint_y=None, height=dp(40),
            color=self.kivy_color('info'), font_size=sp(11),
        )
        root.add_widget(self.usb_iso_lbl)

        # BotÃ£o gravar
        self.btn_write = RoundedButton(
            text="ðŸ’¾  GRAVAR ISO NO PENDRIVE",
            bg_color=self.hex('error'),
            text_color='#ffffff',
            size_hint_y=None, height=dp(56),
        )
        self.btn_write.bind(on_release=self._start_write)
        root.add_widget(self.btn_write)

        # Voltar
        back = RoundedButton(
            text="â† Voltar",
            bg_color=self.hex('button'),
            text_color=self.hex('fg'),
            size_hint_y=None, height=dp(44),
        )
        back.bind(on_release=lambda b: self.go_to('home'))
        root.add_widget(back)

        s.add_widget(root)
        self._selected_usb = None
        return s

    def _detect_drives(self, *args):
        self.usb_list.clear_widgets()
        self.log("ðŸ” Detectando pendrives...", "info")
        drives = self._get_usb_drives_mobile()

        if not drives:
            lbl = Label(
                text="âŒ Nenhum pendrive OTG detectado\n\n"
                     "ðŸ’¡ Conecte o pendrive via cabo OTG\n"
                     "ðŸ’¡ Autorize o acesso quando pedido",
                color=self.kivy_color('warning'),
                size_hint_y=None, height=dp(100),
                halign='center',
            )
            self.usb_list.add_widget(lbl)
            return

        for d in drives:
            sg = d.get('size', 0) / (1024**3)
            btn = RoundedButton(
                text=f"ðŸ”Œ {d['model']}\n"
                     f"   {d['path']}  â€¢  {sg:.1f} GB",
                bg_color=self.hex('button'),
                text_color=self.hex('fg'),
                size_hint_y=None, height=dp(60),
            )
            btn.bind(on_release=lambda b, dr=d: self._select_drive(dr))
            self.usb_list.add_widget(btn)

        self.log(f"âœ… {len(drives)} pendrive(s) detectado(s)", "success")

    def _get_usb_drives_mobile(self):
        """Detecta pendrives em Android/Termux."""
        drives = []
        # Android storage mounts
        for base in ('/storage', '/mnt/media_rw', '/mnt/usb'):
            try:
                if not os.path.isdir(base):
                    continue
                for entry in os.listdir(base):
                    if entry in ('emulated', 'self'):
                        continue
                    full = os.path.join(base, entry)
                    if os.path.ismount(full) and os.access(full, os.R_OK):
                        try:
                            st = os.statvfs(full)
                            size = st.f_blocks * st.f_frsize
                        except Exception:
                            size = 0
                        drives.append({
                            'model': f'OTG {entry}',
                            'path': full,
                            'size': size,
                        })
            except Exception:
                pass

        # /dev/block
        try:
            if os.path.isdir('/dev/block'):
                for name in os.listdir('/dev/block'):
                    if name.startswith('sd') and name[-1].isdigit():
                        dev = f'/dev/block/{name}'
                        drives.append({
                            'model': f'Block {name}',
                            'path': dev,
                            'size': 0,
                        })
        except Exception:
            pass

        return drives

    def _select_drive(self, drive: dict):
        self._selected_usb = drive
        self.usb_iso_lbl.text = (
            f"âœ… Alvo: {drive['path']}\n"
            f"ðŸ’¿ ISO: {Path(self.selected_iso).name if self.selected_iso else '(nenhuma)'}"
        )
        self.log(f"ðŸŽ¯ Pendrive alvo: {drive['path']}", "success")

    def _start_write(self, *args):
        if not self._selected_usb:
            self._show_info("Erro", "Selecione um pendrive primeiro")
            return
        if not self.selected_iso or not os.path.isfile(self.selected_iso):
            self._show_info("Erro", "Selecione uma ISO primeiro")
            return
        if not _is_admin():
            self._show_info(
                "Sem ROOT",
                "GravaÃ§Ã£o requer privilÃ©gios de root.\n\n"
                "No Termux: execute 'tsu' antes de rodar.\n"
                "No APK: o app precisa de root.")
            return

        self.log(f"ðŸ’¾ Gravando {self.selected_iso} â†’ {self._selected_usb['path']}", "warning")
        self._show_info(
            "ðŸš§ Em desenvolvimento",
            "A gravaÃ§Ã£o via DD no mobile estÃ¡ em desenvolvimento.\n\n"
            "Use a versÃ£o desktop para gravar no pendrive.")

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # TELA LOG
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    def _build_log(self) -> Screen:
        s = LogScreen(name='log')
        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))

        header = self._make_header("ðŸ“‹ Log de OperaÃ§Ãµes", 'home')
        root.add_widget(header)

        scroll = ScrollView()
        self.log_label = Label(
            text="", size_hint_y=None,
            color=self.kivy_color('fg'),
            font_size=sp(10),
            halign='left', valign='top',
            markup=False,
        )
        self.log_label.bind(
            width=lambda *a: setattr(self.log_label, 'text_size', (self.log_label.width, None)))
        scroll.add_widget(self.log_label)
        root.add_widget(scroll)

        # BotÃµes
        btn_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(6))
        btn_clear = RoundedButton(
            text="ðŸ—‘ï¸ Limpar",
            bg_color=self.hex('button'),
            text_color=self.hex('fg'),
        )
        btn_clear.bind(on_release=lambda b: self._clear_log())
        btn_row.add_widget(btn_clear)

        btn_save = RoundedButton(
            text="ðŸ’¾ Salvar",
            bg_color=self.hex('accent'),
            text_color='#000000',
        )
        btn_save.bind(on_release=lambda b: self._save_log())
        btn_row.add_widget(btn_save)
        root.add_widget(btn_row)

        back = RoundedButton(
            text="â† Voltar",
            bg_color=self.hex('button'),
            text_color=self.hex('fg'),
            size_hint_y=None, height=dp(44),
        )
        back.bind(on_release=lambda b: self.go_to('home'))
        root.add_widget(back)

        s.add_widget(root)
        Clock.schedule_interval(self._refresh_log, 1.0)
        return s

    def _refresh_log(self, dt):
        try:
            self.log_label.text = "\n".join(self._log_lines[-100:])
        except Exception:
            pass

    def _clear_log(self):
        self._log_lines = []
        self.log("ðŸ—‘ï¸ Log limpo", "success")

    def _save_log(self):
        try:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = LOG_DIR / f"log_{ts}.txt"
            with open(path, 'w', encoding='utf-8') as f:
                f.write("\n".join(self._log_lines))
            self.log(f"ðŸ’¾ Log salvo: {path}", "success")
            self._show_info("Log salvo", str(path))
        except Exception as e:
            self.log(f"âŒ Erro: {e}", "error")

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # TELA ABOUT
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    def _build_about(self) -> Screen:
        s = AboutScreen(name='about')
        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))

        header = self._make_header("â„¹ï¸ Sobre", 'home')
        root.add_widget(header)

        scroll = ScrollView()
        content = BoxLayout(
            orientation='vertical', size_hint_y=None, spacing=dp(6),
            padding=dp(8),
        )
        content.bind(minimum_height=content.setter('height'))

        about_text = (
            f"[b][color={self.hex('accent')}]"
            f"DARKPENBOOT PRO v{APP_VERSION} (Mobile)[/color][/b]\n\n"
            f"Autor: {APP_AUTHOR}\n"
            f"GitHub: github.com/Avlis1412\n\n"
            f"[b][color={self.hex('accent2')}]"
            f"ðŸŸ£ INSPIRAÃ‡ÃƒO NIXOS[/color][/b]\n"
            f"Este projeto adota princÃ­pios do NixOS:\n"
            f"â€¢ Build reprodutÃ­vel\n"
            f"â€¢ DependÃªncias declarativas\n"
            f"â€¢ Isolamento total\n\n"
            f"NixOSÂ® Ã© marca registrada da NixOS Foundation\n"
            f"(Stichting NixOS Foundation). Sem afiliaÃ§Ã£o.\n\n"
            f"[b][color={self.hex('accent')}]"
            f"ðŸŒ LINKS NIXOS[/color][/b]\n"
            f"â€¢ GovernanÃ§a: nixos.org/governance/\n"
            f"â€¢ Download: nixos.org/download/\n"
            f"â€¢ ConstituiÃ§Ã£o:\n"
            f"  github.com/NixOS/org\n\n"
            f"[b][color={self.hex('accent')}]"
            f"âš–ï¸ LICENÃ‡AS[/color][/b]\n"
            f"â€¢ Nixpkgs: MIT\n"
            f"â€¢ Nix: LGPL-2.1\n"
            f"â€¢ Logo NixOS: CC BY 4.0\n\n"
            f"[b][color={self.hex('success')}]"
            f"â¤ï¸ APOIAR (PIX)[/color][/b]\n"
            f"Nome: {PIX_RECEIVER_NAME}\n"
            f"Banco: {PIX_BANK_NAME}\n"
            f"Chave: {PIX_KEY}\n"
        )

        lbl = Label(
            text=about_text, markup=True,
            color=self.kivy_color('fg'),
            font_size=sp(11),
            size_hint_y=None, halign='left', valign='top',
        )
        lbl.bind(width=lambda *a: setattr(lbl, 'text_size', (lbl.width, None)))
        lbl.bind(texture_size=lambda *a: setattr(lbl, 'height',
                                                  lbl.texture_size[1]))
        content.add_widget(lbl)

        # BotÃµes
        for text, url in [
            ("ðŸŒ GitHub", GITHUB_URL),
            ("ðŸŸ£ NixOS Governance", NIXOS_GOVERNANCE_URL),
            ("ðŸ“¥ NixOS Download", NIXOS_DOWNLOAD_URL),
            ("ðŸ“œ ConstituiÃ§Ã£o NixOS", NIXOS_CONSTITUTION_URL),
            ("â­ PREMIUM R$ 10", PREMIUM_CHECKOUT_URL),
        ]:
            btn = RoundedButton(
                text=text,
                bg_color=self.hex('button'),
                text_color=self.hex('fg'),
                size_hint_y=None, height=dp(46),
            )
            btn.bind(on_release=lambda b, u=url: webbrowser.open(u))
            content.add_widget(btn)

        scroll.add_widget(content)
        root.add_widget(scroll)

        # Voltar
        back = RoundedButton(
            text="â† Voltar",
            bg_color=self.hex('button'),
            text_color=self.hex('fg'),
            size_hint_y=None, height=dp(44),
        )
        back.bind(on_release=lambda b: self.go_to('home'))
        root.add_widget(back)

        s.add_widget(root)
        return s

    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    # HELPERS UI
    # â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    def _make_header(self, title_text: str, back_screen: str) -> BoxLayout:
        row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))

        btn_back = RoundedButton(
            text="â†",
            bg_color=self.hex('button'),
            text_color=self.hex('fg'),
            size_hint_x=0.15,
            font_size=sp(20),
            radius=10,
        )
        btn_back.bind(on_release=lambda b: self.go_to(back_screen))
        row.add_widget(btn_back)

        lbl = Label(
            text=title_text,
            color=self.kivy_color('accent'),
            font_size=sp(16),
            bold=True,
            size_hint_x=0.85,
        )
        row.add_widget(lbl)
        return row

    def _show_info(self, title: str, msg: str):
        popup = Popup(
            title=title,
            title_color=self.kivy_color('accent'),
            separator_color=self.kivy_color('accent'),
            content=Label(
                text=msg,
                color=self.kivy_color('fg'),
                font_size=sp(12),
            ),
            size_hint=(0.9, 0.5),
        )
        # BotÃ£o fechar
        popup.content = BoxLayout(orientation='vertical', spacing=dp(8),
                                   padding=dp(8))
        popup.content.add_widget(Label(
            text=msg, color=self.kivy_color('fg'),
            font_size=sp(12), halign='center',
        ))
        btn = RoundedButton(
            text="OK",
            bg_color=self.hex('accent'),
            text_color='#000000',
            size_hint_y=None, height=dp(44),
        )
        btn.bind(on_release=lambda b: popup.dismiss())
        popup.content.add_widget(btn)
        popup.open()

    # â”€â”€â”€ Ciclo de vida â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    def on_pause(self):
        """Android: pausa segura."""
        return True

    def on_resume(self):
        """Android: retomada."""
        pass

    def on_stop(self):
        """Salva config ao sair."""
        try:
            save_config(self.user_config)
        except Exception:
            pass


# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
# ENTRY POINT
# â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
def main():
    DarkPenBootKivyApp().run()


if __name__ == "__main__":
    main()