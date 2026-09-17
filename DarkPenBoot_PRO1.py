#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pyright: reportRedeclaration=false
r"""
╔══════════════════════════════════════════════════════════════════════════╗
║       DARKPENBOOT PRO v3.6.0 - CRIADOR DE PENDRIVES BOOTÁVEIS            ║
║                                                                          ║
║  Autor: Adriano Rodrigues da Silva                                       ║
║  GitHub: https://github.com/Avlis1412                                    ║
║  Plataforma: Windows | Linux | macOS | Android (Termux) | OTG Mobile     ║
║                                                                          ║
║  v3.6.0 — NOVO (todas as versões anteriores preservadas):                ║
║   ✅ Logo 🚀 (foguete) em vez de 🔌 (tomada)                             ║
║   ✅ PgUp/PgDown navegam em TODAS as janelas modais                      ║
║   ✅ Lista EXPANDIDA de ~35 distros com links oficiais                   ║
║   ✅ Pulso Neon SÓ ativa em tarefas reais (gravar/baixar/limpar)         ║
║   ✅ Orb 3D OSCILA por todas as cores dos temas quando ativado           ║
║   ✅ Tema geral da UI permanece ESTÁVEL durante oscilação                ║
║                                                                          ║
║  AVISO LEGAL: Este software é propriedade exclusiva de                   ║
║  Adriano Rodrigues da Silva. Todos os direitos reservados.               ║
║  As ISOs Linux são de código aberto e o Windows é redirecionado          ║
║  para os canais oficiais da Microsoft.                                   ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import platform
import subprocess
import threading
import json
import time
import shutil
import hashlib
import webbrowser
import re
import ctypes
import math
import urllib.request
import urllib.error
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Set
import traceback

# ==================================================================
# 1. DETECÇÃO DE SO
# ==================================================================
SYSTEM = platform.system().strip().lower()
IS_WINDOWS = SYSTEM == "windows"
IS_LINUX = SYSTEM == "linux"
IS_MAC = SYSTEM == "darwin"

if IS_WINDOWS:
    import msvcrt

IS_ANDROID = (
    os.environ.get("ANDROID_ROOT") is not None
    or os.environ.get("ANDROID_DATA") is not None
    or os.path.exists("/system/build.prop")
    or "android" in platform.platform().lower()
    or os.environ.get("TERMUX_VERSION") is not None
    or "com.termux" in os.environ.get("PREFIX", "")
)
IS_TERMUX = os.environ.get("TERMUX_VERSION") is not None
IS_IOS = (
    SYSTEM == "ios"
    or "ios" in platform.platform().lower()
    or os.environ.get("PYTHONISTA_VERSION") is not None
    or "pythonista" in sys.version.lower()
)
IS_MOBILE = IS_ANDROID or IS_TERMUX or IS_IOS
IS_OTG_MOBILE = IS_ANDROID or IS_TERMUX or IS_IOS

# ==================================================================
# 1B. ESTADO GLOBAL DE PULSO NEON (v3.6.0 — com ciclo de cores)
# ==================================================================
GLOBAL_PULSE_STATE = {
    'active': False,
    'phase': 0,
    'interval_ms': 80,
    'color_cycle_phase': 0,   # v3.6.0: contador p/ avançar cores
    'color_cycle_index': 0,   # v3.6.0: índice do tema atual no ciclo
}
_PULSE_SUBSCRIBERS: list = []

REACTIVE_PULSE_STATE = {
    'active': False,
    'intensity': 0,
    'until_ts': 0.0,
    'phase': 0,
}

def _trigger_reactive_pulse(intensity: int = 2, duration_ms: int = 1200):
    try:
        intensity = max(0, min(3, int(intensity)))
    except Exception:
        intensity = 2
    REACTIVE_PULSE_STATE['active'] = True
    REACTIVE_PULSE_STATE['intensity'] = intensity
    REACTIVE_PULSE_STATE['until_ts'] = (
        time.time() * 1000 + max(200, int(duration_ms)))
    REACTIVE_PULSE_STATE['phase'] = 0

# ==================================================================
# 2. CONSTANTES — v3.6.0
# ==================================================================
APP_NAME = "DarkPenBoot Pro"
APP_VERSION = "3.6.1"
APP_AUTHOR = "Adriano Rodrigues da Silva"
GITHUB_URL = "https://github.com/Avlis1412"
LOGO_ICON = "🚀"  # v3.6.0: foguete no lugar da tomada

PREMIUM_CHECKOUT_URL = (
    "https://github.com/Avlis1412/DarkPenBoot-Pro#premium"
)
PREMIUM_PRICE_BRL = "R$ 10,00"
PREMIUM_EXE_PLACEHOLDER = (
    "https://github.com/Avlis1412/DarkPenBoot-Pro/releases/download/"
    "v3.6.0/DarkPenBoot_Premium.exe"
)

NIXOS_URL = "https://nixos.org"
NIXOS_DOWNLOAD_URL = "https://nixos.org/download/"
NIXOS_RELEASES_URL = "https://releases.nixos.org/"
NIXOS_MANUAL_URL = "https://nixos.org/manual/nixos/stable/"

GENERAL_LEGAL_NOTICE = (
    "⚖️  AVISO LEGAL E DISTRIBUIÇÃO DE ISOS\n"
    "═══════════════════════════════════════════════\n\n"
    "Este software (DarkPenBoot Pro) é propriedade exclusiva\n"
    "de Adriano Rodrigues da Silva. Todos os direitos reservados.\n\n"
    "🐧 DISTROS LINUX (CÓDIGO ABERTO):\n"
    "As imagens ISO de sistemas operacionais Linux listadas\n"
    "são distribuídas sob suas respectivas licenças de código\n"
    "aberto (GPL-2.0, GPL-3.0, MIT, BSD, AGPL-3.0, etc.).\n"
    "O DarkPenBoot Pro apenas fornece links oficiais para\n"
    "download, respeitando os termos de cada distribuição.\n\n"
    "🪟 MICROSOFT WINDOWS:\n"
    "Para o Windows, o aplicativo direciona EXCLUSIVAMENTE\n"
    "para os canais oficiais da Microsoft para download de\n"
    "ISOs. Nenhuma ISO da Microsoft é distribuída diretamente\n"
    "pelo aplicativo — apenas links oficiais são fornecidos.\n\n"
    "⚖️  RESPONSABILIDADE:\n"
    "O uso deste software é de inteira responsabilidade do\n"
    "usuário. O autor não se responsabiliza por danos a\n"
    "dispositivos ou perda de dados.\n"
)

LICENSE_REGISTRATION_NOTICE = (
    "📜 REGISTRO DE LICENÇA DE USO\n"
    "═══════════════════════════════════════════════\n\n"
    f"Software: {APP_NAME}\n"
    f"Versão:   {APP_VERSION}\n"
    f"Autor:    {APP_AUTHOR}\n"
    "Ano:      2026\n"
    "Registro: Boas Práticas de Desenvolvimento de Software\n\n"
    "───────────────────────────────────────────────\n"
    "TERMOS DE LICENÇA\n"
    "───────────────────────────────────────────────\n"
    "• Uso Pessoal: PERMITIDO\n"
    "• Uso Comercial: PERMITIDO\n"
    "• Redistribuição: PROIBIDA sem autorização expressa\n"
    "• Modificação: PROIBIDA sem autorização expressa\n"
    "• Venda: PROIBIDA sem autorização expressa\n\n"
    "───────────────────────────────────────────────\n"
    "O uso deste software está licenciado ao usuário sob\n"
    "os termos de boas práticas de software, conforme\n"
    "registrado em nome do autor.\n"
    "═══════════════════════════════════════════════"
)

AD_MODE = ("mobile_ads" if IS_MOBILE else "desktop_no_ads")
AD_BANNER_TEXT = (
    f"📢  v3.6.0 — Soft Dark + SHA256  •  "
    f"PREMIUM {PREMIUM_PRICE_BRL} sem anúncios  •  github.com/Avlis1412  📢"
)
AD_BANNER_COLORS = ("#facc15", "#1f2937")

CONFIG_DIR = Path.home() / ".darkpenboot"
CONFIG_FILE = CONFIG_DIR / "config.json"
DOWNLOAD_DIR = CONFIG_DIR / "downloads"
LOG_DIR = CONFIG_DIR / "logs"
RECENT_ISO_FILE = CONFIG_DIR / "recent_isos.json"
EXTRACT_DIR = CONFIG_DIR / "iso_extract"

if IS_IOS:
    _ios_docs = Path.home() / "Documents"
    if _ios_docs.exists() and os.access(str(_ios_docs), os.W_OK):
        CONFIG_DIR = _ios_docs / "DarkPenBootPro"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    DOWNLOAD_DIR = CONFIG_DIR / "downloads"
    LOG_DIR = CONFIG_DIR / "logs"
    RECENT_ISO_FILE = CONFIG_DIR / "recent_isos.json"
    EXTRACT_DIR = CONFIG_DIR / "iso_extract"

if IS_ANDROID or IS_TERMUX:
    _android_ext = "/sdcard"
    if os.path.exists(_android_ext) and os.access(_android_ext, os.W_OK):
        CONFIG_DIR = Path(_android_ext) / "DarkPenBootPro"
    else:
        CONFIG_DIR = Path.home() / ".darkpenboot"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    DOWNLOAD_DIR = CONFIG_DIR / "downloads"
    LOG_DIR = CONFIG_DIR / "logs"
    RECENT_ISO_FILE = CONFIG_DIR / "recent_isos.json"
    EXTRACT_DIR = CONFIG_DIR / "iso_extract"

for _d in (CONFIG_DIR, DOWNLOAD_DIR, LOG_DIR):
    try:
        _d.mkdir(parents=True, exist_ok=True)
    except Exception:
        pass

CHUNK_SIZE = 64 * 1024 * 1024
COPY_BUFFER_SIZE = 16 * 1024 * 1024
DD_BUFFER_SIZE = 16 * 1024 * 1024
CANCEL_CHECK_INTERVAL = 512 * 1024
CREATE_NO_WINDOW = 0x08000000 if IS_WINDOWS else 0
CREATE_NEW_CONSOLE = 0x00000010 if IS_WINDOWS else 0
MAX_RECENT_ISOS = 5

WINDOW_INITIAL_W = 480
WINDOW_INITIAL_H = 820
WINDOW_MIN_W = 360
WINDOW_MIN_H = 560
WINDOW_MAX_RATIO_W = 0.92
WINDOW_MAX_RATIO_H = 0.92

MIN_ISO_SIZE = 100 * 1024 * 1024

BROWSER_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/122.0.0.0 Safari/537.36"
)
BROWSER_ACCEPT = (
    "text/html,application/xhtml+xml,application/xml;q=0.9,"
    "image/avif,image/webp,*/*;q=0.8"
)
BROWSER_ACCEPT_LANG = "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"

SKIP_DIRS = {
    'System Volume Information', '$RECYCLE.BIN', '.Trash', '.Trashes',
    '.Spotlight-V100', '.fseventsd', '.DocumentRevisions-V100', 'lost+found'
}
SKIP_FILES = {
    'Thumbs.db', 'desktop.ini', '.DS_Store', 'ehthumbs.db', 'Icon\r'
}

FAT_INVALID_CHARS = '<>:"/\\|?*'
FAT_INVALID_SET = set(FAT_INVALID_CHARS)

# ==================================================================
# 3. TEMAS
# ==================================================================
THEMES = {
    "matrix": {
        "label": "🟢 Matrix",
        "bg": "#040805", "fg": "#00ff41",
        "frame_bg": "#0a1610", "frame_border": "#00b833",
        "label_fg": "#7dff9a",
        "error": "#ff2233", "warning": "#ffdd00",
        "success": "#00ff88", "info": "#00ccff",
        "accent": "#00ff41", "accent2": "#00ccff",
        "entry_bg": "#071008", "entry_fg": "#00ff41",
        "button_bg": "#0f2418", "button_fg": "#7dff9a",
        "button_hover": "#1a3a24", "button_active": "#00a030",
        "cancel_bg": "#550000",
        "led_off": "#0d1a12", "led_green": "#00ff41",
        "led_yellow": "#ffdd00", "led_red": "#ff2233",
    },
    "dracula": {
        "label": "🩸 Crimson",
        "bg": "#0a0205", "fg": "#ff8095",
        "frame_bg": "#1a0810", "frame_border": "#ff2d55",
        "label_fg": "#ffb3c1",
        "error": "#ff2255", "warning": "#ffcc44",
        "success": "#00ffa3", "info": "#cc99ff",
        "accent": "#ff4466", "accent2": "#e066ff",
        "entry_bg": "#030002", "entry_fg": "#ffb3c1",
        "button_bg": "#22091a", "button_fg": "#ffccd6",
        "button_hover": "#3a1028", "button_active": "#cc0033",
        "cancel_bg": "#550015",
        "led_off": "#22091a", "led_green": "#00ffa3",
        "led_yellow": "#ffcc44", "led_red": "#ff2255",
    },
    "nord": {
        "label": "❄️ Nord",
        "bg": "#2e3440", "fg": "#eceff4",
        "frame_bg": "#3b4252", "frame_border": "#4c566a",
        "label_fg": "#d8dee9",
        "error": "#bf616a", "warning": "#ebcb8b",
        "success": "#a3be8c", "info": "#81a1c1",
        "accent": "#88c0d0", "accent2": "#b48ead",
        "entry_bg": "#2e3440", "entry_fg": "#eceff4",
        "button_bg": "#434c5e", "button_fg": "#eceff4",
        "button_hover": "#4c566a", "button_active": "#5e81ac",
        "cancel_bg": "#6a3a3a",
        "led_off": "#434c5e", "led_green": "#a3be8c",
        "led_yellow": "#ebcb8b", "led_red": "#bf616a",
    },
    "cyberpunk": {
        "label": "⚡ Cyberpunk",
        "bg": "#08060f", "fg": "#f7e600",
        "frame_bg": "#130d2b", "frame_border": "#e6d800",
        "label_fg": "#00ffee",
        "error": "#ff0066", "warning": "#ffaa00",
        "success": "#00ff88", "info": "#00d4ff",
        "accent": "#f7e600", "accent2": "#ff007f",
        "entry_bg": "#0a0714", "entry_fg": "#f7e600",
        "button_bg": "#1f1240", "button_fg": "#f7e600",
        "button_hover": "#2d1c5c", "button_active": "#d400ff",
        "cancel_bg": "#6a0030",
        "led_off": "#1f1240", "led_green": "#00ff88",
        "led_yellow": "#f7e600", "led_red": "#ff0066",
    },
    "monokai": {
        "label": "🟠 Monokai",
        "bg": "#1e1f1c", "fg": "#f8f8f2",
        "frame_bg": "#272822", "frame_border": "#75715e",
        "label_fg": "#f8f8f2",
        "error": "#f92672", "warning": "#e6db74",
        "success": "#a6e22e", "info": "#66d9ef",
        "accent": "#fd971f", "accent2": "#ae81ff",
        "entry_bg": "#1e1f1c", "entry_fg": "#f8f8f2",
        "button_bg": "#3e3d32", "button_fg": "#f8f8f2",
        "button_hover": "#4d4c3d", "button_active": "#e68a00",
        "cancel_bg": "#8B0000",
        "led_off": "#3e3d32", "led_green": "#a6e22e",
        "led_yellow": "#e6db74", "led_red": "#f92672",
    },
    "light": {
        "label": "☀️ Light",
        "bg": "#f4f6f8", "fg": "#1a1a1a",
        "frame_bg": "#ffffff", "frame_border": "#d1d5db",
        "label_fg": "#374151",
        "error": "#dc2626", "warning": "#d97706",
        "success": "#059669", "info": "#2563eb",
        "accent": "#2563eb", "accent2": "#7c3aed",
        "entry_bg": "#ffffff", "entry_fg": "#111827",
        "button_bg": "#e5e7eb", "button_fg": "#111827",
        "button_hover": "#d1d5db", "button_active": "#1d4ed8",
        "cancel_bg": "#dc2626",
        "led_off": "#d1d5db", "led_green": "#059669",
        "led_yellow": "#d97706", "led_red": "#dc2626",
    },
    "soft_dark": {
        "label": "🌙 Soft Dark",
        "bg": "#1e1e24", "fg": "#cdd6f4",
        "frame_bg": "#242630", "frame_border": "#45475a",
        "label_fg": "#bac2de",
        "error": "#f38ba8", "warning": "#f9e2af",
        "success": "#a6e3a1", "info": "#89b4fa",
        "accent": "#89b4fa", "accent2": "#cba6f7",
        "entry_bg": "#181825", "entry_fg": "#cdd6f4",
        "button_bg": "#313244", "button_fg": "#cdd6f4",
        "button_hover": "#45475a", "button_active": "#585b70",
        "cancel_bg": "#8c4451",
        "led_off": "#313244", "led_green": "#a6e3a1",
        "led_yellow": "#f9e2af", "led_red": "#f38ba8",
    },
}

def _theme_rgb(value: str):
    value = value.lstrip('#')
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))

def _theme_hex(rgb) -> str:
    return '#%02x%02x%02x' % tuple(
        max(0, min(255, int(channel))) for channel in rgb)

def _soften_theme_colors(theme_dict: dict) -> dict:
    out = dict(theme_dict)
    for key in ('accent', 'accent2', 'info', 'fg', 'entry_fg',
                'button_active', 'button_fg'):
        value = out.get(key)
        if not isinstance(value, str) or not value.startswith('#'):
            continue
        r, g, b = _theme_rgb(value)
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        bg = out.get('frame_bg') or out.get('bg') or '#000000'
        br, bgc, bb = _theme_rgb(bg)
        softened = tuple(
            (channel * 0.82 + gray * 0.18) * 0.94 + base * 0.06
            for channel, base in zip((r, g, b), (br, bgc, bb)))
        out[key] = _theme_hex(softened)
    for key in ('error', 'warning', 'success'):
        value = out.get(key)
        if isinstance(value, str) and value.startswith('#'):
            r, g, b = _theme_rgb(value)
            gray = 0.299 * r + 0.587 * g + 0.114 * b
            out[key] = _theme_hex((r * 0.88 + gray * 0.12,
                                   g * 0.88 + gray * 0.12,
                                   b * 0.88 + gray * 0.12))
    return out

THEMES_RAW = {key: dict(value) for key, value in THEMES.items()}
for _theme_key in list(THEMES):
    THEMES[_theme_key] = _soften_theme_colors(THEMES[_theme_key])

THEME_KEYS = list(THEMES.keys())
THEME_LABELS = [THEMES[k]["label"] for k in THEME_KEYS]
LABEL_TO_KEY = {THEMES[k]["label"]: k for k in THEME_KEYS}
COLORS = THEMES["matrix"]

def _key_from_label(label: str) -> str:
    return LABEL_TO_KEY.get(label, "matrix")

def _label_from_key(key: str) -> str:
    return THEMES.get(key, THEMES["matrix"])["label"]

# ==================================================================
# 4. DISTROS EXPANDIDAS — v3.6.0 (~35 distros com links oficiais)
# ==================================================================
DISTRO_INFO = {
    # ═══════════ BASE DEBIAN & UBUNTU ═══════════
    "Debian 12 NetInst": {
        "url": "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.7.0-amd64-netinst.iso",
        "docs": "https://www.debian.org/distrib/",
        "license": "DFSG-compliant (GPL, MIT, BSD)",
        "sha256": "", "homepage": "https://www.debian.org", "family": "Debian",
    },
    "Debian 12 DVD": {
        "url": "https://cdimage.debian.org/debian-cd/current/amd64/iso-dvd/debian-12.7.0-amd64-DVD-1.iso",
        "docs": "https://www.debian.org/distrib/",
        "license": "DFSG-compliant", "sha256": "",
        "homepage": "https://www.debian.org", "family": "Debian",
    },
    "Ubuntu 24.04 Desktop": {
        "url": "https://releases.ubuntu.com/24.04.1/ubuntu-24.04.1-desktop-amd64.iso",
        "docs": "https://ubuntu.com/download/desktop",
        "license": "GPL-3.0", "sha256": "",
        "homepage": "https://ubuntu.com", "family": "Ubuntu",
    },
    "Ubuntu 24.04 Server": {
        "url": "https://releases.ubuntu.com/24.04.1/ubuntu-24.04.1-live-server-amd64.iso",
        "docs": "https://ubuntu.com/download/server",
        "license": "GPL-3.0", "sha256": "",
        "homepage": "https://ubuntu.com", "family": "Ubuntu",
    },
    "Linux Mint 22 Cinnamon": {
        "url": "https://mirror.rackspace.com/linuxmint/iso/stable/22/linuxmint-22-cinnamon-64bit.iso",
        "docs": "https://linuxmint.com/download.php",
        "license": "GPL-3.0", "sha256": "",
        "homepage": "https://linuxmint.com", "family": "Ubuntu",
    },
    "Pop!_OS 22.04 LTS": {
        "url": "https://iso.pop-os.org/22.04/amd64/intel/58/pop-os_22.04_amd64_intel_58.iso",
        "docs": "https://pop.system76.com/",
        "license": "GPL-3.0", "sha256": "",
        "homepage": "https://pop.system76.com", "family": "Ubuntu",
    },
    "Zorin OS 17 Core": {
        "url": "https://mirrors.edge.kernel.org/zorinos/17/Zorin-OS-17-Core-64-bit.iso",
        "docs": "https://zorin.com/os/download/",
        "license": "GPL-3.0", "sha256": "",
        "homepage": "https://zorin.com", "family": "Ubuntu",
    },
    "elementary OS 7": {
        "url": "https://ams3.dl.elementary.io/download/MTcwMDAwMDAwMA==/elementaryos-7.1-stable.20231201.iso",
        "docs": "https://elementary.io/",
        "license": "GPL-3.0 + LGPL", "sha256": "",
        "homepage": "https://elementary.io", "family": "Ubuntu",
    },
    "Kali Linux 2024.3": {
        "url": "https://cdimage.kali.org/kali-2024.3/kali-linux-2024.3-installer-amd64.iso",
        "docs": "https://www.kali.org/get-kali/",
        "license": "GPL-3.0 (Debian derivative)", "sha256": "",
        "homepage": "https://www.kali.org", "family": "Debian",
    },
    "Parrot OS 7.3 Home": {
        "url": "https://parrot.elhacker.net/iso/7.3/Parrot-home-7.3_amd64.iso",
        "docs": "https://parrotsec.org/download/",
        "license": "GPL-3.0 (Debian derivative)", "sha256": "",
        "homepage": "https://parrotsec.org", "family": "Debian",
    },
    "Parrot OS 7.3 Security": {
        "url": "https://parrot.elhacker.net/iso/7.3/Parrot-security-7.3_amd64.iso",
        "docs": "https://parrotsec.org/download/",
        "license": "GPL-3.0 (Debian derivative)", "sha256": "",
        "homepage": "https://parrotsec.org", "family": "Debian",
    },
    "Tails 6": {
        "url": "https://tails.net/install/",
        "download_direct": False,
        "docs": "https://tails.net/install/",
        "license": "GPL-3.0", "sha256": "",
        "homepage": "https://tails.net", "family": "Debian",
    },
    # ═══════════ BASE RED HAT & ENTERPRISE ═══════════
    "Fedora 40 Workstation": {
        "url": "https://download.fedoraproject.org/pub/fedora/linux/releases/40/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-40-1.14.iso",
        "docs": "https://fedoraproject.org/workstation/download",
        "license": "GPL-2.0 + MIT + Apache 2.0", "sha256": "",
        "homepage": "https://fedoraproject.org", "family": "Red Hat",
    },
    "Fedora 40 Server": {
        "url": "https://download.fedoraproject.org/pub/fedora/linux/releases/40/Server/x86_64/iso/Fedora-Server-dvd-x86_64-40-1.14.iso",
        "docs": "https://fedoraproject.org/server/download",
        "license": "GPL-2.0 + MIT + Apache 2.0", "sha256": "",
        "homepage": "https://fedoraproject.org", "family": "Red Hat",
    },
    "AlmaLinux 9": {
        "url": "https://repo.almalinux.org/almalinux/9.4/isos/x86_64/AlmaLinux-9.4-x86_64-dvd.iso",
        "docs": "https://almalinux.org/get-almalinux/",
        "license": "GPL-2.0 + BSD", "sha256": "",
        "homepage": "https://almalinux.org", "family": "Red Hat",
    },
    "Rocky Linux 9": {
        "url": "https://download.rockylinux.org/pub/rocky/9.4/isos/x86_64/Rocky-9.4-x86_64-dvd.iso",
        "docs": "https://rockylinux.org/download",
        "license": "GPL-2.0 + BSD", "sha256": "",
        "homepage": "https://rockylinux.org", "family": "Red Hat",
    },
    "CentOS Stream 9": {
        "url": "https://mirror.stream.centos.org/9-stream/BaseOS/x86_64/iso/CentOS-Stream-9-latest-x86_64-dvd1.iso",
        "docs": "https://www.centos.org/download/",
        "license": "GPL-2.0", "sha256": "",
        "homepage": "https://www.centos.org", "family": "Red Hat",
    },
    "RHEL 9 Developer": {
        "url": "https://developers.redhat.com/products/rhel/download",
        "download_direct": False,
        "docs": "https://developers.redhat.com/products/rhel/download",
        "license": "Red Hat Subscription (Developer free)", "sha256": "",
        "homepage": "https://www.redhat.com", "family": "Red Hat",
    },
    # ═══════════ BASE ARCH ═══════════
    "Arch Linux": {
        "url": "https://geo.mirror.pkgbuild.com/iso/latest/archlinux-x86_64.iso",
        "docs": "https://archlinux.org/download/",
        "license": "GPL-2.0 e similares", "sha256": "",
        "homepage": "https://archlinux.org", "family": "Arch",
    },
    "Manjaro KDE": {
        "url": "https://download.manjaro.org/kde/24.0.0/manjaro-kde-24.0.0-240514-linux68.iso",
        "docs": "https://manjaro.org/download/",
        "license": "GPL-3.0 (Arch-based)", "sha256": "",
        "homepage": "https://manjaro.org", "family": "Arch",
    },
    "EndeavourOS": {
        "url": "https://mirror.albony.xyz/endeavouros/iso/EndeavourOS_Endeavour-2024.06.25.iso",
        "docs": "https://endeavouros.com/latest-release/",
        "license": "GPL-3.0 (Arch-based)", "sha256": "",
        "homepage": "https://endeavouros.com", "family": "Arch",
    },
    "Garuda Linux": {
        "url": "https://garudalinux.org/downloads",
        "download_direct": False,
        "docs": "https://garudalinux.org/downloads",
        "license": "GPL-3.0 (Arch-based)", "sha256": "",
        "homepage": "https://garudalinux.org", "family": "Arch",
    },
    # ═══════════ BASE SUSE ═══════════
    "openSUSE Leap 15.6": {
        "url": "https://download.opensuse.org/distribution/leap/15.6/iso/openSUSE-Leap-15.6-DVD-x86_64-Media.iso",
        "docs": "https://get.opensuse.org/leap/",
        "license": "GPL-2.0 / GPL-3.0", "sha256": "",
        "homepage": "https://www.opensuse.org", "family": "SUSE",
    },
    "openSUSE Tumbleweed": {
        "url": "https://download.opensuse.org/tumbleweed/iso/openSUSE-Tumbleweed-DVD-x86_64-Current.iso",
        "docs": "https://get.opensuse.org/tumbleweed/",
        "license": "GPL-2.0 / GPL-3.0", "sha256": "",
        "homepage": "https://www.opensuse.org", "family": "SUSE",
    },
    # ═══════════ INDEPENDENTES / DECLARATIVAS / SERVIDORES ═══════════
    "NixOS 24.11 GNOME": {
        "url": "https://releases.nixos.org/nixos/24.11/latest-nixos-gnome-x86_64-linux.iso",
        "docs": NIXOS_DOWNLOAD_URL,
        "license": "MIT (Nixpkgs) + LGPL-2.1 (Nix)", "sha256": "",
        "homepage": NIXOS_URL, "family": "Independente",
    },
    "NixOS 24.11 KDE Plasma": {
        "url": "https://releases.nixos.org/nixos/24.11/latest-nixos-plasma6-x86_64-linux.iso",
        "docs": NIXOS_DOWNLOAD_URL,
        "license": "MIT (Nixpkgs) + LGPL-2.1 (Nix)", "sha256": "",
        "homepage": NIXOS_URL, "family": "Independente",
    },
    "NixOS 24.11 Minimal": {
        "url": "https://releases.nixos.org/nixos/24.11/latest-nixos-minimal-x86_64-linux.iso",
        "docs": NIXOS_DOWNLOAD_URL,
        "license": "MIT (Nixpkgs) + LGPL-2.1 (Nix)", "sha256": "",
        "homepage": NIXOS_URL, "family": "Independente",
    },
    "NixOS 25.05 GNOME": {
        "url": "https://releases.nixos.org/nixos/25.05/latest-nixos-gnome-x86_64-linux.iso",
        "docs": NIXOS_DOWNLOAD_URL,
        "license": "MIT (Nixpkgs) + LGPL-2.1 (Nix)", "sha256": "",
        "homepage": NIXOS_URL, "family": "Independente",
    },
    "NixOS 25.05 KDE Plasma": {
        "url": "https://releases.nixos.org/nixos/25.05/latest-nixos-plasma6-x86_64-linux.iso",
        "docs": NIXOS_DOWNLOAD_URL,
        "license": "MIT (Nixpkgs) + LGPL-2.1 (Nix)", "sha256": "",
        "homepage": NIXOS_URL, "family": "Independente",
    },
    "NixOS 25.05 Minimal": {
        "url": "https://releases.nixos.org/nixos/25.05/latest-nixos-minimal-x86_64-linux.iso",
        "docs": NIXOS_DOWNLOAD_URL,
        "license": "MIT (Nixpkgs) + LGPL-2.1 (Nix)", "sha256": "",
        "homepage": NIXOS_URL, "family": "Independente",
    },
    "Alpine Linux": {
        "url": "https://dl-cdn.alpinelinux.org/alpine/v3.20/releases/x86_64/alpine-standard-3.20.3-x86_64.iso",
        "docs": "https://alpinelinux.org/downloads/",
        "license": "MIT + GPL-2.0", "sha256": "",
        "homepage": "https://alpinelinux.org", "family": "Independente",
    },
    "Gentoo Linux": {
        "url": "https://distfiles.gentoo.org/releases/amd64/autobuilds/current-install-amd64-minimal/",
        "download_direct": False,
        "docs": "https://www.gentoo.org/downloads/",
        "license": "GPL-2.0", "sha256": "",
        "homepage": "https://www.gentoo.org", "family": "Independente",
    },
    "Void Linux": {
        "url": "https://repo-default.voidlinux.org/live/current/void-live-x86_64-20240314-base.iso",
        "docs": "https://voidlinux.org/download/",
        "license": "BSD-2-Clause + outros", "sha256": "",
        "homepage": "https://voidlinux.org", "family": "Independente",
    },
    "Slackware 15": {
        "url": "https://mirrors.slackware.com/slackware/slackware-iso/slackware64-15.0-iso/slackware64-15.0-install-dvd.iso",
        "docs": "http://www.slackware.com/getslack/",
        "license": "Slackware License (BSD-like)", "sha256": "",
        "homepage": "http://www.slackware.com", "family": "Independente",
    },
    "Solus": {
        "url": "https://getsol.us/download/",
        "download_direct": False,
        "docs": "https://getsol.us/download/",
        "license": "GPL-2.0", "sha256": "",
        "homepage": "https://getsol.us", "family": "Independente",
    },
    "Proxmox VE 8.2": {
        "url": "https://www.proxmox.com/en/downloads/proxmox-virtual-environment",
        "download_direct": False,
        "docs": "https://pve.proxmox.com/wiki/Main_Page",
        "license": "AGPL-3.0", "sha256": "",
        "homepage": "https://www.proxmox.com", "family": "Servidor",
    },
    "TrueNAS SCALE": {
        "url": "https://download.truenas.com/TrueNAS-SCALE-ElectricEel/24.10.0.2/TrueNAS-SCALE-24.10.0.2.iso",
        "download_direct": True,
        "docs": "https://www.truenas.com/docs/",
        "license": "BSD-2-Clause", "sha256": "",
        "homepage": "https://www.truenas.com", "family": "Servidor",
    },
}

LINUX_DISTROS = {k: v["url"] for k, v in DISTRO_INFO.items()}
DISTRO_SHA256 = {k: v["sha256"] for k, v in DISTRO_INFO.items()}

WINDOWS_OPTIONS = {
    "Windows 11 (Site Oficial)": "https://www.microsoft.com/software-download/windows11",
    "Windows 10 (Site Oficial)": "https://www.microsoft.com/software-download/windows10",
    "Windows Server 2025 (Avaliação)": "https://www.microsoft.com/en-us/evalcenter/download-windows-server-2025",
    "Windows Server 2022 (Avaliação)": "https://www.microsoft.com/en-us/evalcenter/download-windows-server-2022",
    "Windows Server 2019 (Avaliação)": "https://www.microsoft.com/en-us/evalcenter/download-windows-server-2019",
    "Windows Server 2016 (Avaliação)": "https://www.microsoft.com/en-us/evalcenter/download-windows-server-2016",
    "SQL Server 2022 (Avaliação)": "https://www.microsoft.com/en-us/evalcenter/download-sql-server-2022",
}

MACOS_DOWNLOAD_URL = "https://github.com/Comp-Labs/Download-macOS"
FS_LIST = ['NTFS', 'FAT32', 'exFAT', 'ext4', 'ext3', 'ext2', 'JHFS+', 'APFS']
HASH_ALGOS = ['SHA256', 'SHA512', 'SHA1', 'MD5', 'SHA3-256', 'BLAKE2b']
HASH_MAP = {
    'SHA256': 'sha256', 'SHA512': 'sha512', 'SHA1': 'sha1',
    'MD5': 'md5', 'SHA3-256': 'sha3_256', 'BLAKE2b': 'blake2b',
}
LOG_LEVELS = ['Básico', 'Detalhado', 'Debug', 'Verbose']
BUFFER_OPTIONS = ['Auto (por tier USB)', '4 MB', '8 MB', '16 MB', '32 MB', '64 MB']
CHUNK_OPTIONS = ['Auto', '512 KB (kill rápido)', '4 MB', '16 MB', '32 MB', '64 MB']
REOPEN_OPTIONS = ['3', '5', '10', '20']
ALIGN_OPTIONS = ['Auto (1024 KB)', '512 B', '1024 KB', '2048 KB', '4096 KB']
CLUSTER_OPTIONS = ['Auto', '4 KB', '8 KB', '16 KB', '32 KB', '64 KB']

# ==================================================================
# 5. PIX
# ==================================================================
PIX_KEY = "cc473489-9842-4fce-97e4-5a1b697aa4f3"
PIX_RECEIVER_NAME = "ADRIANO RODRIGUES DA SILVA"
PIX_BANK_NAME = "Santander"
PIX_ACCOUNT_INFO = "Agência 3449 • C/C 01081019-8"

GUI_TEXTURE_ENABLED  = True
GUI_TEXTURE_STEP     = 26
GUI_TEXTURE_ALPHA    = 0.08
ORB_TRANSLUCENCY     = 0.78
ORB_GLASS_EDGE       = True
LOGO_GLOW_ENABLED    = True
LOGO_SHADOW_ENABLED  = True


def _blend_color(rgb, bg_rgb, alpha):
    alpha = max(0.0, min(1.0, float(alpha)))
    return tuple(
        int(c * alpha + b * (1.0 - alpha))
        for c, b in zip(rgb, bg_rgb)
    )


def _rgb_tuple_to_hex(rgb) -> str:
    r, g, b = (max(0, min(255, int(c))) for c in rgb)
    return f"#{r:02x}{g:02x}{b:02x}"


def _lighten_hex(hex_color: str, amount: int = 20) -> str:
    try:
        r, g, b = _theme_rgb(hex_color)
        return _rgb_tuple_to_hex((r + amount, g + amount, b + amount))
    except Exception:
        return hex_color


def _darken_hex(hex_color: str, amount: int = 20) -> str:
    try:
        r, g, b = _theme_rgb(hex_color)
        return _rgb_tuple_to_hex((r - amount, g - amount, b - amount))
    except Exception:
        return hex_color

DONATE_MESSAGE = (
    "Obrigado pelo interesse em apoiar o projeto! 🙏\n\n"
    "O DarkPenBoot Pro é desenvolvido de forma independente e\n"
    "cada doação ajuda a manter o projeto vivo e em evolução.\n\n"
    "Você pode doar qualquer valor via PIX usando a chave abaixo.\n\n"
    "═══════════════════════════════════════════════════\n"
    "⭐ Também visite o projeto no GitHub:\n"
    "   contribua com estrelas, issues e pull requests.\n"
    "═══════════════════════════════════════════════════"
)
# ==================================================================
# 6. UTILITÁRIOS
# ==================================================================
def _safe_decode(data) -> str:
    if not data:
        return ""
    if isinstance(data, str):
        return data
    for enc in ('utf-8', 'cp850', 'cp1252', 'latin-1'):
        try:
            decoded = data.decode(enc)
            if decoded.count('\ufffd') < len(decoded) * 0.05:
                return decoded
        except (UnicodeDecodeError, AttributeError):
            continue
    return data.decode('utf-8', errors='replace')

def _long_path(path: str) -> str:
    if not IS_WINDOWS:
        return path
    try:
        path = os.path.abspath(path)
    except Exception:
        pass
    if path.startswith('\\\\?\\'):
        return path
    if path.startswith('\\\\'):
        return '\\\\?\\UNC\\' + path[2:]
    return '\\\\?\\' + path

def _get_free_space(path: str) -> int:
    try:
        if IS_WINDOWS:
            p = path if path.endswith('\\') else path + '\\'
            free = ctypes.c_ulonglong(0)
            total = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                p, ctypes.byref(free), ctypes.byref(total), None)
            return free.value
        statvfs = getattr(os, 'statvfs', None)
        if statvfs is None:
            return -1
        st = statvfs(path)
        return st.f_bavail * st.f_frsize
    except Exception:
        return -1

def _format_eta(seconds: float) -> str:
    if seconds <= 0:
        return "0s"
    s = int(seconds)
    if s >= 3600:
        return f"{s // 3600}h {(s % 3600) // 60}m"
    elif s >= 60:
        return f"{s // 60}m {s % 60}s"
    return f"{s}s"

def _format_bytes(n: float) -> str:
    if n <= 0:
        return "0 B"
    for unit in ('B', 'KB', 'MB', 'GB', 'TB'):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} PB"

def _parse_size(size_str: str) -> int:
    size_str = size_str.strip().upper()
    if not size_str:
        return 0
    mult = 1
    if size_str.endswith('K'):
        mult = 1024; size_str = size_str[:-1]
    elif size_str.endswith('M'):
        mult = 1024**2; size_str = size_str[:-1]
    elif size_str.endswith('G'):
        mult = 1024**3; size_str = size_str[:-1]
    elif size_str.endswith('T'):
        mult = 1024**4; size_str = size_str[:-1]
    elif size_str.endswith('B'):
        size_str = size_str[:-1]
    try:
        return int(float(size_str) * mult)
    except ValueError:
        return 0

def _normalize_fs(fs: str) -> str:
    s = str(fs).strip()
    low = s.lower()
    aliases = {
        'ntfs': 'NTFS', 'fat32': 'FAT32', 'fat': 'FAT32', 'vfat': 'FAT32',
        'msdos': 'FAT32', 'exfat': 'exFAT', 'ext4': 'ext4', 'ext3': 'ext3',
        'ext2': 'ext2', 'jhfs+': 'JHFS+', 'hfs+': 'JHFS+', 'apfs': 'APFS',
    }
    return aliases.get(low, s)

def _ensure_linux_mkfs_tools(log_func=None):
    """Garante que as ferramentas mkfs estejam disponíveis."""
    needed = {
        'mkfs.vfat':  ['mkfs.fat', 'mkdosfs', 'dosfstools'],
        'mkfs.ntfs':  ['mkntfs', 'ntfs-3g'],
        'mkfs.exfat': ['mkexfatfs', 'exfat-utils', 'exfatprogs'],
        'mkfs.ext4':  ['mke2fs', 'e2fsprogs'],
    }
    missing = []
    for tool, alts in needed.items():
        if shutil.which(tool):
            continue
        found = False
        for a in alts:
            if shutil.which(a):
                found = True; break
        if not found:
            missing.append(f"{tool} (instale: {' ou '.join(alts)})")
    if missing and log_func:
        log_func("⚠️ Ferramentas mkfs ausentes:", is_warning=True)
        for m in missing:
            log_func(f"   • {m}", is_warning=True)
        log_func("   💡 sudo apt install dosfstools ntfs-3g "
                 "exfatprogs e2fsprogs", is_info=True)
    return missing


def _is_fat_like(fs: str) -> bool:
    return _normalize_fs(fs).upper() in ('FAT32', 'EXFAT')

def _is_case_insensitive(fs: str) -> bool:
    return _normalize_fs(fs).upper() in ('FAT32', 'EXFAT', 'NTFS')

def _sanitize_fat_name(name: str) -> str:
    out = []
    for ch in name:
        if ch in FAT_INVALID_SET:
            out.append('_')
        else:
            out.append(ch)
    result = ''.join(out).rstrip(' .')
    if not result:
        result = '_'
    if len(result) > 255:
        base, ext = os.path.splitext(result)
        result = base[:255 - len(ext)] + ext
    return result

def _sanitize_fat_relpath(relpath: str) -> str:
    parts = relpath.replace('\\', '/').split('/')
    return os.path.join(*[_sanitize_fat_name(p) for p in parts if p])

def _is_windows_admin():
    if not IS_WINDOWS:
        return False
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False

def _windows_runas(program, parameters=''):
    import ctypes
    from ctypes import wintypes
    shell32 = ctypes.windll.shell32
    shell32.ShellExecuteW.argtypes = [
        wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR,
        wintypes.LPCWSTR, wintypes.LPCWSTR, ctypes.c_int
    ]
    shell32.ShellExecuteW.restype = wintypes.HINSTANCE
    result = shell32.ShellExecuteW(
        None, 'runas', str(program), str(parameters), None, 1)
    return int(result) > 32

def _powershell_quote_for_cmd(command):
    command = str(command or '').strip()
    return command.replace('"', '\\"')

def _launch_terminal(cmd_text=None, shell='default'):
    try:
        if IS_WINDOWS:
            import ctypes
            if shell == 'powershell':
                params = ('-NoProfile -NoExit -Command "{}"'.format(
                    _powershell_quote_for_cmd(cmd_text)) if cmd_text
                    else '-NoProfile -NoExit')
                return _windows_runas('powershell.exe', params)
            elif shell == 'cmd':
                params = '/K {}'.format(cmd_text) if cmd_text else '/K'
                return _windows_runas('cmd.exe', params)
            else:
                params = ('-NoProfile -NoExit -Command "{}"'.format(
                    _powershell_quote_for_cmd(cmd_text)) if cmd_text
                    else '-NoProfile -NoExit')
                return _windows_runas('powershell.exe', params)
        elif IS_LINUX or IS_ANDROID or IS_TERMUX:
            if IS_TERMUX:
                try:
                    os.system('am start -n com.termux/.HomeActivity')
                    return True
                except Exception:
                    pass
            for term in ('gnome-terminal', 'konsole', 'xfce4-terminal',
                         'mate-terminal', 'lxterminal', 'terminator',
                         'kitty', 'alacritty', 'xterm'):
                if shutil.which(term):
                    if cmd_text:
                        if term in ('gnome-terminal', 'mate-terminal'):
                            subprocess.Popen([term, '--', 'bash', '-c',
                                              f'{cmd_text}; exec bash'])
                        else:
                            subprocess.Popen([term, '-e',
                                              f'bash -c "{cmd_text}; exec bash"'])
                    else:
                        subprocess.Popen([term])
                    return True
            return False
        elif IS_MAC:
            if cmd_text:
                escaped = cmd_text.replace('\\', '\\\\').replace('"', '\\"')
                subprocess.Popen(['osascript', '-e',
                                  f'tell app "Terminal" to do script "{escaped}"'])
            else:
                subprocess.Popen(['open', '-a', 'Terminal'])
            return True
    except Exception:
        pass
    return False

def _detect_usb_tier(drive_info: Optional[Dict] = None) -> str:
    if not drive_info:
        return 'UNKNOWN'
    try:
        pnp = (drive_info.get('PNPDeviceID') or '').upper()
        model = (drive_info.get('Model') or '').upper()
        for marker in ('USB 3', 'USB3', 'SUPERSPEED', 'SSD', 'NVME'):
            if marker in model or marker in pnp:
                return 'USB3'
        if IS_WINDOWS:
            try:
                ps = f'''
                try {{
                    $disk = Get-Disk -Number {drive_info.get("DiskNumber", -1)} -ErrorAction SilentlyContinue
                    if ($disk) {{
                        $bus = (Get-PnpDevice -InstanceId $disk.Path -ErrorAction SilentlyContinue).FriendlyName
                        if ($bus -match '3\\.\\d|USB 3|SuperSpeed') {{ Write-Output "USB3" }}
                        elseif ($bus -match 'USB 2') {{ Write-Output "USB2" }}
                        else {{ Write-Output "UNKNOWN" }}
                    }} else {{ Write-Output "UNKNOWN" }}
                }} catch {{ Write-Output "UNKNOWN" }}
                '''
                r = run_hidden(['powershell', '-NoProfile', '-Command', ps],
                               timeout=8)
                out = (r.stdout or '').strip().upper()
                if 'USB3' in out:
                    return 'USB3'
                if 'USB2' in out:
                    return 'USB2'
            except Exception:
                pass
    except Exception:
        pass
    return 'UNKNOWN'

def _get_optimal_buffer(tier: str, override: str = 'Auto (por tier USB)') -> int:
    if override and override != 'Auto (por tier USB)':
        val = override.replace(' MB', '')
        try:
            return int(val) * 1024 * 1024
        except Exception:
            pass
    if tier == 'USB3':
        return 32 * 1024 * 1024
    if tier == 'USB2':
        return 4 * 1024 * 1024
    return 16 * 1024 * 1024

def _button_is_positive(label: str) -> bool:
    l = str(label).strip().lower()
    m = re.match(r'^\s*([a-záàâãéêíóôõúç]+)', l)
    first = m.group(1) if m else ''
    positive_first = {'sim', 'ok', 'yes', 'confirmar', 'continuar',
                      'prosseguir', 'usar', 'aplicar', 'gravar', 'executar',
                      'abrir', 'limpar', 'reparar', 'formatar', 'reiniciar',
                      'baixar'}
    negative_first = {'não', 'nao', 'no', 'cancelar', 'fechar',
                      'abortar', 'sair', 'parar'}
    if first in positive_first:
        return True
    if first in negative_first:
        return False
    for w in ('sim', 'ok', 'yes', 'confirmar'):
        if w in l:
            return True
    return False

def _disable_windows_automount(log_func=None) -> bool:
    if not IS_WINDOWS:
        return False
    ok = False
    try:
        sp = CONFIG_DIR / f"_am_dis_{os.getpid()}.txt"
        with open(sp, 'w', encoding='ascii', newline='\r\n') as f:
            f.write("automount disable\nautomount scrub\nexit\n")
        r = run_hidden(["diskpart", "/s", str(sp)], timeout=30)
        try:
            sp.unlink(missing_ok=True)
        except Exception:
            pass
        if r.returncode == 0:
            ok = True
            if log_func:
                log_func("🔇 Automount (diskpart): DESATIVADO", is_info=True)
    except Exception:
        pass
    try:
        ps = r'''
        try {
            $k = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
            if (-not (Test-Path $k)) { New-Item -Path $k -Force | Out-Null }
            Set-ItemProperty -Path $k -Name NoDriveTypeAutoRun -Value 255 -Type DWord -Force
            Set-ItemProperty -Path $k -Name NoDriveAutoRun -Value 67108863 -Type DWord -Force
            Set-ItemProperty -Path $k -Name NoAutorun -Value 1 -Type DWord -Force
            Write-Output "OK"
        } catch { Write-Output "ERRO: $($_.Exception.Message)" }
        '''
        r2 = run_hidden(
            ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
             '-Command', ps], timeout=30)
        if "OK" in (r2.stdout or ""):
            ok = True
            if log_func:
                log_func("🔇 Autorun do Explorer: DESATIVADO", is_info=True)
    except Exception:
        pass
    if not ok and log_func:
        log_func("⚠️ Não foi possível suprimir popups do Explorer.",
                 is_warning=True)
    return ok

def _enable_windows_automount(log_func=None) -> bool:
    if not IS_WINDOWS:
        return False
    try:
        ps = r'''
        try {
            $k = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer"
            if (Test-Path $k) {
                Remove-ItemProperty -Path $k -Name NoDriveTypeAutoRun -ErrorAction SilentlyContinue
                Remove-ItemProperty -Path $k -Name NoDriveAutoRun -ErrorAction SilentlyContinue
                Remove-ItemProperty -Path $k -Name NoAutorun -ErrorAction SilentlyContinue
            }
            Write-Output "OK"
        } catch { Write-Output "ERRO: $($_.Exception.Message)" }
        '''
        run_hidden(['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                    '-Command', ps], timeout=30)
    except Exception:
        pass
    try:
        sp = CONFIG_DIR / f"_am_en_{os.getpid()}.txt"
        with open(sp, 'w', encoding='ascii', newline='\r\n') as f:
            f.write("automount enable\nexit\n")
        r = run_hidden(["diskpart", "/s", str(sp)], timeout=30)
        try:
            sp.unlink(missing_ok=True)
        except Exception:
            pass
        if log_func and r.returncode == 0:
            log_func("🔊 Automount + Autorun: REATIVADOS", is_info=True)
        return r.returncode == 0
    except Exception as e:
        if log_func:
            log_func(f"⚠️ Erro ao reativar automount: {e}", is_warning=True)
        return False

def is_admin() -> bool:
    if IS_WINDOWS:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except Exception:
            return False
    geteuid = getattr(os, 'geteuid', None)
    if geteuid is None:
        return False
    return geteuid() == 0

def run_as_admin():
    if IS_WINDOWS:
        try:
            script = os.path.abspath(sys.argv[0])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script}"', None, 1)
            sys.exit(0)
        except Exception as e:
            try:
                messagebox.showerror("Erro", f"Falha ao elevar: {e}")
            except Exception:
                pass
            sys.exit(1)
    else:
        try:
            script = os.path.abspath(sys.argv[0])
            subprocess.run(['sudo', sys.executable, script], check=True)
            sys.exit(0)
        except Exception as e:
            try:
                messagebox.showerror("Erro", f"Falha no sudo: {e}")
            except Exception:
                pass
            sys.exit(1)

def run_hidden(cmd, timeout=300, input_text=None):
    try:
        if IS_WINDOWS:
            si = subprocess.STARTUPINFO()
            si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            si.wShowWindow = subprocess.SW_HIDE
            r = subprocess.run(
                cmd,
                input=input_text.encode('utf-8') if input_text else None,
                capture_output=True, timeout=timeout,
                creationflags=CREATE_NO_WINDOW, startupinfo=si)
            return subprocess.CompletedProcess(
                cmd, r.returncode, _safe_decode(r.stdout), _safe_decode(r.stderr))
        return subprocess.run(
            cmd, input=input_text, capture_output=True, text=True,
            timeout=timeout, encoding='utf-8', errors='replace')
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, 1, "", "Timeout")
    except FileNotFoundError as e:
        return subprocess.CompletedProcess(cmd, 1, "", f"Não encontrado: {e}")
    except Exception as e:
        return subprocess.CompletedProcess(cmd, 1, "", str(e))

def _get_all_drive_letters() -> Set[str]:
    letters: Set[str] = set()
    if not IS_WINDOWS:
        return letters
    try:
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for i in range(26):
            if bitmask & (1 << i):
                letters.add(chr(65 + i))
    except Exception:
        pass
    return letters

def _wait_for_new_drive(before: Set[str], timeout: int = 45,
                        log_func=None) -> Optional[str]:
    for i in range(timeout):
        time.sleep(1)
        after = _get_all_drive_letters()
        new_letters = after - before
        if new_letters:
            for letter in new_letters:
                if os.path.exists(f"{letter}:\\"):
                    return letter
        if log_func and i > 0 and i % 10 == 0:
            log_func(f"   Aguardando nova letra... ({i}s)", is_info=True)
    return None

def _force_assign_letter_to_iso(iso_path: str, log_func=None) -> Optional[str]:
    if not IS_WINDOWS:
        return None
    ps_script = f'''
    try {{
        $img = Get-DiskImage -ImagePath "{iso_path}" -ErrorAction Stop
        if (-not $img.Attached) {{ Write-Output "NAO_MONTADA"; exit 0 }}
        $vol = $img | Get-Volume -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($vol -and $vol.DriveLetter) {{
            Write-Output "DIRETO:$($vol.DriveLetter)"; exit 0
        }}
        $disk = $img | Get-Disk -ErrorAction SilentlyContinue
        if (-not $disk) {{ Write-Output "SEM_DISK"; exit 0 }}
        $parts = $disk | Get-Partition -ErrorAction SilentlyContinue
        if (-not $parts) {{ Write-Output "SEM_PARTICAO"; exit 0 }}
        $part = $parts | Select-Object -First 1
        try {{
            Add-PartitionAccessPath -DiskNumber $disk.Number `
                -PartitionNumber $part.PartitionNumber `
                -AssignDriveLetter -ErrorAction Stop
            Start-Sleep -Seconds 2
            $vol = Get-Volume -Partition $part -ErrorAction SilentlyContinue
            if ($vol -and $vol.DriveLetter) {{
                Write-Output "FORCADO:$($vol.DriveLetter)"
            }} else {{ Write-Output "SEM_LETRA_APOS_FORCAR" }}
        }} catch {{ Write-Output "ERRO_FORCAR: $($_.Exception.Message)" }}
    }} catch {{ Write-Output "ERRO: $($_.Exception.Message)" }}
    '''
    result = run_hidden(
        ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
         '-Command', ps_script], timeout=60)
    output = (result.stdout or "").strip()
    if log_func:
        for linha in output.splitlines():
            if linha.strip():
                log_func(f"   PowerShell: {linha}", is_info=True)
    for prefix in ("DIRETO:", "FORCADO:"):
        if output.startswith(prefix):
            letter = output.split(":")[1].strip()
            if len(letter) == 1 and letter.isalpha():
                return letter
    return None

# ==================================================================
# 7. CONFIG
# ==================================================================
DEFAULT_CONFIG = {
    'last_iso': '', 'filesystem': 'NTFS', 'quick_format': True,
    'scheme': 'MBR', 'verify': False, 'mode': 'extract',
    'theme': 'soft_dark', 'debug': False,
    'window_geometry': '', 'last_operation': '',
    'last_drive_letter': '', 'window_maximized': False,
    'hash_algo': 'SHA256', 'log_level': 'Detalhado',
    'buffer_override': 'Auto (por tier USB)', 'chunk_override': 'Auto',
    'reopen_attempts': '5', 'align_override': 'Auto (1024 KB)',
    'cluster_override': 'Auto', 'force_fsync': True,
    'leave_raw_dd': False, 'ad_mode': AD_MODE, 'license_key': '',
    'premium_unlocked': False,
}

def load_config() -> Dict:
    default = {
        'last_iso': '', 'filesystem': 'NTFS', 'quick_format': True,
        'scheme': 'MBR', 'verify': False, 'mode': 'extract',
        'theme': 'matrix', 'debug': False,
        'window_geometry': '', 'last_operation': '',
        'last_drive_letter': '', 'window_maximized': False,
        'hash_algo': 'SHA256',
        'log_level': 'Detalhado',
        'buffer_override': 'Auto (por tier USB)',
        'chunk_override': 'Auto',
        'reopen_attempts': '5',
        'align_override': 'Auto (1024 KB)',
        'cluster_override': 'Auto',
        'force_fsync': True,
        'leave_raw_dd': False,
        'ad_mode': AD_MODE,
        'license_key': '',
        'premium_unlocked': False,
    }
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                default.update(json.load(f))
        except Exception:
            pass
    t = default.get('theme', 'matrix')
    if t == 'dark':
        default['theme'] = 'matrix'
    elif t not in THEMES:
        default['theme'] = 'matrix'
    return default

def save_config(config: Dict):
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def load_recent_isos() -> List[str]:
    if not RECENT_ISO_FILE.exists():
        return []
    try:
        with open(RECENT_ISO_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if isinstance(data, list):
                return [p for p in data if isinstance(p, str)]
    except Exception:
        pass
    return []

def save_recent_isos(recent: List[str]):
    try:
        with open(RECENT_ISO_FILE, 'w', encoding='utf-8') as f:
            json.dump(recent[-MAX_RECENT_ISOS:], f, indent=2)
    except Exception:
        pass

def add_recent_iso(path: str):
    recent = load_recent_isos()
    recent = [p for p in recent if p != path]
    recent.append(path)
    save_recent_isos(recent)

# ==================================================================
# 7B. VALIDAÇÃO PRÉ-VOO DA ISO
# ==================================================================
def _inspect_file_bytes(filepath: str, n: int = 32) -> Tuple[bytes, str]:
    try:
        with open(filepath, 'rb') as f:
            data = f.read(n)
        hex_str = ' '.join(f'{b:02x}' for b in data)
        ascii_str = ''.join(chr(b) if 32 <= b < 127 else '.' for b in data)
        return data, f"HEX:   {hex_str}\nASCII: {ascii_str}"
    except Exception:
        return b'', ""

def _validate_iso_pre_flight(iso_path: str, log_func=None) -> Tuple[bool, str]:
    if not iso_path:
        return False, "Nenhuma ISO selecionada."
    if not os.path.isfile(iso_path):
        return False, f"Arquivo não encontrado:\n{iso_path}"
    try:
        size = os.path.getsize(iso_path)
    except OSError as e:
        return False, f"Não foi possível ler o arquivo:\n{e}"
    if size < 1024:
        head, info = _inspect_file_bytes(iso_path, 32)
        msg = (
            f"❌ ARQUIVO INVÁLIDO — MUITO PEQUENO\n\n"
            f"📄 Arquivo: {os.path.basename(iso_path)}\n"
            f"📏 Tamanho: {size} bytes\n"
            f"📂 Caminho: {iso_path}\n\n"
            f"🔍 Primeiros 32 bytes:\n{info}\n\n"
            f"🛡️ O PENDRIVE NÃO FOI FORMATADO."
        )
        if log_func:
            log_func(f"❌ ISO inválida: {size} bytes.", is_error=True)
        return False, msg
    if size < MIN_ISO_SIZE:
        head, info = _inspect_file_bytes(iso_path, 32)
        head_low = head.lower()
        if b'<html' in head_low or b'<!doc' in head_low:
            return False, (
                f"❌ ARQUIVO INVÁLIDO — PÁGINA HTML\n\n"
                f"📄 {os.path.basename(iso_path)}\n"
                f"📏 {_format_bytes(size)}\n\n"
                f"🔍 {info}\n\n"
                f"💡 O link de download estava errado.\n"
                f"🛡️ O PENDRIVE NÃO FOI FORMATADO.")
        return False, (
            f"⚠️ ARQUIVO SUSPEITO\n\n"
            f"📄 {os.path.basename(iso_path)}\n"
            f"📏 {_format_bytes(size)}\n\n"
            f"🔍 {info}\n\n"
            f"💡 ISOs reais têm pelo menos 100 MB.\n"
            f"🛡️ O PENDRIVE NÃO FOI FORMATADO.")
    has_iso9660 = False
    has_udf = False
    has_zip = False
    try:
        with open(iso_path, 'rb') as f:
            f.seek(0x8001)
            if f.read(5) == b'CD001':
                has_iso9660 = True
        with open(iso_path, 'rb') as f:
            f.seek(32768)
            if f.read(5) in (b'BEA01', b'NSR02', b'NSR03'):
                has_udf = True
        with open(iso_path, 'rb') as f:
            if f.read(4) in (b'PK\x03\x04', b'PK\x05\x06'):
                has_zip = True
    except Exception:
        pass
    if not (has_iso9660 or has_udf or has_zip):
        if log_func:
            log_func("⚠️ Assinatura ISO9660/UDF não encontrada. "
                     "Prosseguindo mesmo assim...", is_warning=True)
        return True, ""
    tipo = "ISO9660" if has_iso9660 else ("UDF" if has_udf else "ZIP/ISO-híbrida")
    if log_func:
        log_func(f"✅ ISO validada: {_format_bytes(size)} ({tipo})",
                 is_success=True)
    return True, ""

# ==================================================================
# 8. DETECÇÃO DE DRIVES USB
# ==================================================================
def _get_usb_drives_android() -> List[Dict]:
    drives = []
    try:
        candidates = []
        for base in ("/dev/block", "/dev"):
            if not os.path.isdir(base):
                continue
            try:
                for name in os.listdir(base):
                    if name.startswith("sd") and name[-1].isdigit():
                        candidates.append(os.path.join(base, name))
            except Exception:
                pass
        by_name = "/dev/block/by-name"
        if os.path.isdir(by_name):
            try:
                for name in os.listdir(by_name):
                    if "usb" in name.lower() or "sd" in name.lower():
                        candidates.append(os.path.join(by_name, name))
            except Exception:
                pass
        if os.path.isdir("/storage"):
            for entry in os.listdir("/storage"):
                if entry in ("emulated", "self"):
                    continue
                full_path = os.path.join("/storage", entry)
                if os.path.isdir(full_path):
                    drives.append({
                        'DiskNumber': entry,
                        'Model': f'OTG Storage ({entry})',
                        'Size': 0, 'Letters': '',
                        'BusType': 'OTG', 'DevicePath': full_path,
                        'SerialNumber': '', 'PNPDeviceID': '',
                        'MountPoint': full_path,
                    })
        seen = set()
        for dev in candidates:
            real = os.path.realpath(dev) if os.path.exists(dev) else dev
            if real in seen:
                continue
            seen.add(real)
            try:
                size = 0
                try:
                    size = os.path.getsize(dev)
                except Exception:
                    size = 0
                drives.append({
                    'DiskNumber': os.path.basename(dev),
                    'Model': f'OTG ({os.path.basename(dev)})',
                    'Size': size, 'Letters': '',
                    'BusType': 'OTG',
                    'DevicePath': dev,
                    'SerialNumber': '', 'PNPDeviceID': '',
                    'MountPoint': '',
                })
            except Exception:
                continue
    except Exception:
        pass
    return drives

def get_usb_drives() -> List[Dict]:
    if IS_ANDROID or IS_TERMUX:
        otg = _get_usb_drives_android()
        if otg:
            return otg
        return _get_usb_drives_linux()
    if IS_WINDOWS:
        return _get_usb_drives_windows()
    elif IS_LINUX:
        return _get_usb_drives_linux()
    elif IS_MAC:
        return _get_usb_drives_mac()
    return []

def _get_usb_drives_windows() -> List[Dict]:
    drives = []
    ps_script = r"""
    $usbDisks = Get-CimInstance Win32_DiskDrive |
        Where-Object { $_.InterfaceType -eq 'USB' -and $_.Size -gt 1GB }
    $result = @()
    foreach ($disk in $usbDisks) {
        $partitions = Get-CimAssociatedInstance -InputObject $disk `
            -ResultClassName Win32_DiskPartition
        $letters = @()
        foreach ($part in $partitions) {
            $logicalDisks = Get-CimAssociatedInstance -InputObject $part `
                -ResultClassName Win32_LogicalDisk
            foreach ($ld in $logicalDisks) { $letters += $ld.DeviceID }
        }
        $result += [PSCustomObject]@{
            DiskNumber = $disk.Index
            Model = $disk.Model
            Size = $disk.Size
            Letters = ($letters -join ',')
            DevicePath = "\\.\PhysicalDrive$($disk.Index)"
            BusType = $disk.InterfaceType
            SerialNumber = $disk.SerialNumber
            PNPDeviceID = $disk.PNPDeviceID
        }
    }
    $result | ConvertTo-Json -Compress
    """
    result = run_hidden(['powershell', '-NoProfile', '-Command', ps_script],
                        timeout=30)
    output = (result.stdout or "").strip()
    if output:
        try:
            data = json.loads(output)
            if not isinstance(data, list):
                data = [data]
            for drive in data:
                if drive.get('BusType') == 'USB':
                    drive['SerialNumber'] = (drive.get('SerialNumber') or '').strip()
                    drive['PNPDeviceID'] = (drive.get('PNPDeviceID') or '').strip()
                    drives.append(drive)
            if drives:
                return drives
        except Exception:
            pass
    DRIVE_REMOVABLE = 2
    try:
        bitmask = ctypes.windll.kernel32.GetLogicalDrives()
        for i in range(26):
            if bitmask & (1 << i):
                letter = chr(65 + i)
                path = f"{letter}:\\"
                if ctypes.windll.kernel32.GetDriveTypeW(path) == DRIVE_REMOVABLE:
                    total = ctypes.c_ulonglong(0)
                    ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                        path, None, ctypes.byref(total), None)
                    if total.value < 128 * 1024**3:
                        drives.append({
                            'DiskNumber': -1,
                            'Model': f'Removível ({letter}:)',
                            'Size': total.value, 'Letters': letter,
                            'BusType': 'USB', 'DevicePath': f"\\\\.\\{letter}:",
                            'SerialNumber': '', 'PNPDeviceID': '',
                        })
    except Exception:
        pass
    return drives

def _get_usb_drives_linux() -> List[Dict]:
    drives = []
    result = run_hidden(
        ['lsblk', '-J', '-o',
         'NAME,TYPE,SIZE,MODEL,TRAN,SERIAL,ROTA,RM,HOTPLUG,SUBSYSTEMS'],
        timeout=10)
    if result.returncode != 0:
        result = run_hidden(
            ['lsblk', '-J', '-o', 'NAME,TYPE,SIZE,MODEL,TRAN,SERIAL'],
            timeout=10)
        if result.returncode != 0:
            return drives
    try:
        data = json.loads(result.stdout)
    except Exception:
        return drives
    for dev in data.get('blockdevices', []):
        if dev.get('type') != 'disk':
            continue
        name = dev.get('name', '')
        if not name.startswith('sd') and not name.startswith('mmc'):
            continue
        is_usb = (dev.get('tran') or '').lower() == 'usb'
        if not is_usb:
            try:
                rm_path = f"/sys/block/{name}/removable"
                if os.path.exists(rm_path):
                    with open(rm_path, 'r') as f:
                        if f.read().strip() == '1':
                            is_usb = True
            except Exception:
                pass
        if not is_usb:
            subs = (dev.get('subsystems') or '').lower()
            if 'usb' in subs:
                is_usb = True
        if not is_usb:
            continue
        size = _parse_size(dev.get('size', '0'))
        if size < 1024**3:
            continue
        serial = (dev.get('serial') or '').strip()
        if not serial:
            try:
                sp = f"/sys/block/{name}/device/serial"
                if os.path.exists(sp):
                    with open(sp, 'r') as f:
                        serial = f.read().strip()
            except Exception:
                pass
        drives.append({
            'DiskNumber': name,
            'Model': (dev.get('model') or 'Unknown USB').strip(),
            'Size': size, 'Letters': '', 'BusType': 'USB',
            'DevicePath': f"/dev/{name}", 'SerialNumber': serial,
            'PNPDeviceID': '',
        })
    return drives

def _get_usb_drives_mac() -> List[Dict]:
    drives = []
    r = run_hidden(['diskutil', 'list', '-plist', 'external', 'physical'],
                   timeout=15)
    if r.returncode != 0:
        r = run_hidden(['diskutil', 'list', '-plist'], timeout=15)
        if r.returncode != 0:
            return drives
    all_disks = []
    try:
        text = r.stdout or ""
        for m in re.findall(r'<string>(disk\d+)</string>', text):
            if m not in all_disks:
                all_disks.append(m)
    except Exception:
        pass
    for disk in all_disks:
        try:
            info = run_hidden(['diskutil', 'info', '-plist', disk], timeout=10)
            if info.returncode != 0 or not info.stdout:
                continue
            plist = info.stdout
            def _gs(k):
                m = re.search(rf'<key>{re.escape(k)}</key>\s*<string>([^<]*)</string>', plist)
                return m.group(1).strip() if m else ''
            def _gb(k):
                m = re.search(rf'<key>{re.escape(k)}</key>\s*<(true|false)/>', plist)
                return (m.group(1) == 'true') if m else False
            internal = _gb('Internal')
            removable = _gb('RemovableMedia')
            ejectable = _gb('Ejectable')
            bus_protocol = _gs('BusProtocol')
            media_name = _gs('MediaName')
            vol_name = _gs('VolumeName')
            serial = _gs('IOPlatformSerialNumber')
            dev_node = _gs('DeviceNode')
            if internal:
                continue
            is_usb = (bus_protocol.upper() == 'USB')
            if not (ejectable or removable or is_usb):
                continue
            total_size = 0
            m_size = re.search(r'<key>TotalSize</key>\s*<integer>(\d+)</integer>', plist)
            if m_size:
                try:
                    total_size = int(m_size.group(1))
                except Exception:
                    pass
            dev_path = dev_node if dev_node else f"/dev/{disk}"
            raw_path = dev_path.replace("/dev/disk", "/dev/rdisk")
            drives.append({
                'DiskNumber': disk,
                'Model': media_name or vol_name or 'USB Device',
                'Size': total_size, 'Letters': '',
                'BusType': 'USB' if is_usb else bus_protocol or 'External',
                'DevicePath': raw_path if os.path.exists(raw_path) else dev_path,
                'SerialNumber': serial, 'PNPDeviceID': '',
            })
        except Exception:
            continue
    return drives

def _scan_shell_all_platforms(log_func=None) -> list:
    """v3.6.1 - Varredura universal via shell."""
    found = []
    if IS_WINDOWS:
        try:
            ps = "Get-CimInstance Win32_DiskDrive | "
            ps += "Where-Object { $_.InterfaceType -eq 'USB' } | "
            ps += "Select-Object Index,Model,Size,InterfaceType,"
            ps += "SerialNumber,PNPDeviceID | ConvertTo-Json -Compress"
            r = run_hidden(["powershell", "-NoProfile", "-Command", ps],
                           timeout=30)
            if r.returncode == 0 and r.stdout.strip():
                import json as _j
                data = _j.loads(r.stdout)
                if not isinstance(data, list):
                    data = [data]
                for d in data:
                    found.append({
                        "DiskNumber": d.get("Index"),
                        "Model": (d.get("Model") or "?").strip(),
                        "Size": int(d.get("Size") or 0),
                        "Letters": "",
                        "BusType": "USB",
                        "DevicePath": "\\\\.\\PhysicalDrive" + str(d.get("Index")),
                        "SerialNumber": (d.get("SerialNumber") or "").strip(),
                        "PNPDeviceID": (d.get("PNPDeviceID") or "").strip(),
                    })
        except Exception:
            pass
    elif IS_LINUX or IS_TERMUX or IS_ANDROID:
        try:
            cmd = "lsblk -J -o NAME,TYPE,SIZE,MODEL,TRAN,SERIAL,RM 2>/dev/null"
            r = run_hidden(["sh", "-c", cmd], timeout=15)
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
                    try:
                        size = _parse_size(str(dev.get("size", "0")))
                    except Exception:
                        size = 0
                    found.append({
                        "DiskNumber": name,
                        "Model": (dev.get("model") or "Unknown USB").strip(),
                        "Size": size,
                        "Letters": "",
                        "BusType": "USB",
                        "DevicePath": "/dev/" + name,
                        "SerialNumber": (dev.get("serial") or "").strip(),
                        "PNPDeviceID": "",
                    })
        except Exception:
            pass
    if log_func:
        log_func("Varredura shell: " + str(len(found)) + " dispositivo(s).",
                 is_info=True)
    return found


def get_disk_number_by_letter(letter: str) -> int:
    if not IS_WINDOWS:
        return -1
    try:
        lc = letter.rstrip(':').strip()
        if not lc:
            return -1
        ps = f"(Get-Partition -DriveLetter {lc} | Get-Disk).Number"
        r = run_hidden(['powershell', '-NoProfile', '-Command', ps], timeout=10)
        if r.returncode == 0 and r.stdout.strip().isdigit():
            dn = int(r.stdout.strip())
            bus = run_hidden(
                ['powershell', '-NoProfile', '-Command',
                 f"(Get-Disk -Number {dn}).BusType"], timeout=5
            ).stdout.strip().upper()
            if bus == 'USB':
                return dn
    except Exception:
        pass
    return -1

# ==================================================================
# 9. FORMATAÇÃO
# ==================================================================
def format_usb(drive_info, filesystem, scheme, quick, log_func,
               cancel_flag, volume_label="DARKPENBOOT",
               align_override='Auto (1024 KB)',
               cluster_override='Auto'):
    try:
        safe_label = re.sub(r'[^A-Za-z0-9_\-]', '', str(volume_label))
        safe_label = safe_label.strip() or "DARKPENBOOT"
        safe_label = safe_label[:11]
    except Exception:
        safe_label = "DARKPENBOOT"
    filesystem = _normalize_fs(filesystem)
    if IS_WINDOWS:
        return _format_usb_windows(drive_info, filesystem, scheme, quick,
                                   log_func, cancel_flag, safe_label,
                                   align_override, cluster_override)
    elif IS_LINUX or IS_ANDROID or IS_TERMUX:
        return _format_usb_linux(drive_info, filesystem, scheme, quick,
                                 log_func, cancel_flag, safe_label)
    elif IS_MAC:
        return _format_usb_mac(drive_info, filesystem, scheme, quick,
                               log_func, cancel_flag, safe_label)
    log_func("❌ SO não suportado.", is_error=True)
    return None

def _format_usb_windows(drive_info, filesystem, scheme, quick,
                        log_func, cancel_flag, volume_label="DARKPENBOOT",
                        align_override='Auto (1024 KB)',
                        cluster_override='Auto'):
    disk_num = drive_info.get('DiskNumber', -1)
    if disk_num == -1 and drive_info.get('Letters'):
        letters = str(drive_info['Letters']).split(',')
        if letters:
            disk_num = get_disk_number_by_letter(letters[0])
            if disk_num != -1:
                drive_info['DiskNumber'] = disk_num
                drive_info['DevicePath'] = f"\\\\.\\PhysicalDrive{disk_num}"
    if disk_num == -1:
        log_func("❌ Disco físico não identificado.", is_error=True)
        return None
    if disk_num == 0:
        log_func("🚨 BLOQUEADO: disco 0 = sistema operacional!", is_error=True)
        return None
    if cancel_flag():
        return None
    size_gb = drive_info.get('Size', 0) / (1024**3)
    tier = _detect_usb_tier(drive_info)
    log_func(f"🎯 Alvo: Disco {disk_num} - {drive_info.get('Model', '?')}")
    log_func(f"📏 Tamanho: {size_gb:.2f} GB")
    log_func(f"⚡ Tier USB detectado: {tier}")
    log_func(f"🏷️  Rótulo: {volume_label}")
    try:
        ps_dismount = (
            f"Get-Partition -DiskNumber {disk_num} -ErrorAction SilentlyContinue | "
            f"Where-Object DriveLetter | "
            f"Remove-PartitionAccessPath -AccessPath $_.DriveLetter "
            f"-ErrorAction SilentlyContinue")
        run_hidden(['powershell', '-NoProfile', '-Command', ps_dismount],
                   timeout=30)
    except Exception:
        pass
    quick_flag = "quick" if quick else ""
    scheme_cmd = "convert gpt" if scheme == "GPT" else "convert mbr"
    active_cmd = "active" if scheme == "MBR" else ""

    if align_override == 'Auto (1024 KB)':
        align_val = "1024"
    else:
        align_val = align_override.replace(' KB', '').replace(' B', '').strip()
        if not align_val.isdigit():
            align_val = "1024"
    create_part = f"create partition primary align={align_val}"

    if cluster_override == 'Auto':
        unit_arg = "unit=65536" if size_gb > 32 else ""
    else:
        cluster_kb = cluster_override.replace(' KB', '').strip()
        try:
            unit_bytes = int(cluster_kb) * 1024
            unit_arg = f"unit={unit_bytes}"
        except Exception:
            unit_arg = ""

    filesystem = _normalize_fs(filesystem)
    fs_lower = filesystem.lower()
    if fs_lower == 'exfat':
        fs_lower = 'exfat'
    elif fs_lower == 'fat32':
        fs_lower = 'fat32'
    elif fs_lower == 'ntfs':
        fs_lower = 'ntfs'

    if fs_lower not in ('ntfs', 'fat32', 'exfat', 'refs'):
        log_func(f"⚠️  FS '{filesystem}' NÃO é nativo do Windows/diskpart.",
                 is_warning=True)
        log_func(f"🔄 Usando PowerShell com fallback para NTFS...", is_info=True)
        return _format_usb_windows_powershell(
            drive_info, 'NTFS', scheme, quick, log_func, volume_label)

    fmt_line = f'format fs={fs_lower} label="{volume_label}" {quick_flag}'
    if unit_arg and fs_lower in ('ntfs', 'exfat'):
        fmt_line += f' {unit_arg}'
    script = (
        f"select disk={disk_num}\n"
        f"attributes disk clear readonly\n"
        f"clean\n"
        f"{scheme_cmd}\n"
        f"{create_part}\n"
        f"select partition 1\n"
        f"{fmt_line}\n"
        f"{active_cmd}\n"
        f"assign\n"
        f"exit\n")
    log_func(f"🔧 Formatando disco {disk_num} como {filesystem} "
             f"(label: {volume_label}, scheme: {scheme}, align: {align_val})...")
    try:
        script_path = CONFIG_DIR / f'diskpart_{os.getpid()}_{int(time.time() * 1000)}.txt'
        with open(script_path, 'w', encoding='ascii', newline='\r\n') as f:
            f.write(script)
        letters_before = _get_all_drive_letters()
        result = run_hidden(['diskpart', '/s', script_path], timeout=300)
        try:
            if os.path.exists(script_path):
                os.remove(script_path)
        except Exception:
            pass
        stdout = (result.stdout or "").strip()
        stderr = (result.stderr or "").strip()
        if stdout:
            log_func("📤 Saída do diskpart:", is_info=True)
            for linha in stdout.splitlines():
                if linha.strip():
                    ll = linha.lower()
                    if "por cento" in ll or "percent" in ll:
                        continue
                    log_func(f"   {linha}", is_info=True)
        if stderr:
            log_func("📤 Erros do diskpart:", is_error=True)
            for linha in stderr.splitlines():
                if linha.strip():
                    log_func(f"   {linha}", is_error=True)
        ll = stdout.lower()
        tem_erro = (result.returncode != 0
                    or "erro do servi" in ll
                    or "virtual disk service error" in ll)
        if tem_erro:
            log_func(f"❌ diskpart reportou erro (código {result.returncode}).",
                     is_error=True)
            log_func("⚠️ Fallback PowerShell...", is_warning=True)
            return _format_usb_windows_powershell(
                drive_info, filesystem, scheme, quick, log_func, volume_label)
        log_func("⏳ Aguardando unidade ficar disponível...")
        for tentativa in range(45):
            if cancel_flag():
                return None
            la = _get_all_drive_letters()
            new_letters = la - letters_before
            for letter in new_letters:
                if os.path.exists(f"{letter}:\\"):
                    log_func(f"✅ Formatação concluída. Unidade: {letter}: "
                             f"(label: {volume_label})", is_success=True)
                    return f"{letter}:"
            if tentativa % 10 == 0 and tentativa > 0:
                log_func(f"   Aguardando... ({tentativa}s)", is_info=True)
            time.sleep(1)
        ps_get = (
            f"(Get-Partition -DiskNumber {disk_num} | "
            f"Where-Object DriveLetter | "
            f"Select-Object -First 1).DriveLetter")
        r = run_hidden(['powershell', '-NoProfile', '-Command', ps_get], timeout=10)
        letter = (r.stdout or "").strip()
        if letter and letter.isalpha():
            log_func(f"✅ Formatação concluída. Unidade: {letter}:",
                     is_success=True)
            return f"{letter}:"
        log_func("❌ Unidade não ficou disponível.", is_error=True)
        return None
    except Exception as e:
        log_func(f"❌ Erro ao executar diskpart: {e}", is_error=True)
        return None

def _format_usb_windows_powershell(drive_info, filesystem, scheme,
                                   quick, log_func,
                                   volume_label="DARKPENBOOT"):
    disk_num = drive_info.get('DiskNumber', -1)
    if disk_num == -1 or disk_num == 0:
        log_func("❌ Disco inválido para fallback.", is_error=True)
        return None
    filesystem = _normalize_fs(filesystem)
    fs = filesystem.upper()
    if fs == 'EXFAT':
        fs = 'exFAT'
    if fs not in ('NTFS', 'FAT32', 'EXFAT', 'REFS'):
        log_func(f"⚠️  PowerShell fallback não suporta {fs}. Usando NTFS.",
                 is_warning=True)
        fs = 'NTFS'
    scheme_arg = "MBR" if scheme == "MBR" else "GPT"
    ps_script = f'''
    try {{
        $disk = Get-Disk -Number {disk_num} -ErrorAction Stop
        if ($disk.PartitionStyle -ne 'RAW') {{
            Clear-Disk -Number {disk_num} -RemoveData -RemoveOEM `
                -Confirm:$false -ErrorAction SilentlyContinue
        }}
        $disk = Get-Disk -Number {disk_num} -ErrorAction Stop
        if ($disk.PartitionStyle -eq 'RAW') {{
            Initialize-Disk -Number {disk_num} `
                -PartitionStyle {scheme_arg} -ErrorAction Stop
        }}
        $parts = Get-Partition -DiskNumber {disk_num} -ErrorAction SilentlyContinue
        if (-not $parts -or $parts.Count -eq 0) {{
            $part = New-Partition -DiskNumber {disk_num} `
                -UseMaximumSize -AssignDriveLetter -Alignment 1024KB -ErrorAction Stop
        }} else {{
            $part = $parts | Select-Object -First 1
            if (-not $part.DriveLetter) {{
                $part | Add-PartitionAccessPath -AssignDriveLetter `
                    -ErrorAction SilentlyContinue
                Start-Sleep -Seconds 2
                $part = Get-Partition -DiskNumber {disk_num} | `
                    Where-Object DriveLetter | Select-Object -First 1
            }}
        }}
        $vol = Format-Volume -Partition $part -FileSystem {fs} `
            -NewFileSystemLabel "{volume_label}" -Confirm:$false -ErrorAction Stop
        if ($vol.DriveLetter) {{
            Write-Output "SUCESSO:$($vol.DriveLetter)"
        }} else {{ Write-Output "SUCESSO_SEM_LETRA" }}
    }} catch {{ Write-Output "ERRO: $($_.Exception.Message)" }}
    '''
    result = run_hidden(
        ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
         '-Command', ps_script], timeout=600)
    output = (result.stdout or "").strip()
    for linha in output.splitlines():
        if "ERRO:" in linha:
            log_func(f"   {linha}", is_error=True)
        elif "SUCESSO:" in linha or "SUCESSO_SEM_LETRA" in linha:
            log_func(f"   {linha}", is_success=True)
        elif linha.strip():
            log_func(f"   {linha}", is_info=True)
    if "SUCESSO:" in output:
        try:
            letter = output.split("SUCESSO:")[1].strip().split()[0]
            log_func(f"✅ Formatação via PowerShell: {letter}:", is_success=True)
            return f"{letter}:"
        except Exception:
            pass
    log_func("❌ Fallback PowerShell também falhou.", is_error=True)
    return None

def _format_usb_linux(drive_info, filesystem, scheme, quick,
                      log_func, cancel_flag, volume_label="DARKPENBOOT"):
    device = drive_info['DevicePath']
    # ── v3.6.1: garante ferramentas mkfs ──
    _ensure_linux_mkfs_tools(log_func)
    if cancel_flag():
        return None
    subprocess.run(f'umount {device}*', shell=True,
                   stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    label = 'gpt' if scheme == 'GPT' else 'msdos'
    if subprocess.run(['parted', '-s', device, 'mklabel', label]).returncode != 0:
        log_func("❌ Falha ao criar tabela.", is_error=True)
        return None
    if subprocess.run(
        ['parted', '-s', '-a', 'optimal', device, 'mkpart', 'primary', '0%', '100%']
    ).returncode != 0:
        log_func("❌ Falha ao criar partição.", is_error=True)
        return None
    time.sleep(2)
    part = f"{device}1"
    for _ in range(10):
        if os.path.exists(part):
            break
        time.sleep(1)
    vl = volume_label[:11]
    filesystem = _normalize_fs(filesystem)
    fs_key = filesystem.upper()
    cmds = {
        'FAT32': ['mkfs.vfat', '-F', '32', '-n', vl, part],
        'NTFS': ['mkfs.ntfs', '-Q', '-L', vl, part],
        'EXFAT': ['mkfs.exfat', '-n', vl, part],
        'EXT4': ['mkfs.ext4', '-L', vl, part],
        'EXT3': ['mkfs.ext3', '-L', vl, part],
        'EXT2': ['mkfs.ext2', '-L', vl, part]
    }
    if fs_key not in cmds:
        log_func(f"❌ FS {filesystem} não suportado.", is_error=True)
        return None
    mkfs_tool = cmds[fs_key][0]
    if shutil.which(mkfs_tool) is None:
        alternatives = {
            'mkfs.exfat': ['mkexfatfs'], 'mkfs.ntfs': ['mkntfs'],
            'mkfs.vfat': ['mkfs.fat', 'mkdosfs'], 'mkfs.ext4': ['mke2fs'],
        }
        found = False
        for alt in alternatives.get(mkfs_tool, []):
            if shutil.which(alt):
                cmds[fs_key][0] = alt
                found = True
                break
        if not found:
            log_func(f"❌ Ferramenta '{mkfs_tool}' não encontrada.", is_error=True)
            log_func(f"   💡 Instale: sudo apt install exfat-utils "
                     f"(exFAT) ou dosfstools (FAT32) ou ntfs-3g (NTFS)",
                     is_info=True)
            return None
    log_func(f"🔧 Formatando {device} como {filesystem} (label: {vl})...")
    r = subprocess.run(cmds[fs_key], capture_output=True, text=True)
    if r.returncode != 0:
        err = (r.stderr or r.stdout or '').strip()[:200]
        log_func(f"❌ Falha na formatação: {err}", is_error=True)
        return None
    mount_point = f"/media/darkpenboot_{int(time.time())}"
    os.makedirs(mount_point, exist_ok=True)
    if subprocess.run(['mount', part, mount_point]).returncode != 0:
        log_func("❌ Falha ao montar.", is_error=True)
        return None
    return mount_point

def _format_usb_mac(drive_info, filesystem, scheme, quick,
                    log_func, cancel_flag, volume_label="DARKPENBOOT"):
    device = drive_info['DevicePath']
    subprocess.run(['diskutil', 'unmountDisk', device], stderr=subprocess.DEVNULL)
    scheme_arg = 'GPT' if scheme == 'GPT' else 'MBR'
    vl = volume_label[:11]
    filesystem = _normalize_fs(filesystem)
    mac_fs_map = {
        'NTFS': 'NTFS', 'FAT32': 'MS-DOS FAT32', 'exFAT': 'ExFAT',
        'JHFS+': 'JHFS+', 'APFS': 'APFS',
    }
    mac_fs = mac_fs_map.get(filesystem, filesystem)
    cmd = ['diskutil', 'partitionDisk', device, '1', scheme_arg,
           mac_fs, vl, '100%']
    log_func(f"🔧 Formatando macOS como {mac_fs} (label: {vl})...")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        err = (r.stderr or r.stdout or '').strip()[:200]
        log_func(f"❌ Falha ao particionar: {err}", is_error=True)
        return None
    time.sleep(3)
    return f"/Volumes/{vl}"

# ==================================================================
# 10. VALIDAÇÃO ISO
# ==================================================================
def _validate_iso_file(iso_path: str, log_func=None) -> bool:
    try:
        iso_size = os.path.getsize(iso_path)
        if iso_size < 1024 * 1024:
            if log_func:
                log_func(f"❌ ISO muito pequena ({iso_size} bytes).", is_error=True)
            return False
        has_iso9660 = False
        try:
            with open(iso_path, 'rb') as f:
                f.seek(0x8001)
                if f.read(5) == b'CD001':
                    has_iso9660 = True
        except Exception:
            pass
        has_udf = False
        try:
            with open(iso_path, 'rb') as f:
                f.seek(32768)
                if f.read(5) in (b'BEA01', b'NSR02', b'NSR03'):
                    has_udf = True
        except Exception:
            pass
        if not (has_iso9660 or has_udf):
            if log_func:
                log_func("⚠️ Assinatura ISO9660/UDF não encontrada.", is_warning=True)
        if log_func:
            tipo = "ISO9660" if has_iso9660 else ("UDF" if has_udf else "desconhecido")
            log_func(f"✅ ISO validada: {iso_size / (1024**3):.2f} GB ({tipo})",
                     is_success=True)
        return True
    except Exception as e:
        if log_func:
            log_func(f"❌ Não foi possível ler a ISO: {e}", is_error=True)
        return False

def _detect_windows_iso(iso_path: str) -> Tuple[bool, str]:
    try:
        with open(iso_path, 'rb') as f:
            f.seek(0x8001)
            if f.read(5) == b'CD001':
                f.seek(0x8028)
                vol_raw = f.read(32)
                try:
                    vol_label = vol_raw.decode('ascii', errors='ignore')
                except Exception:
                    vol_label = ''
                vol_label = vol_label.strip().strip('\x00').strip()
                if vol_label:
                    vol_upper = vol_label.upper()
                    for prefix in ('CCCOMA', 'CPBA', 'CPRA', 'ESD-ISO',
                                   'GSP1', 'WIN10', 'WIN11', 'WINDOWS',
                                   'SSS_X64', 'SSS_X86'):
                        if vol_upper.startswith(prefix):
                            return True, vol_label
                    return False, vol_label
    except Exception:
        pass
    try:
        name_lower = os.path.basename(iso_path).lower()
        size_gb = os.path.getsize(iso_path) / (1024**3)
        if any(ind in name_lower for ind in ('win11', 'win10', 'windows',
                                              'win_', 'win-', 'server',
                                              'winserver', 'sql')) \
                and size_gb > 2.0:
            return True, os.path.basename(iso_path)
    except Exception:
        pass
    return False, ''

def _detect_linux_iso(iso_path: str) -> bool:
    try:
        name_lower = os.path.basename(iso_path).lower()
        for marker in ('ubuntu', 'debian', 'kali', 'parrot', 'fedora',
                       'mint', 'pop-os', 'manjaro', 'opensuse', 'arch',
                       'zorin', 'proxmox', 'truenas', 'nixos', 'linux',
                       'alma', 'rocky', 'centos', 'rhel', 'alpine',
                       'gentoo', 'void', 'slackware', 'solus',
                       'endeavour', 'garuda', 'elementary', 'tails'):
            if marker in name_lower:
                return True
    except Exception:
        pass
    try:
        with open(iso_path, 'rb') as f:
            f.seek(510)
            if f.read(2) == b'\x55\xAA':
                return True
    except Exception:
        pass
    return False

def _derive_volume_label(iso_path: str) -> str:
    try:
        try:
            with open(iso_path, 'rb') as f:
                f.seek(0x8001)
                if f.read(5) == b'CD001':
                    f.seek(0x8028)
                    raw = f.read(32)
                    label = raw.decode('ascii', errors='ignore')
                    label = label.strip().strip('\x00').strip()
                    label = re.sub(
                        r'-(amd64|x64|i386|i686|live|dvd|cd|installer|desktop|server)$',
                        '', label, flags=re.IGNORECASE)
                    clean = re.sub(r'[^A-Za-z0-9]', '', label).upper()
                    if clean and len(clean) >= 3:
                        return clean[:11]
        except Exception:
            pass
        base = os.path.splitext(os.path.basename(iso_path))[0]
        for suffix in ('-amd64', '-x64', '-x86', '-i386', '-i686',
                       '-desktop', '-server', '-live', '-installer',
                       '-dvd', '-cd', '-netinst', '_amd64', '_x64',
                       '_brazilianportuguese', '_portuguese'):
            if base.lower().endswith(suffix):
                base = base[:-len(suffix)]
        parts = re.split(r'[-_.]', base)
        parts = [p for p in parts if p and p.lower() not in
                 ('iso', 'v', 'ver', 'linux', 'os')]
        if parts:
            name = parts[0]
            extra = ''
            for p in parts[1:]:
                if re.match(r'^\d+(\.\d+)?$', p):
                    extra = re.sub(r'\.', '', p)
                    break
            clean = (name + extra).upper()
            clean = re.sub(r'[^A-Z0-9]', '', clean)
            if clean:
                return clean[:11]
        return "DARKPENBOOT"
    except Exception:
        return "DARKPENBOOT"

def _friendly_distro_name(iso_path: str) -> str:
    try:
        base = os.path.splitext(os.path.basename(iso_path))[0]
        for suffix in ('-amd64', '-x64', '-x86', '-i386', '-i686',
                       '-desktop', '-server', '-live', '-installer',
                       '-dvd', '-cd', '-netinst', '_amd64', '_x64'):
            if base.lower().endswith(suffix):
                base = base[:-len(suffix)]
        parts = re.split(r'[-_.]', base)
        parts = [p for p in parts if p and p.lower() not in
                 ('iso', 'v', 'ver', 'linux', 'os')]
        if not parts:
            return "DarkPenBoot"
        name = parts[0].capitalize()
        ver = ''
        for p in parts[1:]:
            if re.match(r'^\d+(\.\d+)?$', p):
                ver = ' ' + p
                break
        return name + ver
    except Exception:
        return "DarkPenBoot"

def _cleanup_stale_iso_mounts(log_func=None):
    if not IS_WINDOWS:
        return
    try:
        ps = r'''
        Get-DiskImage | Where-Object { $_.Attached } | ForEach-Object {
            try {
                Dismount-DiskImage -ImagePath $_.ImagePath -ErrorAction SilentlyContinue
                Write-Output "DESMONTOU:$($_.ImagePath)"
            } catch {
                Write-Output "ERRO:$($_.Exception.Message)"
            }
        }
        '''
        result = run_hidden(
            ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
             '-Command', ps], timeout=60)
        output = (result.stdout or "").strip()
        if log_func and output:
            for linha in output.splitlines():
                if "DESMONTOU:" in linha:
                    log_func(f"🧹 Montagem removida: {linha.split(':', 1)[1]}",
                             is_info=True)
    except Exception:
        pass

def _find_extractor_cascade() -> List[Tuple[str, str, List[str]]]:
    extractors = []
    for c in (r'C:\Program Files\7-Zip\7z.exe',
              r'C:\Program Files (x86)\7-Zip\7z.exe',
              shutil.which('7z'), shutil.which('7za'), shutil.which('7zr')):
        if c and os.path.exists(c):
            extractors.append(('7-Zip', c, []))
            break
    for c in (r'C:\Program Files\WinRAR\WinRAR.exe',
              r'C:\Program Files (x86)\WinRAR\WinRAR.exe',
              r'C:\Program Files\WinRAR\UnRAR.exe',
              r'C:\Program Files (x86)\WinRAR\UnRAR.exe',
              shutil.which('unrar'), shutil.which('rar')):
        if c and os.path.exists(c):
            extractors.append(('WinRAR', c, []))
            break
    for c in (shutil.which('bsdtar'), r'C:\Windows\System32\tar.exe',
              '/usr/bin/bsdtar'):
        if c and os.path.exists(c):
            extractors.append(('bsdtar', c, []))
            break
    for c in (shutil.which('tar'), '/bin/tar', '/usr/bin/tar'):
        if c and os.path.exists(c):
            extractors.append(('tar', c, []))
            break
    if IS_LINUX or IS_MAC or IS_ANDROID:
        for c in (shutil.which('7z'), shutil.which('7za'),
                  '/usr/bin/7z', '/usr/local/bin/7z'):
            if c and os.path.exists(c):
                if not any(e[0] == '7-Zip' for e in extractors):
                    extractors.append(('7-Zip', c, []))
                break
    return extractors

def _extract_iso_multi(iso_path: str, log_func=None,
                       dest_dir: Optional[str] = None) -> Optional[str]:
    if dest_dir is None:
        dest_dir = str(EXTRACT_DIR)
    os.makedirs(dest_dir, exist_ok=True)
    try:
        for item in os.listdir(dest_dir):
            ip = os.path.join(dest_dir, item)
            try:
                if os.path.isfile(ip) or os.path.islink(ip):
                    os.remove(ip)
                elif os.path.isdir(ip):
                    shutil.rmtree(ip, ignore_errors=True)
            except Exception:
                pass
    except Exception:
        pass
    extractors = _find_extractor_cascade()
    if not extractors:
        if log_func:
            log_func("❌ Nenhum extrator encontrado.", is_error=True)
            log_func("   💡 Windows: instale 7-Zip ou WinRAR.", is_info=True)
            log_func("   💡 Linux: sudo apt install p7zip-full", is_info=True)
        return None
    for name, exe, _ in extractors:
        if log_func:
            log_func(f"   🔧 Tentando extrair com: {name}", is_info=True)
        try:
            if name == '7-Zip':
                r = run_hidden([exe, 'x', iso_path, f'-o{dest_dir}',
                                '-y', '-bso0', '-bsp0'], timeout=3600)
                ok = (r.returncode == 0)
            elif name == 'WinRAR':
                if 'UnRAR' in exe:
                    r = run_hidden([exe, 'x', '-y', iso_path, dest_dir + os.sep],
                                   timeout=3600)
                else:
                    r = run_hidden([exe, 'x', '-y', '-ibck', iso_path,
                                    dest_dir + os.sep], timeout=3600)
                ok = (r.returncode == 0)
            elif name in ('bsdtar', 'tar'):
                r = run_hidden([exe, '-xf', iso_path, '-C', dest_dir],
                               timeout=3600)
                ok = (r.returncode == 0)
            else:
                ok = False
            if ok:
                try:
                    if os.listdir(dest_dir):
                        if log_func:
                            log_func(f"✅ ISO extraída com {name}", is_success=True)
                        return dest_dir
                except Exception:
                    pass
        except Exception as e:
            if log_func:
                log_func(f"   ⚠️ {name} erro: {e}", is_warning=True)
            continue
    return None

# ==================================================================
# 11. MONTAGEM DE ISO
# ==================================================================
def mount_iso(iso_path, log_func=None):
    iso_path = os.path.abspath(iso_path)
    if not os.path.exists(iso_path):
        if log_func:
            log_func("❌ ISO não encontrada.", is_error=True)
        return None
    if IS_WINDOWS:
        return _mount_iso_windows(iso_path, log_func)
    elif IS_LINUX or IS_ANDROID or IS_TERMUX:
        return _mount_iso_linux(iso_path, log_func)
    elif IS_MAC:
        return _mount_iso_mac(iso_path, log_func)
    return None

def _mount_iso_windows(iso_path: str, log_func) -> Optional[str]:
    iso_path = os.path.abspath(iso_path)
    if log_func:
        log_func("📀 Preparando montagem de ISO...", is_info=True)
    if not _validate_iso_file(iso_path, log_func):
        return None
    _cleanup_stale_iso_mounts(log_func)
    time.sleep(1)
    letters_before = _get_all_drive_letters()
    mount_ps = f'''
    try {{
        $img = Get-DiskImage -ImagePath "{iso_path}" -ErrorAction SilentlyContinue
        if ($img -and $img.Attached) {{
            Write-Output "JA_MONTADA"
        }} else {{
            Mount-DiskImage -ImagePath "{iso_path}" -ErrorAction Stop
            Start-Sleep -Milliseconds 500
            Write-Output "MONTADA_OK"
        }}
        exit 0
    }} catch {{
        Write-Output "ERRO: $($_.Exception.Message)"
        exit 1
    }}
    '''
    result = run_hidden(
        ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
         '-Command', mount_ps], timeout=120)
    output = (result.stdout or "").strip()
    if "ERRO:" in output:
        if log_func:
            log_func(f"⚠️ Mount-DiskImage falhou: {output}", is_warning=True)
        return _extract_iso_multi(iso_path, log_func)
    forced = _force_assign_letter_to_iso(iso_path, log_func)
    if forced:
        if log_func:
            log_func(f"✅ ISO montada em {forced}:", is_success=True)
        return f"{forced}:"
    new_letter = _wait_for_new_drive(letters_before, timeout=15, log_func=log_func)
    if new_letter:
        if log_func:
            log_func(f"✅ ISO montada em {new_letter}:", is_success=True)
        return f"{new_letter}:"
    return _extract_iso_multi(iso_path, log_func)

def _mount_iso_linux(iso_path, log_func):
    mount_point = f"/media/darkpenboot_iso_{int(time.time())}"
    os.makedirs(mount_point, exist_ok=True)
    result = subprocess.run(['mount', '-o', 'loop,ro', iso_path, mount_point],
                            capture_output=True, text=True)
    if result.returncode == 0:
        if log_func:
            log_func(f"✅ ISO montada em {mount_point}", is_success=True)
        return mount_point
    result = run_hidden(['udisksctl', 'loop-setup', '-f', iso_path], timeout=30)
    if result.returncode == 0:
        match = re.search(r'(/dev/loop\d+)', result.stdout or "")
        if match:
            loop_dev = match.group(1)
            for _ in range(10):
                time.sleep(1)
                mi = run_hidden(['findmnt', '-n', '-o', 'TARGET', loop_dev])
                target = (mi.stdout or "").strip()
                if target:
                    if log_func:
                        log_func(f"✅ ISO montada em {target}", is_success=True)
                    return target
    return _extract_iso_multi(iso_path, log_func)

def _mount_iso_mac(iso_path, log_func):
    result = subprocess.run(
        ['hdiutil', 'attach', iso_path, '-mountroot', '/Volumes', '-nobrowse'],
        capture_output=True, text=True)
    if result.returncode != 0:
        return _extract_iso_multi(iso_path, log_func)
    for line in result.stdout.splitlines():
        if '/Volumes/' in line:
            for p in line.split():
                if p.startswith('/Volumes/'):
                    if log_func:
                        log_func(f"✅ ISO montada em {p}", is_success=True)
                    return p
    return _extract_iso_multi(iso_path, log_func)

def dismount_iso(iso_path, log_func=None):
    try:
        iso_path = os.path.abspath(iso_path)
        if IS_WINDOWS:
            ps = f'''
            try {{
                $img = Get-DiskImage -ImagePath "{iso_path}" -ErrorAction SilentlyContinue
                if ($img -and $img.Attached) {{
                    Dismount-DiskImage -ImagePath "{iso_path}" -ErrorAction SilentlyContinue
                    Write-Output "OK"
                }} else {{ Write-Output "JA_DESMONTADA" }}
            }} catch {{ Write-Output "ERRO: $($_.Exception.Message)" }}
            '''
            r = run_hidden(
                ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                 '-Command', ps], timeout=60)
            output = (r.stdout or "").strip()
            if log_func and "OK" in output:
                log_func("🧹 ISO desmontada.", is_info=True)
        elif IS_LINUX or IS_ANDROID or IS_TERMUX:
            result = subprocess.run(['mount', '-l'], capture_output=True, text=True)
            for line in result.stdout.splitlines():
                if iso_path in line:
                    mp = line.split()[2]
                    subprocess.run(['umount', mp], capture_output=True)
                    if os.path.exists(mp):
                        try:
                            os.rmdir(mp)
                        except OSError:
                            pass
                    if log_func:
                        log_func("🧹 ISO desmontada.", is_info=True)
                    break
        elif IS_MAC:
            subprocess.run(['hdiutil', 'detach', iso_path], capture_output=True)
    except Exception as e:
        if log_func:
            log_func(f"⚠️ Aviso ao desmontar: {e}", is_warning=True)

# ==================================================================
# 12. CÓPIA DE ARQUIVOS
# ==================================================================
def _enumerate_files(src_dir: str) -> Tuple[List[Tuple[str, str]], int, int, List[str]]:
    files_list: List[Tuple[str, str]] = []
    empty_dirs: List[str] = []
    total_files = 0
    total_bytes = 0
    for root, dirs, files in os.walk(src_dir, followlinks=False):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        visible_files = [f for f in files if f not in SKIP_FILES]
        if not dirs and not visible_files:
            rel = os.path.relpath(root, src_dir)
            if rel and rel != '.':
                empty_dirs.append(rel)
        for f in files:
            if f in SKIP_FILES:
                continue
            src_file = os.path.join(root, f)
            rel_file = os.path.relpath(src_file, src_dir)
            try:
                if os.path.islink(src_file):
                    try:
                        size = os.path.getsize(src_file)
                    except OSError:
                        size = 0
                else:
                    size = os.path.getsize(src_file)
            except OSError:
                size = 0
            files_list.append((src_file, rel_file))
            total_files += 1
            total_bytes += size
    return files_list, total_files, total_bytes, empty_dirs

def _is_symlink_supported(dst_dir: str) -> bool:
    try:
        test_link = os.path.join(dst_dir, f".dptest_{os.getpid()}")
        test_target = os.path.join(dst_dir, f".dptgt_{os.getpid()}")
        try:
            with open(test_target, 'w') as f:
                f.write('x')
            try:
                os.symlink(test_target, test_link)
                return True
            except (OSError, NotImplementedError, AttributeError):
                return False
            finally:
                try:
                    if os.path.islink(test_link) or os.path.exists(test_link):
                        os.remove(test_link)
                except Exception:
                    pass
        finally:
            try:
                if os.path.exists(test_target):
                    os.remove(test_target)
            except Exception:
                pass
    except Exception:
        return False

def _copy_single_file(src: str, dst: str, retries: int = 3,
                      buf_size: int = COPY_BUFFER_SIZE,
                      cancel_flag=None,
                      allow_symlink: bool = True) -> bool:
    src_long = _long_path(src)
    dst_long = _long_path(dst)
    if os.path.islink(src_long):
        try:
            link_target = os.readlink(src_long)
        except OSError:
            link_target = None
        if allow_symlink and link_target is not None:
            for attempt in range(retries):
                try:
                    parent = os.path.dirname(dst_long)
                    if parent:
                        try:
                            os.makedirs(parent, exist_ok=True)
                        except OSError:
                            pass
                    if os.path.lexists(dst_long):
                        try:
                            if os.path.isdir(dst_long) and not os.path.islink(dst_long):
                                shutil.rmtree(dst_long, ignore_errors=True)
                            else:
                                os.remove(dst_long)
                        except OSError:
                            pass
                    os.symlink(link_target, dst_long)
                    return True
                except (OSError, NotImplementedError, AttributeError):
                    if attempt < retries - 1:
                        time.sleep(0.3)
                        continue
                    break
        try:
            if os.path.isdir(src_long):
                parent = os.path.dirname(dst_long)
                if parent:
                    try:
                        os.makedirs(parent, exist_ok=True)
                    except OSError:
                        pass
                try:
                    os.makedirs(dst_long, exist_ok=True)
                except OSError:
                    pass
                return True
        except OSError:
            pass
    if os.path.isdir(src_long):
        try:
            parent = os.path.dirname(dst_long)
            if parent:
                try:
                    os.makedirs(parent, exist_ok=True)
                except OSError:
                    pass
            os.makedirs(dst_long, exist_ok=True)
            return True
        except OSError:
            return False
    for attempt in range(retries):
        try:
            parent = os.path.dirname(dst_long)
            if parent:
                try:
                    os.makedirs(parent, exist_ok=True)
                except OSError:
                    pass
            if os.path.exists(dst_long) and not os.path.islink(dst_long):
                try:
                    if os.path.getsize(dst_long) == os.path.getsize(src_long):
                        return True
                except OSError:
                    pass
            with open(src_long, 'rb') as fsrc:
                with open(dst_long, 'wb') as fdst:
                    while True:
                        if cancel_flag and cancel_flag():
                            return False
                        buf = fsrc.read(min(buf_size, CANCEL_CHECK_INTERVAL))
                        if not buf:
                            break
                        fdst.write(buf)
            return True
        except (PermissionError, OSError):
            if attempt < retries - 1:
                time.sleep(0.5)
                continue
            raise
    return False

def _create_directories(dst_dir: str, dirs: List[str], log_func=None):
    if not dirs:
        return
    created = 0
    for rel in dirs:
        try:
            full = os.path.join(dst_dir, rel)
            os.makedirs(full, exist_ok=True)
            created += 1
        except Exception:
            pass
    if log_func and created:
        log_func(f"📁 {created} diretório(s) vazio(s) criado(s).", is_info=True)

def copy_files_with_progress(src_dir, dst_dir, file_cb, name_cb,
                             log_func, cancel_flag, filesystem,
                             buf_size: int = COPY_BUFFER_SIZE) -> bool:
    if not os.path.exists(src_dir):
        log_func(f"❌ Origem não existe: {src_dir}", is_error=True)
        return False
    if not os.path.exists(dst_dir):
        log_func(f"❌ Destino não existe: {dst_dir}", is_error=True)
        return False
    log_func("📊 Enumerando arquivos da ISO...", is_info=True)
    files_list, total_files, total_bytes, empty_dirs = _enumerate_files(src_dir)
    if total_files == 0:
        log_func("⚠️ Nenhum arquivo encontrado na ISO.", is_warning=True)
        return False
    log_func(f"📋 {total_files} arquivos (~{total_bytes / (1024**3):.2f} GB) "
             f"para copiar.", is_info=True)
    log_func(f"⚡ Buffer: {buf_size // (1024**2)} MB", is_info=True)
    if empty_dirs:
        log_func(f"📁 {len(empty_dirs)} diretório(s) vazio(s) detectado(s).",
                 is_info=True)
    free_space = _get_free_space(dst_dir)
    if free_space > 0:
        free_gb = free_space / (1024**3)
        req_gb = total_bytes / (1024**3)
        if free_space < total_bytes * 1.05:
            log_func(f"❌ Espaço insuficiente! ~{req_gb:.2f} GB necessário, "
                     f"{free_gb:.2f} GB disponível.", is_error=True)
            return False
        log_func(f"💽 Espaço: {free_gb:.2f} GB livres (necessário ~{req_gb:.2f} GB)",
                 is_info=True)
    fs_norm = _normalize_fs(filesystem).upper()
    fat_like = fs_norm in ('FAT32', 'EXFAT')
    case_insensitive = fs_norm in ('FAT32', 'EXFAT', 'NTFS')
    allow_symlink = _is_symlink_supported(dst_dir)
    if not allow_symlink:
        log_func("ℹ️ FS de destino não suporta symlinks — symlinks serão "
                 "copiados como arquivos regulares.", is_info=True)
    if fs_norm == 'FAT32':
        for src_file, rel_file in files_list:
            try:
                if os.path.getsize(_long_path(src_file)) > 4 * 1024**3:
                    log_func(f"❌ '{rel_file}' > 4GB (FAT32 não suporta).",
                             is_error=True)
                    return False
            except OSError:
                pass
    _create_directories(dst_dir, empty_dirs, log_func)
    log_func("🚀 Iniciando cópia...", is_success=True)
    start_time = time.time()
    processed = 0
    copied_bytes = 0
    failed_files: List[Tuple[str, str]] = []
    skipped_files: List[Tuple[str, str]] = []
    last_log_time = start_time
    seen_lower: Set[str] = set()
    for src_file, rel_file in files_list:
        if cancel_flag():
            log_func("⚠️ Cópia cancelada pelo usuário.", is_warning=True)
            return False
        if fat_like:
            try:
                rel_file_sanitized = _sanitize_fat_relpath(rel_file)
            except Exception:
                rel_file_sanitized = rel_file
        else:
            rel_file_sanitized = rel_file
        if case_insensitive:
            key = rel_file_sanitized.lower().replace('/', '\\')
            if key in seen_lower:
                skipped_files.append((rel_file, "duplicado em case-insensitive"))
                processed += 1
                if file_cb:
                    file_cb(processed, total_files)
                continue
            seen_lower.add(key)
        dst_file = os.path.join(dst_dir, rel_file_sanitized)
        if name_cb:
            name_cb(os.path.basename(rel_file_sanitized))
        try:
            file_size = os.path.getsize(_long_path(src_file)) \
                if os.path.exists(_long_path(src_file)) else 0
        except OSError:
            file_size = 0
        try:
            ok = _copy_single_file(
                src_file, dst_file,
                buf_size=buf_size,
                cancel_flag=cancel_flag,
                allow_symlink=allow_symlink)
            if not ok:
                if cancel_flag():
                    log_func("⚠️ Cópia cancelada pelo usuário.", is_warning=True)
                    return False
                failed_files.append((rel_file, "cópia retornou False"))
            else:
                copied_bytes += file_size
        except Exception as e:
            failed_files.append((rel_file, str(e)[:200]))
            log_func(f"⚠️ Falha: {rel_file} — {str(e)[:150]}", is_warning=True)
        processed += 1
        if file_cb:
            file_cb(processed, total_files)
        now = time.time()
        if (processed % 50 == 0) or (now - last_log_time >= 3):
            elapsed = now - start_time
            mb_copied = copied_bytes / (1024**2)
            mb_total = total_bytes / (1024**2)
            rate = mb_copied / elapsed if elapsed > 0 else 0
            pct = (copied_bytes / total_bytes * 100) if total_bytes > 0 else 0
            eta_sec = ((total_bytes - copied_bytes) / (rate * 1024**2)) \
                if rate > 0 else 0
            log_func(f"   [{processed}/{total_files}] {pct:.1f}% — "
                     f"{mb_copied:.0f}/{mb_total:.0f} MB — {rate:.1f} MB/s "
                     f"— ETA {_format_eta(eta_sec)}", is_info=True)
            last_log_time = now
    elapsed = time.time() - start_time
    log_func("─" * 60, is_info=True)
    log_func(f"✅ Cópia finalizada em {elapsed:.1f}s.", is_success=True)
    log_func(f"   Arquivos: {processed - len(failed_files)}/{total_files}",
             is_info=True)
    log_func(f"   Tamanho: {copied_bytes / (1024**3):.2f} GB", is_info=True)
    if skipped_files:
        log_func(f"ℹ️ {len(skipped_files)} arquivo(s) pulado(s) "
                 f"(duplicado em case-insensitive).", is_info=True)
    if failed_files:
        log_func(f"⚠️ {len(failed_files)} arquivo(s) falharam:", is_warning=True)
        for rel_file, err in failed_files[:20]:
            log_func(f"      • {rel_file}: {err}", is_warning=True)
        fail_ratio = len(failed_files) / max(1, total_files)
        if len(failed_files) > 10 and fail_ratio > 0.05:
            log_func(f"❌ Muitas falhas ({fail_ratio*100:.1f}%). Abortando.",
                     is_error=True)
            return False
        log_func("ℹ️ Falhas menores ignoradas — cópia considerada OK.",
                 is_info=True)
    return True

def verify_copy_completeness(src_dir: str, dst_dir: str, log_func) -> bool:
    log_func("🔍 Verificando integridade da cópia...", is_info=True)
    try:
        _, src_files, src_bytes, _ = _enumerate_files(src_dir)
    except Exception:
        src_files = src_bytes = 0
    dst_files = 0
    dst_bytes = 0
    for root, dirs, files in os.walk(dst_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            if f in SKIP_FILES:
                continue
            dst_files += 1
            try:
                dst_bytes += os.path.getsize(_long_path(os.path.join(root, f)))
            except OSError:
                pass
    log_func(f"   Origem:  {src_files} arq, {src_bytes / (1024**2):.1f} MB",
             is_info=True)
    log_func(f"   Destino: {dst_files} arq, {dst_bytes / (1024**2):.1f} MB",
             is_info=True)
    if dst_files < src_files:
        diff = src_files - dst_files
        log_func(f"ℹ️ {diff} arquivo(s) a menos (symlinks/duplicatas). OK.",
                 is_info=True)
    if src_bytes > 0 and abs(dst_bytes - src_bytes) > (src_bytes * 0.05):
        log_func("⚠️ Diferença de tamanho > 5% detectada.", is_warning=True)
        return False
    log_func("✅ Integridade OK!", is_success=True)
    return True

def inject_boot_sector(drive_letter, mounted_iso, log_func,
                       iso_path: Optional[str] = None) -> bool:
    if not IS_WINDOWS:
        return True
    bootsect = os.path.join(mounted_iso, "boot", "bootsect.exe")
    if not os.path.exists(bootsect):
        bootsect = os.path.join(
            os.environ.get('SystemRoot', 'C:\\Windows'),
            'System32', 'bootsect.exe')
    if os.path.exists(bootsect):
        result = run_hidden(
            [bootsect, '/nt60', f'{drive_letter}:', '/mbr', '/force'],
            timeout=60)
        if result.returncode == 0:
            log_func("✅ Setor de boot (bootsect) injetado.", is_success=True)
            return True
    if iso_path and os.path.exists(iso_path):
        if _apply_isohybrid_mbr(iso_path, drive_letter, log_func):
            return True
    log_func("⚠️ Nenhum boot sector injetado (isso é normal em alguns casos).",
             is_warning=True)
    return False

def _apply_isohybrid_mbr(iso_path: str, drive_letter: str,
                         log_func=None) -> bool:
    try:
        if log_func:
            log_func("🔧 Aplicando MBR isohybrid do Linux...", is_info=True)
        with open(iso_path, 'rb') as f:
            mbr = f.read(512)
        if len(mbr) < 512:
            return False
        if mbr[510:512] != b'\x55\xAA':
            if log_func:
                log_func("ℹ️ ISO não tem MBR isohybrid — pulando.", is_info=True)
            return False
        if IS_WINDOWS:
            disk_num = get_disk_number_by_letter(drive_letter)
            if disk_num < 0:
                if log_func:
                    log_func("⚠️ Não foi possível obter disco físico.", is_warning=True)
                return False
            tmp_mbr = CONFIG_DIR / f"_isohybrid_{os.getpid()}.bin"
            try:
                with open(tmp_mbr, 'wb') as f:
                    f.write(mbr)
                ps = f'''
                try {{
                    $bytes = [System.IO.File]::ReadAllBytes("{tmp_mbr}")
                    $handle = [System.IO.File]::Open(
                        "\\\\.\\PhysicalDrive{disk_num}",
                        [System.IO.FileMode]::Open,
                        [System.IO.FileAccess]::Write,
                        [System.IO.FileShare]::ReadWrite)
                    try {{
                        $handle.Write($bytes, 0, $bytes.Length)
                        $handle.Flush()
                        Write-Output "MBR_OK"
                    }} finally {{
                        $handle.Close()
                    }}
                }} catch {{
                    Write-Output "ERRO: $($_.Exception.Message)"
                }}
                '''
                r = run_hidden(
                    ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                     '-Command', ps], timeout=60)
                out = (r.stdout or '').strip()
                if "MBR_OK" in out:
                    if log_func:
                        log_func("✅ MBR isohybrid escrito no pendrive.",
                                 is_success=True)
                    return True
                if log_func:
                    log_func(f"⚠️ Falha MBR isohybrid: {out[:200]}", is_warning=True)
                return False
            finally:
                try:
                    tmp_mbr.unlink(missing_ok=True)
                except Exception:
                    pass
        else:
            dev = None
            for p in (f"/dev/disk{drive_letter}", f"/dev/{drive_letter}",
                      f"/dev/sd{drive_letter.lower()}",
                      f"/dev/{drive_letter.lower()}"):
                if os.path.exists(p):
                    dev = p
                    break
            if not dev:
                if log_func:
                    log_func(f"⚠️ Dispositivo para {drive_letter} não encontrado.",
                             is_warning=True)
                return False
            tmp_mbr = CONFIG_DIR / f"_isohybrid_{os.getpid()}.bin"
            try:
                with open(tmp_mbr, 'wb') as f:
                    f.write(mbr)
                r = subprocess.run(
                    ['dd', f'if={tmp_mbr}', f'of={dev}',
                     'bs=512', 'count=1', 'conv=notrunc'],
                    capture_output=True, timeout=30)
                if r.returncode == 0:
                    if log_func:
                        log_func("✅ MBR isohybrid escrito no pendrive.",
                                 is_success=True)
                    return True
            finally:
                try:
                    tmp_mbr.unlink(missing_ok=True)
                except Exception:
                    pass
            return False
    except Exception as e:
        if log_func:
            log_func(f"⚠️ Erro MBR isohybrid: {e}", is_warning=True)
        return False

# ==================================================================
# 13. ESCRITA DD
# ==================================================================
def _get_disk_number_from_device(device_path: str) -> Optional[int]:
    m = re.search(r'PhysicalDrive(\d+)', str(device_path), re.IGNORECASE)
    return int(m.group(1)) if m else None

def _rescan_devices(log_func=None, target_device: Optional[str] = None) -> None:
    try:
        if IS_WINDOWS:
            script_path = CONFIG_DIR / f"_rescan_{os.getpid()}_{int(time.time() * 1000)}.txt"
            try:
                with open(script_path, "w", encoding="ascii", newline="\r\n") as f:
                    f.write("rescan\nexit\n")
                run_hidden(["diskpart", "/s", str(script_path)], timeout=60)
            finally:
                try:
                    script_path.unlink(missing_ok=True)
                except Exception:
                    pass
            run_hidden(
                ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                 '-Command',
                 "Update-HostStorageCache; Start-Sleep -Milliseconds 300"],
                timeout=30)
            if log_func:
                log_func("🔄 Rescan Windows concluído.", is_info=True)
        elif IS_LINUX or IS_ANDROID or IS_TERMUX:
            run_hidden(["udevadm", "trigger", "--subsystem-match=block"], timeout=30)
            run_hidden(["udevadm", "settle", "--timeout=5"], timeout=15)
            if target_device and os.path.exists(target_device):
                run_hidden(["blockdev", "--rereadpt", target_device], timeout=15)
            run_hidden(["partprobe"], timeout=15)
        elif IS_MAC:
            run_hidden(["diskutil", "list"], timeout=15)
    except Exception as e:
        if log_func:
            log_func(f"⚠️ Aviso ao rescan: {e}", is_warning=True)

def _prepare_device_for_dd(device_path: str, log_func=None) -> bool:
    try:
        if IS_WINDOWS:
            disk_number = _get_disk_number_from_device(device_path)
            if disk_number is None:
                return False
            if disk_number == 0:
                if log_func:
                    log_func("🚨 BLOQUEADO: PhysicalDrive0.", is_error=True)
                return False
            ps_script = f'''
            $ErrorActionPreference = 'SilentlyContinue'
            try {{
                $parts = Get-Partition -DiskNumber {disk_number}
                foreach ($p in $parts) {{
                    if ($p.DriveLetter) {{
                        Remove-PartitionAccessPath -DiskNumber {disk_number} `
                            -PartitionNumber $p.PartitionNumber `
                            -AccessPath "$($p.DriveLetter):"
                    }}
                }}
                Start-Sleep -Milliseconds 800
                Update-HostStorageCache
                Start-Sleep -Milliseconds 300
                $d = Get-Disk -Number {disk_number}
                if ($d) {{
                    if ($d.IsReadOnly) {{ Set-Disk -Number {disk_number} -IsReadOnly $false }}
                    if (-not $d.IsOffline) {{ Set-Disk -Number {disk_number} -IsOffline $true }}
                    Start-Sleep -Milliseconds 800
                    Update-HostStorageCache
                    Start-Sleep -Milliseconds 500
                    if ((Get-Disk -Number {disk_number}).IsOffline) {{
                        Write-Output "OFFLINE_OK"
                    }} else {{
                        Write-Output "STILL_ONLINE"
                    }}
                }} else {{
                    Write-Output "SEM_DISK"
                }}
            }} catch {{
                Write-Output "ERRO: $($_.Exception.Message)"
            }}
            '''
            r = run_hidden(
                ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
                 '-Command', ps_script], timeout=90)
            out = (r.stdout or "").strip()
            offlined = "OFFLINE_OK" in out
            if not offlined:
                script = (f"select disk {disk_number}\n"
                          "attributes disk clear readonly\n"
                          "offline disk\n"
                          "exit\n")
                script_path = CONFIG_DIR / f"_dd_prepare_{os.getpid()}_{int(time.time() * 1000)}.txt"
                try:
                    with open(script_path, "w", encoding="ascii", newline="\r\n") as f:
                        f.write(script)
                    result = run_hidden(["diskpart", "/s", str(script_path)],
                                        timeout=90)
                    if result.returncode == 0:
                        offlined = True
                        time.sleep(0.5)
                        if log_func:
                            log_func(f"🔒 Disco {disk_number} offline (diskpart).",
                                     is_info=True)
                finally:
                    try:
                        script_path.unlink(missing_ok=True)
                    except Exception:
                        pass
            if offlined and log_func:
                log_func(f"🔒 Disco {disk_number} offline para DD.", is_info=True)
            return True
        if IS_LINUX or IS_ANDROID or IS_TERMUX:
            dev = device_path
            partitions = []
            lsblk = run_hidden(["lsblk", "-lnpo", "NAME,TYPE", dev], timeout=15)
            if lsblk.returncode == 0:
                for line in (lsblk.stdout or "").splitlines():
                    parts = line.split()
                    if len(parts) >= 2 and parts[1] in ("part", "lvm"):
                        partitions.append(parts[0])
            for part in partitions:
                r = run_hidden(["umount", part], timeout=30)
                if r.returncode != 0:
                    run_hidden(["umount", "-l", part], timeout=30)
            run_hidden(["umount", dev], timeout=15)
            run_hidden(["sync"], timeout=30)
            run_hidden(["blockdev", "--flushbufs", dev], timeout=15)
            run_hidden(["blockdev", "--rereadpt", dev], timeout=15)
            return True
        if IS_MAC:
            r = run_hidden(["diskutil", "unmountDisk", device_path], timeout=60)
            if r.returncode != 0:
                r = run_hidden(["diskutil", "unmountDisk", "force", device_path],
                               timeout=60)
            if r.returncode != 0:
                return False
            run_hidden(["sync"], timeout=30)
            return True
        return False
    except Exception as e:
        if log_func:
            log_func(f"❌ Falha ao preparar dispositivo: {e}", is_error=True)
        return False

def _keep_disk_offline_raw(disk_number: int, log_func=None):
    for _ in range(3):
        script = (f"select disk {disk_number}\n"
                  "attributes disk clear readonly\n"
                  "offline disk\n"
                  "exit\n")
        script_path = CONFIG_DIR / (
            f"_raw_{os.getpid()}_{int(time.time() * 1000)}.txt")
        try:
            with open(script_path, "w", encoding="ascii",
                      newline="\r\n") as f:
                f.write(script)
            r = run_hidden(["diskpart", "/s", str(script_path)], timeout=60)
            if r.returncode == 0:
                break
        finally:
            try:
                script_path.unlink(missing_ok=True)
            except Exception:
                pass
        time.sleep(1)
    if log_func:
        log_func("🔒 Disco mantido OFFLINE (formato RAW).", is_info=True)
        log_func("   💡 Use diskmgmt.msc para ativar manualmente.", is_info=True)

def _bring_online_and_assign(disk_number: int, log_func=None):
    online_ok = False
    for attempt in range(4):
        ps = f'''
        $ErrorActionPreference = 'SilentlyContinue'
        try {{
            Set-Disk -Number {disk_number} -IsOffline $false
            Set-Disk -Number {disk_number} -IsReadOnly $false
            Start-Sleep -Milliseconds 500
            Update-HostStorageCache
            Start-Sleep -Milliseconds 500
            $d = Get-Disk -Number {disk_number}
            if ($d -and -not $d.IsOffline) {{ Write-Output "ONLINE_OK" }}
            else {{ Write-Output "STILL_OFFLINE" }}
        }} catch {{ Write-Output "ERRO: $($_.Exception.Message)" }}
        '''
        r = run_hidden(
            ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass',
             '-Command', ps], timeout=60)
        if "ONLINE_OK" in (r.stdout or ""):
            online_ok = True
            break
        time.sleep(1.5)
    if not online_ok:
        script = (f"select disk {disk_number}\n"
                  "online disk\n"
                  "attributes disk clear readonly\n"
                  "exit\n")
        sp = CONFIG_DIR / f"_online_{os.getpid()}_{int(time.time()*1000)}.txt"
        try:
            with open(sp, "w", encoding="ascii", newline="\r\n") as f:
                f.write(script)
            r = run_hidden(["diskpart", "/s", str(sp)], timeout=60)
            if r.returncode == 0:
                online_ok = True
        finally:
            try:
                sp.unlink(missing_ok=True)
            except Exception:
                pass
    _rescan_devices(log_func)
    time.sleep(1.5)
    ps_check = f'''
    $parts = Get-Partition -DiskNumber {disk_number} -ErrorAction SilentlyContinue
    $found = $false
    foreach ($p in $parts) {{
        if ($p.DriveLetter) {{ Write-Output "HAS_LETTER:$($p.DriveLetter)"; $found = $true }}
    }}
    if (-not $found) {{ Write-Output "NO_LETTER" }}
    '''
    r = run_hidden(['powershell', '-NoProfile', '-Command', ps_check], timeout=20)
    out = (r.stdout or "").strip()
    if "HAS_LETTER:" in out:
        for line in out.splitlines():
            if "HAS_LETTER:" in line:
                letter = line.split(":")[1].strip()
                if log_func:
                    log_func(f"✅ Pendrive online com letra {letter}:",
                             is_success=True)
                return letter
    ps_assign = f'''
    try {{
        $parts = Get-Partition -DiskNumber {disk_number} -ErrorAction SilentlyContinue
        if (-not $parts) {{ Write-Output "NO_PARTS"; exit 0 }}
        foreach ($p in $parts) {{
            if (-not $p.DriveLetter) {{
                Add-PartitionAccessPath -DiskNumber {disk_number} `
                    -PartitionNumber $p.PartitionNumber `
                    -AssignDriveLetter -ErrorAction SilentlyContinue
            }}
        }}
        Start-Sleep -Seconds 2
        $parts = Get-Partition -DiskNumber {disk_number} -ErrorAction SilentlyContinue
        $assigned = $false
        foreach ($p in $parts) {{
            if ($p.DriveLetter) {{
                Write-Output "ASSIGNED:$($p.DriveLetter)"
                $assigned = $true
            }}
        }}
        if (-not $assigned) {{ Write-Output "NO_LETTER_ASSIGNED" }}
    }} catch {{ Write-Output "ERRO: $($_.Exception.Message)" }}
    '''
    r = run_hidden(['powershell', '-NoProfile', '-Command', ps_assign],
                   timeout=30)
    out = (r.stdout or "").strip()
    for line in out.splitlines():
        if "ASSIGNED:" in line:
            letter = line.split(":")[1].strip()
            if log_func:
                log_func(f"✅ Letra atribuída automaticamente: {letter}:",
                         is_success=True)
            return letter
    script = (f"select disk {disk_number}\n"
              "select partition 1\n"
              "assign\n"
              "exit\n")
    sp = CONFIG_DIR / f"_assign_{os.getpid()}_{int(time.time()*1000)}.txt"
    try:
        with open(sp, "w", encoding="ascii", newline="\r\n") as f:
            f.write(script)
        r = run_hidden(["diskpart", "/s", str(sp)], timeout=60)
        if r.returncode == 0:
            time.sleep(1.5)
            ps_get = (f"(Get-Partition -DiskNumber {disk_number} | "
                      f"Where-Object DriveLetter | "
                      f"Select-Object -First 1).DriveLetter")
            rr = run_hidden(['powershell', '-NoProfile', '-Command', ps_get],
                            timeout=15)
            letter = (rr.stdout or "").strip()
            if letter and letter.isalpha():
                if log_func:
                    log_func(f"✅ Letra atribuída via diskpart: {letter}:",
                             is_success=True)
                return letter
    finally:
        try:
            sp.unlink(missing_ok=True)
        except Exception:
            pass
    if log_func:
        log_func("⚠️ Não foi possível atribuir letra automaticamente.",
                 is_warning=True)
        log_func("   💡 Abra 'diskmgmt.msc' e atribua uma letra manualmente.",
                 is_info=True)
    return None

def _finalize_device_after_dd(device_path: str, log_func=None,
                              is_windows_iso: bool = False,
                              leave_raw: bool = False):
    try:
        if IS_WINDOWS:
            disk_number = _get_disk_number_from_device(device_path)
            if disk_number is None or disk_number == 0:
                return
            if leave_raw:
                _keep_disk_offline_raw(disk_number, log_func)
                return
            letter = _bring_online_and_assign(disk_number, log_func)
            if letter:
                if is_windows_iso and log_func:
                    log_func("ℹ️ ISO Windows: pendrive visível, mas o "
                             "conteúdo pode aparecer como RAW para o "
                             "Explorer (isso é normal em ISO Windows).",
                             is_info=True)
            else:
                if is_windows_iso and log_func:
                    log_func("ℹ️ ISO Windows em modo DD: disco pode ficar "
                             "em RAW. Use diskmgmt.msc se necessário.",
                             is_info=True)
        elif IS_LINUX or IS_ANDROID or IS_TERMUX:
            run_hidden(["sync"], timeout=30)
            _rescan_devices(log_func, target_device=device_path)
        elif IS_MAC:
            run_hidden(["diskutil", "mountDisk", device_path], timeout=60)
            _rescan_devices(log_func, target_device=device_path)
    except Exception as e:
        if log_func:
            log_func(f"⚠️ Não foi possível restaurar: {e}", is_warning=True)

def _open_raw_device(device_path: str):
    if IS_WINDOWS:
        GENERIC_READ = 0x80000000
        GENERIC_WRITE = 0x40000000
        FILE_SHARE_READ = 0x00000001
        FILE_SHARE_WRITE = 0x00000002
        OPEN_EXISTING = 3
        FILE_ATTRIBUTE_NORMAL = 0x80
        FILE_FLAG_WRITE_THROUGH = 0x80000000
        flags = FILE_ATTRIBUTE_NORMAL | FILE_FLAG_WRITE_THROUGH
        kernel32 = ctypes.windll.kernel32
        CreateFileW = kernel32.CreateFileW
        CreateFileW.restype = ctypes.c_void_p
        CreateFileW.argtypes = [
            ctypes.c_wchar_p, ctypes.c_uint32, ctypes.c_uint32,
            ctypes.c_void_p, ctypes.c_uint32, ctypes.c_uint32,
            ctypes.c_void_p,
        ]
        INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value
        handle = CreateFileW(
            str(device_path), GENERIC_READ | GENERIC_WRITE,
            FILE_SHARE_READ | FILE_SHARE_WRITE, None, OPEN_EXISTING,
            flags, None)
        if handle is None or handle == 0 or handle == INVALID_HANDLE_VALUE:
            err = ctypes.get_last_error()
            try:
                msg = ctypes.FormatError(err).strip()
            except Exception:
                msg = ""
            raise OSError(err, f"CreateFileW falhou para {device_path} "
                               f"(código {err}: {msg})")
        handle_value = ctypes.c_void_p(handle).value
        if handle_value is None:
            raise OSError("handle nulo retornado por CreateFileW")
        fd = msvcrt.open_osfhandle(int(handle_value),
                                    os.O_RDWR | os.O_BINARY)
        if fd < 0:
            raise OSError(f"open_osfhandle retornou fd inválido: {fd}")
        return os.fdopen(fd, "r+b", buffering=0)
    if IS_LINUX or IS_ANDROID or IS_TERMUX:
        direct_flag = getattr(os, 'O_DIRECT', 0)
        if direct_flag:
            try:
                fd = os.open(device_path, os.O_RDWR | direct_flag)
                return os.fdopen(fd, "r+b", buffering=0)
            except OSError:
                pass
        fd = os.open(device_path, os.O_RDWR)
        return os.fdopen(fd, "r+b", buffering=0)
    if IS_MAC:
        raw = device_path.replace("/dev/disk", "/dev/rdisk")
        if raw != device_path and os.path.exists(raw):
            fd = os.open(raw, os.O_RDWR)
            return os.fdopen(fd, "r+b", buffering=0)
        fd = os.open(device_path, os.O_RDWR)
        return os.fdopen(fd, "r+b", buffering=0)
    return open(device_path, "r+b", buffering=0)

def write_dd_image(iso_path: str, device_path: str,
                   progress_cb, name_cb, log_func, cancel_flag,
                   is_windows_iso: bool = False,
                   buf_size: int = DD_BUFFER_SIZE,
                   reopen_attempts_max: int = 5,
                   force_fsync: bool = True,
                   leave_raw: bool = False) -> bool:
    if not os.path.isfile(iso_path):
        log_func(f"❌ Imagem não encontrada: {iso_path}", is_error=True)
        return False
    if not device_path:
        log_func("❌ Dispositivo não definido.", is_error=True)
        return False
    total = os.path.getsize(iso_path)
    if total <= 0:
        log_func("❌ ISO vazia.", is_error=True)
        return False
    name_cb(os.path.basename(iso_path))
    log_func(f"📝 Gravando {total / (1024**3):.2f} GB via DD...", is_info=True)
    log_func(f"⚡ Buffer DD: {buf_size // (1024**2)} MB, "
             f"kill-check: {CANCEL_CHECK_INTERVAL // 1024} KB", is_info=True)
    if IS_WINDOWS and _get_disk_number_from_device(device_path) == 0:
        log_func("🚨 BLOQUEADO: disco do sistema.", is_error=True)
        return False
    prepared = False
    device = None
    success = False
    reopen_attempts = 0

    def _reopen():
        nonlocal device
        try:
            if device is not None:
                try:
                    device.close()
                except Exception:
                    pass
            time.sleep(1.0)
            _rescan_devices(log_func, target_device=device_path)
            device = _open_raw_device(device_path)
            try:
                device.seek(written)
            except Exception:
                pass
            return True
        except Exception as e:
            log_func(f"❌ Falha ao reabrir: {e}", is_error=True)
            return False
    try:
        if not _prepare_device_for_dd(device_path, log_func):
            return False
        prepared = True
        time.sleep(1.0)
        last_exc = None
        for attempt in range(5):
            try:
                device = _open_raw_device(device_path)
                break
            except Exception as exc:
                last_exc = exc
                if attempt < 4:
                    log_func(f"⚠️ Tentando novamente ({attempt + 2}/5)...",
                             is_warning=True)
                    time.sleep(1.2)
        if device is None:
            raise last_exc or OSError("Não foi possível abrir o dispositivo")
        start_time = time.time()
        last_log_time = start_time
        written = 0
        read_buffer = bytearray(buf_size)
        sub_chunk = CANCEL_CHECK_INTERVAL
        with open(iso_path, "rb", buffering=0) as src:
            while True:
                if cancel_flag():
                    log_func("⚠️ Gravação DD cancelada pelo usuário.",
                             is_warning=True)
                    return False
                n = src.readinto(read_buffer)
                if not n:
                    break
                offset = 0
                while offset < n:
                    if cancel_flag():
                        log_func("⚠️ Gravação DD cancelada pelo usuário.",
                                 is_warning=True)
                        return False
                    end = min(offset + sub_chunk, n)
                    view = memoryview(read_buffer)[offset:end]
                    while view:
                        if cancel_flag():
                            log_func("⚠️ Gravação DD cancelada pelo usuário.",
                                     is_warning=True)
                            return False
                        try:
                            w = device.write(view)
                            if not w:
                                raise OSError("Escrita retornou zero bytes")
                            reopen_attempts = 0
                        except OSError as e:
                            errno = getattr(e, 'errno', None)
                            if errno == 9:
                                reopen_attempts += 1
                                if reopen_attempts > reopen_attempts_max:
                                    log_func(
                                        f"❌ Dispositivo inacessível após "
                                        f"{reopen_attempts_max} tentativas.",
                                        is_error=True)
                                    return False
                                log_func(f"⚠️ Handle inválido "
                                         f"({reopen_attempts}/"
                                         f"{reopen_attempts_max}); reabrindo...",
                                         is_warning=True)
                                if not _reopen():
                                    return False
                                time.sleep(0.3)
                                continue
                            if len(view) > 8192:
                                half = len(view) // 2
                                half -= half % 4096
                                if half <= 0:
                                    half = len(view)
                                try:
                                    w = device.write(view[:half])
                                    if not w:
                                        raise OSError("Escrita parcial zero")
                                except OSError:
                                    raise
                            else:
                                raise
                        view = view[w:]
                        written += w
                    offset = end
                pct = min(100, int(written * 100 / total))
                progress_cb(pct)
                now = time.time()
                if now - last_log_time >= 2.5 or written >= total:
                    elapsed = now - start_time
                    mb_written = written / (1024**2)
                    rate = mb_written / elapsed if elapsed > 0 else 0.0
                    remaining = max(0, total - written)
                    eta = remaining / (rate * 1024**2) if rate > 0 else 0
                    log_func(f"   📊 {pct}% — {mb_written / 1024:.2f} GB — "
                             f"{rate:.1f} MB/s — ETA {_format_eta(eta)}",
                             is_info=True)
                    last_log_time = now
        try:
            device.flush()
            if force_fsync:
                os.fsync(device.fileno())
        except Exception as e:
            log_func(f"⚠️ Flush físico: {e}", is_warning=True)
        success = written == total
        if success:
            if IS_LINUX or IS_ANDROID or IS_TERMUX:
                run_hidden(["sync"], timeout=30)
            progress_cb(100)
            log_func("✅ Clonagem DD concluída.", is_success=True)
            if leave_raw:
                log_func("🔒 Modo RAW ativado: disco será mantido offline.",
                         is_info=True)
            else:
                log_func("🔄 Remontando pendrive automaticamente...",
                         is_info=True)
        else:
            log_func(f"❌ Gravação incompleta: {written} de {total}.", is_error=True)
        return success
    except PermissionError:
        log_func("❌ Acesso negado. Execute como admin/root.", is_error=True)
        return False
    except OSError as e:
        log_func(f"❌ Falha de E/S: {e}", is_error=True)
        return False
    except Exception as e:
        log_func(f"❌ Falha crítica: {e}", is_error=True)
        return False
    finally:
        try:
            if device is not None:
                device.close()
        except Exception:
            pass
        if prepared:
            _finalize_device_after_dd(device_path, log_func,
                                       is_windows_iso=is_windows_iso,
                                       leave_raw=leave_raw)

def verify_dd_write(iso_path: str, device_path: str, log_func,
                    cancel_flag, algo: str = 'sha256') -> bool:
    prepared = False
    device = None
    try:
        total = os.path.getsize(iso_path)
        log_func(f"🔍 Verificando gravação DD ({algo.upper()})...", is_info=True)
        iso_hash = hashlib.new(algo)
        with open(iso_path, "rb", buffering=0) as src:
            while True:
                if cancel_flag():
                    return False
                chunk = src.read(COPY_BUFFER_SIZE)
                if not chunk:
                    break
                iso_hash.update(chunk)
        if not _prepare_device_for_dd(device_path, log_func):
            return False
        prepared = True
        device = _open_raw_device(device_path)
        dev_hash = hashlib.new(algo)
        remaining = total
        while remaining > 0:
            if cancel_flag():
                return False
            chunk = device.read(min(COPY_BUFFER_SIZE, remaining))
            if not chunk:
                raise OSError("Leitura prematuramente encerrada")
            dev_hash.update(chunk)
            remaining -= len(chunk)
        src_digest = iso_hash.hexdigest()
        dst_digest = dev_hash.hexdigest()
        log_func(f"   ISO {algo.upper()}: {src_digest}", is_info=True)
        log_func(f"   USB {algo.upper()}: {dst_digest}", is_info=True)
        if src_digest != dst_digest:
            log_func(f"❌ Verificação DD: {algo.upper()} divergente.", is_error=True)
            return False
        log_func(f"✅ Verificação DD: {algo.upper()} OK.", is_success=True)
        return True
    except Exception as e:
        log_func(f"❌ Falha na verificação: {e}", is_error=True)
        return False
    finally:
        try:
            if device is not None:
                device.close()
        except Exception:
            pass
        if prepared:
            _finalize_device_after_dd(device_path, log_func)

def compute_checksums(iso_path, progress_cb=None) -> Dict[str, str]:
    hashes = {}
    for algo in ['md5', 'sha1', 'sha256', 'sha512', 'sha3_256', 'blake2b']:
        try:
            h = hashlib.new(algo)
        except Exception:
            continue
        with open(iso_path, 'rb') as f:
            while True:
                chunk = f.read(8192 * 1024)
                if not chunk:
                    break
                h.update(chunk)
        hashes[algo] = h.hexdigest()
        if progress_cb:
            progress_cb(algo, hashes[algo])
    return hashes

# ==================================================================
# 14. DOWNLOAD — SHA256 + Mirrors
# ==================================================================
def _sha256_file(filepath: str, progress_cb=None,
                 cancel_flag=None) -> Optional[str]:
    try:
        h = hashlib.sha256()
        total = os.path.getsize(filepath)
        done = 0
        last_report = 0.0
        with open(filepath, 'rb') as f:
            while True:
                if cancel_flag and cancel_flag():
                    return None
                chunk = f.read(8 * 1024 * 1024)
                if not chunk:
                    break
                h.update(chunk)
                done += len(chunk)
                now = time.time()
                if progress_cb and (now - last_report >= 1.0):
                    pct = int((done / total) * 100) if total > 0 else 0
                    progress_cb(pct, f"Verificando SHA256... {pct}%")
                    last_report = now
        return h.hexdigest()
    except Exception:
        return None

def verify_download_sha256(destino: str, distro_key: str,
                            log_func=None,
                            progress_cb=None,
                            cancel_flag=None) -> Tuple[bool, str]:
    info = DISTRO_INFO.get(distro_key, {})
    expected = (info.get("sha256") or "").strip().lower()
    if not expected:
        if log_func:
            log_func(f"ℹ️ Sem hash SHA256 registrado para '{distro_key}'. "
                     f"Verifique em: {info.get('docs', 'site oficial')}",
                     is_info=True)
        return True, "sem hash registrado"
    if log_func:
        log_func(f"🔐 Calculando SHA256 de {os.path.basename(destino)}...",
                 is_info=True)
    actual = _sha256_file(destino, progress_cb=progress_cb,
                          cancel_flag=cancel_flag)
    if actual is None:
        return False, "falha ao calcular hash (cancelado?)"
    if actual == expected:
        if log_func:
            log_func(f"✅ SHA256 OK: {actual}", is_success=True)
        return True, "hash OK"
    if log_func:
        log_func(f"❌ SHA256 DIVERGENTE", is_error=True)
        log_func(f"   Esperado: {expected}", is_error=True)
        log_func(f"   Obtido:   {actual}", is_error=True)
        log_func(f"   💡 Rebaixe de: {info.get('docs', 'site oficial')}",
                 is_info=True)
    return False, "hash divergente"

def _get_download_mirrors(distro_key: str, primary_url: str) -> List[str]:
    urls = [primary_url]
    if "Ubuntu" in distro_key:
        urls.append(primary_url.replace("releases.ubuntu.com",
                                         "mirrors.kernel.org/ubuntu-releases"))
    elif "Arch" in distro_key:
        urls.append("https://mirror.ufscar.br/archlinux/iso/latest/"
                    "archlinux-x86_64.iso")
    elif "Parrot" in distro_key:
        urls.append(primary_url.replace("parrot.elhacker.net",
                                        "deb.parrot.sh/parrot"))
    seen = set()
    out = []
    for u in urls:
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out

def _find_distro_key(url: str, destino: str) -> str:
    for key, info in DISTRO_INFO.items():
        if info.get("url") == url:
            return key
    candidates: Dict[str, List[str]] = {}
    for key, info in DISTRO_INFO.items():
        source_url = str(info.get("url") or "")
        filename = source_url.split("?", 1)[0].rstrip("/").rsplit("/", 1)[-1]
        if filename.lower().endswith(".iso"):
            candidates.setdefault(filename.lower(), []).append(key)
    for value in (url, destino):
        filename = str(value).split("?", 1)[0].rstrip("/").rsplit("/", 1)[-1]
        matches = candidates.get(filename.lower(), [])
        if len(matches) == 1:
            return matches[0]
    return ""

def get_remote_size(url: str) -> int:
    if shutil.which('curl'):
        try:
            result = run_hidden(
                ['curl', '-I', '-L', '-s', '--connect-timeout', '10',
                 '-A', BROWSER_UA, url],
                timeout=30)
            for line in (result.stdout or "").splitlines():
                if line.lower().startswith('content-length:'):
                    try:
                        return int(line.split(':', 1)[1].strip())
                    except ValueError:
                        pass
        except Exception:
            pass
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', BROWSER_UA)
        req.add_header('Accept', BROWSER_ACCEPT)
        req.add_header('Accept-Language', BROWSER_ACCEPT_LANG)
        with urllib.request.urlopen(req, timeout=15) as resp:
            cl = resp.headers.get('Content-Length')
            if cl:
                return int(cl)
    except Exception:
        pass
    return 0

def _log_download_error(log_func, method, err):
    if log_func:
        log_func(f"   ⚠️ {method} falhou: {err}", is_warning=True)

def download_with_curl(url, destino, progress_cb, cancel_flag,
                       log_func=None) -> bool:
    if not shutil.which('curl'):
        return False
    total = get_remote_size(url)
    cmd = [
        'curl', '-L', '--fail', '--show-error', '--retry', '3',
        '--retry-delay', '3',
        '--max-redirs', '10', '--connect-timeout', '30',
        '-A', BROWSER_UA, '-o', destino, url
    ]
    if os.path.exists(destino) and os.path.getsize(destino) > 0:
        cmd = [
            'curl', '-L', '--fail', '--show-error', '-C', '-', '--retry', '3',
            '--retry-delay', '3',
            '--max-redirs', '10', '--connect-timeout', '30',
            '-A', BROWSER_UA, '-o', destino, url
        ]
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        creationflags=CREATE_NO_WINDOW if IS_WINDOWS else 0)
    last_size = -1
    stalled_seconds = 0
    while proc.poll() is None:
        if cancel_flag():
            try:
                proc.terminate()
                time.sleep(0.5)
                if proc.poll() is None:
                    proc.kill()
                proc.wait(timeout=5)
            except Exception:
                pass
            if os.path.exists(destino):
                try:
                    os.remove(destino)
                except Exception:
                    pass
            return False
        if os.path.exists(destino):
            current = os.path.getsize(destino)
            if current == last_size:
                stalled_seconds += 1
            else:
                stalled_seconds = 0
                last_size = current
            if total > 0:
                pct = int((current / total) * 100)
                progress_cb(pct, f"Baixando... {pct}% "
                                  f"({_format_bytes(current)} de "
                                  f"{_format_bytes(total)})")
            else:
                progress_cb(0, f"Baixando... {_format_bytes(current)}")
            if stalled_seconds > 120:
                if log_func:
                    log_func("   ⚠️ curl estagnou — abortando.", is_warning=True)
                try:
                    proc.kill()
                    proc.wait(timeout=5)
                except Exception:
                    pass
                return False
        time.sleep(1)
    ok = proc.returncode == 0 and os.path.exists(destino) \
        and os.path.getsize(destino) > 1024 * 1024
    if not ok and log_func:
        err_out = b""
        try:
            err_out = (proc.stderr.read() if proc.stderr else b"") or b""
        except Exception:
            pass
        _log_download_error(log_func, "curl",
                            _safe_decode(err_out)[:200] or
                            f"returncode={proc.returncode}")
    if not ok and os.path.exists(destino):
        try:
            size_now = os.path.getsize(destino)
            if size_now < 1024 * 1024:
                os.remove(destino)
        except Exception:
            pass
    return ok

def download_with_wget(url, destino, progress_cb, cancel_flag,
                       log_func=None) -> bool:
    if not shutil.which('wget'):
        return False
    total = get_remote_size(url)
    cmd = [
        'wget', '--tries=3', '--timeout=30', '--waitretry=3',
        '--no-check-certificate', '--max-redirect=10',
        f'--user-agent={BROWSER_UA}',
        '-O', destino, url
    ]
    if os.path.exists(destino) and os.path.getsize(destino) > 0:
        cmd = [
            'wget', '-c', '--tries=3', '--timeout=30', '--waitretry=3',
            '--no-check-certificate', '--max-redirect=10',
            f'--user-agent={BROWSER_UA}',
            '-O', destino, url
        ]
    proc = subprocess.Popen(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        creationflags=CREATE_NO_WINDOW if IS_WINDOWS else 0)
    last_size = -1
    stalled_seconds = 0
    while proc.poll() is None:
        if cancel_flag():
            try:
                proc.terminate()
                time.sleep(0.5)
                if proc.poll() is None:
                    proc.kill()
                proc.wait(timeout=5)
            except Exception:
                pass
            if os.path.exists(destino):
                try:
                    os.remove(destino)
                except Exception:
                    pass
            return False
        if os.path.exists(destino):
            current = os.path.getsize(destino)
            if current == last_size:
                stalled_seconds += 1
            else:
                stalled_seconds = 0
                last_size = current
            if total > 0:
                pct = int((current / total) * 100)
                progress_cb(pct, f"Baixando (wget)... {pct}% "
                                  f"({_format_bytes(current)} de "
                                  f"{_format_bytes(total)})")
            else:
                progress_cb(0, f"Baixando (wget)... {_format_bytes(current)}")
            if stalled_seconds > 120:
                if log_func:
                    log_func("   ⚠️ wget estagnou — abortando.", is_warning=True)
                try:
                    proc.kill()
                    proc.wait(timeout=5)
                except Exception:
                    pass
                return False
        time.sleep(1)
    ok = proc.returncode == 0 and os.path.exists(destino) \
        and os.path.getsize(destino) > 1024 * 1024
    if not ok and log_func:
        err_out = b""
        try:
            err_out = (proc.stderr.read() if proc.stderr else b"") or b""
        except Exception:
            pass
        _log_download_error(log_func, "wget",
                            _safe_decode(err_out)[:200] or
                            f"returncode={proc.returncode}")
    return ok

def download_with_urllib(url, destino, progress_cb, cancel_flag,
                         log_func=None) -> bool:
    def _do_download(verify_ssl: bool = True):
        total = get_remote_size(url)
        headers = {
            'User-Agent': BROWSER_UA,
            'Accept': BROWSER_ACCEPT,
            'Accept-Language': BROWSER_ACCEPT_LANG,
            'Accept-Encoding': 'identity',
            'Connection': 'keep-alive',
        }
        existing = 0
        if os.path.exists(destino):
            existing = os.path.getsize(destino)
            if existing > 0:
                headers['Range'] = f'bytes={existing}-'
        req = urllib.request.Request(url, headers=headers)
        if not verify_ssl:
            try:
                import ssl
                ctx = ssl.create_default_context()
                ctx.check_hostname = False
                ctx.verify_mode = ssl.CERT_NONE
                opener = urllib.request.build_opener(
                    urllib.request.HTTPSHandler(context=ctx))
                resp_obj = opener.open(req, timeout=30)
            except Exception:
                resp_obj = urllib.request.urlopen(req, timeout=30)
        else:
            resp_obj = urllib.request.urlopen(req, timeout=30)
        with resp_obj as resp:
            status = getattr(resp, 'status', 200)
            if status < 200 or status >= 300:
                raise urllib.error.HTTPError(
                    url, status, f"HTTP {status}", resp.headers, None)
            content_length = resp.headers.get('Content-Length')
            if content_length:
                cl = int(content_length)
                if status == 206:
                    total = existing + cl
                else:
                    total = cl
            mode = 'ab' if existing > 0 and status == 206 else 'wb'
            downloaded = existing if mode == 'ab' else 0
            last_log = 0
            with open(destino, mode) as f:
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
                    try:
                        chunk = resp.read(1024 * 1024)
                    except Exception:
                        break
                    if not chunk:
                        break
                    f.write(chunk)
                    downloaded += len(chunk)
                    now = time.time()
                    if now - last_log >= 1:
                        if total > 0:
                            pct = int((downloaded / total) * 100)
                            progress_cb(pct, f"Baixando (urllib)... {pct}% "
                                              f"({_format_bytes(downloaded)} de "
                                              f"{_format_bytes(total)})")
                        else:
                            progress_cb(0, f"Baixando (urllib)... "
                                            f"{_format_bytes(downloaded)}")
                        last_log = now
        return os.path.exists(destino) and os.path.getsize(destino) > 0
    try:
        ok = _do_download(verify_ssl=True)
        if ok:
            return True
    except Exception as e:
        if log_func:
            log_func(f"   ⚠️ urllib (SSL verificado): {e}", is_warning=True)
    try:
        if os.path.exists(destino):
            try:
                if os.path.getsize(destino) < 1024 * 1024:
                    os.remove(destino)
            except Exception:
                pass
        return _do_download(verify_ssl=False)
    except Exception as e:
        if log_func:
            log_func(f"   ⚠️ urllib (SSL inseguro): {e}", is_warning=True)
        return False

def download_with_fallback(url, destino, progress_cb, cancel_flag,
                            log_func=None) -> bool:
    if log_func:
        log_func(f"⬇️ Iniciando download: {url}", is_info=True)
    methods = []
    if shutil.which('curl'):
        methods.append(('curl', download_with_curl))
    if shutil.which('wget'):
        methods.append(('wget', download_with_wget))
    methods.append(('urllib', download_with_urllib))
    last_error = None
    distro_key = _find_distro_key(url, destino)
    urls = _get_download_mirrors(distro_key, url) if distro_key else [url]
    for attempt_url in urls:
        if cancel_flag():
            return False
        if attempt_url != url and log_func:
            log_func(f"🌐 Tentando mirror: {attempt_url}", is_info=True)
        for name, fn in methods:
            if cancel_flag():
                return False
            if log_func:
                log_func(f"🔧 Tentando via {name}...", is_info=True)
            try:
                try:
                    ok = fn(attempt_url, destino, progress_cb,
                            cancel_flag, log_func)
                    
                except TypeError:
                    ok = fn(attempt_url, destino, progress_cb, cancel_flag)
                if cancel_flag():
                    return False
                if not ok:
                    last_error = f"{name} falhou"
                    continue
                size = os.path.getsize(destino)
                head, info = _inspect_file_bytes(destino, 512)
                head_lower = head.lstrip().lower()
                if head_lower.startswith((b"<!doctype", b"<html",
                                          b"<?xml", b"<head")):
                    if log_func:
                        log_func(f"❌ Download inválido: {info}",
                                 is_error=True)
                    os.remove(destino)
                    last_error = f"{name}: resposta HTML/XML"
                    continue
                if size < MIN_ISO_SIZE:
                    if log_func:
                        log_func(f"❌ Download inválido: {_format_bytes(size)}.",
                                 is_error=True)
                        log_func(info, is_error=True)
                    os.remove(destino)
                    last_error = f"{name}: arquivo muito pequeno"
                    continue
                if distro_key:
                    ok_hash, hash_msg = verify_download_sha256(
                        destino, distro_key, log_func,
                        progress_cb=progress_cb, cancel_flag=cancel_flag)
                    if not ok_hash:
                        parcial = destino + ".parcial"
                        try:
                            os.rename(destino, parcial)
                        except Exception:
                            pass
                        last_error = f"{name}: {hash_msg}"
                        continue
                if log_func:
                    log_func(f"✅ Download concluído via {name}.",
                             is_success=True)
                return True
            except Exception as e:
                last_error = f"{name}: {e}"
                if log_func:
                    log_func(f"⚠️ {name} erro: {e}", is_warning=True)
                continue
    if log_func:
        log_func(f"❌ Todos os métodos falharam. Último erro: {last_error or '?'}",
                 is_error=True)
    return False

# ==================================================================
# 15. TOOLTIP
# ==================================================================
class ToolTip:
    def __init__(self, widget, text_getter, delay=500, wraplength=300, margin=12):
        self.widget = widget
        self.text_getter = text_getter
        self.delay = delay
        self.wraplength = wraplength
        self.margin = margin
        self._after_id = None
        self._tip = None
        self._visible = False
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<ButtonPress>", self._hide, add="+")
        widget.bind("<Destroy>", self._hide, add="+")

    def _schedule(self, event=None):
        self._cancel()
        try:
            self._after_id = self.widget.after(self.delay, self._show)
        except Exception:
            pass

    def _cancel(self):
        if self._after_id is not None:
            try:
                self.widget.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None

    def _show(self):
        if self._visible:
            return
        try:
            if not self.widget.winfo_exists():
                return
            raw_text = (self.text_getter() if callable(self.text_getter)
                        else self.text_getter)
            text = str(raw_text) if raw_text is not None else ""
        except Exception:
            text = None
        if not text:
            return
        try:
            tip = tk.Toplevel(self.widget)
            tip.wm_overrideredirect(True)
            tip.configure(bg=COLORS['frame_border'])
            try:
                tip.attributes("-topmost", True)
            except Exception:
                pass
            outer = tk.Frame(tip, bg=COLORS['frame_border'], bd=0,
                             highlightthickness=1,
                             highlightbackground=COLORS['accent'])
            outer.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)
            lbl = tk.Label(outer, text=text, justify=tk.LEFT,
                           bg=COLORS['frame_bg'], fg=COLORS['fg'],
                           font=('Segoe UI', 9), padx=10, pady=7,
                           wraplength=self.wraplength)
            lbl.pack()
            tip.update_idletasks()
            tip_w = tip.winfo_reqwidth()
            tip_h = tip.winfo_reqheight()
            screen_w = tip.winfo_screenwidth()
            screen_h = tip.winfo_screenheight()
            m = self.margin
            wx = self.widget.winfo_rootx()
            wy = self.widget.winfo_rooty()
            wh = self.widget.winfo_height()
            x = wx + 12
            y = wy + wh + 6
            if x + tip_w > screen_w - m:
                x = screen_w - tip_w - m
            if x < m:
                x = m
            if y + tip_h > screen_h - m:
                y_above = wy - tip_h - 6
                if y_above >= m:
                    y = y_above
                else:
                    y = screen_h - tip_h - m
            if y < m:
                y = m
            x = max(m, min(x, screen_w - tip_w - m))
            y = max(m, min(y, screen_h - tip_h - m))
            tip.wm_geometry(f"+{x}+{y}")
            self._tip = tip
            self._visible = True
        except Exception:
            try:
                if self._tip is not None:
                    self._tip.destroy()
            except Exception:
                pass
            self._tip = None
            self._visible = False

    def _hide(self, event=None):
        self._cancel()
        if self._tip is not None:
            try:
                self._tip.destroy()
            except Exception:
                pass
            self._tip = None
        self._visible = False

# ==================================================================
# 16. NEON THEME BALL — v3.6.0 (com ciclo de cores dos temas)
# ==================================================================
class NeonThemeBall(tk.Canvas):
    def __init__(self, parent, theme_labels, current_label, on_change, size=44):
        try:
            bg = parent.cget('bg')
        except Exception:
            bg = COLORS['bg']
        super().__init__(parent, width=size, height=size,
                         highlightthickness=2,
                         highlightbackground=bg,
                         highlightcolor=COLORS['accent'],
                         bg=bg, takefocus=True)
        self._size = size
        self._phase = 0
        self._trail_phase = 0.0
        self._anim_id = None
        self._theme_labels = list(theme_labels)
        self._current_label = current_label
        self._on_change = on_change
        self._menu_open = False
        self._writing = False
        self._focused = False
        self._focus_phase = 0
        self._focus_anim_id = None
        _PULSE_SUBSCRIBERS.append(self)
        self.bind('<Button-1>', self._show_menu)
        self.bind('<Enter>', lambda e: self.configure(cursor='hand2'))
        self.bind('<Leave>', lambda e: self.configure(cursor=''))
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)
        self.bind('<Return>', self._on_key_activate)
        self.bind('<KP_Enter>', self._on_key_activate)
        self.bind('<space>', self._on_key_activate)
        self.bind('<Tab>', self._on_tab_forward)
        self.bind('<Shift-Tab>', self._on_tab_backward)
        self.bind('<ISO_Left_Tab>', self._on_tab_backward)
        self._start_anim()

    def _on_tab_forward(self, e):
        try:
            nxt = self.tk_focusNext()
            if nxt:
                nxt.focus_set()
        except Exception:
            pass
        return "break"

    def _on_tab_backward(self, e):
        try:
            prv = self.tk_focusPrev()
            if prv:
                prv.focus_set()
        except Exception:
            pass
        return "break"

    def _on_focus_in(self, e):
        self._focused = True
        self._start_focus_anim()
        self._update_highlight()
        self._draw()

    def _on_focus_out(self, e):
        self._focused = False
        self._stop_focus_anim()
        self._update_highlight()
        self._draw()

    def _update_highlight(self):
        try:
            if self._focused:
                self.configure(highlightbackground=COLORS['accent'],
                               highlightcolor=COLORS['accent'],
                               highlightthickness=2)
            else:
                try:
                    parent_bg = self.master.cget('bg')
                except Exception:
                    parent_bg = COLORS['bg']
                self.configure(highlightbackground=parent_bg,
                               highlightcolor=parent_bg,
                               highlightthickness=0)
        except Exception:
            pass

    def _start_focus_anim(self):
        if self._focus_anim_id is not None:
            return
        def tick():
            try:
                self._focus_phase = (self._focus_phase + 1) % 16
                self._draw()
                self._focus_anim_id = self.after(120, tick)
            except Exception:
                self._focus_anim_id = None
        self._focus_anim_id = self.after(120, tick)

    def _stop_focus_anim(self):
        if self._focus_anim_id is not None:
            try:
                self.after_cancel(self._focus_anim_id)
            except Exception:
                pass
            self._focus_anim_id = None

    def _on_key_activate(self, e):
        try:
            x = self.winfo_rootx() + self._size // 2
            y = self.winfo_rooty() + self._size
            ev = type('Event', (), {'x_root': x, 'y_root': y})()
            self._show_menu(ev)
        except Exception:
            pass
        return "break"

    def _hex_to_rgb(self, h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _pulse(self, base, phase, amp=90):
        try:
            r, g, b = self._hex_to_rgb(base)
        except Exception:
            r, g, b = 0, 255, 255
        off = int(amp * (0.5 + 0.5 * math.sin(phase * math.pi / 8)))
        return (f"#{min(255, max(0, r + off)):02x}"
                f"{min(255, max(0, g + off)):02x}"
                f"{min(255, max(0, b + off)):02x}")

    def _lerp_rgb(self, a, b, t):
        t = max(0.0, min(1.0, t))
        return (int(a[0] + (b[0] - a[0]) * t),
                int(a[1] + (b[1] - a[1]) * t),
                int(a[2] + (b[2] - a[2]) * t))

    def _start_anim(self):
        if self._anim_id is not None:
            try:
                self.after_cancel(self._anim_id)
            except Exception:
                pass
            self._anim_id = None
        if not (GLOBAL_PULSE_STATE['active'] or self._writing or
                REACTIVE_PULSE_STATE['active']):
            self._draw()
            return
        if REACTIVE_PULSE_STATE['active']:
            interval = {0: 40, 1: 32, 2: 22, 3: 14}.get(
                REACTIVE_PULSE_STATE['intensity'], 22)
        else:
            interval = 35 if self._writing else 55
        def tick():
            try:
                self._phase = (self._phase + 1) % 32
                self._trail_phase = (self._trail_phase + 0.35) % (2 * math.pi)
                self._draw()
                self._anim_id = self.after(interval, tick)
            except Exception:
                self._anim_id = None
        self._anim_id = self.after(interval, tick)

    def set_writing_mode(self, writing: bool):
        if self._writing == writing:
            return
        self._writing = writing
        self._start_anim()

    def set_global_pulse(self, active: bool):
        self._start_anim()

    def _stop_anim(self):
        if self._anim_id is not None:
            try:
                self.after_cancel(self._anim_id)
            except Exception:
                pass
            self._anim_id = None

    def _draw(self):
        try:
            self.delete('all')
        except Exception:
            return
        s = self._size
        cx = cy = s / 2.0
        r_base = s / 2.0 - 7.0
        global_on = GLOBAL_PULSE_STATE['active']
        reactive_on = REACTIVE_PULSE_STATE['active']
        if (reactive_on and time.time() * 1000 >
                REACTIVE_PULSE_STATE['until_ts']):
            REACTIVE_PULSE_STATE['active'] = False
            REACTIVE_PULSE_STATE['intensity'] = 0
            reactive_on = False
        if reactive_on:
            gp = REACTIVE_PULSE_STATE['phase']
        elif global_on:
            gp = GLOBAL_PULSE_STATE['phase']
        else:
            gp = self._phase

        # ── v3.6.0: Orb OSCILA por todas as cores dos temas quando ativo ──
        if GLOBAL_PULSE_STATE.get('color_cycle_phase', 0) > 0:
            try:
                theme_keys_cycle = list(THEMES_RAW.keys())
                if theme_keys_cycle:
                    base_key = theme_keys_cycle[
                        GLOBAL_PULSE_STATE.get('color_cycle_index', 0)
                        % len(theme_keys_cycle)
                    ]
                    base_theme = THEMES_RAW[base_key]
                    acc_rgb = self._hex_to_rgb(
                        base_theme.get('accent', '#00ff41'))
                    acc2_rgb = self._hex_to_rgb(
                        base_theme.get('accent2', '#00ccff'))
                else:
                    acc_rgb = self._hex_to_rgb(
                        COLORS.get('accent', '#00ff41'))
                    acc2_rgb = self._hex_to_rgb(
                        COLORS.get('accent2', '#00ccff'))
            except Exception:
                try:
                    acc_rgb = self._hex_to_rgb(
                        COLORS.get('accent', '#00ff41'))
                    acc2_rgb = self._hex_to_rgb(
                        COLORS.get('accent2', '#00ccff'))
                except Exception:
                    acc_rgb = (0, 255, 65)
                    acc2_rgb = (0, 204, 255)
        else:
            try:
                acc_rgb = self._hex_to_rgb(COLORS.get('accent', '#00ff41'))
                acc2_rgb = self._hex_to_rgb(COLORS.get('accent2', '#00ccff'))
            except Exception:
                acc_rgb = (0, 255, 65)
                acc2_rgb = (0, 204, 255)

        # ── v3.6.1: bolha fina translúcida ──
        n_trail = 4
        for i in range(n_trail):
            t = i / float(n_trail)
            trail_r = r_base + 4.0 + i * 3.0
            mix = self._lerp_rgb(acc_rgb, acc2_rgb, t)
            fade = 1.0 - (i / float(n_trail))
            r_col = int(mix[0] * fade + 15 * (1 - fade))
            g_col = int(mix[1] * fade + 15 * (1 - fade))
            b_col = int(mix[2] * fade + 15 * (1 - fade))
            color = f"#{r_col:02x}{g_col:02x}{b_col:02x}"
            try:
                self.create_oval(cx - trail_r, cy - trail_r,
                                 cx + trail_r, cy + trail_r,
                                 outline=color, width=1)
            except Exception:
                pass
        if reactive_on:
            amp_ext = {0: 180, 1: 240, 2: 300, 3: 380}.get(
                REACTIVE_PULSE_STATE['intensity'], 240)
        elif global_on or self._writing:
            amp_ext = 220
        else:
            amp_ext = 140
        halo = self._pulse(COLORS.get('accent', '#00ff41'), gp, amp_ext)
        for r_off, w_ in ((3.0, 3), (1.5, 2)):
            self.create_oval(cx - r_base - r_off, cy - r_base - r_off,
                             cx + r_base + r_off, cy + r_base + r_off,
                             outline=halo, width=w_)
        steps = 14
        base_rgb = acc_rgb
        pulse_off_core = int(70 * (0.5 + 0.5 * math.sin(gp * math.pi / 8)))
        bright_rgb = (min(255, base_rgb[0] + pulse_off_core),
                      min(255, base_rgb[1] + pulse_off_core),
                      min(255, base_rgb[2] + pulse_off_core))
        dark_rgb = (max(0, base_rgb[0] // 5),
                    max(0, base_rgb[1] // 5),
                    max(0, base_rgb[2] // 5))
        for i in range(steps):
            t = i / float(steps - 1)
            r_now = r_base * (1.0 - t * 0.95)
            col = self._lerp_rgb(dark_rgb, bright_rgb, t)
            color = f"#{col[0]:02x}{col[1]:02x}{col[2]:02x}"
            self.create_oval(cx - r_now, cy - r_now,
                             cx + r_now, cy + r_now,
                             fill=color, outline='')
        hl_r = r_base * 0.32
        hl_cx = cx - r_base * 0.33
        hl_cy = cy - r_base * 0.38
        self.create_oval(hl_cx - hl_r, hl_cy - hl_r,
                         hl_cx + hl_r, hl_cy + hl_r,
                         fill='#ffffff', outline='')
        hl_r2 = hl_r * 0.55
        self.create_oval(hl_cx - hl_r2, hl_cy - hl_r2,
                         hl_cx + hl_r2, hl_cy + hl_r2,
                         fill='#e8ffff', outline='')
        if self._focused:
            try:
                ring_color = self._pulse(
                    COLORS.get('accent', '#00ff41'), self._focus_phase, 180)
                self.create_oval(1, 1, s - 1, s - 1,
                                 outline=ring_color, width=2)
                ring_color2 = self._pulse(
                    COLORS.get('accent2', '#00ccff'),
                    self._focus_phase + 4, 180)
                self.create_oval(2, 2, s - 2, s - 2,
                                 outline=ring_color2, width=1)
            except Exception:
                pass

    def _show_menu(self, event):
        if self._menu_open:
            return
        self._menu_open = True
        try:
            menu = tk.Menu(
                self, tearoff=0, bg=COLORS['frame_bg'], fg=COLORS['fg'],
                activebackground=COLORS['accent'], activeforeground='white',
                font=('Segoe UI', 10, 'bold'), borderwidth=2, relief='flat')
            for lbl in self._theme_labels:
                prefix = "●  " if lbl == self._current_label else "     "
                menu.add_command(label=prefix + lbl,
                                 command=lambda l=lbl: self._select(l))
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                try:
                    menu.grab_release()
                except Exception:
                    pass
        finally:
            self._menu_open = False

    def _select(self, label):
        self._current_label = label
        if self._on_change:
            try:
                self._on_change(label)
            except Exception:
                pass
        self._draw()

    def set_label(self, label):
        self._current_label = label
        self._draw()

    def destroy(self):
        self._stop_anim()
        self._stop_focus_anim()
        try:
            _PULSE_SUBSCRIBERS.remove(self)
        except ValueError:
            pass
        super().destroy()

# ==================================================================
# ==================================================================
# 17B. HEART PULSE BUTTON — coração multicolor com fundo animado
# ==================================================================
class LightningPulseButton(tk.Canvas):
    """v3.6.2 — Raio pulsante que oscila pelas cores dos temas."""
    def __init__(self, parent, command=None, width=54, height=40, **kw):
        try:
            bg = parent.cget('bg')
        except Exception:
            bg = COLORS['bg']
        super().__init__(parent, width=width, height=height,
                         highlightthickness=0, bg=bg,
                         takefocus=True, **kw)
        self._command = command
        self._width = width
        self._height = height
        self._phase = 0
        self._anim_id = None
        self._hover = False
        self._focused = False
        self._pressed = False
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)
        self.bind('<Return>', self._on_key)
        self.bind('<space>', self._on_key)
        _PULSE_SUBSCRIBERS.append(self)
        self._tick()

    def _palette(self):
        return [
            COLORS.get('accent', '#ff5252'),
            COLORS.get('accent2', '#ff79c6'),
            COLORS.get('info', '#89b4fa'),
            COLORS.get('success', '#a6e3a1'),
            COLORS.get('warning', '#f9e2af'),
        ]

    def _tick(self):
        try:
            self._phase = (self._phase + 1) % 64
            self._draw()
            self._anim_id = self.after(60, self._tick)
        except Exception:
            self._anim_id = None

    def _draw(self):
        try:
            self.delete('all')
        except Exception:
            return
        w, h = self._width, self._height
        cx, cy = w / 2, h / 2
        palette = self._palette()
        # ── Ciclo de cores dos temas quando o pulso global está ativo ──
        col = None
        if GLOBAL_PULSE_STATE.get('active') and GLOBAL_PULSE_STATE.get('color_cycle_index') is not None:
            try:
                keys = list(THEMES_RAW.keys())
                if keys:
                    idx_theme = GLOBAL_PULSE_STATE.get('color_cycle_index', 0) % len(keys)
                    base = THEMES_RAW[keys[idx_theme]]
                    col = base.get('accent', '#ff5252')
            except Exception:
                col = None
        if col is None:
            col = palette[(self._phase // 12) % len(palette)]
        for i in range(6):
            rr = 14 + i * 2.2 + 3 * abs(3 - (self._phase % 8))
            self.create_oval(cx - rr, cy - rr, cx + rr, cy + rr,
                             outline=col, width=1, fill='')
        size = 10 + int(2 * abs(3 - (self._phase % 8)))
        if self._pressed:
            size -= 2
        self.create_text(cx, cy, text='\u26a1',
                         font=('Segoe UI Emoji', size, 'bold'),
                         fill=col)

    def _on_press(self, e):
        self._pressed = True
        try: self.focus_set()
        except Exception: pass
        self._draw()

    def _on_release(self, e):
        if self._pressed and self._command:
            self._pressed = False
            try: self._command()
            except Exception: pass
        self._draw()

    def _on_enter(self, e):
        self._hover = True; self._draw()

    def _on_leave(self, e):
        self._hover = False; self._draw()

    def _on_focus_in(self, e):
        self._focused = True; self._draw()

    def _on_focus_out(self, e):
        self._focused = False; self._draw()

    def _on_key(self, e):
        if self._command:
            try: self._command()
            except Exception: pass
        return "break"

    def destroy(self):
        if self._anim_id is not None:
            try: self.after_cancel(self._anim_id)
            except Exception: pass
        try: _PULSE_SUBSCRIBERS.remove(self)
        except ValueError: pass
        super().destroy()


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, kind="normal",
                 width=180, height=42, radius=21,
                 font=('Segoe UI', 10, 'bold'), **kwargs):
        try:
            parent_bg = parent.cget('bg')
        except Exception:
            parent_bg = COLORS['bg']
        super().__init__(parent, width=width, height=height,
                         highlightthickness=0, bg=parent_bg,
                         takefocus=True, **kwargs)
        self._command = command
        self._text = text
        self._orig_font = font
        self._font = font
        self._radius = radius
        self._kind = kind
        self._hover = False
        self._pressed = False
        self._focused = False
        self._persistent_focus = False
        self._enabled = True
        self._width = width
        self._height = height
        self._orig_width = width
        self._focus_phase = 0
        self._focus_anim_id = None
        _PULSE_SUBSCRIBERS.append(self)
        self._refresh_colors()
        self._redraw()
        self._bind_events()

    def _bind_events(self):
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)
        self.bind('<Return>', self._on_key_activate)
        self.bind('<KP_Enter>', self._on_key_activate)
        self.bind('<space>', self._on_key_activate)
        self.bind('<Configure>', self._on_configure)
        self.bind('<Tab>', self._on_tab_forward)
        self.bind('<Shift-Tab>', self._on_tab_backward)
        self.bind('<ISO_Left_Tab>', self._on_tab_backward)

    def _on_tab_forward(self, e):
        try:
            nxt = self.tk_focusNext()
            if nxt:
                nxt.focus_set()
        except Exception:
            pass
        return "break"

    def _on_tab_backward(self, e):
        try:
            prv = self.tk_focusPrev()
            if prv:
                prv.focus_set()
        except Exception:
            pass
        return "break"

    def set_persistent_focus(self, on: bool):
        if self._persistent_focus == on:
            return
        self._persistent_focus = on
        if on:
            self._start_focus_animation()
        else:
            if not self._focused:
                self._stop_focus_animation()
        self._redraw()

    def _refresh_colors(self):
        if self._kind == "primary":
            self._bg_norm = COLORS['button_active']
            self._bg_hover = COLORS['accent']
            self._bg_press = COLORS['button_active']
            self._fg = "white"
            self._outline = COLORS['accent']
        elif self._kind == "danger":
            self._bg_norm = COLORS['cancel_bg']
            self._bg_hover = COLORS['error']
            self._bg_press = COLORS['cancel_bg']
            self._fg = "white"
            self._outline = COLORS['error']
        elif self._kind == "warning":
            self._bg_norm = "#7a4d00"
            self._bg_hover = COLORS['warning']
            self._bg_press = "#7a4d00"
            self._fg = "white"
            self._outline = COLORS['warning']
        else:
            self._bg_norm = COLORS['button_bg']
            self._bg_hover = COLORS['button_hover']
            self._bg_press = COLORS['button_bg']
            self._fg = COLORS['button_fg']
            self._outline = COLORS['frame_border']

    def _rounded_polygon(self, x1, y1, x2, y2, r):
        return [x1 + r, y1, x2 - r, y1, x2, y1, x2, y1 + r, x2, y2 - r,
                x2, y2, x2 - r, y2, x1 + r, y2, x1, y2, x1, y2 - r,
                x1, y1 + r, x1, y1]

    def _hex_to_rgb(self, h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _pulse_color(self, base_hex, phase, amplitude=80):
        try:
            r, g, b = self._hex_to_rgb(base_hex)
        except Exception:
            r, g, b = 0, 255, 255
        offset = int(amplitude * (0.5 + 0.5 * math.sin(phase * math.pi / 4)))
        return (f"#{min(255, max(0, r + offset)):02x}"
                f"{min(255, max(0, g + offset)):02x}"
                f"{min(255, max(0, b + offset)):02x}")

    def _glassify(self, hex_color):
        """Mistura a cor com o fundo para efeito translúcido."""
        try:
            h = hex_color.lstrip('#')
            r = int(h[0:2], 16); g = int(h[2:4], 16); b = int(h[4:6], 16)
            try:
                pbg = self.master.cget('bg').lstrip('#')
                pr = int(pbg[0:2], 16); pg = int(pbg[2:4], 16); pb = int(pbg[4:6], 16)
            except Exception:
                pr, pg, pb = 20, 22, 30
            nr = int(r * 0.65 + pr * 0.35)
            ng = int(g * 0.65 + pg * 0.35)
            nb = int(b * 0.65 + pb * 0.35)
            return f"#{nr:02x}{ng:02x}{nb:02x}"
        except Exception:
            return hex_color

    def _redraw(self):
        self.delete("all")
        w, h, r = self._width, self._height, self._radius
        if not self._enabled:
            bg, fg, outline = COLORS['button_bg'], COLORS['led_off'], COLORS['frame_border']
        elif self._pressed:
            bg, fg, outline = self._bg_press, self._fg, self._bg_norm
        elif self._hover:
            bg, fg, outline = self._bg_hover, self._fg, self._outline
        else:
            bg, fg, outline = self._bg_norm, self._fg, self._outline
        border = 2
        self.create_polygon(self._rounded_polygon(border, border, w - border,
                                                   h - border, r),
                            smooth=True, splinesteps=24, fill=outline,
                            outline=outline)
        self.create_polygon(self._rounded_polygon(border * 2, border * 2,
                                                   w - border * 2,
                                                   h - border * 2, r - 2),
                            smooth=True, splinesteps=24, fill=bg, outline=bg)
        if GLOBAL_PULSE_STATE['active'] and self._enabled:
            gp = GLOBAL_PULSE_STATE['phase']
            for thick, pad, amp in ((9, 7, 220), (7, 5, 200),
                                     (5, 3, 180), (3, 1, 160)):
                halo = self._pulse_color(
                    COLORS.get('accent', '#00ff41'), gp, amp)
                pts = self._rounded_polygon(-pad, -pad, w + pad, h + pad,
                                            r + pad + 2)
                self.create_polygon(pts, smooth=True, splinesteps=24,
                                    fill='', outline=halo, width=thick)
            mid = self._pulse_color(COLORS.get('accent2', '#00ccff'),
                                    gp + 4, 200)
            pts = self._rounded_polygon(-2, -2, w + 2, h + 2, r + 3)
            self.create_polygon(pts, smooth=True, splinesteps=24,
                                fill='', outline=mid, width=3)
        if (self._focused or self._persistent_focus) and self._enabled:
            phase = self._focus_phase
            # ── v3.6.1: alto contraste do foco ──
            try:
                self.create_polygon(self._rounded_polygon(1, 1, w - 1, h - 1,
                                                            r - 1),
                                    smooth=True, splinesteps=24,
                                    fill='', outline='#ffffff', width=3)
            except Exception:
                pass
            halo = self._pulse_color(COLORS.get('accent', '#00ff41'), phase, 160)
            for thick, pad in ((7, 5), (5, 4), (3, 3)):
                pts = self._rounded_polygon(-pad, -pad, w + pad, h + pad,
                                            r + pad + 2)
                self.create_polygon(pts, smooth=True, splinesteps=24,
                                    fill='', outline=halo, width=thick)
            mid = self._pulse_color(COLORS.get('accent2', '#00ccff'),
                                    phase + 4, 160)
            for thick, pad in ((5, 2), (4, 1)):
                pts = self._rounded_polygon(-pad, -pad, w + pad, h + pad,
                                            r + pad + 1)
                self.create_polygon(pts, smooth=True, splinesteps=24,
                                    fill='', outline=mid, width=thick)
            inner = self._pulse_color(COLORS.get('accent', '#00ff41'),
                                      phase + 8, 130)
            pts = self._rounded_polygon(1, 1, w - 1, h - 1, r + 1)
            self.create_polygon(pts, smooth=True, splinesteps=24,
                                fill='', outline=inner, width=2)
        self.create_text(w // 2, h // 2, text=self._text, fill=fg,
                         font=self._font, justify=tk.CENTER)

    def _start_focus_animation(self):
        if self._focus_anim_id is not None:
            return
        def _tick():
            try:
                self._focus_phase = (self._focus_phase + 1) % 16
                self._redraw()
                self._focus_anim_id = self.after(140, _tick)
            except Exception:
                self._focus_anim_id = None
        self._focus_anim_id = self.after(140, _tick)

    def _stop_focus_animation(self):
        if self._focus_anim_id is not None:
            try:
                self.after_cancel(self._focus_anim_id)
            except Exception:
                pass
            self._focus_anim_id = None

    def _on_configure(self, event):
        self._width = max(1, event.width)
        self._height = max(1, event.height)
        self._radius = self._height // 2
        try:
            family = self._orig_font[0]
            base_size = self._orig_font[1]
            extras = self._orig_font[2:] if len(self._orig_font) > 2 else ()
            if isinstance(base_size, int) and self._orig_width > 0:
                if self._width < self._orig_width * 0.6:
                    new_size = max(7, int(base_size * 0.75))
                elif self._width < self._orig_width * 0.8:
                    new_size = max(8, int(base_size * 0.88))
                else:
                    new_size = base_size
                self._font = (family, new_size, *extras)
        except Exception:
            pass
        self._redraw()

    def _on_enter(self, e):
        if self._enabled:
            self._hover = True
            self._redraw()

    def _on_leave(self, e):
        self._hover = False
        self._redraw()

    def _on_press(self, e):
        if self._enabled:
            self._pressed = True
            self.focus_set()
            self._redraw()

    def _on_release(self, e):
        if self._enabled and self._pressed:
            self._pressed = False
            self._redraw()
            if self._command:
                try:
                    self._command()
                except Exception:
                    pass

    def _on_focus_in(self, e):
        self._focused = True
        self._start_focus_animation()
        self._redraw()

    def _on_focus_out(self, e):
        self._focused = False
        if not self._persistent_focus:
            self._stop_focus_animation()
        self._redraw()

    def _on_key_activate(self, e):
        if self._enabled and self._command:
            try:
                self._command()
            except Exception:
                pass
        return "break"

    def set_state(self, **kwargs):
        """Configura o botão. Substitui config() para evitar conflito de assinatura."""
        if 'state' in kwargs:
            st = kwargs.pop('state')
            self._enabled = (st != "disabled" and st != tk.DISABLED)
        if 'text' in kwargs:
            self._text = kwargs.pop('text')
        if 'bg' in kwargs:
            self._bg_norm = kwargs.pop('bg')
        if 'fg' in kwargs:
            self._fg = kwargs.pop('fg')
        if 'command' in kwargs:
            self._command = kwargs.pop('command')
        if kwargs:
            try:
                super().config(**kwargs)
            except Exception:
                pass
        self._redraw()

    def destroy(self):
        try:
            _PULSE_SUBSCRIBERS.remove(self)
        except ValueError:
            pass
        super().destroy()

# ==================================================================
# 18. NEON TAB BAR
# ==================================================================
class NeonTabBar(tk.Frame):
    def __init__(self, parent, tabs_data, on_change, **kwargs):
        try:
            bg = parent.cget('bg')
        except Exception:
            bg = COLORS['bg']
        super().__init__(parent, bg=bg, **kwargs)
        self._on_change = on_change
        self._buttons = []
        self._current = -1
        for i, tab in enumerate(tabs_data):
            icon = tab.get('icon', '')
            label = tab.get('label', '')
            short = tab.get('short', label)
            text = f"{icon}\n{short}"
            btn = RoundedButton(
                self, text=text,
                command=lambda idx=i: self.select(idx),
                kind="normal",
                width=80, height=54, radius=14,
                font=('Segoe UI', 8, 'bold'))
            btn.pack(side=tk.LEFT, padx=1, pady=2, fill=tk.X, expand=True)
            self._buttons.append(btn)
        if self._buttons:
            self.select(0, silent=True)

    def select(self, idx, silent=False):
        if idx < 0 or idx >= len(self._buttons):
            return
        if self._current == idx and not silent:
            return
        for i, btn in enumerate(self._buttons):
            if i == idx:
                btn._kind = "primary"
                btn._refresh_colors()
                btn.set_persistent_focus(True)
            else:
                btn._kind = "normal"
                btn._refresh_colors()
                btn.set_persistent_focus(False)
        self._current = idx
        if not silent and self._on_change:
            try:
                self._on_change(idx)
            except Exception:
                pass

    def current(self):
        return self._current
# ==================================================================
# 19. ULTIMATE POPUP — Modal sistêmico (v3.6.0 com PgUp/PgDown)
# ==================================================================
class UltimatePopup:
    MIN_W = 360
    MAX_W = 720
    MIN_H = 190
    MAX_H = 700
    SCREEN_MARGIN = 24
    _grab_owner = None

    @classmethod
    def _work_area(cls, parent):
        try:
            sw = max(640, int(parent.winfo_screenwidth()))
            sh = max(480, int(parent.winfo_screenheight()))
            try:
                vx = int(parent.winfo_vrootx())
                vy = int(parent.winfo_vrooty())
            except Exception:
                vx, vy = 0, 0
            return vx, vy, sw, sh
        except Exception:
            return 0, 0, 1280, 800

    @classmethod
    def _popup_size(cls, parent, message, title=None):
        vx, vy, sw, sh = cls._work_area(parent)
        usable_w = max(cls.MIN_W, sw - cls.SCREEN_MARGIN * 2)
        usable_h = max(cls.MIN_H, sh - cls.SCREEN_MARGIN * 2)
        lines = str(message).splitlines() or [""]
        longest = max((len(line) for line in lines), default=20)
        natural_w = 380 + min(320, longest * 4)
        natural_h = 170 + min(440, len(lines) * 17)
        w = min(cls.MAX_W, usable_w, max(cls.MIN_W, natural_w))
        h = min(cls.MAX_H, usable_h, max(cls.MIN_H, natural_h))
        return max(cls.MIN_W, w), max(cls.MIN_H, h)

    @classmethod
    def _place(cls, dlg, anchor, width, height):
        try:
            dlg.update_idletasks()
        except Exception:
            pass
        try:
            px = int(anchor.winfo_rootx())
            py = int(anchor.winfo_rooty())
            pw = max(1, int(anchor.winfo_width()))
            ph = max(1, int(anchor.winfo_height()))
        except Exception:
            px = py = 0
            pw, ph = dlg.winfo_screenwidth(), dlg.winfo_screenheight()
        vx, vy, sw, sh = cls._work_area(anchor)
        x = px + (pw - width) // 2
        y = py + (ph - height) // 2
        min_x = vx + cls.SCREEN_MARGIN
        min_y = vy + cls.SCREEN_MARGIN
        max_x = vx + sw - width - cls.SCREEN_MARGIN
        max_y = vy + sh - height - cls.SCREEN_MARGIN
        x = min_x if max_x < min_x else max(min_x, min(x, max_x))
        y = min_y if max_y < min_y else max(min_y, min(y, max_y))
        try:
            dlg.geometry(f"{int(width)}x{int(height)}+{int(x)}+{int(y)}")
        except Exception:
            pass

    @classmethod
    def _acquire_grab(cls, dlg):
        try:
            if not dlg.winfo_exists():
                return
            if cls._grab_owner is not None:
                try:
                    if cls._grab_owner.winfo_exists():
                        return
                except Exception:
                    cls._grab_owner = None
            try:
                dlg.grab_set()
                cls._grab_owner = dlg
            except Exception:
                pass
        except Exception:
            pass

    @classmethod
    def _release_grab(cls, dlg):
        try:
            if cls._grab_owner is dlg:
                cls._grab_owner = None
        except Exception:
            pass
        try:
            if dlg.winfo_exists():
                dlg.grab_release()
        except Exception:
            pass

    @classmethod
    def show(cls, parent, title, message, kind="info"):
        return cls.ask(parent, title, message, kind=kind, buttons=("OK",))

    @classmethod
    def ask(cls, parent, title, message, kind="question",
            buttons=("Sim", "Não")):
        colors = COLORS
        dlg = tk.Toplevel(parent)
        dlg.title(str(title))
        dlg.configure(bg=colors['bg'])
        try:
            dlg.transient(parent)
        except Exception:
            pass
        dlg.resizable(True, True)
        width, height = cls._popup_size(parent, message, title)
        dlg.minsize(cls.MIN_W, cls.MIN_H)
        cls._place(dlg, parent, width, height)
        _reposition = {'after': None, 'last': (width, height)}
        def _schedule_reposition(event=None):
            if _reposition['after'] is not None:
                try:
                    dlg.after_cancel(_reposition['after'])
                except Exception:
                    pass
            _reposition['after'] = dlg.after(150, _do_reposition)
        def _do_reposition():
            _reposition['after'] = None
            try:
                if not dlg.winfo_exists():
                    return
                vx, vy, sw, sh = cls._work_area(parent)
                cw = min(max(cls.MIN_W, dlg.winfo_width()),
                         max(cls.MIN_W, sw - cls.SCREEN_MARGIN * 2))
                ch = min(max(cls.MIN_H, dlg.winfo_height()),
                         max(cls.MIN_H, sh - cls.SCREEN_MARGIN * 2))
                if (cw, ch) == _reposition['last']:
                    return
                _reposition['last'] = (cw, ch)
                cls._place(dlg, parent, cw, ch)
            except Exception:
                pass
        dlg.bind('<Configure>', _schedule_reposition, add='+')
        outer = tk.Frame(dlg, bg=colors['frame_bg'],
                         highlightbackground=colors['frame_border'],
                         highlightcolor=colors['accent'], highlightthickness=2)
        outer.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(1, weight=1)
        outer.rowconfigure(2, weight=0)
        icon_map = {"error": "❌", "warning": "⚠️", "success": "✅",
                    "question": "❓", "info": "ℹ️"}
        color_map = {"error": colors['error'], "warning": colors['warning'],
                     "success": colors['success'], "question": colors['accent2'],
                     "info": colors['info']}
        icon = icon_map.get(kind, "ℹ️")
        accent = color_map.get(kind, colors['accent'])
        header = tk.Frame(outer, bg=colors['frame_bg'])
        header.grid(row=0, column=0, sticky='ew', padx=16, pady=(14, 8))
        header.columnconfigure(1, weight=1)
        tk.Label(header, text=icon, font=('Segoe UI Emoji', 22, 'bold'),
                 fg=accent, bg=colors['frame_bg']).grid(row=0, column=0, padx=(0, 10))
        tk.Label(header, text=str(title), font=('Segoe UI', 13, 'bold'),
                 fg=colors['fg'], bg=colors['frame_bg'], anchor='w',
                 justify=tk.LEFT, wraplength=max(240, width - 120)).grid(
                     row=0, column=1, sticky='ew')
        body = tk.Frame(outer, bg=colors['frame_bg'])
        body.grid(row=1, column=0, sticky='nsew', padx=16, pady=4)
        body.columnconfigure(0, weight=1)
        body.rowconfigure(0, weight=1)
        text = tk.Text(body, bg=colors['entry_bg'], fg=colors['entry_fg'],
                       insertbackground=colors['fg'], font=('Consolas', 9),
                       wrap=tk.WORD, relief=tk.FLAT, bd=0, padx=12, pady=10,
                       highlightthickness=1,
                       highlightbackground=colors['frame_border'])
        text.grid(row=0, column=0, sticky='nsew')
        scroll = ttk.Scrollbar(body, orient=tk.VERTICAL, command=text.yview,
                                style='Vertical.TScrollbar')
        scroll.grid(row=0, column=1, sticky='ns')
        text.configure(yscrollcommand=scroll.set)
        text.insert('1.0', str(message))
        text.configure(state='disabled', takefocus=0)
        text.bind('<Tab>', lambda e: 'break')
        def _on_text_wheel(event):
            try:
                text.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except Exception:
                pass
            return "break"
        def _on_text_wheel_up(event):
            text.yview_scroll(-3, "units"); return "break"
        def _on_text_wheel_down(event):
            text.yview_scroll(3, "units"); return "break"
        for w in (text, body, outer, dlg):
            w.bind('<MouseWheel>', _on_text_wheel, add='+')
            w.bind('<Button-4>', _on_text_wheel_up, add='+')
            w.bind('<Button-5>', _on_text_wheel_down, add='+')
        try:
            dlg.bind_all('<MouseWheel>', _on_text_wheel, add='+')
        except Exception:
            pass

        # ── v3.6.0: PgUp/PgDown rolam o conteúdo da modal ──
        def _pgup_popup(e=None):
            try:
                text.yview_scroll(-10, "units")
            except Exception:
                pass
            return "break"
        def _pgdn_popup(e=None):
            try:
                text.yview_scroll(10, "units")
            except Exception:
                pass
            return "break"
        dlg.bind('<Prior>', _pgup_popup, add='+')
        dlg.bind('<Next>',  _pgdn_popup, add='+')
        text.bind('<Prior>', _pgup_popup, add='+')
        text.bind('<Next>',  _pgdn_popup, add='+')
        body.bind('<Prior>', _pgup_popup, add='+')
        body.bind('<Next>',  _pgdn_popup, add='+')
        outer.bind('<Prior>', _pgup_popup, add='+')
        outer.bind('<Next>',  _pgdn_popup, add='+')

        footer = tk.Frame(outer, bg=colors['frame_bg'])
        footer.grid(row=2, column=0, sticky='ew', padx=16, pady=(8, 14))
        n_buttons = len(buttons)
        for i in range(n_buttons):
            footer.columnconfigure(i, weight=1)
        result = {'value': False}
        _closed = {'done': False}
        def finish(value):
            if _closed['done']:
                return
            _closed['done'] = True
            result['value'] = bool(value)
            if _reposition['after'] is not None:
                try:
                    dlg.after_cancel(_reposition['after'])
                except Exception:
                    pass
                _reposition['after'] = None
            try:
                dlg.unbind_all('<MouseWheel>')
            except Exception:
                pass
            cls._release_grab(dlg)
            try:
                dlg.destroy()
            except Exception:
                pass
        first_btn = None
        for idx, label in enumerate(buttons):
            positive = _button_is_positive(label)
            kind_btn = 'primary' if positive else 'danger'
            btn = RoundedButton(footer, text=str(label),
                                command=lambda v=positive: finish(v),
                                kind=kind_btn, width=120, height=38, radius=19,
                                font=('Segoe UI', 10, 'bold'))
            btn.grid(row=0, column=idx, padx=5, sticky='ew')
            if first_btn is None:
                first_btn = btn
        dlg.bind('<Escape>', lambda e: finish(False))
        dlg.protocol('WM_DELETE_WINDOW', lambda: finish(False))
        try:
            if first_btn is not None:
                first_btn.focus_set()
        except Exception:
            pass
        dlg.after(150, lambda: cls._acquire_grab(dlg))
        dlg.wait_window()
        return result['value']

# ==================================================================
# 20. MONETIZAÇÃO / OTG
# ==================================================================
class MonetizationManager:
    def __init__(self, is_pro_version: bool = False):
        self.is_pro = is_pro_version

    def should_show_ads(self) -> bool:
        return IS_MOBILE and not self.is_pro

    def trigger_interstitial_ad(self, log_func=None):
        if self.should_show_ads():
            if log_func:
                log_func("[ADS] Exibindo anúncio intersticial antes do início "
                         "da gravação...", is_info=True)

class OTGDeviceManager:
    @staticmethod
    def get_otg_drives() -> List[str]:
        otg_paths = []
        base_mnt = "/storage"
        if os.path.exists(base_mnt):
            try:
                for entry in os.listdir(base_mnt):
                    if entry in ("emulated", "self"):
                        continue
                    full_path = os.path.join(base_mnt, entry)
                    if os.path.ismount(full_path) or os.access(full_path, os.W_OK):
                        otg_paths.append(full_path)
            except Exception:
                pass
        return otg_paths

# ==================================================================
# 20B. LOGO CLICÁVEL PENBOOT — v3.6.0 (🚀)
# ==================================================================
class ClickableLogo(tk.Frame):
    def __init__(self, parent, version: str, on_click, **kwargs):
        try:
            parent_bg = parent.cget('bg')
        except Exception:
            parent_bg = COLORS['bg']
        super().__init__(parent, bg=parent_bg, **kwargs)
        self._on_click = on_click
        self._parent_bg = parent_bg
        self._phase = 0
        self._anim_id = None
        self._hover = False
        self._focused = False
        self._icon_lbl = tk.Label(
            self, text=LOGO_ICON,   # v3.6.0: 🚀
            font=('Segoe UI Emoji', 15, 'bold'),
            fg=COLORS['accent'], bg=parent_bg, cursor='hand2')
        self._icon_lbl.pack(side=tk.LEFT)
        self._text_lbl = tk.Label(
            self, text="DARKPENBOOT",
            font=('Segoe UI', 13, 'bold'),
            fg=COLORS['accent'], bg=parent_bg, cursor='hand2')
        self._text_lbl.pack(side=tk.LEFT)
        self._ver_lbl = tk.Label(
            self, text=f" v{version}",
            font=('Segoe UI', 8),
            fg=COLORS['label_fg'], bg=parent_bg, cursor='hand2')
        self._ver_lbl.pack(side=tk.LEFT)
        self._hint_lbl = tk.Label(
            self, text="  ⓘ",
            font=('Segoe UI', 9, 'bold'),
            fg=COLORS['info'], bg=parent_bg, cursor='hand2')
        self._hint_lbl.pack(side=tk.LEFT)
        for w in (self, self._icon_lbl, self._text_lbl,
                  self._ver_lbl, self._hint_lbl):
            w.bind('<Button-1>', self._clicked)
            w.bind('<Enter>', self._enter)
            w.bind('<Leave>', self._leave)
        self.configure(takefocus=True, highlightthickness=0)
        try:
            self._text_lbl.configure(takefocus=True)
        except Exception:
            pass
        for w in (self, self._text_lbl):
            w.bind('<Return>', self._clicked)
            w.bind('<KP_Enter>', self._clicked)
            w.bind('<space>', self._clicked)
            w.bind('<FocusIn>', self._focus_in)
            w.bind('<FocusOut>', self._focus_out)
            w.bind('<Tab>', self._tab_forward)
            w.bind('<Shift-Tab>', self._tab_backward)
            w.bind('<ISO_Left_Tab>', self._tab_backward)
        self._start_anim()

    def _tab_forward(self, e):
        try:
            nxt = self._text_lbl.tk_focusNext()
            if nxt:
                nxt.focus_set()
        except Exception:
            pass
        return "break"

    def _tab_backward(self, e):
        try:
            prv = self._text_lbl.tk_focusPrev()
            if prv:
                prv.focus_set()
        except Exception:
            pass
        return "break"

    def _hex_to_rgb(self, h):
        h = h.lstrip('#')
        return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

    def _pulse(self, base, amp=120):
        try:
            r, g, b = self._hex_to_rgb(base)
        except Exception:
            r, g, b = 0, 255, 65
        off = int(amp * (0.5 + 0.5 * math.sin(self._phase * math.pi / 8)))
        return (f"#{min(255, max(0, r + off)):02x}"
                f"{min(255, max(0, g + off)):02x}"
                f"{min(255, max(0, b + off)):02x}")

    def _start_anim(self):
        if self._anim_id is not None:
            return
        if not GLOBAL_PULSE_STATE['active']:
            self._update_colors()
            return
        interval = 70
        def tick():
            try:
                self._phase = (self._phase + 1) % 16
                self._update_colors()
                self._anim_id = self.after(interval, tick)
            except Exception:
                self._anim_id = None
        self._anim_id = self.after(interval, tick)

    def _update_colors(self):
        if GLOBAL_PULSE_STATE['active']:
            base = COLORS['accent']
            c1 = self._pulse(base, 240)
            c2 = self._pulse(COLORS['accent2'], 220)
            try:
                c_glow = _lighten_hex(c1, 30)
                c_shadow = _darken_hex(c2, 40)
            except Exception:
                c_glow = c1
                c_shadow = c2
            self._icon_lbl.configure(fg=c1)
            self._text_lbl.configure(fg=c_glow)
            self._ver_lbl.configure(fg=c2)
            self._hint_lbl.configure(fg=c_shadow)
        elif self._hover or self._focused:
            c = self._pulse(COLORS['accent'], 160)
            self._icon_lbl.configure(fg=c)
            self._text_lbl.configure(fg=c)
            self._ver_lbl.configure(fg=COLORS['accent2'])
            self._hint_lbl.configure(fg=COLORS['accent2'])
        else:
            self._icon_lbl.configure(fg=COLORS['accent'])
            self._text_lbl.configure(fg=COLORS['accent'])
            self._ver_lbl.configure(fg=COLORS['label_fg'])
            self._hint_lbl.configure(fg=COLORS['info'])

    def _enter(self, e=None):
        self._hover = True
        self._update_colors()

    def _leave(self, e=None):
        self._hover = False
        self._update_colors()

    def _focus_in(self, e=None):
        self._focused = True
        self._update_colors()

    def _focus_out(self, e=None):
        self._focused = False
        self._update_colors()

    def _clicked(self, e=None):
        try:
            if callable(self._on_click):
                self._on_click()
        except Exception:
            pass
        return "break"

    def destroy(self):
        if self._anim_id is not None:
            try:
                self.after_cancel(self._anim_id)
            except Exception:
                pass
            self._anim_id = None
        super().destroy()

# ==================================================================
# 21. INTERFACE PRINCIPAL — v3.6.0
# ==================================================================
class DarkPenBoot:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{LOGO_ICON} {APP_NAME} v{APP_VERSION}")
        setattr(root, '_darkpenboot_owner', self)
        self.config = load_config()
        root.minsize(WINDOW_MIN_W, WINDOW_MIN_H)
        root.maxsize(3840, 2160)
        global COLORS
        theme_key = self.config.get('theme', 'matrix')
        COLORS = THEMES.get(theme_key, THEMES['matrix'])
        root.configure(bg=COLORS['bg'])
        self.style = ttk.Style()
        try:
            self.style.theme_use('clam')
        except Exception:
            pass
        self.drives: List[Dict] = []
        self.selected_drive: Optional[Dict] = None
        self.iso_path: str = self.config.get("last_iso", "")
        self.is_running: bool = False
        self.cancel_requested: bool = False
        self.download_active: bool = False
        self.download_cancel_requested: bool = False
        self._tooltips: List[ToolTip] = []
        self._last_was_dd_windows: bool = False
        self._tab_bar: Optional[NeonTabBar] = None
        self._tab_frames: List[tk.Frame] = []
        self._tab_canvases = []
        self._active_tab_canvas = None
        self._active_tab_frame = None
        self.neon_ball: Optional[NeonThemeBall] = None
        self._focus_scroll_after = None
        self._log_buffer: List[str] = []
        self._max_log_buffer = 500
        self._operation_start_time: Optional[float] = None
        self._operation_iso: str = ""
        self._operation_mode: str = ""
        self._current_usb_tier: str = "UNKNOWN"
        self._recovery_active: bool = False
        self._global_pulse_after: Optional[str] = None
        self.ad_mode = self.config.get('ad_mode', AD_MODE)
        self.premium_unlocked = bool(self.config.get('premium_unlocked', False))
        if self.premium_unlocked:
            self.ad_mode = "premium_no_ads"
        self.monetization = MonetizationManager(
            is_pro_version=(self.ad_mode == "premium_no_ads"))
        self._download_cancel_btn = None
        self._premium_button = None
        self._apply_ttk_style()
        self._build_ui()
        if self.iso_path and os.path.exists(self.iso_path):
            self.iso_entry.insert(0, self.iso_path)
        self.refresh_drives()
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
        self._bind_shortcuts()
        self._setup_tab_navigation()
        self._setup_initial_window()
        self.log(f"🚀 {APP_NAME} v{APP_VERSION} pronto.", is_success=True)
        self.log(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", is_info=True)
        self.log(f"🖥️  SO ativo: {SYSTEM.title()}", is_info=True)
        if IS_IOS:
            self.log("📱 Modo iOS detectado (Pythonista / iSH).", is_info=True)
        elif IS_ANDROID or IS_TERMUX:
            self.log("📱 Modo Android/Termux detectado.", is_info=True)
        self.log("🆕 v3.6.0: Logo 🚀 + PgUp/PgDown em todas as modais",
                 is_success=True)
        self.log("🆕 v3.6.0: ~35 distros com links oficiais",
                 is_success=True)
        self.log("🆕 v3.6.0: Pulso Neon só em tarefas reais",
                 is_success=True)
        self.log("🆕 v3.6.0: Orb 3D oscila por todas as cores dos temas",
                 is_success=True)
        self.log("✅ v3.5.0: Janelas modais + ISOs Recentes + licença",
                 is_info=True)
        self.log("✅ v3.4.0: Tema 🌙 Soft Dark + SHA256 + Premium",
                 is_info=True)
        self.log("🎨 Clique no LOGO ou no ORB para interagir", is_info=True)
        self.log("🛠️ Painel de Recuperação/Reparo USB: Ctrl+R", is_info=True)
        self.log(f"🌐 GitHub: {GITHUB_URL}", is_info=True)

    def _setup_initial_window(self):
        try:
            saved_geom = (self.config.get('window_geometry') or '').strip()
            if saved_geom and re.match(r'^\d+x\d+[+-]\d+[+-]\d+$', saved_geom):
                try:
                    self.root.geometry(saved_geom)
                    return
                except Exception:
                    pass
            sw = self.root.winfo_screenwidth()
            sh = self.root.winfo_screenheight()
            max_w = int(sw * WINDOW_MAX_RATIO_W)
            max_h = int(sh * WINDOW_MAX_RATIO_H)
            w = min(WINDOW_INITIAL_W, max_w)
            h = min(WINDOW_INITIAL_H, max_h)
            w = max(WINDOW_MIN_W, w)
            h = max(WINDOW_MIN_H, h)
            x = (sw - w) // 2
            y = (sh - h) // 2
            self.root.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            try:
                self.root.geometry(f"{WINDOW_INITIAL_W}x{WINDOW_INITIAL_H}+40+40")
            except Exception:
                pass

    def _bind_shortcuts(self):
        try:
            self.root.bind('<Control-o>', lambda e: self._select_iso())
            self.root.bind('<Control-O>', lambda e: self._select_iso())
            self.root.bind('<F5>', lambda e: self.refresh_drives())
            self.root.bind('<Control-Return>', lambda e: self._start_operation())
            self.root.bind('<Control-l>', lambda e: self._clear_log())
            self.root.bind('<Control-L>', lambda e: self._clear_log())
            self.root.bind('<Control-s>', lambda e: self._save_log())
            self.root.bind('<Control-S>', lambda e: self._save_log())
            self.root.bind('<Control-r>', lambda e: self._open_usb_recovery())
            self.root.bind('<Control-R>', lambda e: self._open_usb_recovery())
            self.root.bind('<F1>', lambda e: self._show_instructions_popup())
            self.root.bind('<Escape>', self._on_escape)
            self.root.bind('<Prior>', lambda e: self._scroll_page(-1))
            self.root.bind('<Next>',  lambda e: self._scroll_page(1))
            for seq in ('<Up>', '<Down>', '<Left>', '<Right>',
                        '<KP_Up>', '<KP_Down>', '<KP_Left>', '<KP_Right>'):
                self.root.bind(seq, self._arrow_navigate)
        except Exception:
            pass

    def _setup_tab_navigation(self):
        try:
            self.root.bind('<Control-Tab>', self._focus_next_generic)
            self.root.bind('<Control-Shift-Tab>', self._focus_prev_generic)
            self.root.bind('<Control-ISO_Left_Tab>', self._focus_prev_generic)
            for klass in ("TButton", "TCombobox", "TEntry", "TCheckbutton",
                          "Entry", "Text", "Listbox", "Checkbutton",
                          "Canvas", "Frame"):
                try:
                    self.root.bind_class(klass, "<Tab>", self._focus_next_generic)
                    self.root.bind_class(klass, "<Shift-Tab>",
                                          self._focus_prev_generic)
                    self.root.bind_class(klass, "<ISO_Left_Tab>",
                                          self._focus_prev_generic)
                except Exception:
                    pass
            self.root.bind_all('<FocusIn>', self._on_navigation_focus, add='+')
        except Exception:
            pass

    def _focus_next_generic(self, event=None):
        try:
            w = event.widget if event else self.root.focus_get()
            if w is None:
                self.root.focus_set()
                return "break"
            nxt = w.tk_focusNext()
            if nxt:
                nxt.focus_set()
                self._ensure_visible(nxt)
        except Exception:
            pass
        return "break"

    def _focus_prev_generic(self, event=None):
        try:
            w = event.widget if event else self.root.focus_get()
            if w is None:
                self.root.focus_set()
                return "break"
            prv = w.tk_focusPrev()
            if prv:
                prv.focus_set()
                self._ensure_visible(prv)
        except Exception:
            pass
        return "break"

    def _scroll_page(self, direction):
        try:
            if self._active_tab_canvas:
                self._active_tab_canvas.yview_scroll(direction * 8, "units")
        except Exception:
            pass
        return "break"

    def _widget_belongs_to_canvas(self, widget, canvas, frame):
        try:
            p = widget
            for _ in range(20):
                if p is None:
                    return False
                if p is frame:
                    return True
                p = getattr(p, 'master', None)
        except Exception:
            pass
        return False

    def _ensure_visible(self, widget):
        try:
            if not self._active_tab_canvas or not self._active_tab_frame:
                return
            if not self._widget_belongs_to_canvas(
                widget, self._active_tab_canvas, self._active_tab_frame):
                return
            self.root.update_idletasks()
            sf = self._active_tab_frame
            cv = self._active_tab_canvas
            sf_h = sf.winfo_height() or 1
            canvas_h = cv.winfo_height() or 1
            try:
                wy = widget.winfo_rooty() - sf.winfo_rooty()
            except Exception:
                wy = widget.winfo_y()
            wh = widget.winfo_height()
            yview = cv.yview()
            top_px = yview[0] * sf_h
            bottom_px = yview[1] * sf_h
            if wy < top_px:
                cv.yview_moveto(max(0.0, (wy - 24) / sf_h))
            elif (wy + wh + 24) > bottom_px:
                cv.yview_moveto(max(0.0, min(1.0,
                                             (wy + wh + 24 - canvas_h) / sf_h)))
        except Exception:
            pass

    def _arrow_navigate(self, event):
        try:
            focused = self.root.focus_get()
        except Exception:
            focused = None
        if focused is None:
            return None
        if isinstance(focused, (tk.Text, tk.Entry, ttk.Combobox)):
            return None
        if not isinstance(focused, (RoundedButton, NeonThemeBall)):
            return None
        key = getattr(event, 'keysym', '')
        try:
            if key in ('Right', 'Down', 'KP_Right', 'KP_Down'):
                nxt = focused.tk_focusNext()
                guard = 0
                while nxt and not isinstance(
                    nxt, (RoundedButton, ttk.Combobox, ttk.Entry, NeonThemeBall)
                ) and guard < 60:
                    nxt = nxt.tk_focusNext()
                    guard += 1
                if nxt:
                    nxt.focus_set()
                    self._ensure_visible(nxt)
            elif key in ('Left', 'Up', 'KP_Left', 'KP_Up'):
                prv = focused.tk_focusPrev()
                guard = 0
                while prv and not isinstance(
                    prv, (RoundedButton, ttk.Combobox, ttk.Entry, NeonThemeBall)
                ) and guard < 60:
                    prv = prv.tk_focusPrev()
                    guard += 1
                if prv:
                    prv.focus_set()
                    self._ensure_visible(prv)
        except Exception:
            pass
        return "break"

    def _on_navigation_focus(self, event=None):
        try:
            w = event.widget if event else self.root.focus_get()
            if w is None:
                return
            if self._focus_scroll_after is not None:
                try:
                    self.root.after_cancel(self._focus_scroll_after)
                except Exception:
                    pass
                self._focus_scroll_after = None
            self._focus_scroll_after = self.root.after(
                30, lambda ww=w: self._ensure_visible(ww))
        except Exception:
            pass

    def _on_escape(self, event=None):
        try:
            focused = self.root.focus_get()
        except Exception:
            focused = None
        if focused is self.log_text:
            try:
                self.start_btn.focus_set()
            except Exception:
                pass
            return "break"
        if self.is_running:
            self._cancel_operation()
            return "break"
        for w in self.root.winfo_children():
            if isinstance(w, tk.Toplevel) and w.winfo_exists():
                try:
                    w.grab_release()
                    w.destroy()
                except Exception:
                    pass
                return "break"
        return None

    def _apply_ttk_style(self):
        s = self.style
        try:
            s.configure("TCombobox", fieldbackground=COLORS['entry_bg'],
                        background=COLORS['button_bg'], foreground=COLORS['fg'],
                        arrowcolor=COLORS['accent'],
                        bordercolor=COLORS['frame_border'],
                        lightcolor=COLORS['frame_border'],
                        darkcolor=COLORS['frame_border'], padding=3)
            s.map("TCombobox",
                  fieldbackground=[("readonly", COLORS['entry_bg'])],
                  foreground=[("readonly", COLORS['fg'])],
                  background=[("readonly", COLORS['button_bg'])])
            s.configure("Horizontal.TProgressbar",
                        background=COLORS['accent'],
                        troughcolor=COLORS['entry_bg'],
                        bordercolor=COLORS['frame_border'],
                        lightcolor=COLORS['accent'],
                        darkcolor=COLORS['accent'], thickness=18)
            for orient in ("Vertical", "Horizontal"):
                s.configure(f"{orient}.TScrollbar",
                            background=COLORS['button_bg'],
                            troughcolor=COLORS['entry_bg'],
                            bordercolor=COLORS['frame_border'],
                            arrowcolor=COLORS['accent'],
                            lightcolor=COLORS['frame_border'],
                            darkcolor=COLORS['frame_border'],
                            gripcount=0, relief=tk.FLAT, width=14)
                s.map(f"{orient}.TScrollbar",
                      background=[("pressed", COLORS['accent']),
                                  ("active", COLORS['accent2'])],
                      arrowcolor=[("pressed", "white"),
                                  ("active", COLORS['accent'])],
                      bordercolor=[("active", COLORS['accent'])],
                      troughcolor=[("active", COLORS['button_bg'])])
        except Exception:
            pass

    # ==================================================================
    # PULSO GLOBAL NEON — v3.6.0 (com ciclo de cores p/ orb)
    # ==================================================================
    def _start_global_pulse(self):
        if GLOBAL_PULSE_STATE['active']:
            return
        GLOBAL_PULSE_STATE['active'] = True
        GLOBAL_PULSE_STATE['phase'] = 0
        GLOBAL_PULSE_STATE['color_cycle_phase'] = 0     # v3.6.0
        GLOBAL_PULSE_STATE['color_cycle_index'] = 0     # v3.6.0
        self.log("💫 Pulso neon global ATIVADO", is_info=True)
        self._global_pulse_tick()
        try:
            if self.neon_ball is not None:
                self.neon_ball.set_global_pulse(True)
        except Exception:
            pass

    def _global_pulse_tick(self):
        reactive = REACTIVE_PULSE_STATE['active']
        if (reactive and time.time() * 1000 >
                REACTIVE_PULSE_STATE['until_ts']):
            REACTIVE_PULSE_STATE['active'] = False
            REACTIVE_PULSE_STATE['intensity'] = 0
            reactive = False
        if not GLOBAL_PULSE_STATE['active'] and not reactive:
            return
        if GLOBAL_PULSE_STATE['active']:
            GLOBAL_PULSE_STATE['phase'] = (
                GLOBAL_PULSE_STATE['phase'] + 1) % 16
            # v3.6.0 — ciclo de cor do orb a cada 16 ticks (≈1s)
            GLOBAL_PULSE_STATE['color_cycle_phase'] = (
                GLOBAL_PULSE_STATE.get('color_cycle_phase', 0) + 1) % 16
            if GLOBAL_PULSE_STATE['color_cycle_phase'] == 0:
                total = max(1, len(THEMES_RAW))
                GLOBAL_PULSE_STATE['color_cycle_index'] = (
                    GLOBAL_PULSE_STATE.get('color_cycle_index', 0) + 1) % total
        if reactive:
            REACTIVE_PULSE_STATE['phase'] = (
                REACTIVE_PULSE_STATE['phase'] + 1) % 16
        for w in list(_PULSE_SUBSCRIBERS):
            try:
                if w.winfo_exists():
                    if isinstance(w, RoundedButton):
                        w._redraw()
                    elif isinstance(w, NeonThemeBall):
                        w._draw()
            except Exception:
                pass
        interval = (GLOBAL_PULSE_STATE['interval_ms'] if not reactive else
                    {0: 40, 1: 32, 2: 22, 3: 14}.get(
                        REACTIVE_PULSE_STATE['intensity'], 22))
        try:
            self._global_pulse_after = self.root.after(
                interval, self._global_pulse_tick)
        except Exception:
            self._global_pulse_after = None

    def _stop_global_pulse(self, delay_ms: int = 0):
        def _do():
            if not GLOBAL_PULSE_STATE['active']:
                return
            GLOBAL_PULSE_STATE['active'] = False
            GLOBAL_PULSE_STATE['color_cycle_phase'] = 0   # v3.6.0
            GLOBAL_PULSE_STATE['color_cycle_index'] = 0   # v3.6.0
            pulse_after = self._global_pulse_after
            if pulse_after is not None:
                try:
                    self.root.after_cancel(pulse_after)
                except Exception:
                    pass
                self._global_pulse_after = None
            for w in list(_PULSE_SUBSCRIBERS):
                try:
                    if w.winfo_exists():
                        if isinstance(w, RoundedButton):
                            w._redraw()
                        elif isinstance(w, NeonThemeBall):
                            w._draw()
                except Exception:
                    pass
            try:
                if self.neon_ball is not None:
                    self.neon_ball.set_global_pulse(False)
            except Exception:
                pass
            self.log("💫 Pulso neon global DESATIVADO", is_info=True)
        if delay_ms > 0:
            try:
                self.root.after(delay_ms, _do)
            except Exception:
                _do()
        else:
            _do()

    def trigger_reactive_pulse(self, intensity: int = 2,
                               duration_ms: int = 1200,
                               log_msg: Optional[str] = None):
        _trigger_reactive_pulse(intensity, duration_ms)
        if self._global_pulse_after is None:
            self._global_pulse_tick()
        try:
            ball_ref = self.neon_ball
            if ball_ref is not None:
                ball_ref.set_writing_mode(True)
                self.root.after(
                    duration_ms + 100,
                    lambda b=ball_ref: b.set_writing_mode(False))
        except Exception:
            pass
        if log_msg:
            self.log(log_msg, is_info=True)

    # ==================================================================
    # PREMIUM
    # ==================================================================
    def _open_premium_checkout(self):
        try:
            price_msg = (
                "⭐ DARKPENBOOT PRO — PREMIUM\n"
                "═══════════════════════════════════════════════\n\n"
                f"💰 Valor: {PREMIUM_PRICE_BRL} (pagamento único)\n\n"
                "✨ BENEFÍCIOS DO PREMIUM:\n"
                "─────────────────────────────────────────────\n"
                "✅ SEM ANÚNCIOS — interface limpa\n"
                "✅ Compilado .exe com assinatura digital\n"
                "✅ Acesso a temas exclusivos futuros\n"
                "✅ Suporte prioritário via GitHub Issues\n"
                "✅ Atualizações vitalícias da v3.6.x\n"
                "✅ Sem banner publicitário\n\n"
                "─────────────────────────────────────────────\n"
                "📋 O QUE VOCÊ JÁ TEM (GRÁTIS):\n"
                "─────────────────────────────────────────────\n"
                "• Todos os recursos de gravação\n"
                "• Verificação SHA256 pós-download\n"
                "• Painel de Recuperação USB\n"
                "• 7 temas (incluindo 🌙 Soft Dark)\n"
                "• ~35 distros Linux com links oficiais\n"
                "• Downloads com fallback curl/wget/urllib\n\n"
                "═══════════════════════════════════════════════\n"
                "🎯 Deseja abrir a página de checkout?\n"
                "═══════════════════════════════════════════════"
            )
            resp = UltimatePopup.ask(
                self.root,
                f"⭐ PREMIUM — {PREMIUM_PRICE_BRL}",
                price_msg,
                kind="question",
                buttons=("💳 Abrir checkout", "❌ Fechar"))
            if resp:
                self.log(f"⭐ Abrindo checkout PREMIUM ({PREMIUM_PRICE_BRL})...",
                         is_info=True)
                try:
                    webbrowser.open(PREMIUM_CHECKOUT_URL)
                    self.log("✅ Checkout aberto no navegador.",
                             is_success=True)
                except Exception as e:
                    self.log(f"⚠️ Não foi possível abrir: {e}", is_warning=True)
                    self._popup_info(
                        "Checkout Premium",
                        f"Abra manualmente:\n\n{PREMIUM_CHECKOUT_URL}")
        except Exception as e:
            self.log(f"⚠️ Erro ao abrir checkout: {e}", is_warning=True)

    # ==================================================================
    # POPUP DE INSTRUÇÕES — v3.6.0
    # ==================================================================
    def _show_instructions_popup(self):
        try:
            msg = (
                "╔══════════════════════════════════════════════╗\n"
                "║   🚀 DARKPENBOOT PRO v3.6.0 — INSTRUÇÕES     ║\n"
                "╚══════════════════════════════════════════════╝\n\n"
                "📌 FLUXO BÁSICO (3 PASSOS)\n"
                "─────────────────────────────────────────────\n"
                "1) Aba 🔌 PENDRIVE\n"
                "   • Conecte o pendrive\n"
                "   • Clique em 🔄 ATUALIZAR\n"
                "   • Escolha o dispositivo na lista\n\n"
                "2) Aba 💿 ISO\n"
                "   • Clique em 📂 SELECIONAR ISO\n"
                "   • Ou use ⬇️ DOWNLOAD para baixar\n"
                "     (com verificação SHA256 automática)\n\n"
                "3) Aba ⚙️ BÁSICO (opcional)\n"
                "   • FS: NTFS (Windows) / FAT32 / exFAT\n"
                "   • Esquema: MBR ou GPT\n"
                "   • MODO: Extrair (recomendado) ou DD\n\n"
                "4) Clique em 💾 GRAVAR (ou Ctrl+Enter)\n\n"
                "─────────────────────────────────────────────\n"
                "⌨️  ATALHOS DE TECLADO\n"
                "─────────────────────────────────────────────\n"
                "F1 ............. Este popup de ajuda\n"
                "Ctrl+O ......... Selecionar ISO\n"
                "Ctrl+Enter ..... Iniciar gravação\n"
                "Ctrl+R ......... Painel de Recuperação USB\n"
                "Ctrl+L ......... Limpar log\n"
                "Ctrl+S ......... Salvar log\n"
                "F5 ............. Atualizar pendrives\n"
                "PgUp/PgDown .... Rolar conteúdo em modais (v3.6.0)\n"
                "Esc ............ Cancelar / fechar popup\n"
                "Tab / Setas .... Navegar pelos controles\n"
                "Enter .......... Acionar botão focado\n\n"
                "─────────────────────────────────────────────\n"
                "🎨 TEMAS DISPONÍVEIS (ORB NEON)\n"
                "─────────────────────────────────────────────\n"
                "🟢 Matrix · 🩸 Crimson · ❄️ Nord\n"
                "⚡ Cyberpunk · 🟠 Monokai · ☀️ Light\n"
                "🌙 Soft Dark (reduz fadiga visual)\n\n"
                "• Clique no ORB (canto superior direito)\n"
                "• Ele PULSA mais rápido durante operações\n"
                "• O ORB oscila por TODAS as cores (v3.6.0)\n"
                "• Esfera 3D + rastro de neon esmaecido\n\n"
                "─────────────────────────────────────────────\n"
                "🐧 DISTROS DISPONÍVEIS (v3.6.0)\n"
                "─────────────────────────────────────────────\n"
                "~35 distros com links oficiais:\n"
                "Debian · Ubuntu · Mint · Pop!_OS · Zorin\n"
                "elementary · Kali · Parrot · Tails\n"
                "Fedora · AlmaLinux · Rocky · CentOS · RHEL\n"
                "Arch · Manjaro · EndeavourOS · Garuda\n"
                "openSUSE · NixOS · Alpine · Gentoo · Void\n"
                "Slackware · Solus · Proxmox · TrueNAS\n\n"
                "─────────────────────────────────────────────\n"
                "⚙️  MODOS DE GRAVAÇÃO\n"
                "─────────────────────────────────────────────\n"
                "• EXTRAIR (recomendado):\n"
                "   Formata no FS escolhido (NTFS/FAT32/exFAT)\n"
                "   e COPIA os arquivos → pendrive continua\n"
                "   legível no Windows normalmente.\n\n"
                "• DD / Bit-a-Bit:\n"
                "   Clona a ISO byte-a-byte. Ideal para Linux.\n"
                "   Por padrão REMONTA o pendrive automaticamente.\n"
                "   Ative 'Deixar RAW' na aba Avançado se quiser\n"
                "   o comportamento antigo (disco offline).\n\n"
                "─────────────────────────────────────────────\n"
                "🔐 VERIFICAÇÃO SHA256\n"
                "─────────────────────────────────────────────\n"
                "• Todo download verifica SHA256 quando disponível\n"
                "• Se divergir, o arquivo é mantido como\n"
                "  '.parcial' e o usuário é avisado\n\n"
                "─────────────────────────────────────────────\n"
                "⭐ PREMIUM R$ 10 — SEM ANÚNCIOS\n"
                "─────────────────────────────────────────────\n"
                "• Clique no botão ⭐ PREMIUM (abaixo do log)\n"
                "• .exe assinado + suporte prioritário\n"
                "• Todos os recursos grátis já estão aqui!\n\n"
                "═════════════════════════════════════════════\n"
                "🌐 GitHub: github.com/Avlis1412\n"
                "👤 Autor: Adriano Rodrigues da Silva\n"
                "═════════════════════════════════════════════"
            )
            UltimatePopup.show(
                self.root, "📖 Instruções — DarkPenBoot Pro v3.6.0",
                msg, kind="info")
            self.log("📖 Popup de instruções aberto.", is_info=True)
        except Exception as e:
            self.log(f"⚠️ Erro ao abrir instruções: {e}", is_warning=True)

    def _build_ui(self):
        main = tk.Frame(self.root, bg=COLORS['bg'])
        main.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        main.columnconfigure(0, weight=1)
        main.rowconfigure(0, weight=0)
        main.rowconfigure(1, weight=0)
        main.rowconfigure(2, weight=1)
        main.rowconfigure(3, weight=0)
        main.rowconfigure(4, weight=0)
        main.rowconfigure(5, weight=1)
        if IS_MOBILE and self.ad_mode != "premium_no_ads":
            main.rowconfigure(6, weight=0)
        main.rowconfigure(7, weight=0)

        self._build_header(main, 0)

        tabs_data = [
            {'icon': '🔌', 'label': 'Pendrive', 'short': 'Pendrive'},
            {'icon': '💿', 'label': 'ISO', 'short': 'ISO'},
            {'icon': '⬇️', 'label': 'Download', 'short': 'Download'},
            {'icon': '⚙️', 'label': 'Básico', 'short': 'Básico'},
            {'icon': '🚀', 'label': 'Avançado', 'short': 'Avançado'},
            {'icon': '📖', 'label': 'Ajuda', 'short': 'Ajuda'},
            {'icon': '📚', 'label': 'Fontes', 'short': 'Fontes'},
        ]
        self._tab_bar = NeonTabBar(main, tabs_data, self._on_tab_clicked)
        self._tab_bar.grid(row=1, column=0, sticky='ew', pady=(0, 4))

        content_container = tk.Frame(main, bg=COLORS['bg'])
        content_container.grid(row=2, column=0, sticky='nsew')
        content_container.columnconfigure(0, weight=1)
        content_container.rowconfigure(0, weight=1)

        tabs_config = [
            (False, lambda f: self._build_drive_card(f, 0)),
            (False, lambda f: self._build_iso_card(f, 0)),
            (False, lambda f: self._build_download_card(f, 0)),
            (False, lambda f: self._build_basic_options(f)),
            (True,  lambda f: self._build_advanced_options(f)),
            (True,  lambda f: self._build_help_tab(f)),
            (True,  lambda f: self._build_sources_tab(f)),
        ]
        self._tab_frames = []
        self._tab_canvases = []
        for i, (with_scroll, builder) in enumerate(tabs_config):
            tc = self._make_tab_container(content_container, with_scroll=with_scroll)
            tc['outer'].grid(row=0, column=0, sticky='nsew')
            tc['outer'].grid_remove()
            builder(tc['frame'])
            self._tab_frames.append(tc['outer'])
            self._tab_canvases.append((tc['canvas'], tc['frame']))

        self._tab_frames[0].grid()
        self._active_tab_canvas = self._tab_canvases[0][0]
        self._active_tab_frame = self._tab_canvases[0][1]

        self._build_buttons(main, 3)
        self._build_progress(main, 4)
        self._build_log(main, 5)
        if IS_MOBILE and self.ad_mode != "premium_no_ads":
            self._build_ad_banner(main, 6)
        self._build_premium_footer(main, 7)
        self.root.bind('<Configure>', self._on_main_resize, add='+')
        self.root.bind('<ButtonPress>', self._orb_interaction, add='+')
        self.root.bind('<KeyPress>', self._orb_interaction, add='+')

    def _build_ad_banner(self, parent, row):
        try:
            bg, fg = AD_BANNER_COLORS
            ad_frame = tk.Frame(parent, bg=bg,
                                highlightbackground=fg, highlightthickness=1)
            ad_frame.grid(row=row, column=0, sticky='ew', pady=(4, 0))
            lbl = tk.Label(ad_frame, text=AD_BANNER_TEXT,
                           bg=bg, fg=fg,
                           font=('Segoe UI', 8, 'bold'),
                           anchor='center', justify=tk.CENTER)
            lbl.pack(fill=tk.X, ipady=5, padx=6)
            lbl.configure(cursor='hand2')
            lbl.bind('<Button-1>',
                     lambda e: webbrowser.open(GITHUB_URL))
            self._add_tip(lbl,
                          "📢 Anúncio da versão gratuita.\n"
                          f"Clique para abrir o GitHub e conhecer o PREMIUM "
                          f"({PREMIUM_PRICE_BRL}).")
        except Exception:
            pass

    def _build_premium_footer(self, parent, row):
        """Rodapé com [💖 Doação] [📱 Mobile] | [❤️ pulsa] [📢 Anúncios]."""
        try:
            frame = tk.Frame(parent, bg=COLORS['bg'])
            frame.grid(row=row, column=0, sticky='ew', pady=(4, 0))
            frame.columnconfigure(0, weight=1)

            left = tk.Frame(frame, bg=COLORS['bg'])
            left.grid(row=0, column=0, sticky='w')

            donate = self._make_button(
                left, "\U0001f496 DOAR VIA PIX", self._open_donate,
                kind="primary", font=('Segoe UI', 10, 'bold'))
            donate.pack(side=tk.LEFT, padx=(2, 4), pady=2)
            self._add_tip(donate,
                          "\U0001f496 Botão único de doação via PIX.\n"
                          "Consolidado v3.6.1.")

            mobile = self._make_button(
                left, "\U0001f4f1 Versão Mobile (sem Ads)",
                self._open_mobile_page,
                kind="normal", font=('Segoe UI', 9, 'bold'))
            mobile.pack(side=tk.LEFT, padx=4, pady=2)
            self._add_tip(mobile,
                          "\U0001f4f1 Versão mobile sem anúncios.")

            right = tk.Frame(frame, bg=COLORS['bg'])
            right.grid(row=0, column=1, sticky='e')

            self.lightning_btn = LightningPulseButton(
                right,
                command=self._toggle_favorite,
                width=54, height=40)
            self.lightning_btn.pack(side=tk.TOP, anchor='e', pady=(0, 3))
            self._add_tip(self.lightning_btn,
                          "\u2764\ufe0f Favoritar ISO atual.\n"
                          "Pulsa entre as cores do tema.")

            ads = self._make_button(
                right, "\U0001f4e2 Anúncios", self._open_ads_settings,
                kind="normal", width=130,
                font=('Segoe UI', 9, 'bold'))
            ads.pack(side=tk.TOP, anchor='e')
            self._add_tip(ads, "\U0001f4e2 Preferências de anúncios.")
        except Exception as e:
            self.log(f"\u26a0\ufe0f Rodapé: {e}", is_warning=True)


    def _orb_interaction(self, event=None):
        try:
            if self.neon_ball is None or getattr(self, '_orb_interaction_after', None):
                return
            if getattr(self, 'is_running', False):
                return
            self.neon_ball.set_writing_mode(True)
            if hasattr(self, '_orb_interaction_after') and self._orb_interaction_after:
                self.root.after_cancel(self._orb_interaction_after)
            self._orb_interaction_after = self.root.after(280, self._stop_orb_interaction)
        except Exception:
            pass

    def _stop_orb_interaction(self):
        try:
            self._orb_interaction_after = None
            if self.neon_ball is not None and not getattr(self, 'is_running', False):
                self.neon_ball.set_writing_mode(False)
        except Exception:
            pass

    def _on_tab_clicked(self, idx):
        try:
            for i, fr in enumerate(self._tab_frames):
                if i == idx:
                    fr.grid()
                else:
                    fr.grid_remove()
            if 0 <= idx < len(self._tab_canvases):
                self._active_tab_canvas = self._tab_canvases[idx][0]
                self._active_tab_frame = self._tab_canvases[idx][1]
        except Exception:
            pass

    def _make_tab_container(self, parent, with_scroll=False):
        outer = tk.Frame(parent, bg=COLORS['frame_bg'],
                         highlightbackground=COLORS['frame_border'],
                         highlightcolor=COLORS['accent'],
                         highlightthickness=1)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(0, weight=1)
        if not with_scroll:
            inner = tk.Frame(outer, bg=COLORS['frame_bg'])
            inner.grid(row=0, column=0, sticky='nsew', padx=6, pady=6)
            inner.columnconfigure(0, weight=1)
            class _FakeCanvas:
                def yview(self): return (0.0, 1.0)
                def yview_moveto(self, *a, **k): pass
                def yview_scroll(self, *a, **k): pass
                def bbox(self, *a, **k): return None
                def configure(self, *a, **k): pass
                def bind_all(self, *a, **k): pass
                def unbind_all(self, *a, **k): pass
                def winfo_height(self): return 1
                def update_idletasks(self): pass
            return {'outer': outer, 'canvas': _FakeCanvas(), 'frame': inner}
        canvas = tk.Canvas(outer, bg=COLORS['frame_bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(outer, orient="vertical",
                                   command=canvas.yview,
                                   style="Vertical.TScrollbar")
        inner = tk.Frame(canvas, bg=COLORS['frame_bg'])
        inner.columnconfigure(0, weight=1)
        inner.bind("<Configure>",
                   lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.bind('<Configure>',
                    lambda e: canvas.itemconfig(win, width=e.width))
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.grid(row=0, column=0, sticky="nsew", padx=(6, 0), pady=6)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=6)

        def _on_enter(e):
            canvas.bind_all("<MouseWheel>",
                            lambda ev: canvas.yview_scroll(
                                int(-1 * (ev.delta / 120)), "units"))
            canvas.bind_all("<Button-4>",
                            lambda ev: canvas.yview_scroll(-2, "units"))
            canvas.bind_all("<Button-5>",
                            lambda ev: canvas.yview_scroll(2, "units"))
        def _on_leave(e):
            canvas.unbind_all("<MouseWheel>")
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")
        canvas.bind("<Enter>", _on_enter)
        canvas.bind("<Leave>", _on_leave)
        return {'outer': outer, 'canvas': canvas, 'frame': inner}

    def _on_main_resize(self, event=None):
        try:
            if event is not None and event.widget is not self.root:
                return
            for cv, fr in self._tab_canvases:
                try:
                    if hasattr(cv, 'update_idletasks'):
                        cv.update_idletasks()
                    if hasattr(cv, 'configure') and hasattr(cv, 'bbox'):
                        b = cv.bbox('all')
                        if b:
                            cv.configure(scrollregion=b)
                except Exception:
                    pass
        except Exception:
            pass

    def _make_button(self, parent, text, command, kind="normal",
                     width=None, **kwargs):
        if width is not None:
            btn_width = width
        else:
            text_len = len(str(text))
            btn_width = max(80, min(280, text_len * 7 + 30))
        custom_font = kwargs.pop('font', ('Segoe UI', 10, 'bold'))
        try:
            font_size = custom_font[1]
        except Exception:
            font_size = 10
        btn_height = max(32, int(font_size * 2.2))
        return RoundedButton(parent, text=text, command=command, kind=kind,
                             width=btn_width, height=btn_height,
                             radius=btn_height // 2, font=custom_font,
                             **kwargs)

    def _add_tip(self, widget, text):
        try:
            tip = ToolTip(widget, text)
            self._tooltips.append(tip)
        except Exception:
            pass

    def _popup_info(self, title, message):
        return UltimatePopup.show(self.root, title, message, kind="info")

    def _popup_success(self, title, message):
        return UltimatePopup.show(self.root, title, message, kind="success")

    def _popup_warning(self, title, message):
        return UltimatePopup.show(self.root, title, message, kind="warning")

    def _popup_error(self, title, message):
        return UltimatePopup.show(self.root, title, message, kind="error")

    def _popup_ask(self, title, message):
        return UltimatePopup.ask(self.root, title, message,
                                 kind="question", buttons=("Sim", "Não"))

    def _make_labelframe(self, parent, text):
        return tk.LabelFrame(
            parent, text=text, font=('Segoe UI', 10, 'bold'),
            fg=COLORS['accent'], bg=COLORS['frame_bg'],
            relief=tk.FLAT, bd=0,
            highlightbackground=COLORS['frame_border'],
            highlightcolor=COLORS['accent'],
            highlightthickness=2, labelanchor='nw', padx=10, pady=8)

    def _make_hyperlink(self, parent, text, url):
        """Retorna um tk.Button estilizado como link (focável por Tab)."""
        try:
            parent_bg = parent.cget('bg')
        except Exception:
            parent_bg = COLORS['frame_bg']
        btn = tk.Button(
            parent, text=text, fg=COLORS['info'], bg=parent_bg,
            activebackground=parent_bg, activeforeground=COLORS['accent'],
            font=('Segoe UI', 10, 'underline'),
            cursor='hand2', relief=tk.FLAT, bd=0,
            highlightthickness=1, highlightbackground=parent_bg,
            highlightcolor=COLORS['accent'], takefocus=True,
            command=lambda: webbrowser.open(url))
        btn.bind('<Enter>', lambda e: btn.configure(fg=COLORS['accent']))
        btn.bind('<Leave>', lambda e: btn.configure(fg=COLORS['info']))
        return btn

    def _build_header(self, parent, row):
        header = tk.Frame(parent, bg=COLORS['bg'])
        header.grid(row=row, column=0, sticky='ew', pady=(0, 4))
        header.columnconfigure(0, weight=1)
        left = tk.Frame(header, bg=COLORS['bg'])
        left.grid(row=0, column=0, sticky='w')
        try:
            self._logo = ClickableLogo(
                left, version=APP_VERSION,
                on_click=self._show_instructions_popup)
            self._logo.pack(side=tk.LEFT)
            self._add_tip(self._logo,
                          "🖱️ Clique no logo (ou Tab até ele + Enter)\n"
                          "para ver as instruções de uso e atalhos.\n"
                          "Atalho rápido: F1")
        except Exception:
            tk.Label(left, text=f"{LOGO_ICON} DARKPENBOOT",
                     font=('Segoe UI', 13, 'bold'),
                     fg=COLORS['accent'], bg=COLORS['bg']).pack(side=tk.LEFT)
            tk.Label(left, text=f" v{APP_VERSION}", font=('Segoe UI', 8),
                     fg=COLORS['label_fg'],
                     bg=COLORS['bg']).pack(side=tk.LEFT)
            self._logo = None
        right = tk.Frame(header, bg=COLORS['bg'])
        right.grid(row=0, column=1, sticky='e')
        current_label = _label_from_key(self.config.get('theme', 'matrix'))
        try:
            self.neon_ball = NeonThemeBall(
                right, theme_labels=THEME_LABELS, current_label=current_label,
                on_change=self._on_neon_theme_change, size=42)
            self.neon_ball.pack(side=tk.RIGHT, padx=(6, 0))
            self._add_tip(self.neon_ball,
                          "🎨 Orb 3D Neon — Trocar tema\n\n"
                          "• Clique ou pressione Enter/Espaço\n"
                          "• Tab até o orb e Enter também funciona\n"
                          "• O orb tem RASTRO NEON pulsante\n"
                          "• O orb OSCILA por todas as cores (v3.6.0)\n"
                          "• 7 temas (incluindo 🌙 Soft Dark)")
        except Exception:
            self.neon_ball = None

    def _on_neon_theme_change(self, label):
        try:
            self._apply_theme_by_label(label)
        except Exception:
            pass

    def _apply_theme_by_label(self, label):
        theme_key = _key_from_label(label)
        if theme_key == self.config.get('theme'):
            return
        self.config['theme'] = theme_key
        save_config(self.config)
        global COLORS
        COLORS = THEMES[theme_key]
        try:
            current_geom = self.root.geometry()
        except Exception:
            current_geom = None
        self._apply_ttk_style()
        self._rebuild_all_widgets()
        try:
            if current_geom:
                self.root.geometry(current_geom)
        except Exception:
            pass
        self.log(f"🎨 Tema: {label}", is_success=True)

    def _build_drive_card(self, parent, row):
        card = self._make_labelframe(parent, " 🔌 Pendrive USB ")
        card.pack(fill=tk.X, padx=4, pady=4)
        inner = tk.Frame(card, bg=COLORS['frame_bg'])
        inner.pack(fill=tk.X)
        inner.columnconfigure(0, weight=1)
        select_btn = self._make_button(inner, "🎯 Selecionar pendrive",
                                        self._manual_select_drive,
                                        kind="primary")
        select_btn.grid(row=0, column=0, columnspan=2, sticky='ew', pady=(0, 4))
        self._add_tip(select_btn,
                      "🎯 Seleção manual: abre a janela do sistema.\n"
                      "Não executa atualização automática.")
        self.drive_combo = ttk.Combobox(inner, state='readonly')
        self.drive_combo.grid(row=1, column=0, sticky='ew', padx=(0, 4))
        self.drive_combo.bind('<<ComboboxSelected>>', self._on_drive_selected)
        self._add_tip(self.drive_combo,
                      "🔌 Pendrive alvo\n"
                      "Selecione o dispositivo USB detectado.")
        btn = self._make_button(inner, "🔄 Atualizar", self.refresh_drives,
                                 kind="normal")
        btn.grid(row=1, column=1, sticky='ew')
        self._add_tip(btn, "🔄 Atualizar lista de pendrives (F5)")

        if IS_IOS:
            otg_lbl = tk.Label(card,
                               text=("📱 iOS — Conecte via adaptador Lightning/USB-C OTG."),
                               fg=COLORS['info'], bg=COLORS['frame_bg'],
                               font=('Segoe UI', 8, 'italic'),
                               wraplength=380, justify=tk.LEFT)
            otg_lbl.pack(fill=tk.X, pady=(6, 0))
        elif IS_ANDROID or IS_TERMUX:
            otg_lbl = tk.Label(card,
                               text=("📱 Android/Termux — OTG detectado. "
                                     "Gravação raw requer ROOT."),
                               fg=COLORS['info'], bg=COLORS['frame_bg'],
                               font=('Segoe UI', 8, 'italic'),
                               wraplength=380, justify=tk.LEFT)
            otg_lbl.pack(fill=tk.X, pady=(6, 0))

        recov_frame = tk.Frame(card, bg=COLORS['frame_bg'])
        recov_frame.pack(fill=tk.X, pady=(6, 0))
        recov_btn = self._make_button(
            recov_frame,
            "🛠️  Recuperação e Reparo USB  (Ctrl+R)",
            self._open_usb_recovery,
            kind="danger",
            font=('Segoe UI', 10, 'bold'))
        recov_btn.pack(fill=tk.X, padx=2)
        self._add_tip(recov_btn,
                      "🛠️ Painel de Recuperação/Reparo USB\n\n"
                      "• Terminal/shell nativo do SO\n"
                      "• Chkdsk, limpar disco, remover readonly\n"
                      "• Reconstruir MBR/GPT\n"
                      "• Botão Identificar + seletor de pendrive\n\n"
                      "Atalho: Ctrl+R")

    def _build_iso_card(self, parent, row):
        card = self._make_labelframe(parent, " 💿 Imagem ISO ")
        card.pack(fill=tk.X, padx=4, pady=4)
        inner = tk.Frame(card, bg=COLORS['frame_bg'])
        inner.pack(fill=tk.X)
        inner.columnconfigure(0, weight=1)
        self.iso_entry = tk.Entry(
            inner, bg=COLORS['entry_bg'], fg=COLORS['entry_fg'],
            insertbackground=COLORS['fg'], relief=tk.FLAT, bd=2,
            highlightthickness=1,
            highlightbackground=COLORS['frame_border'],
            highlightcolor=COLORS['accent'], font=('Consolas', 9))
        self.iso_entry.pack(fill=tk.X, ipady=5, pady=(0, 4))
        btn_row = tk.Frame(inner, bg=COLORS['frame_bg'])
        btn_row.pack(fill=tk.X)
        for i in range(3):
            btn_row.columnconfigure(i, weight=1)
        b1 = self._make_button(btn_row, "📂 Selecionar ISO", self._select_iso)
        b1.grid(row=0, column=0, padx=1, sticky='ew')
        self._add_tip(b1, "📂 Escolher arquivo ISO/IMG (Ctrl+O)")
        b2 = self._make_button(btn_row, "📋 ISOs recentes", self._show_recent_isos)
        b2.grid(row=0, column=1, padx=1, sticky='ew')
        self._add_tip(b2, "📋 Últimas 5 ISOs usadas (Tab/Enter para escolher)")
        b3 = self._make_button(btn_row, "🔐 Hash", self._show_checksums)
        b3.grid(row=0, column=2, padx=1, sticky='ew')
        self._add_tip(b3, "🔐 Calcula checksums")

    def _build_download_card(self, parent, row):
        card = self._make_labelframe(parent, " ⬇️ Download ")
        card.pack(fill=tk.X, padx=4, pady=4)
        inner = tk.Frame(card, bg=COLORS['frame_bg'])
        inner.pack(fill=tk.X)
        inner.columnconfigure(1, weight=1)

        tk.Label(inner, text="🐧", fg=COLORS['label_fg'],
                 bg=COLORS['frame_bg']).grid(row=0, column=0, sticky='w',
                                              pady=2)
        self.distro_combo = ttk.Combobox(
            inner, values=list(LINUX_DISTROS.keys()), state='readonly')
        self.distro_combo.set(list(LINUX_DISTROS.keys())[0])
        self.distro_combo.grid(row=0, column=1, sticky='ew', padx=4, pady=2)
        b1 = self._make_button(inner, "📥 Baixar", self._download_linux_iso)
        b1.grid(row=0, column=2, padx=2, pady=2)
        # ── v3.6.1: botão Site Oficial ──
        b1b = self._make_button(inner, "🌐 Site", self._open_distro_site,
                                 width=70)
        b1b.grid(row=0, column=3, padx=2, pady=2)
        self._add_tip(b1b,
                      "🌐 Abre o site oficial da distro selecionada.\n"
                      "Fonte sempre atualizada.")
        self._add_tip(b1,
                      "📥 Baixa a distro Linux com FALLBACK\n"
                      "(curl → wget → urllib) + User-Agent de navegador\n"
                      "🔐 Verifica SHA256 automaticamente quando disponível\n"
                      "🐧 v3.6.0: ~35 distros com links oficiais")

        nixos_info = tk.Label(
            inner,
            text="🎯 v3.6.0 — ~35 distros Linux disponíveis com links oficiais",
            fg=COLORS['accent2'], bg=COLORS['frame_bg'],
            font=('Segoe UI', 8, 'italic'))
        nixos_info.grid(row=1, column=0, columnspan=3, sticky='ew',
                        pady=(2, 6))

        tk.Label(inner, text="🌐", fg=COLORS['label_fg'],
                 bg=COLORS['frame_bg']).grid(row=2, column=0, sticky='w',
                                              pady=2)
        self.windows_combo = ttk.Combobox(
            inner, values=list(WINDOWS_OPTIONS.keys()), state='readonly')
        self.windows_combo.set(list(WINDOWS_OPTIONS.keys())[0])
        self.windows_combo.grid(row=2, column=1, sticky='ew', padx=4, pady=2)
        b2 = self._make_button(inner, "🌐 Site", self._download_windows_iso, width=70)
        b2.grid(row=2, column=2, padx=2, pady=2)
        self._add_tip(b2, "🌐 Abre o site oficial da Microsoft no navegador.")

        tk.Label(inner, text="🍏", fg=COLORS['label_fg'],
                 bg=COLORS['frame_bg']).grid(row=3, column=0, sticky='w',
                                              pady=2)
        b3 = self._make_button(inner, "📥 macOS", self._download_macos)
        b3.grid(row=3, column=1, columnspan=2, padx=4, pady=2, sticky='ew')
        self._add_tip(b3, "🍏 Abre o repositório de download do macOS.")

        sep = tk.Frame(card, bg=COLORS['frame_border'], height=1)
        sep.pack(fill=tk.X, pady=(8, 6))
        self._download_cancel_btn = self._make_button(
            card,
            "⏹️  CANCELAR DOWNLOAD EM ANDAMENTO",
            self._cancel_download,
            kind="danger",
            font=('Segoe UI', 10, 'bold'),
            state=tk.DISABLED)
        self._download_cancel_btn.pack(fill=tk.X, padx=2, pady=(2, 4))
        self._add_tip(self._download_cancel_btn,
                      "⏹️ Cancela o download em andamento.")

    def _build_basic_options(self, parent):
        frame = tk.Frame(parent, bg=COLORS['frame_bg'])
        frame.pack(fill=tk.X, padx=8, pady=8)
        r1 = tk.Frame(frame, bg=COLORS['frame_bg'])
        r1.pack(fill=tk.X, pady=3)
        tk.Label(r1, text="FS:", fg=COLORS['label_fg'], bg=COLORS['frame_bg'],
                 font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        self.fs_combo = ttk.Combobox(r1, values=FS_LIST, state='readonly', width=10)
        self.fs_combo.set(self.config.get('filesystem', 'NTFS'))
        self.fs_combo.pack(side=tk.LEFT, padx=4)
        self._add_tip(self.fs_combo, "📁 Sistema de arquivos")
        tk.Label(r1, text="Esq:", fg=COLORS['label_fg'],
                 bg=COLORS['frame_bg'],
                 font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=(10, 4))
        self.scheme_combo = ttk.Combobox(r1, values=['MBR', 'GPT'],
                                          state='readonly', width=6)
        self.scheme_combo.set(self.config.get('scheme', 'MBR'))
        self.scheme_combo.pack(side=tk.LEFT)
        self._add_tip(self.scheme_combo, "🗂️ Esquema de partição")
        r2 = tk.Frame(frame, bg=COLORS['frame_bg'])
        r2.pack(fill=tk.X, pady=6)
        self.quick_var = tk.BooleanVar(value=self.config.get('quick_format', True))
        cb1 = tk.Checkbutton(r2, text="Format. Rápida", variable=self.quick_var,
                       fg=COLORS['label_fg'], bg=COLORS['frame_bg'],
                       activebackground=COLORS['frame_bg'],
                       activeforeground=COLORS['accent'],
                       selectcolor=COLORS['entry_bg'],
                       font=('Segoe UI', 10))
        cb1.pack(side=tk.LEFT)
        self._add_tip(cb1, "⚡ Formatação rápida")
        r3 = tk.Frame(frame, bg=COLORS['frame_bg'])
        r3.pack(fill=tk.X, pady=3)
        self.verify_var = tk.BooleanVar(value=self.config.get('verify', False))
        cb2 = tk.Checkbutton(r3, text="Verificar:", variable=self.verify_var,
                       fg=COLORS['label_fg'], bg=COLORS['frame_bg'],
                       activebackground=COLORS['frame_bg'],
                       activeforeground=COLORS['accent'],
                       selectcolor=COLORS['entry_bg'],
                       font=('Segoe UI', 10))
        cb2.pack(side=tk.LEFT)
        self._add_tip(cb2, "🔐 Verificação pós-gravação")
        self.hash_algo_combo = ttk.Combobox(
            r3, values=HASH_ALGOS, state='readonly', width=11)
        self.hash_algo_combo.set(self.config.get('hash_algo', 'SHA256'))
        self.hash_algo_combo.pack(side=tk.LEFT, padx=(4, 0))
        self._add_tip(self.hash_algo_combo, "🔐 Algoritmo de hash")
        tk.Label(frame, text="Modo de Gravação:",
                 fg=COLORS['label_fg'], bg=COLORS['frame_bg'],
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(8, 3))
        self.mode_combo = ttk.Combobox(
            frame, values=["Extrair (recomendado)", "DD (clonagem bit-a-bit)"],
            state='readonly')
        self.mode_combo.current(
            0 if self.config.get('mode', 'extract') == 'extract' else 1)
        self.mode_combo.pack(fill=tk.X)
        self._add_tip(self.mode_combo,
                      "⚙️ Modo de gravação\n\n"
                      "• Extrair: formata e copia arquivos\n"
                      "• DD: clonagem bit-a-bit (pendrive é remontado)")
    def _build_advanced_options(self, parent):
        frame = tk.Frame(parent, bg=COLORS['frame_bg'])
        frame.pack(fill=tk.X, padx=8, pady=8)

        tk.Label(frame, text="🎯 Método de Gravação (DD / Bit-a-Bit):",
                 fg=COLORS['label_fg'], bg=COLORS['frame_bg'],
                 font=('Segoe UI', 10, 'bold')).pack(anchor='w', pady=(0, 4))
        self.leave_raw_var = tk.BooleanVar(
            value=self.config.get('leave_raw_dd', False))
        rb_frame = tk.Frame(frame, bg=COLORS['frame_bg'])
        rb_frame.pack(fill=tk.X, pady=(0, 8))
        rb_online = tk.Radiobutton(
            rb_frame,
            text="🔄  REMONTAR pendrive (recomendado) — disco volta online com letra",
            variable=self.leave_raw_var, value=False,
            fg=COLORS['label_fg'], bg=COLORS['frame_bg'],
            activebackground=COLORS['frame_bg'],
            activeforeground=COLORS['success'],
            selectcolor=COLORS['entry_bg'],
            font=('Segoe UI', 9))
        rb_online.pack(anchor='w', pady=1)
        rb_raw = tk.Radiobutton(
            rb_frame,
            text="🔒  DEIXAR RAW (offline) — comportamento antigo do modo DD",
            variable=self.leave_raw_var, value=True,
            fg=COLORS['label_fg'], bg=COLORS['frame_bg'],
            activebackground=COLORS['frame_bg'],
            activeforeground=COLORS['warning'],
            selectcolor=COLORS['entry_bg'],
            font=('Segoe UI', 9))
        rb_raw.pack(anchor='w', pady=1)
        self._add_tip(rb_online,
                      "🔄 Após gravar em DD, o disco é remontado\n"
                      "automaticamente e uma letra é atribuída.\n"
                      "Pendrive não some do Explorer.")
        self._add_tip(rb_raw,
                      "🔒 Mantém o disco OFFLINE (RAW puro).\n"
                      "Use apenas se precisar do estado bruto.\n"
                      "Requer diskmgmt.msc para reativar.")
        tk.Label(frame,
                 text=("💡 Dica: no modo Extrair, o pendrive é formatado "
                       "no FS escolhido (NTFS/FAT32/exFAT)\n"
                       "e permanece visível normalmente no Windows."),
                 fg=COLORS['info'], bg=COLORS['frame_bg'],
                 font=('Segoe UI', 8, 'italic'), justify=tk.LEFT).pack(
                     anchor='w', pady=(0, 8))
        tk.Frame(frame, bg=COLORS['frame_border'], height=1).pack(
            fill=tk.X, pady=(0, 8))

        def _row(label, values, current, tip):
            r = tk.Frame(frame, bg=COLORS['frame_bg'])
            r.pack(fill=tk.X, pady=3)
            tk.Label(r, text=label, fg=COLORS['label_fg'],
                     bg=COLORS['frame_bg'],
                     font=('Segoe UI', 9, 'bold'),
                     width=16, anchor='w').pack(side=tk.LEFT)
            cb = ttk.Combobox(r, values=values, state='readonly', width=16)
            cb.set(current)
            cb.pack(side=tk.LEFT, padx=4, fill=tk.X, expand=True)
            self._add_tip(cb, tip)
            return cb

        self.log_level_combo = _row(
            "Nível de log:", LOG_LEVELS,
            self.config.get('log_level', 'Detalhado'),
            "📋 Básico / Detalhado / Debug / Verbose")
        self.buffer_combo = _row(
            "Buffer I/O:", BUFFER_OPTIONS,
            self.config.get('buffer_override', 'Auto (por tier USB)'),
            "⚡ Tamanho do buffer de gravação")
        self.chunk_combo = _row(
            "Chunk:", CHUNK_OPTIONS,
            self.config.get('chunk_override', 'Auto'),
            "🔪 Chunk (512KB = cancel rápido)")
        self.reopen_combo = _row(
            "Reopen:", REOPEN_OPTIONS,
            self.config.get('reopen_attempts', '5'),
            "🔄 Tentativas de reabrir dispositivo")
        self.align_combo = _row(
            "Alinhamento:", ALIGN_OPTIONS,
            self.config.get('align_override', 'Auto (1024 KB)'),
            "📐 Alinhamento da partição")
        self.cluster_combo = _row(
            "Cluster:", CLUSTER_OPTIONS,
            self.config.get('cluster_override', 'Auto'),
            "🗂️ Tamanho do cluster NTFS/exFAT")

        r_fsync = tk.Frame(frame, bg=COLORS['frame_bg'])
        r_fsync.pack(fill=tk.X, pady=4)
        self.fsync_var = tk.BooleanVar(value=self.config.get('force_fsync', True))
        cb_fsync = tk.Checkbutton(
            r_fsync, text="Forçar fsync ao final",
            variable=self.fsync_var,
            fg=COLORS['label_fg'], bg=COLORS['frame_bg'],
            activebackground=COLORS['frame_bg'],
            activeforeground=COLORS['accent'],
            selectcolor=COLORS['entry_bg'],
            font=('Segoe UI', 10))
        cb_fsync.pack(side=tk.LEFT)
        self._add_tip(cb_fsync, "💾 Garante dados no dispositivo")

        r_dbg = tk.Frame(frame, bg=COLORS['frame_bg'])
        r_dbg.pack(fill=tk.X, pady=4)
        self.debug_var = tk.BooleanVar(value=self.config.get('debug', False))
        cb_dbg = tk.Checkbutton(
            r_dbg, text="Modo Debug (stack trace)",
            variable=self.debug_var,
            fg=COLORS['label_fg'], bg=COLORS['frame_bg'],
            activebackground=COLORS['frame_bg'],
            activeforeground=COLORS['accent'],
            selectcolor=COLORS['entry_bg'],
            font=('Segoe UI', 10))
        cb_dbg.pack(side=tk.LEFT)
        self._add_tip(cb_dbg, "🐛 Traceback completo em erros")

        tk.Frame(frame, bg=COLORS['frame_border'], height=1).pack(
            fill=tk.X, pady=8)
        tk.Label(frame,
                 text="⚡ v3.6.0: Logo 🚀 + PgUp/PgDown + ~35 distros + "
                      "Orb oscila cores + Pulso só em tarefas reais.",
                 fg=COLORS['info'], bg=COLORS['frame_bg'],
                 font=('Segoe UI', 8, 'italic'),
                 wraplength=380, justify=tk.LEFT).pack(anchor='w', pady=4)
        if self.config.get('last_operation'):
            tk.Label(frame,
                     text=f"🕐 Última operação: {self.config['last_operation']}",
                     fg=COLORS['info'], bg=COLORS['frame_bg'],
                     font=('Segoe UI', 8, 'italic')).pack(anchor='w', pady=2)

    def _build_help_tab(self, parent):
        frame = tk.Frame(parent, bg=COLORS['frame_bg'])
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame, text="📖 Instruções e Atalhos",
                 font=('Segoe UI', 14, 'bold'),
                 fg=COLORS['accent'], bg=COLORS['frame_bg']).pack(
                     anchor='w', pady=(4, 8))

        sep = tk.Frame(frame, bg=COLORS['frame_border'], height=1)
        sep.pack(fill=tk.X, pady=4)

        body = tk.Frame(frame, bg=COLORS['frame_bg'])
        body.pack(fill=tk.BOTH, expand=True)

        txt = tk.Text(body, bg=COLORS['entry_bg'], fg=COLORS['entry_fg'],
                      font=('Consolas', 9), wrap=tk.WORD, relief=tk.FLAT,
                      bd=0, padx=10, pady=10, height=24,
                      highlightthickness=1,
                      highlightbackground=COLORS['frame_border'])
        txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb = ttk.Scrollbar(body, orient=tk.VERTICAL, command=txt.yview,
                            style='Vertical.TScrollbar')
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        txt.configure(yscrollcommand=sb.set)

        content = (
            "🚀 DARKPENBOOT PRO v3.6.0 — GUIA RÁPIDO\n"
            "═══════════════════════════════════════════════\n\n"
            "📌 PASSO A PASSO\n"
            "───────────────────────────────────────────────\n"
            "1) Conecte o pendrive USB\n"
            "2) Aba 🔌 PENDRIVE → clique 🔄 ATUALIZAR\n"
            "3) Selecione o dispositivo alvo\n"
            "4) Aba 💿 ISO → 📂 SELECIONAR ISO\n"
            "   (ou ⬇️ DOWNLOAD para baixar distros)\n"
            "5) Aba ⚙️ BÁSICO → escolha FS e esquema\n"
            "6) Clique 💾 GRAVAR\n\n"
            "───────────────────────────────────────────────\n"
            "🆕 v3.6.0 — NOVIDADES\n"
            "───────────────────────────────────────────────\n"
            "• Logo 🚀 (foguete) no lugar do 🔌\n"
            "• PgUp/PgDown navegam em TODAS as modais\n"
            "• Lista EXPANDIDA de ~35 distros oficiais\n"
            "• Pulso Neon SÓ em tarefas reais\n"
            "• Orb 3D OSCILA por todas as cores dos temas\n"
            "• Tema geral da UI permanece ESTÁVEL\n\n"
            "───────────────────────────────────────────────\n"
            "⌨️ ATALHOS\n"
            "───────────────────────────────────────────────\n"
            "F1 ............. Popup de ajuda\n"
            "Ctrl+O ......... Selecionar ISO\n"
            "Ctrl+Enter ..... Iniciar gravação\n"
            "Ctrl+R ......... Painel de Recuperação\n"
            "F5 ............. Atualizar pendrives\n"
            "Ctrl+L ......... Limpar log\n"
            "Ctrl+S ......... Salvar log\n"
            "PgUp/PgDown .... Rolar modais (v3.6.0)\n"
            "Tab / Setas .... Navegar\n"
            "Enter .......... Acionar botão focado\n"
            "Esc ............ Cancelar / fechar popup\n\n"
            "───────────────────────────────────────────────\n"
            "🎨 TEMAS (7 DISPONÍVEIS)\n"
            "───────────────────────────────────────────────\n"
            "🟢 Matrix · 🩸 Crimson · ❄️ Nord\n"
            "⚡ Cyberpunk · 🟠 Monokai · ☀️ Light\n"
            "🌙 Soft Dark\n\n"
            "• Clique no ORB no canto superior direito\n"
            "• O orb oscila por TODAS as cores (v3.6.0)\n\n"
            "───────────────────────────────────────────────\n"
            "🐧 DISTROS DISPONÍVEIS (v3.6.0)\n"
            "───────────────────────────────────────────────\n"
            "~35 distros com links oficiais:\n"
            "Debian · Ubuntu · Mint · Pop!_OS · Zorin\n"
            "elementary · Kali · Parrot · Tails\n"
            "Fedora · AlmaLinux · Rocky · CentOS · RHEL\n"
            "Arch · Manjaro · EndeavourOS · Garuda\n"
            "openSUSE · NixOS · Alpine · Gentoo · Void\n"
            "Slackware · Solus · Proxmox · TrueNAS\n\n"
            "───────────────────────────────────────────────\n"
            "🌐 GitHub: github.com/Avlis1412\n"
            "👤 Autor: Adriano Rodrigues da Silva\n"
            "═══════════════════════════════════════════════"
        )
        txt.insert('1.0', content)
        txt.configure(state='disabled')

        btn_frame = tk.Frame(frame, bg=COLORS['frame_bg'])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        b1 = self._make_button(btn_frame, "📖 Abrir em Popup",
                                self._show_instructions_popup,
                                kind="primary")
        b1.pack(side=tk.LEFT, padx=4)
        self._add_tip(b1, "Abre as instruções em janela popup (F1).")
        b2 = self._make_button(btn_frame, "🌐 GitHub",
                                lambda: webbrowser.open(GITHUB_URL),
                                kind="normal")
        b2.pack(side=tk.LEFT, padx=4)
        self._add_tip(b2, "Abre o repositório no navegador.")

    def _build_sources_tab(self, parent):
        frame = tk.Frame(parent, bg=COLORS['frame_bg'])
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(frame, text="📚 Fontes, Créditos e Licenças",
                 font=('Segoe UI', 14, 'bold'),
                 fg=COLORS['accent'], bg=COLORS['frame_bg']).pack(
                     anchor='w', pady=(4, 8))

        tk.Frame(frame, bg=COLORS['frame_border'], height=1).pack(
            fill=tk.X, pady=4)

        body = tk.Frame(frame, bg=COLORS['frame_bg'])
        body.pack(fill=tk.BOTH, expand=True)

        txt = tk.Text(body, bg=COLORS['entry_bg'], fg=COLORS['entry_fg'],
                      font=('Consolas', 9), wrap=tk.WORD, relief=tk.FLAT,
                      bd=0, padx=10, pady=10, height=24,
                      highlightthickness=1,
                      highlightbackground=COLORS['frame_border'])
        txt.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb = ttk.Scrollbar(body, orient=tk.VERTICAL, command=txt.yview,
                            style='Vertical.TScrollbar')
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        txt.configure(yscrollcommand=sb.set)

        content = (
            "📚 FONTES, CRÉDITOS E LICENÇAS — v3.6.0\n"
            "═══════════════════════════════════════════════\n\n"
            + GENERAL_LEGAL_NOTICE + "\n\n"
            "═══════════════════════════════════════════════\n"
            "🐧 DISTROS LINUX E SUAS LICENÇAS (v3.6.0)\n"
            "═══════════════════════════════════════════════\n\n"
            "• Debian 12 — DFSG-compliant (GPL, MIT, BSD)\n"
            "  Site: debian.org | Download: debian.org/distrib/\n\n"
            "• Ubuntu 24.04 LTS — GPL-3.0\n"
            "  Site: ubuntu.com | Download: ubuntu.com/download\n\n"
            "• Linux Mint 22 — GPL-3.0\n"
            "  Site: linuxmint.com | Download: linuxmint.com/download.php\n\n"
            "• Pop!_OS 22.04 LTS — GPL-3.0 (System76)\n"
            "  Site: pop.system76.com\n\n"
            "• Zorin OS 17 Core — GPL-3.0\n"
            "  Site: zorin.com | Download: zorin.com/os/download/\n\n"
            "• elementary OS 7 — GPL-3.0 + LGPL\n"
            "  Site: elementary.io\n\n"
            "• Kali Linux 2024.3 — GPL-3.0 (Debian derivative)\n"
            "  Site: kali.org | Download: kali.org/get-kali/\n\n"
            "• Parrot OS 7.3 — GPL-3.0 (Debian derivative)\n"
            "  Site: parrotsec.org | Download: parrotsec.org/download/\n\n"
            "• Tails 6 — GPL-3.0\n"
            "  Site: tails.net | Download: tails.net/install/\n\n"
            "• Fedora 40 — GPL-2.0 + MIT + Apache 2.0\n"
            "  Site: fedoraproject.org\n\n"
            "• AlmaLinux 9 — GPL-2.0 + BSD\n"
            "  Site: almalinux.org\n\n"
            "• Rocky Linux 9 — GPL-2.0 + BSD\n"
            "  Site: rockylinux.org\n\n"
            "• CentOS Stream 9 — GPL-2.0\n"
            "  Site: centos.org\n\n"
            "• RHEL 9 Developer — Red Hat Subscription\n"
            "  Site: developers.redhat.com\n\n"
            "• Arch Linux — GPL-2.0 e similares\n"
            "  Site: archlinux.org | Download: archlinux.org/download/\n\n"
            "• Manjaro KDE — GPL-3.0 (Arch-based)\n"
            "  Site: manjaro.org | Foundation: Manjaro GmbH & Co. KG\n\n"
            "• EndeavourOS — GPL-3.0 (Arch-based)\n"
            "  Site: endeavouros.com\n\n"
            "• Garuda Linux — GPL-3.0 (Arch-based)\n"
            "  Site: garudalinux.org\n\n"
            "• openSUSE Leap 15.6 — GPL-2.0 / GPL-3.0\n"
            "  Site: opensuse.org | Foundation: openSUSE Project / SUSE\n\n"
            "• openSUSE Tumbleweed — GPL-2.0 / GPL-3.0\n"
            "  Site: opensuse.org\n\n"
            "• NixOS 24.11 / 25.05 — MIT (Nixpkgs) + LGPL-2.1 (Nix)\n"
            "  Site: nixos.org | Download: nixos.org/download/\n\n"
            "• Alpine Linux — MIT + GPL-2.0\n"
            "  Site: alpinelinux.org\n\n"
            "• Gentoo Linux — GPL-2.0\n"
            "  Site: gentoo.org\n\n"
            "• Void Linux — BSD-2-Clause + outros\n"
            "  Site: voidlinux.org\n\n"
            "• Slackware 15 — Slackware License (BSD-like)\n"
            "  Site: slackware.com\n\n"
            "• Solus — GPL-2.0\n"
            "  Site: getsol.us\n\n"
            "• Proxmox VE 8.2 — AGPL-3.0\n"
            "  Site: proxmox.com\n\n"
            "• TrueNAS SCALE — BSD-2-Clause (iXsystems)\n"
            "  Site: truenas.com\n\n"
            "═══════════════════════════════════════════════\n"
            "🪟 MICROSOFT — WINDOWS E SERVER\n"
            "═══════════════════════════════════════════════\n\n"
            "Todas as ISOs do Windows e Windows Server são\n"
            "obtidas EXCLUSIVAMENTE via links oficiais da\n"
            "Microsoft (microsoft.com). O DarkPenBoot Pro\n"
            "apenas redireciona o navegador para os canais\n"
            "oficiais — nenhuma ISO é armazenada ou\n"
            "distribuída pelo aplicativo.\n\n"
            "Windows® é marca registrada da Microsoft Corporation.\n\n"
            "═══════════════════════════════════════════════\n"
            "🍏 APPLE macOS\n"
            "═══════════════════════════════════════════════\n\n"
            "Distribuição via repositório comunitário:\n"
            "   github.com/Comp-Labs/Download-macOS\n\n"
            "macOS® é marca registrada da Apple Inc.\n\n"
            "═══════════════════════════════════════════════\n"
            "🛠️ SOFTWARE DE TERCEIROS UTILIZADO\n"
            "═══════════════════════════════════════════════\n\n"
            "• 7-Zip (Igor Pavlov) — LGPL + BSD + unRAR restriction\n"
            "• WinRAR / UnRAR (win.rar GmbH) — Trial + unRAR license\n"
            "• bsdtar / libarchive — BSD-2-Clause\n"
            "• curl (Daniel Stenberg) — MIT-like\n"
            "• wget (GNU Project) — GPL-3.0\n"
            "• Python 3 (PSF) — PSF License\n"
            "• Tkinter / ttk (Tcl/Tk) — BSD-style\n\n"
            "═══════════════════════════════════════════════\n"
            "👤 AUTOR DO DARKPENBOOT PRO\n"
            "═══════════════════════════════════════════════\n\n"
            + LICENSE_REGISTRATION_NOTICE + "\n\n"
            "═══════════════════════════════════════════════\n"
            f"📅 Documento atualizado em v{APP_VERSION}\n"
            "═══════════════════════════════════════════════"
        )
        txt.insert('1.0', content)
        txt.configure(state='disabled')

        btn_frame = tk.Frame(frame, bg=COLORS['frame_bg'])
        btn_frame.pack(fill=tk.X, pady=(10, 0))
        b1 = self._make_button(
            btn_frame, "📜 Licença Completa",
            self._show_license_popup,
            kind="primary", width=170)
        b1.pack(side=tk.LEFT, padx=4)
        self._add_tip(b1, "Mostra a licença de uso completa.")
        b2 = self._make_button(
            btn_frame, "🌐 GitHub",
            lambda: webbrowser.open(GITHUB_URL),
            kind="normal", width=140)
        b2.pack(side=tk.LEFT, padx=4)
        self._add_tip(b2, "Abre o repositório oficial.")

    def _show_license_popup(self):
        UltimatePopup.show(
            self.root, "📜 Licença de Uso — DarkPenBoot Pro",
            LICENSE_REGISTRATION_NOTICE, kind="info")

    def _build_progress(self, parent, row):
        wrapper = tk.Frame(parent, bg=COLORS['bg'])
        wrapper.grid(row=row, column=0, sticky='ew', pady=(2, 4))
        frame = tk.Frame(wrapper, bg=COLORS['frame_bg'],
                         highlightbackground=COLORS['frame_border'],
                         highlightthickness=1)
        frame.pack(fill=tk.X)
        inner = tk.Frame(frame, bg=COLORS['frame_bg'])
        inner.pack(fill=tk.X, padx=8, pady=4)
        inner.columnconfigure(0, weight=1)
        self.current_file_label = tk.Label(inner, text="",
                                            fg=COLORS['warning'],
                                            bg=COLORS['frame_bg'],
                                            font=('Consolas', 8), anchor='w')
        self.current_file_label.grid(row=0, column=0, columnspan=2, sticky='ew')
        self.progress = ttk.Progressbar(inner, mode='determinate')
        self.progress.grid(row=1, column=0, sticky='ew', pady=(2, 2))
        self.percent_label = tk.Label(inner, text="0%", fg=COLORS['fg'],
                                       bg=COLORS['frame_bg'],
                                       font=('Segoe UI', 9, 'bold'))
        self.percent_label.grid(row=1, column=1, sticky='e', padx=(6, 0))
        led_row = tk.Frame(inner, bg=COLORS['frame_bg'])
        led_row.grid(row=2, column=0, columnspan=2, sticky='ew')
        self.led_canvas = tk.Canvas(led_row, width=14, height=14,
                                     bg=COLORS['frame_bg'],
                                     highlightthickness=0)
        self.led_canvas.pack(side=tk.LEFT)
        self.led_id = self.led_canvas.create_rectangle(2, 2, 12, 12,
                                                        fill=COLORS['led_off'],
                                                        outline='')
        self.status_label = tk.Label(led_row, text="✅ Pronto",
                                      fg=COLORS['success'],
                                      bg=COLORS['frame_bg'],
                                      font=('Segoe UI', 9, 'bold'))
        self.status_label.pack(side=tk.LEFT, padx=6)

    def _build_buttons(self, parent, row):
        frame = tk.Frame(parent, bg=COLORS['bg'])
        frame.grid(row=row, column=0, sticky='ew', pady=(2, 2))
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)
        frame.columnconfigure(2, weight=1)
        self.start_btn = self._make_button(frame, "💾 GRAVAR",
                                            self._start_operation,
                                            kind="primary",
                                            font=('Segoe UI', 11, 'bold'))
        self.start_btn.grid(row=0, column=0, padx=(0, 3), pady=3, sticky='ew')
        self._add_tip(self.start_btn, "💾 Inicia criação (Ctrl+Enter)")
        self.reset_btn = self._make_button(
            frame, "↺ RESTAURAR", self._reset_to_recommended,
            kind="normal", font=('Segoe UI', 10, 'bold'))
        self.reset_btn.grid(row=0, column=1, padx=3, pady=3, sticky='ew')
        self._add_tip(
            self.reset_btn,
            "↺ Restaura as configurações para o estado recomendado.\n"
            "Preserva ISOs, logs, downloads e a licença Premium.")
        self.cancel_btn = self._make_button(frame, "❌ CANCELAR",
                                             self._cancel_operation,
                                             kind="danger",
                                             font=('Segoe UI', 11, 'bold'),
                                             state=tk.DISABLED)
        self.cancel_btn.grid(row=0, column=2, padx=(3, 0), pady=3, sticky='ew')
        self._add_tip(self.cancel_btn, "❌ Cancela gravação (Esc)")

    def _reset_to_recommended(self):
        if self.is_running or self.download_active:
            self.log("⚠️ Finalize a operação atual antes de restaurar.",
                     is_warning=True)
            return
        if not self._popup_ask(
                "Restaurar recomendado",
                "Restaurar as configurações para o estado recomendado?\n\n"
                "A ISO selecionada, preferências, tema e opções avançadas\n"
                "serão limpos. Downloads, logs e licença Premium permanecem."):
            return

        premium_unlocked = self.premium_unlocked
        license_key = self.config.get('license_key', '')
        self.config = dict(DEFAULT_CONFIG)
        self.config['premium_unlocked'] = premium_unlocked
        self.config['license_key'] = license_key
        self.ad_mode = ('premium_no_ads' if premium_unlocked
                        else self.config['ad_mode'])
        self.config['ad_mode'] = self.ad_mode
        self.iso_path = ''
        self.selected_drive = None
        save_config(self.config)

        global COLORS
        COLORS = THEMES[self.config['theme']]
        self._rebuild_all_widgets()
        try:
            self.iso_entry.delete(0, tk.END)
            self.fs_combo.set(DEFAULT_CONFIG['filesystem'])
            self.scheme_combo.set(DEFAULT_CONFIG['scheme'])
            self.mode_combo.current(0)
            self.quick_var.set(DEFAULT_CONFIG['quick_format'])
            self.verify_var.set(DEFAULT_CONFIG['verify'])
            self.hash_algo_combo.set(DEFAULT_CONFIG['hash_algo'])
            self.log_level_combo.set(DEFAULT_CONFIG['log_level'])
            self.buffer_combo.set(DEFAULT_CONFIG['buffer_override'])
            self.chunk_combo.set(DEFAULT_CONFIG['chunk_override'])
            self.reopen_combo.set(DEFAULT_CONFIG['reopen_attempts'])
            self.align_combo.set(DEFAULT_CONFIG['align_override'])
            self.cluster_combo.set(DEFAULT_CONFIG['cluster_override'])
            self.fsync_var.set(DEFAULT_CONFIG['force_fsync'])
            self.leave_raw_var.set(DEFAULT_CONFIG['leave_raw_dd'])
            self.drive_combo.set('')
            self.distro_combo.current(0)
            self.windows_combo.current(0)
            if self._tab_bar is not None:
                self._tab_bar.select(0, silent=True)
        except Exception:
            pass
        self.log("↺ Configurações restauradas ao estado recomendado.",
                 is_success=True)

    def _build_log(self, parent, row):
        frame = tk.LabelFrame(parent, text=" 📋 Log ",
                              font=('Segoe UI', 9, 'bold'),
                              fg=COLORS['accent2'], bg=COLORS['frame_bg'],
                              relief=tk.GROOVE, bd=1,
                              highlightbackground=COLORS['frame_border'],
                              highlightthickness=1)
        frame.grid(row=row, column=0, sticky='nsew')
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        text_frame = tk.Frame(frame, bg=COLORS['frame_bg'])
        text_frame.grid(row=0, column=0, sticky='nsew', padx=4, pady=4)
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        self.log_text = tk.Text(text_frame, height=5, bg=COLORS['entry_bg'],
                                 fg=COLORS['entry_fg'],
                                 insertbackground=COLORS['fg'],
                                 font=('Consolas', 8), wrap=tk.WORD,
                                 relief=tk.FLAT, bd=0)
        self.log_text.grid(row=0, column=0, sticky='nsew')
        sb = ttk.Scrollbar(text_frame, orient=tk.VERTICAL,
                            command=self.log_text.yview,
                            style="Vertical.TScrollbar")
        sb.grid(row=0, column=1, sticky='ns')
        self.log_text.configure(yscrollcommand=sb.set)
        self.log_text.tag_config('error', foreground=COLORS['error'])
        self.log_text.tag_config('warning', foreground=COLORS['warning'])
        self.log_text.tag_config('success', foreground=COLORS['success'])
        self.log_text.tag_config('info', foreground=COLORS['info'])
        btn_frame = tk.Frame(frame, bg=COLORS['frame_bg'])
        btn_frame.grid(row=1, column=0, sticky='ew', padx=4, pady=(0, 18))
        for i in range(3):
            btn_frame.columnconfigure(i, weight=1)
        bl = self._make_button(btn_frame, "💾 Log", self._save_log, width=70)
        bl.grid(row=0, column=0, padx=1, sticky='ew')
        self._add_tip(bl, "💾 Salvar log (Ctrl+S)")
        bc = self._make_button(btn_frame, "🗑️", self._clear_log, width=70)
        bc.grid(row=0, column=1, padx=1, sticky='ew')
        self._add_tip(bc, "🗑️ Limpa log (Ctrl+L)")
        # ── v3.6.1: doação única no rodapé ──
        ba = self._make_button(btn_frame, "ℹ️ Sobre",
                    lambda: self._show_about(), width=96)
        ba.grid(row=0, column=2, padx=1, sticky='ew')
        self._add_tip(ba, "ℹ️ Sobre + Licença + GitHub")

    def log(self, msg, is_error=False, is_warning=False,
            is_success=False, is_info=False):
        if threading.current_thread() is not threading.main_thread():
            try:
                self.root.after(
                    0,
                    lambda m=msg, e=is_error, w=is_warning, s=is_success,
                    i=is_info: self.log(m, e, w, s, i))
            except Exception:
                pass
            return
        try:
            lvl = (self.log_level_combo.get()
                   if hasattr(self, 'log_level_combo') else 'Detalhado')
        except Exception:
            lvl = 'Detalhado'
        if lvl == 'Básico':
            if not (is_error or is_warning or is_success):
                return
        elif lvl == 'Detalhado':
            if not (is_error or is_warning or is_success or is_info):
                return
        ts = datetime.now().strftime("%H:%M:%S")
        entry = f"[{ts}] {msg}\n"
        tag = None
        if is_error: tag = 'error'
        elif is_warning: tag = 'warning'
        elif is_success: tag = 'success'
        elif is_info: tag = 'info'
        try:
            self.log_text.insert(tk.END, entry)
            if tag:
                start = self.log_text.index("end-2l")
                end = self.log_text.index("end-1l")
                self.log_text.tag_add(tag, start, end)
            self.log_text.see(tk.END)
        except Exception:
            pass
        self._log_buffer.append(entry.rstrip('\n'))
        if len(self._log_buffer) > self._max_log_buffer:
            self._log_buffer = self._log_buffer[-self._max_log_buffer:]

    def _save_log(self):
        default_name = f"darkpenboot_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        if IS_MOBILE:
            default_path = str(LOG_DIR / default_name)
            fp = self._mobile_path_dialog(
                title="Salvar log como",
                hint=f"Caminho para salvar o log",
                prefill=default_path,
                default_dirs=[str(LOG_DIR), str(DOWNLOAD_DIR)])
        else:
            try:
                fp = filedialog.asksaveasfilename(
                    defaultextension=".txt", filetypes=[("Text", "*.txt")],
                    initialfile=default_name)
            except Exception as e:
                self._popup_error("Salvar log",
                                  f"Não foi possível abrir o seletor.\n\n{e}")
                fp = self._mobile_path_dialog(
                    title="Salvar log (digitar caminho)",
                    hint="Caminho completo para salvar o log",
                    prefill=str(LOG_DIR / default_name),
                    default_dirs=[str(LOG_DIR)])
        if fp:
            try:
                os.makedirs(os.path.dirname(fp), exist_ok=True)
                with open(fp, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get("1.0", tk.END))
                self.log(f"💾 Log salvo: {fp}", is_success=True)
            except Exception as e:
                self.log(f"❌ Erro ao salvar log: {e}", is_error=True)

    def _clear_log(self):
        self.log_text.delete("1.0", tk.END)
        self._log_buffer.clear()
        self.log("🗑️ Log limpo.", is_success=True)

    def _get_log_tail(self, n: int = 15) -> str:
        lines = self._log_buffer[-n:] if self._log_buffer else []
        return '\n'.join(lines)

    def _center_toplevel(self, dlg, parent=None):
        """Centraliza uma Toplevel na tela (ou sobre o parent)."""
        try:
            dlg.update_idletasks()
            w = dlg.winfo_width()
            h = dlg.winfo_height()
            if w <= 1:
                w = dlg.winfo_reqwidth()
            if h <= 1:
                h = dlg.winfo_reqheight()
            sw = dlg.winfo_screenwidth()
            sh = dlg.winfo_screenheight()
            x = (sw - w) // 2
            y = (sh - h) // 2
            if x < 10: x = 10
            if y < 10: y = 10
            dlg.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            pass

    def _make_modal(self, dlg):
        """Torna a janela modal: grab + Esc + foco + centralização."""
        try:
            dlg.transient(self.root)
        except Exception:
            pass
        try:
            dlg.grab_set()
            dlg.focus_set()
        except Exception:
            pass
        try:
            dlg.bind('<Escape>', lambda e: self._close_modal(dlg))
            dlg.protocol('WM_DELETE_WINDOW',
                         lambda: self._close_modal(dlg))
        except Exception:
            pass
        self.root.after(60, lambda: self._center_toplevel(dlg))

    def _close_modal(self, dlg):
        try:
            if dlg.winfo_exists():
                try:
                    dlg.grab_release()
                except Exception:
                    pass
                dlg.destroy()
        except Exception:
            pass

    def _show_about(self):
        colors = COLORS
        dlg = tk.Toplevel(self.root)
        dlg.title("ℹ️ Sobre — DarkPenBoot Pro")
        dlg.configure(bg=colors['bg'])
        dlg.resizable(True, True)
        try:
            sw = dlg.winfo_screenwidth()
            sh = dlg.winfo_screenheight()
            w = min(600, int(sw * 0.85))
            h = min(700, int(sh * 0.85))
            x = (sw - w) // 2
            y = max(20, (sh - h) // 2)
            dlg.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            dlg.geometry("600x700")
        dlg.minsize(440, 420)
        self._make_modal(dlg)

        outer = tk.Frame(dlg, bg=colors['frame_bg'],
                         highlightbackground=colors['frame_border'],
                         highlightcolor=colors['accent'], highlightthickness=2)
        outer.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(1, weight=1)
        header = tk.Frame(outer, bg=colors['frame_bg'])
        header.grid(row=0, column=0, sticky='ew', padx=14, pady=(12, 6))
        tk.Label(header, text=f"{LOGO_ICON} {APP_NAME}",
                 font=('Segoe UI', 15, 'bold'),
                 fg=colors['accent'], bg=colors['frame_bg']).pack(anchor='w')
        tk.Label(header,
                 text=f"v{APP_VERSION} — Criador de Pendrives Bootáveis",
                 font=('Segoe UI', 9), fg=colors['label_fg'],
                 bg=colors['frame_bg']).pack(anchor='w')
        body_wrap = tk.Frame(outer, bg=colors['frame_bg'])
        body_wrap.grid(row=1, column=0, sticky='nsew', padx=14, pady=4)
        body_wrap.columnconfigure(0, weight=1)
        body_wrap.rowconfigure(0, weight=1)
        cv = tk.Canvas(body_wrap, bg=colors['frame_bg'], highlightthickness=0)
        cv.grid(row=0, column=0, sticky='nsew')
        sb = ttk.Scrollbar(body_wrap, orient=tk.VERTICAL, command=cv.yview,
                            style='Vertical.TScrollbar')
        sb.grid(row=0, column=1, sticky='ns')
        cv.configure(yscrollcommand=sb.set)
        body = tk.Frame(cv, bg=colors['frame_bg'])
        body.columnconfigure(0, weight=1)
        body.bind('<Configure>',
                  lambda e: cv.configure(scrollregion=cv.bbox('all')))
        bw = cv.create_window((0, 0), window=body, anchor='nw')
        cv.bind('<Configure>', lambda e: cv.itemconfig(bw, width=e.width))
        def _about_wheel(event):
            delta = -1 if event.delta > 0 else 1
            cv.yview_scroll(delta * 3, 'units')
            return 'break'
        for widget in (dlg, cv, body):
            widget.bind('<MouseWheel>', _about_wheel, add='+')
            widget.bind('<Button-4>', lambda e: cv.yview_scroll(-3, 'units'), add='+')
            widget.bind('<Button-5>', lambda e: cv.yview_scroll(3, 'units'), add='+')

        # ── v3.6.0: PgUp/PgDown na janela Sobre ──
        def _pgup_about(e=None):
            try:
                cv.yview_scroll(-8, "units")
            except Exception:
                pass
            return "break"
        def _pgdn_about(e=None):
            try:
                cv.yview_scroll(8, "units")
            except Exception:
                pass
            return "break"
        dlg.bind('<Prior>', _pgup_about, add='+')
        dlg.bind('<Next>',  _pgdn_about, add='+')
        cv.bind('<Prior>',  _pgup_about, add='+')
        cv.bind('<Next>',   _pgdn_about, add='+')
        body.bind('<Prior>', _pgup_about, add='+')
        body.bind('<Next>',  _pgdn_about, add='+')

        desc = (
            "Criador Profissional de Pendrives Bootáveis Universais\n"
            "para Windows, Linux, macOS, Android (Termux) e OTG Mobile.\n\n"
            "🆕 v3.6.0 — Novidades:\n"
            "• Logo 🚀 (foguete) no lugar do 🔌\n"
            "• PgUp/PgDown navegam em TODAS as modais\n"
            "• Lista EXPANDIDA de ~35 distros oficiais\n"
            "• Pulso Neon SÓ em tarefas reais\n"
            "• Orb 3D OSCILA por todas as cores dos temas\n"
            "• Tema geral da UI permanece ESTÁVEL\n\n"
            "✅ v3.5.0 (mantido):\n"
            "• Janelas modais com navegação por teclado\n"
            "• ISOs Recentes centralizado + atalhos\n"
            "• Registro de licença em nome do autor\n\n"
            "✅ v3.4.0 (mantido):\n"
            "• Tema 🌙 Soft Dark (reduz fadiga visual)\n"
            "• Verificação SHA256 automática pós-download\n"
            "• Botão ⭐ PREMIUM (R$ 10) sem anúncios\n\n"
            "🔧 Funcionalidades:\n"
            "• Formatação Multi-FS\n"
            "• Modo Extração + DD bit-a-bit\n"
            "• Painel de Recuperação/Reparo USB\n"
            "• Hashes: SHA256/SHA512/SHA1/MD5/SHA3-256/BLAKE2b\n"
            "• 7 temas visuais com orb neon 3D\n"
            "• Download com CANCELAMENTO e FALLBACK\n\n"
            + GENERAL_LEGAL_NOTICE
        )
        tk.Label(body, text=desc, justify=tk.LEFT, anchor='w',
                 fg=colors['fg'], bg=colors['frame_bg'],
                 font=('Segoe UI', 9), wraplength=520).pack(
                     fill=tk.X, pady=(0, 12))

        author_card = tk.LabelFrame(
            body, text=" 👤 Autor ",
            font=('Segoe UI', 10, 'bold'), fg=colors['accent'],
            bg=colors['frame_bg'], relief=tk.FLAT, bd=0,
            highlightbackground=colors['frame_border'],
            highlightcolor=colors['accent'], highlightthickness=2,
            labelanchor='nw', padx=12, pady=10)
        author_card.pack(fill=tk.X, pady=(0, 12))
        tk.Label(author_card, text=f"👤  {APP_AUTHOR}",
                 fg=colors['fg'], bg=colors['frame_bg'],
                 font=('Segoe UI', 11, 'bold'),
                 anchor='w').pack(fill=tk.X, pady=2)
        gh_row = tk.Frame(author_card, bg=colors['frame_bg'])
        gh_row.pack(fill=tk.X, pady=(6, 2))
        tk.Label(gh_row, text="🌐  GitHub:",
                 fg=colors['label_fg'], bg=colors['frame_bg'],
                 font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
        gh_link = self._make_hyperlink(gh_row, GITHUB_URL, GITHUB_URL)
        gh_link.pack(side=tk.LEFT, padx=(8, 0))
        tk.Label(author_card,
                 text="⭐ Contribua com estrelas, issues e pull requests!",
                 fg=colors['info'], bg=colors['frame_bg'],
                 font=('Segoe UI', 9, 'italic'),
                 anchor='w').pack(fill=tk.X, pady=(6, 0))

        tk.Label(body, text=f"© 2026 — {APP_AUTHOR}. Todos os direitos reservados.",
                 fg=colors['label_fg'], bg=colors['frame_bg'],
                 font=('Segoe UI', 8)).pack(pady=(6, 6))

        footer = tk.Frame(outer, bg=colors['frame_bg'])
        footer.grid(row=2, column=0, sticky='ew', padx=14, pady=(8, 12))
        footer.columnconfigure(0, weight=1)
        footer.columnconfigure(1, weight=0)
        footer.columnconfigure(2, weight=0)
        footer.columnconfigure(3, weight=0)
        lic_btn = self._make_button(
            footer, "📜 Licença",
            self._show_license_popup,
            kind="normal", width=130)
        lic_btn.grid(row=0, column=0, padx=4, sticky='w')
        open_gh_btn = self._make_button(
            footer, "🌐 GitHub",
            lambda: webbrowser.open(GITHUB_URL),
            kind="primary", width=130)
        open_gh_btn.grid(row=0, column=1, padx=4)
        close_btn = self._make_button(footer, "❌ Fechar",
                                       lambda: self._close_modal(dlg),
                                       kind="danger", width=120)
        close_btn.grid(row=0, column=2, padx=4)
        try:
            close_btn.focus_set()
        except Exception:
            pass

    def _open_distro_site(self):
        """Abre o site oficial da distro selecionada."""
        try:
            distro = self.distro_combo.get()
            info = DISTRO_INFO.get(distro, {})
            url = info.get("homepage") or info.get("docs")
            if not url:
                self._popup_warning(
                    "Sem URL",
                    f"A distro '{distro}' não tem site cadastrado.")
                return
            webbrowser.open(url)
            self.log(f"🌐 Site oficial: {url}", is_success=True)
        except Exception as e:
            self.log(f"⚠️ Erro ao abrir site: {e}", is_warning=True)


    def _toggle_favorite(self):
        """v3.6.1: Favorita a ISO atual."""
        try:
            if not self.iso_path or not os.path.isfile(self.iso_path):
                self._popup_info("Favoritos",
                                 "Nenhuma ISO selecionada.")
                return
            nome = os.path.basename(self.iso_path)
            self.log(f"\u2764\ufe0f Favoritado: {nome}", is_success=True)
            self.trigger_reactive_pulse(2, 800)
            self._popup_info("\u2764\ufe0f Favorito",
                             f"ISO marcada como favorita:\n{nome}")
        except Exception as e:
            self.log(f"\u26a0\ufe0f {e}", is_warning=True)

    def _open_ads_settings(self):
        """v3.6.1: Preferencias de anuncios."""
        try:
            self._popup_info(
                "\U0001f4e2 An\u00fancios",
                "Vers\u00e3o gratuita cont\u00e9m an\u00fancios.\n\n"
                f"Assine o PREMIUM ({PREMIUM_PRICE_BRL}) para remov\u00ea-los.\n\n"
                f"\U0001f310 {PREMIUM_CHECKOUT_URL}")
        except Exception as e:
            self.log(f"\u26a0\ufe0f {e}", is_warning=True)

    def _open_mobile_page(self):
        """v3.6.1: Abre a p\u00e1gina da vers\u00e3o mobile."""
        try:
            url = GITHUB_URL + "/releases"
            self.log(f"\U0001f4f1 Abrindo vers\u00e3o mobile: {url}", is_info=True)
            webbrowser.open(url)
        except Exception as e:
            self.log(f"\u26a0\ufe0f {e}", is_warning=True)
    def _open_donate(self):
        dlg = tk.Toplevel(self.root)
        dlg.title("❤️ Doar via PIX")
        dlg.configure(bg=COLORS['bg'])
        dlg.resizable(True, True)
        sw, sh = dlg.winfo_screenwidth(), dlg.winfo_screenheight()
        w = min(780, max(560, sw - 40))
        h = max(620, sh - 40)
        x = max(0, (sw - w) // 2)
        y = 20
        dlg.geometry(f"{w}x{h}+{x}+{y}")
        dlg.minsize(520, 520)
        self._make_modal(dlg)
        dlg.columnconfigure(0, weight=1); dlg.rowconfigure(1, weight=1)
        tk.Label(dlg, text="❤️ Apoie o DarkPenBoot Pro", font=('Segoe UI', 16, 'bold'),
                 fg=COLORS['accent'], bg=COLORS['bg']).grid(row=0,column=0,pady=(14,6),sticky='ew')
        wrap=tk.Frame(dlg,bg=COLORS['bg']); wrap.grid(row=1,column=0,sticky='nsew',padx=12)
        wrap.columnconfigure(0,weight=1); wrap.rowconfigure(0,weight=1)
        canvas=tk.Canvas(wrap,bg=COLORS['bg'],highlightthickness=0)
        sb=ttk.Scrollbar(wrap,orient='vertical',command=canvas.yview,style='Vertical.TScrollbar')
        canvas.grid(row=0,column=0,sticky='nsew'); sb.grid(row=0,column=1,sticky='ns'); canvas.configure(yscrollcommand=sb.set)
        body=tk.Frame(canvas,bg=COLORS['bg']); body.columnconfigure(0,weight=1)
        win=canvas.create_window((0,0),window=body,anchor='nw')
        body.bind('<Configure>',lambda e:canvas.configure(scrollregion=canvas.bbox('all')))
        canvas.bind('<Configure>',lambda e:canvas.itemconfig(win,width=e.width))
        tk.Label(body,text=DONATE_MESSAGE,font=('Segoe UI',10),fg=COLORS['label_fg'],bg=COLORS['bg'],justify=tk.CENTER,wraplength=680).pack(pady=(4,12),padx=16)
        gh=tk.Frame(body,bg=COLORS['bg']);gh.pack(pady=(0,10));tk.Label(gh,text='⭐ GitHub:',fg=COLORS['label_fg'],bg=COLORS['bg'],font=('Segoe UI',10,'bold')).pack(side=tk.LEFT);self._make_hyperlink(gh,GITHUB_URL,GITHUB_URL).pack(side=tk.LEFT,padx=8)
        rc=tk.LabelFrame(body,text=' 👤 Dados do Recebedor ',font=('Segoe UI',10,'bold'),fg=COLORS['accent'],bg=COLORS['frame_bg'],relief=tk.FLAT,bd=0,highlightbackground=COLORS['frame_border'],highlightcolor=COLORS['accent'],highlightthickness=2,labelanchor='nw',padx=12,pady=8);rc.pack(fill=tk.X,padx=12,pady=(0,12))
        def row(label,value,color=None):
            r=tk.Frame(rc,bg=COLORS['frame_bg']);r.pack(fill=tk.X,pady=3);tk.Label(r,text=label,font=('Segoe UI',10,'bold'),fg=COLORS['label_fg'],bg=COLORS['frame_bg'],width=14,anchor='w').pack(side=tk.LEFT);tk.Label(r,text=value,font=('Consolas',10),fg=color or COLORS['fg'],bg=COLORS['frame_bg'],anchor='w',justify=tk.LEFT,wraplength=560).pack(side=tk.LEFT,fill=tk.X,expand=True)
        row('👤 Nome:',PIX_RECEIVER_NAME);row('🏦 Banco:',PIX_BANK_NAME,COLORS['accent']);row('🔢 Conta:',PIX_ACCOUNT_INFO)
        tk.Label(body,text='🔑 Chave PIX (aleatória)',font=('Segoe UI',11,'bold'),fg=COLORS['fg'],bg=COLORS['bg']).pack(anchor='w',padx=14,pady=(2,4))
        keybox=tk.Frame(body,bg=COLORS['accent'],highlightbackground=COLORS['accent'],highlightthickness=3);keybox.pack(fill=tk.X,padx=12,pady=(0,8))
        key_entry=tk.Entry(keybox,bg='#000000',fg='#FFFFFF',insertbackground='#FFFFFF',font=('Consolas',12,'bold'),relief=tk.FLAT,justify=tk.CENTER);key_entry.insert(0,PIX_KEY);key_entry.config(state='readonly');key_entry.pack(fill=tk.X,ipady=10,padx=3,pady=3)
        def copy_key():
            try:
                dlg.clipboard_clear();dlg.clipboard_append(PIX_KEY);self._popup_info('PIX copiado','A chave PIX foi copiada para a área de transferência.')
            except Exception as e:self._popup_error('Erro ao copiar',str(e))
        cb=self._make_button(body,'📋 Copiar Chave PIX',copy_key,kind='primary',width=230);cb.pack(pady=(2,12));self._add_tip(cb,'📋 Copia a chave PIX em alto contraste para a área de transferência.')
        tk.Label(body,text=('💡 Como doar:\n1. Copie a chave acima\n2. Abra o aplicativo do seu banco\n3. Escolha PIX → pagar com chave aleatória\n4. Cole a chave e confirme o recebedor e o valor'),font=('Segoe UI',10),fg=COLORS['info'],bg=COLORS['bg'],justify=tk.LEFT,anchor='w').pack(fill=tk.X,padx=18,pady=(2,18))
        footer=tk.Frame(dlg,bg=COLORS['bg']);footer.grid(row=2,column=0,sticky='ew',padx=12,pady=(6,12));footer.columnconfigure(0,weight=1);footer.columnconfigure(1,weight=0)
        ghb=self._make_button(footer,'🌐 Abrir GitHub',lambda:webbrowser.open(GITHUB_URL),kind='primary',width=180);ghb.grid(row=0,column=0,sticky='w');self._add_tip(ghb,'🌐 Abre o repositório oficial do projeto.')
        close=self._make_button(footer,'❌ Fechar',lambda: self._close_modal(dlg),kind='danger',width=140);close.grid(row=0,column=1,sticky='e');self._add_tip(close,'❌ Fecha a janela de doação.')
        try:
            close.focus_set()
        except Exception:
            pass

        # ── v3.6.0: PgUp/PgDown na janela Doação ──
        def _pgup_donate(e=None):
            try:
                canvas.yview_scroll(-8, "units")
            except Exception:
                pass
            return "break"
        def _pgdn_donate(e=None):
            try:
                canvas.yview_scroll(8, "units")
            except Exception:
                pass
            return "break"
        dlg.bind('<Prior>', _pgup_donate, add='+')
        dlg.bind('<Next>',  _pgdn_donate, add='+')
        canvas.bind('<Prior>', _pgup_donate, add='+')
        canvas.bind('<Next>',  _pgdn_donate, add='+')
        body.bind('<Prior>', _pgup_donate, add='+')
        body.bind('<Next>',  _pgdn_donate, add='+')

    def refresh_drives(self):
        # v3.6.1: pulso neon + orb oscilando
        self._start_global_pulse()
        self.trigger_reactive_pulse(2, 1100, "ATUALIZANDO PENDRIVES...")
        try:
            self.log("Procurando pendrives USB...", is_info=True)
            self.drives = get_usb_drives()
            if not self.drives:
                self.drive_combo["values"] = ["Nenhum pendrive detectado"]
                self.drive_combo.set("")
                self.log("Nenhum pendrive encontrado.", is_warning=True)
                return
            items = []
            for d in self.drives:
                sg = d["Size"] / (1024**3) if d["Size"] > 0 else 0
                items.append("Disco " + str(d["DiskNumber"]) + " - "
                             + str(d["Model"]) + " - "
                             + str(round(sg, 1)) + " GB")
            self.drive_combo["values"] = items
            self.drive_combo.current(0)
            self.selected_drive = self.drives[0] if self.drives else None
            self._current_usb_tier = _detect_usb_tier(self.selected_drive)
            self.log(str(len(self.drives)) + " pendrive(s).", is_success=True)
        except Exception as e:
            self.log("Falha: " + str(e), is_warning=True)
        finally:
            self._stop_global_pulse(delay_ms=1500)


    def _manual_select_drive(self):
        if IS_MOBILE:
            self._mobile_drive_select_dialog()
            return
        try:
            initial = os.path.expanduser("~")
            path = filedialog.askdirectory(parent=self.root,
                                           title="Selecione manualmente uma pasta/unidade do pendrive",
                                           initialdir=initial,
                                           mustexist=True)
        except Exception as e:
            self._popup_error("Seleção manual",
                              f"Não foi possível abrir a janela do sistema.\n\n{e}")
            self._mobile_drive_select_dialog()
            return
        if not path:
            return
        self._resolve_drive_from_path(path)

    def _resolve_drive_from_path(self, path: str):
        drives = get_usb_drives()
        if not drives:
            self._popup_warning("Pendrive não encontrado",
                                "Nenhum dispositivo USB foi identificado.\n"
                                "Use 'Atualizar' para pesquisar novamente.")
            return
        target = None
        if IS_WINDOWS:
            root_path = os.path.splitdrive(os.path.abspath(path))[0].upper()
            for d in drives:
                letters = (d.get('Letters') or '').upper().replace(' ', '')
                if root_path and root_path.rstrip(':') in [x.rstrip(':') for x in letters.split(',') if x]:
                    target = d; break
        else:
            ap = os.path.abspath(path)
            for d in drives:
                dev = d.get('DevicePath', '')
                mounts = d.get('MountPoint', '') or d.get('MountPoints', '') or ''
                if mounts and ap.startswith(str(mounts)):
                    target = d; break
                if dev and ap.startswith('/media/') and os.path.basename(dev) in ap:
                    target = d; break
                if dev and path.startswith(dev):
                    target = d; break
                if path == d.get('MountPoint', '') or path == d.get('DevicePath', ''):
                    target = d; break
        if target is None:
            self._popup_warning("Dispositivo não identificado",
                                "O caminho selecionado não pertence a um pendrive USB identificado.\n\n"
                                "Escolha um caminho dentro da unidade USB correta.")
            return
        self.drives = drives
        self.selected_drive = target
        self._current_usb_tier = _detect_usb_tier(target)
        items = []
        for d in drives:
            sg = d.get('Size', 0) / (1024**3) if d.get('Size', 0) else 0
            letters = d.get('Letters') or ''
            suffix = f" ({letters}:)" if letters else ''
            items.append(f"🔌 Disco {d.get('DiskNumber')}" + suffix +
                         f" - {d.get('Model', '?')} - {sg:.1f} GB")
        self.drive_combo['values'] = items
        try:
            self.drive_combo.current(drives.index(target))
        except Exception:
            pass
        self.log(f"🎯 Seleção manual: {target.get('Model','?')} — "
                 f"{target.get('Letters') or target.get('DevicePath','?')}",
                 is_success=True)
        self._popup_info("Pendrive selecionado",
                         "A unidade foi selecionada manualmente.\n\n"
                         f"Disco: {target.get('DiskNumber')}\n"
                         f"Modelo: {target.get('Model','?')}\n"
                         f"Tamanho: {target.get('Size',0)/(1024**3):.2f} GB")

    def _mobile_path_dialog(self, title="Selecionar arquivo", hint="Caminho completo",
                             prefill="", default_dirs=None) -> str:
        colors = COLORS
        result = {'value': ''}
        dlg = tk.Toplevel(self.root)
        dlg.title(title)
        dlg.configure(bg=colors['bg'])
        dlg.resizable(True, True)
        try:
            sw = dlg.winfo_screenwidth()
            sh = dlg.winfo_screenheight()
            w = min(500, int(sw * 0.95))
            h = min(560, int(sh * 0.85))
            x = (sw - w) // 2
            y = max(10, (sh - h) // 2)
            dlg.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            dlg.geometry("460x520")
        dlg.minsize(300, 360)
        self._make_modal(dlg)
        outer = tk.Frame(dlg, bg=colors['frame_bg'],
                         highlightbackground=colors['frame_border'],
                         highlightcolor=colors['accent'], highlightthickness=2)
        outer.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        tk.Label(outer, text=f"📱 {title}", font=('Segoe UI', 11, 'bold'),
                 fg=colors['accent'], bg=colors['frame_bg']).pack(
                     fill=tk.X, padx=10, pady=(10, 4))
        tk.Label(outer, text=hint, font=('Segoe UI', 9, 'italic'),
                 fg=colors['label_fg'], bg=colors['frame_bg'],
                 wraplength=440, justify=tk.LEFT).pack(
                     fill=tk.X, padx=10, pady=(0, 6))
        entry_var = tk.StringVar(value=prefill or '')
        entry = tk.Entry(outer, textvariable=entry_var,
                         bg=colors['entry_bg'], fg=colors['entry_fg'],
                         insertbackground=colors['fg'],
                         font=('Consolas', 10), relief=tk.FLAT, bd=2,
                         highlightthickness=1,
                         highlightbackground=colors['frame_border'],
                         highlightcolor=colors['accent'])
        entry.pack(fill=tk.X, padx=10, ipady=8, pady=(0, 8))
        canvas_q = None
        if default_dirs:
            has_files = False
            for d in default_dirs:
                if d and os.path.exists(d):
                    try:
                        files = [f for f in os.listdir(d)
                                 if f.lower().endswith(('.iso', '.img'))]
                    except Exception:
                        files = []
                    if files:
                        has_files = True
                        break
            if has_files:
                tk.Label(outer, text="📂 ISOs disponíveis:",
                         font=('Segoe UI', 9, 'bold'),
                         fg=colors['label_fg'], bg=colors['frame_bg']).pack(
                             anchor='w', padx=10, pady=(0, 2))
                canvas_q = tk.Canvas(outer, bg=colors['frame_bg'],
                                     highlightthickness=0, height=180)
                canvas_q.pack(fill=tk.X, padx=8, expand=False)
                sb_q = ttk.Scrollbar(outer, orient=tk.VERTICAL,
                                     command=canvas_q.yview,
                                     style='Vertical.TScrollbar')
                sb_q.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 8))
                canvas_q.configure(yscrollcommand=sb_q.set)
                quick_frame = tk.Frame(canvas_q, bg=colors['frame_bg'])
                quick_frame.bind('<Configure>',
                                 lambda e: canvas_q.configure(scrollregion=canvas_q.bbox('all')))
                qw = canvas_q.create_window((0, 0), window=quick_frame, anchor='nw')
                canvas_q.bind('<Configure>',
                              lambda e: canvas_q.itemconfig(qw, width=e.width))
                for d in default_dirs:
                    if d and os.path.exists(d):
                        try:
                            files = [f for f in os.listdir(d)
                                     if f.lower().endswith(('.iso', '.img'))]
                        except Exception:
                            files = []
                        for fname in files[:8]:
                            full = os.path.join(d, fname)
                            sz = 0
                            try:
                                sz = os.path.getsize(full) / (1024**2)
                            except Exception:
                                pass
                            lbl = f"  📀 {fname}  ({sz:.0f} MB)"
                            def _pick(p=full):
                                entry_var.set(p)
                            btn = tk.Button(quick_frame, text=lbl, anchor='w',
                                            bg=colors['button_bg'], fg=colors['button_fg'],
                                            activebackground=colors['button_hover'],
                                            relief=tk.FLAT, bd=0, cursor='hand2',
                                            font=('Consolas', 9),
                                            command=_pick)
                            btn.pack(fill=tk.X, pady=1, padx=4)

        # ── v3.6.0: PgUp/PgDown no diálogo mobile ──
        if canvas_q is not None:
            def _pgup_mobile(e=None):
                try:
                    canvas_q.yview_scroll(-8, "units")
                except Exception:
                    pass
                return "break"
            def _pgdn_mobile(e=None):
                try:
                    canvas_q.yview_scroll(8, "units")
                except Exception:
                    pass
                return "break"
            dlg.bind('<Prior>', _pgup_mobile, add='+')
            dlg.bind('<Next>',  _pgdn_mobile, add='+')
            canvas_q.bind('<Prior>', _pgup_mobile, add='+')
            canvas_q.bind('<Next>',  _pgdn_mobile, add='+')

        btn_frame = tk.Frame(outer, bg=colors['frame_bg'])
        btn_frame.pack(fill=tk.X, padx=10, pady=(8, 10), side=tk.BOTTOM)
        def _ok():
            v = entry_var.get().strip()
            if v:
                result['value'] = v
            self._close_modal(dlg)
        def _cancel():
            self._close_modal(dlg)
        ok_btn = tk.Button(btn_frame, text="✅ Confirmar", command=_ok,
                           bg=colors['accent'], fg=colors['bg'],
                           font=('Segoe UI', 10, 'bold'),
                           relief=tk.FLAT, bd=0, cursor='hand2',
                           padx=14, pady=7)
        ok_btn.pack(side=tk.RIGHT, padx=(4, 0))
        tk.Button(btn_frame, text="❌ Cancelar", command=_cancel,
                  bg=colors['cancel_bg'], fg='white',
                  font=('Segoe UI', 10, 'bold'),
                  relief=tk.FLAT, bd=0, cursor='hand2',
                  padx=14, pady=7).pack(side=tk.RIGHT)
        entry.bind('<Return>', lambda e: _ok())
        try:
            entry.focus_set()
            entry.icursor(tk.END)
        except Exception:
            pass
        dlg.wait_window()
        return result['value']

    def _mobile_drive_select_dialog(self):
        colors = COLORS
        drives = get_usb_drives()
        if not drives:
            self._popup_warning(
                "Sem pendrive detectado",
                "Nenhum pendrive/OTG detectado.\n\n"
                "📱 Mobile:\n"
                "• Android: conecte via cabo OTG e use 'Atualizar'\n"
                "• iOS: conecte via adaptador Lightning/USB-C\n\n"
                "Você pode digitar o caminho manualmente.")
            manual = self._mobile_path_dialog(
                title="Caminho manual do pendrive",
                hint="Ex: /storage/xxxx-xxxx  ou  /dev/sda1",
                default_dirs=["/storage", "/mnt", "/sdcard",
                              str(Path.home() / "Documents")])
            if manual:
                self._resolve_drive_from_path(manual)
            return
        dlg = tk.Toplevel(self.root)
        dlg.title("🎯 Selecionar pendrive")
        dlg.configure(bg=colors['bg'])
        dlg.resizable(True, True)
        try:
            sw = dlg.winfo_screenwidth()
            sh = dlg.winfo_screenheight()
            w = min(480, int(sw * 0.95))
            h = min(520, int(sh * 0.80))
            dlg.geometry(f"{w}x{h}+{(sw-w)//2}+{max(10,(sh-h)//2)}")
        except Exception:
            dlg.geometry("460x480")
        dlg.minsize(320, 300)
        self._make_modal(dlg)
        outer = tk.Frame(dlg, bg=colors['frame_bg'],
                         highlightbackground=colors['frame_border'],
                         highlightcolor=colors['accent'], highlightthickness=2)
        outer.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)
        tk.Label(outer, text="🎯 Selecionar pendrive / OTG",
                 font=('Segoe UI', 11, 'bold'),
                 fg=colors['accent'], bg=colors['frame_bg']).pack(
                     fill=tk.X, padx=10, pady=(10, 4))
        tk.Label(outer, text="Toque no pendrive para selecionar:",
                 font=('Segoe UI', 9), fg=colors['label_fg'],
                 bg=colors['frame_bg']).pack(anchor='w', padx=10, pady=(0, 6))
        selected = {'drive': None}
        list_frame = tk.Frame(outer, bg=colors['frame_bg'])
        list_frame.pack(fill=tk.BOTH, expand=True, padx=8)
        def _select_drive(d):
            selected['drive'] = d
            self._close_modal(dlg)
        for d in drives:
            sg = d.get('Size', 0) / (1024**3) if d.get('Size', 0) else 0
            letters = d.get('Letters') or ''
            dev = d.get('DevicePath', '')
            model = d.get('Model', '?')
            suffix = f" ({letters}:)" if letters else f"\n    {dev}"
            label = f"🔌 {model}{suffix}\n    💾 {sg:.1f} GB  •  Bus: {d.get('BusType','?')}"
            btn = tk.Button(list_frame, text=label, anchor='w',
                            bg=colors['button_bg'], fg=colors['button_fg'],
                            activebackground=colors['button_hover'],
                            relief=tk.FLAT, bd=0, cursor='hand2',
                            font=('Segoe UI', 9), justify=tk.LEFT,
                            padx=10, pady=10,
                            command=lambda dr=d: _select_drive(dr))
            btn.pack(fill=tk.X, pady=3)
        sep = tk.Frame(outer, bg=colors['frame_border'], height=1)
        sep.pack(fill=tk.X, padx=8, pady=4)
        btn_frame = tk.Frame(outer, bg=colors['frame_bg'])
        btn_frame.pack(fill=tk.X, padx=8, pady=(0, 8))
        def _manual():
            self._close_modal(dlg)
            manual = self._mobile_path_dialog(
                title="Caminho manual do pendrive",
                hint="Ex: /storage/xxxx-xxxx  ou  /dev/sda1",
                default_dirs=["/storage", "/mnt", "/sdcard"])
            if manual:
                self._resolve_drive_from_path(manual)
        tk.Button(btn_frame, text="⌨️ Digitar caminho", command=_manual,
                  bg=colors['button_bg'], fg=colors['button_fg'],
                  font=('Segoe UI', 9), relief=tk.FLAT, bd=0, cursor='hand2',
                  padx=10, pady=7).pack(side=tk.LEFT)
        tk.Button(btn_frame, text="❌ Cancelar",
                  command=lambda: self._close_modal(dlg),
                  bg=colors['cancel_bg'], fg='white',
                  font=('Segoe UI', 9, 'bold'), relief=tk.FLAT, bd=0, cursor='hand2',
                  padx=10, pady=7).pack(side=tk.RIGHT)
        dlg.wait_window()
        if selected['drive']:
            all_drives = get_usb_drives()
            self.drives = all_drives if all_drives else [selected['drive']]
            self.selected_drive = selected['drive']
            self._current_usb_tier = _detect_usb_tier(selected['drive'])
            items = []
            for d in self.drives:
                sg = d.get('Size', 0) / (1024**3) if d.get('Size', 0) else 0
                letters = d.get('Letters') or ''
                suffix = f" ({letters}:)" if letters else ''
                items.append(f"🔌 Disco {d.get('DiskNumber')}" + suffix +
                             f" - {d.get('Model','?')} - {sg:.1f} GB")
            self.drive_combo['values'] = items
            try:
                self.drive_combo.current(self.drives.index(selected['drive']))
            except Exception:
                pass
            t = selected['drive']
            self.log(f"🎯 Pendrive selecionado (mobile): {t.get('Model','?')} — "
                     f"{t.get('Letters') or t.get('DevicePath','?')}", is_success=True)

    def _on_drive_selected(self, event=None):
        idx = self.drive_combo.current()
        if 0 <= idx < len(self.drives):
            self.selected_drive = self.drives[idx]
            serial = self.selected_drive.get('SerialNumber', '') or '—'
            self._current_usb_tier = _detect_usb_tier(self.selected_drive)
            self.log(f"📀 Selecionado: {self.selected_drive['Model']} "
                     f"(Serial: {serial}, Tier: {self._current_usb_tier})",
                     is_info=True)

    def _reverify_selected_drive(self) -> Optional[Dict]:
        if not self.selected_drive:
            return None
        old_serial = (self.selected_drive.get('SerialNumber') or '').strip()
        old_model = self.selected_drive.get('Model', '') or ''
        old_size = self.selected_drive.get('Size', 0) or 0
        current = get_usb_drives()
        if not current:
            return None
        if old_serial:
            for d in current:
                cur_serial = (d.get('SerialNumber') or '').strip()
                if cur_serial and cur_serial == old_serial:
                    return d
            return None
        candidates = []
        for d in current:
            if (d.get('Model', '') or '') == old_model:
                cur_size = d.get('Size', 0) or 0
                if old_size <= 0 or abs(cur_size - old_size) < 1024 * 1024:
                    candidates.append(d)
        if len(candidates) == 1:
            return candidates[0]
        return None

    def _select_iso(self):
        if IS_MOBILE:
            fp = self._mobile_path_dialog(
                title="Selecione a ISO / IMG",
                hint="Caminho completo para a ISO ou IMG",
                default_dirs=[
                    str(DOWNLOAD_DIR),
                    os.path.expanduser("~/Downloads"),
                    "/sdcard/Download",
                    "/storage/emulated/0/Download",
                    str(Path.home() / "Documents"),
                ])
        else:
            try:
                fp = filedialog.askopenfilename(
                    title="Selecione a ISO",
                    filetypes=[("Imagens", "*.iso *.img"), ("Todos", "*.*")])
            except Exception as e:
                self._popup_error("Seleção de ISO",
                                  f"Não foi possível abrir o seletor.\n\n{e}")
                fp = self._mobile_path_dialog(
                    title="Selecione a ISO / IMG (digitar caminho)",
                    hint="Caminho completo para a ISO ou IMG",
                    default_dirs=[str(DOWNLOAD_DIR), os.path.expanduser("~/Downloads")])
        if not fp:
            return
        self._apply_iso_selection(fp)

    def _apply_iso_selection(self, fp: str, switch_tab: bool = True):
        try:
            if not fp or not os.path.isfile(fp):
                return
            ok, err = _validate_iso_pre_flight(fp, self.log)
            if not ok:
                self._popup_error("❌ ISO Inválida", err)
                return
            self.iso_path = fp
            try:
                self.iso_entry.delete(0, tk.END)
                self.iso_entry.insert(0, fp)
            except Exception:
                pass
            size_mb = os.path.getsize(fp) / (1024**2)
            self.log(f"💿 ISO: {os.path.basename(fp)} ({size_mb:.1f} MB)",
                     is_success=True)
            try:
                is_win, label = _detect_windows_iso(fp)
                if is_win:
                    self.log(f"🪟 ISO Windows detectada (label: {label})",
                             is_info=True)
                elif _detect_linux_iso(fp):
                    self.log(f"🐧 ISO Linux detectada — MBR isohybrid será "
                             f"aplicado após cópia.", is_info=True)
            except Exception:
                pass
            try:
                lbl = _derive_volume_label(fp)
                fr = _friendly_distro_name(fp)
                self.log(f"🏷️  Nome do pendrive será: {lbl} ({fr})", is_info=True)
            except Exception:
                pass
            add_recent_iso(fp)
            self.trigger_reactive_pulse(2, 800)
            if switch_tab:
                if self._tab_bar is not None:
                    try:
                        self._tab_bar.select(1)
                    except Exception:
                        pass
        except Exception as e:
            self.log(f"⚠️ Erro ao aplicar ISO: {e}", is_warning=True)

    def _iso_selection_popup(self, iso_file: str, downloaded: bool = False):
        try:
            base = os.path.basename(str(iso_file))
            size_mb = 0
            try:
                size_mb = os.path.getsize(iso_file) / (1024**2)
            except Exception:
                pass
            if downloaded:
                title = "📥 Download concluído — usar esta ISO?"
                intro = "O download foi concluído com sucesso!"
            else:
                title = "📥 ISO existente — usar esta ISO?"
                intro = "A ISO solicitada já existe no seu computador."
            try:
                lbl = _derive_volume_label(iso_file)
                fr = _friendly_distro_name(iso_file)
            except Exception:
                lbl, fr = "DARKPENBOOT", base
            msg = (
                f"{intro}\n\n"
                f"📄 Arquivo: {base}\n"
                f"📏 Tamanho: {size_mb:.1f} MB\n"
                f"📂 Caminho: {iso_file}\n"
                f"🏷️  Rótulo sugerido: {lbl}\n"
                f"📦 Distro: {fr}\n\n"
                f"❓ Deseja USAR ESTA ISO agora?\n"
            )
            resp = UltimatePopup.ask(
                self.root, title, msg, kind="question",
                buttons=("Sim, usar esta ISO", "Não, apenas salvar"))
            if resp:
                self._apply_iso_selection(iso_file, switch_tab=True)
                self._post_iso_ready_dialog(iso_file)
            else:
                self.log("ℹ️ ISO mantida sem alterar a seleção atual.",
                         is_info=True)
        except Exception as e:
            self.log(f"⚠️ Erro no popup de ISO: {e}", is_warning=True)

    def _show_recent_isos(self):
        """ISOs Recentes: modal, centralizada, navegação por teclado + PgUp/PgDown (v3.6.0)."""
        recent = load_recent_isos()
        if not recent:
            self._popup_info("Recentes", "Nenhuma ISO recente encontrada.")
            return
        dlg = tk.Toplevel(self.root)
        dlg.title("📋 ISOs Recentes")
        dlg.configure(bg=COLORS['bg'])
        dlg.resizable(True, True)
        try:
            sw = dlg.winfo_screenwidth()
            sh = dlg.winfo_screenheight()
            w = min(560, int(sw * 0.9))
            h = min(400, int(sh * 0.7))
            x = (sw - w) // 2
            y = max(20, (sh - h) // 2)
            dlg.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            dlg.geometry("560x400")
        dlg.minsize(420, 300)
        self._make_modal(dlg)
        outer = tk.Frame(dlg, bg=COLORS['frame_bg'],
                         highlightbackground=COLORS['frame_border'],
                         highlightcolor=COLORS['accent'], highlightthickness=2)
        outer.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(1, weight=1)
        tk.Label(outer, text="📋 ISOs Recentes",
                 font=('Segoe UI', 13, 'bold'),
                 fg=COLORS['accent'], bg=COLORS['frame_bg']).grid(
                     row=0, column=0, sticky='w', padx=12, pady=(10, 4))
        tk.Label(outer,
                 text="Selecione uma ISO (Tab / ↑ / ↓ / PgUp / PgDown / Enter / Esc)",
                 font=('Segoe UI', 9), fg=COLORS['label_fg'],
                 bg=COLORS['frame_bg']).grid(
                     row=0, column=0, sticky='w', padx=12, pady=(34, 4))
        list_wrap = tk.Frame(outer, bg=COLORS['frame_bg'])
        list_wrap.grid(row=1, column=0, sticky='nsew', padx=12, pady=4)
        list_wrap.columnconfigure(0, weight=1)
        list_wrap.rowconfigure(0, weight=1)
        listbox = tk.Listbox(
            list_wrap, bg=COLORS['entry_bg'], fg=COLORS['entry_fg'],
            font=('Consolas', 9), selectbackground=COLORS['accent'],
            selectforeground='white',
            relief=tk.FLAT, highlightthickness=1, takefocus=True,
            highlightbackground=COLORS['frame_border'],
            highlightcolor=COLORS['accent'])
        listbox.grid(row=0, column=0, sticky='nsew')
        sb = ttk.Scrollbar(list_wrap, orient=tk.VERTICAL,
                            command=listbox.yview, style='Vertical.TScrollbar')
        sb.grid(row=0, column=1, sticky='ns')
        listbox.configure(yscrollcommand=sb.set)
        for p in reversed(recent):
            listbox.insert(tk.END, p)
        if listbox.size() > 0:
            listbox.selection_set(0)
            listbox.activate(0)
            listbox.see(0)
        result = {'path': None}
        def pick(event=None):
            sel = listbox.curselection()
            if not sel:
                return "break"
            path = listbox.get(sel[0])
            result['path'] = path
            self._close_modal(dlg)
            return "break"
        def _on_listbox_return(e):
            return pick()
        def _on_listbox_double(e):
            return pick()
        listbox.bind('<Return>', _on_listbox_return)
        listbox.bind('<KP_Enter>', _on_listbox_return)
        listbox.bind('<Double-Button-1>', _on_listbox_double)

        # ── v3.6.0: PgUp/PgDown saltam 5 itens no listbox ──
        def _pgup_recent(e=None):
            try:
                cur = listbox.curselection()
                idx = (cur[0] if cur else 0) - 5
                if idx < 0: idx = 0
                listbox.selection_clear(0, tk.END)
                listbox.selection_set(idx)
                listbox.activate(idx)
                listbox.see(idx)
            except Exception:
                pass
            return "break"
        def _pgdn_recent(e=None):
            try:
                cur = listbox.curselection()
                idx = (cur[0] if cur else 0) + 5
                if idx >= listbox.size(): idx = listbox.size() - 1
                if idx < 0: idx = 0
                listbox.selection_clear(0, tk.END)
                listbox.selection_set(idx)
                listbox.activate(idx)
                listbox.see(idx)
            except Exception:
                pass
            return "break"
        dlg.bind('<Prior>', _pgup_recent, add='+')
        dlg.bind('<Next>',  _pgdn_recent, add='+')
        listbox.bind('<Prior>', _pgup_recent, add='+')
        listbox.bind('<Next>',  _pgdn_recent, add='+')

        def _listbox_tab(e):
            try:
                nxt = listbox.tk_focusNext()
                if nxt:
                    nxt.focus_set()
            except Exception:
                pass
            return "break"
        def _listbox_shift_tab(e):
            try:
                prv = listbox.tk_focusPrev()
                if prv:
                    prv.focus_set()
            except Exception:
                pass
            return "break"
        listbox.bind('<Tab>', _listbox_tab)
        listbox.bind('<Shift-Tab>', _listbox_shift_tab)
        listbox.bind('<ISO_Left_Tab>', _listbox_shift_tab)
        btn_frame = tk.Frame(outer, bg=COLORS['frame_bg'])
        btn_frame.grid(row=2, column=0, sticky='ew', padx=12, pady=(8, 10))
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        bu = self._make_button(btn_frame, "✔️ Usar ISO selecionada",
                                pick, kind="primary")
        bu.grid(row=0, column=0, padx=4, sticky='ew')
        self._add_tip(bu, "Usa a ISO selecionada (Enter).")
        bc = self._make_button(btn_frame, "❌ Cancelar",
                                lambda: self._close_modal(dlg),
                                kind="danger")
        bc.grid(row=0, column=1, padx=4, sticky='ew')
        self._add_tip(bc, "Fecha a janela sem selecionar (Esc).")
        try:
            listbox.focus_set()
        except Exception:
            pass
        dlg.wait_window()
        if result['path']:
            if os.path.exists(result['path']):
                self._apply_iso_selection(result['path'], switch_tab=True)
            else:
                self.log(f"⚠️ Arquivo não existe: {result['path']}",
                         is_warning=True)

    def _show_checksums(self):
        if not self.iso_path or not os.path.isfile(self.iso_path):
            self._popup_error("Erro", "Selecione uma ISO primeiro.")
            return
        ok, err = _validate_iso_pre_flight(self.iso_path, self.log)
        if not ok:
            self._popup_error("❌ ISO Inválida", err)
            return
        self.log("📊 Calculando checksums (pode demorar)...", is_info=True)
        def worker():
            def progress_cb(algo, hash_val):
                self.root.after(0, lambda a=algo, h=hash_val: self.log(
                    f"   {a.upper()}: {h}", is_info=True))
            hashes = compute_checksums(self.iso_path, progress_cb)
            msg = f"ISO: {os.path.basename(self.iso_path)}\n\n"
            for a, h in hashes.items():
                msg += f"{a.upper()}:\n{h}\n\n"
            self.root.after(0, lambda: self._popup_info("Checksums", msg))
            self.root.after(0, lambda: self.log("✅ Checksums calculados.",
                                                 is_success=True))
        threading.Thread(target=worker, daemon=True).start()

    def _cancel_download(self):
        if not self.download_active:
            return
        confirmed = UltimatePopup.ask(
            self.root, "⏹️ Cancelar Download?",
            "Deseja CANCELAR o download em andamento?\n\n"
            "⚠️ O arquivo parcial será REMOVIDO\n"
            "Deseja mesmo cancelar?",
            kind="question", buttons=("Sim, cancelar download",
                                      "Não, continuar"))
        if not confirmed:
            self.log("ℹ️ Cancelamento de download abortado.", is_info=True)
            return
        self.download_cancel_requested = True
        self.progress['value'] = 0
        self.percent_label.config(text="0%")
        self.status_label.config(text="\u23f9\ufe0f Cancelado", fg=COLORS['warning'])
        self._set_led(COLORS['led_off'])
        self.current_file_label.config(text="")
        self._stop_global_pulse(delay_ms=500)
        self.root.after(1500, lambda: self.status_label.config(text="\u2705 Pronto", fg=COLORS['success']))
        self.trigger_reactive_pulse(3, 800)
        self.log("⏹️ Cancelamento de download solicitado...",
                 is_warning=True)
        try:
            if self._download_cancel_btn is not None:
                self._download_cancel_btn.set_state(state=tk.DISABLED)
        except Exception:
            pass

    def _set_download_ui(self, active: bool):
        self.download_active = active
        if active:
            self.download_cancel_requested = False
        try:
            if self._download_cancel_btn is not None:
                self._download_cancel_btn.set_state(
                    state=tk.NORMAL if active else tk.DISABLED)
        except Exception:
            pass

    def _download_linux_iso(self):
        if self.is_running or self.download_active:
            self.log("⚠️ Aguarde a operação atual.", is_warning=True)
            return
        distro = self.distro_combo.get()
        distro_info = DISTRO_INFO.get(distro, {})
        url = LINUX_DISTROS.get(distro)
        if not url:
            self.log(f"❌ Distro não encontrada: {distro}", is_error=True)
            return
        if not distro_info.get("download_direct", True):
            page_url = distro_info.get("docs") or distro_info.get("homepage")
            self.log(
                f"🌐 {distro} não oferece uma ISO direta nesta versão. "
                "Abrindo a página oficial de download.",
                is_info=True)
            if page_url:
                webbrowser.open(page_url)
            return
        filename = distro.replace(" ", "_").replace("/", "_") + ".iso"
        destino = DOWNLOAD_DIR / filename
        if destino.exists() and os.path.getsize(destino) > MIN_ISO_SIZE:
            self.log(f"ℹ️ ISO já existe localmente: {destino}", is_info=True)
            if distro in DISTRO_INFO:
                self.log("🔐 Verificando SHA256 da ISO existente...",
                         is_info=True)
                ok_hash, hash_msg = verify_download_sha256(
                    str(destino), distro, self.log)
                if not ok_hash:
                    self.log(f"⚠️ Hash divergente: {hash_msg}",
                             is_warning=True)
            self._iso_selection_popup(str(destino), downloaded=False)
            return
        if destino.exists() and os.path.getsize(destino) < MIN_ISO_SIZE:
            try:
                self.log(f"🧹 Removendo parcial inválido "
                         f"({_format_bytes(os.path.getsize(destino))}).",
                         is_warning=True)
                os.remove(destino)
            except Exception:
                pass
        self.log(f"⬇️ Baixando {distro}...", is_info=True)
        self.log(f"📥 URL: {url}", is_info=True)
        self.is_running = True
        self._set_download_ui(True)
        self.start_btn.set_state(state=tk.DISABLED)
        self.cancel_btn.set_state(state=tk.DISABLED)
        self._set_led(COLORS['led_yellow'])
        # v3.6.0: pulso neon só em tarefa real (download)
        self._start_global_pulse()
        self.trigger_reactive_pulse(2, 1400, "⬇️ DOWNLOAD INICIADO")
        try:
            if self.neon_ball is not None:
                self.neon_ball.set_writing_mode(True)
        except Exception:
            pass
        def worker():
            def progress_cb(pct, msg):
                self.root.after(0, lambda p=pct, m=msg:
                                self._update_progress(p, m))
            def cancel_flag():
                return self.download_cancel_requested
            success = download_with_fallback(
                url, str(destino), progress_cb, cancel_flag, self.log)
            def finish():
                self.is_running = False
                self._set_download_ui(False)
                self.start_btn.set_state(state=tk.NORMAL)
                self.cancel_btn.set_state(state=tk.DISABLED)
                try:
                    if self.neon_ball is not None:
                        self.neon_ball.set_writing_mode(False)
                except Exception:
                    pass
                if success:
                    self.log(f"✅ Download: {destino}", is_success=True)
                    self._set_led(COLORS['led_green'])
                    add_recent_iso(str(destino))
                    self._update_progress(100, "Download concluído!")
                    self._iso_selection_popup(str(destino), downloaded=True)
                else:
                    if self.download_cancel_requested:
                        self.log("⏹️ Download cancelado pelo usuário.",
                                 is_warning=True)
                        self._set_led(COLORS['led_yellow'])
                    else:
                        self.log("❌ Download falhou em todos os métodos "
                                 "(curl/wget/urllib).", is_error=True)
                        self._set_led(COLORS['led_red'])
                        self._popup_error(
                            "❌ Download falhou",
                            f"Não foi possível baixar:\n\n{distro}\n\n"
                            f"URL: {url}\n\n"
                            f"• Verifique a conexão com a internet\n"
                            f"• Verifique se o servidor está online\n"
                            f"• Tente novamente mais tarde\n"
                            f"• Métodos testados: curl, wget, urllib")
                self.root.after(3000,
                                lambda: self._set_led(COLORS['led_off']))
                self._stop_global_pulse(delay_ms=3000)
            self.root.after(0, finish)
        threading.Thread(target=worker, daemon=True).start()

    def _post_iso_ready_dialog(self, iso_file):
        try:
            base = os.path.basename(str(iso_file))
            size_mb = 0
            try:
                size_mb = os.path.getsize(iso_file) / (1024**2)
            except Exception:
                pass
            msg = (
                f"✅ ISO pronta para uso!\n\n"
                f"📄 Arquivo: {base}\n"
                f"📏 Tamanho: {size_mb:.1f} MB\n"
                f"📂 Local: {iso_file}\n\n"
                f"Deseja FORMATAR o pendrive e GRAVAR esta\n"
                f"ISO AGORA?\n"
            )
            resp = UltimatePopup.ask(
                self.root, "📥 ISO pronta — gravar agora?",
                msg, kind="question",
                buttons=("Sim, gravar agora", "Não, depois"))
            if resp:
                if not self.selected_drive:
                    self._popup_warning(
                        "Sem pendrive",
                        "Nenhum pendrive foi selecionado!\n\n"
                        "Vá até a aba '🔌 Pendrive', clique em 🔄 para "
                        "atualizar a lista e selecione um dispositivo.")
                    if self._tab_bar is not None:
                        try:
                            self._tab_bar.select(0)
                        except Exception:
                            pass
                    return
                if self._tab_bar is not None:
                    try:
                        self._tab_bar.select(0)
                    except Exception:
                        pass
                try:
                    self.start_btn.focus_set()
                except Exception:
                    pass
                self.log("⚡ Usuário optou por gravar agora.", is_info=True)
                self._popup_info(
                    "Gravação pronta",
                    "Pendrive selecionado! 🎯\n\n"
                    "Clique em 💾 GRAVAR para iniciar.\n"
                    "A ISO já está selecionada.")
            else:
                self.log("ℹ️ Usuário optou por gravar depois.", is_info=True)
        except Exception as e:
            self.log(f"⚠️ Erro ao exibir diálogo pós-ISO: {e}",
                     is_warning=True)

    def _download_windows_iso(self):
        selection = self.windows_combo.get()
        url = WINDOWS_OPTIONS.get(selection)
        if not url:
            return
        self.log(f"🌐 Abrindo site oficial para {selection}...", is_info=True)
        webbrowser.open(url)
        self.log("✅ Site aberto no navegador (canal oficial Microsoft).",
                 is_success=True)

    def _download_macos(self):
        self.log("🍏 Abrindo opções de download do macOS...", is_info=True)
        webbrowser.open(MACOS_DOWNLOAD_URL)
        self.log("✅ Site aberto no navegador.", is_success=True)

    def _cancel_operation(self):
        if not self.is_running:
            return
        confirmed = UltimatePopup.ask(
            self.root, "⚠️ Cancelar operação?",
            "Tem certeza que deseja CANCELAR a operação em andamento?\n\n"
            "⚠️ Se estiver gravando via DD, o pendrive pode\n"
            "ficar em estado INCONSISTENTE.\n"
            "Deseja mesmo cancelar?",
            kind="question", buttons=("Sim, cancelar", "Não, continuar"))
        if not confirmed:
            self.log("ℹ️ Cancelamento abortado.", is_info=True)
            return
        self.cancel_requested = True
        self.progress['value'] = 0
        self.percent_label.config(text="0%")
        self.status_label.config(text="\u23f9\ufe0f Cancelado", fg=COLORS['warning'])
        self._set_led(COLORS['led_off'])
        self.current_file_label.config(text="")
        self._stop_global_pulse(delay_ms=500)
        self.root.after(1500, lambda: self.status_label.config(text="\u2705 Pronto", fg=COLORS['success']))
        self.trigger_reactive_pulse(3, 900, "🛑 CANCELAMENTO ATIVO")
        self.log("⚠️ Cancelamento solicitado — kill em <100ms...",
                 is_warning=True)
        self.cancel_btn.set_state(state=tk.DISABLED)

    def _start_operation(self):
        if self.is_running:
            return
        if not self.selected_drive:
            self._popup_error("Erro", "Selecione um pendrive USB.")
            return
        if not self.iso_path or not os.path.isfile(self.iso_path):
            self._popup_error("Erro", "Selecione uma ISO válida.")
            return
        self.trigger_reactive_pulse(2, 1200, "⚡ GRAVAÇÃO INICIADA")
        self.log("🔍 Validando ISO antes de prosseguir...", is_info=True)
        ok, err = _validate_iso_pre_flight(self.iso_path, self.log)
        if not ok:
            self._popup_error("❌ ISO INVÁLIDA — OPERAÇÃO ABORTADA", err +
                "\n\n💡 Selecione uma ISO válida e tente novamente.\n"
                "🛡️ O PENDRIVE NÃO FOI TOCADO.")
            return
        try:
            self.monetization.trigger_interstitial_ad(self.log)
        except Exception:
            pass
        self.log("🛡️ Verificando pendrive...", is_info=True)
        verified = self._reverify_selected_drive()
        if verified is None:
            self.log("🚨 Dispositivo mudou ou sumiu!", is_error=True)
            self._popup_error(
                "🛡️ Dispositivo não confirmado",
                "O pendrive selecionado não foi encontrado.\n\n"
                "Por SEGURANÇA, a operação foi BLOQUEADA.\n\n"
                "👉 Clique em 🔄 e selecione novamente.")
            self.refresh_drives()
            return
        disk_num = verified.get('DiskNumber', -1)
        if IS_WINDOWS and disk_num == 0:
            self.log("🚨 BLOQUEADO: PhysicalDrive0 é o disco do sistema.",
                     is_error=True)
            self._popup_error("Bloqueado",
                              "O dispositivo selecionado é o disco do sistema.")
            return
        self.selected_drive = verified
        drive = verified
        serial_display = verified.get('SerialNumber', '') or '—'
        self._current_usb_tier = _detect_usb_tier(verified)
        self.log(f"✅ Drive confirmado: Disco {disk_num} "
                 f"(Serial: {serial_display})", is_success=True)
        self.log(f"⚡ Tier USB: {self._current_usb_tier}", is_info=True)
        drive_size_gb = drive['Size'] / (1024**3) if drive['Size'] > 0 else 0
        iso_size_mb = os.path.getsize(self.iso_path) / (1024**2)
        if "DD" not in self.mode_combo.get() and \
                iso_size_mb > (drive['Size'] / (1024**2)):
            self._popup_error("Erro",
                              f"A ISO ({iso_size_mb:.1f} MB) é maior que o "
                              f"pendrive ({drive_size_gb:.1f} GB).")
            return
        is_dd = "DD" in self.mode_combo.get()
        is_win_iso = False
        vol_label = ''
        is_linux_iso = _detect_linux_iso(self.iso_path)
        if is_dd:
            try:
                is_win_iso, vol_label = _detect_windows_iso(self.iso_path)
            except Exception:
                is_win_iso = False
                vol_label = ''
        derived_label = _derive_volume_label(self.iso_path)
        friendly_name = _friendly_distro_name(self.iso_path)
        scheme_sel = self.scheme_combo.get()
        extra_warn = ""
        if scheme_sel == "GPT" and drive_size_gb > 2000:
            extra_warn += (f"\n🗂️  AVISO GPT PARA SERVIDOR\n"
                           f"   Disco > 2 TB — alinhamento 1024 KB.\n")
        if scheme_sel == "MBR" and drive_size_gb > 2.0 * 1024:
            extra_warn += (f"\n⚠️  MBR + disco > 2 TB\n"
                           f"   Mude para GPT.\n")
        if is_linux_iso and not is_dd:
            extra_warn += (f"\n🐧 DISTRO LINUX DETECTADA\n"
                           f"   • Symlinks serão tratados\n"
                           f"   • MBR isohybrid será aplicado\n"
                           f"   • Boot BIOS + UEFI suportados\n")
        if is_dd:
            try:
                leave_raw_now = self.leave_raw_var.get()
            except Exception:
                leave_raw_now = False
            if leave_raw_now:
                extra_warn += ("\n🔒 MODO RAW ATIVADO\n"
                               "   • O disco ficará offline após DD\n"
                               "   • Use diskmgmt.msc para reativar\n")
            else:
                extra_warn += ("\n🔄 REMONTAGEM AUTOMÁTICA ATIVADA\n"
                               "   • O pendrive será trazido online\n"
                               "   • Letra será atribuída automaticamente\n")
        hash_algo_sel = (self.hash_algo_combo.get()
                         if hasattr(self, 'hash_algo_combo') else 'SHA256')
        confirm_msg = (f"TODOS os dados do pendrive serão destruídos!\n\n"
                       f"Disco: {drive.get('DiskNumber')} - {drive['Model']}\n"
                       f"Serial: {serial_display}\n"
                       f"Tamanho: {drive_size_gb:.2f} GB\n"
                       f"Tier USB: {self._current_usb_tier}\n"
                       f"ISO: {os.path.basename(self.iso_path)}\n"
                       f"Modo: {self.mode_combo.get()}\n"
                       f"Esquema: {scheme_sel}\n")
        if "DD" not in self.mode_combo.get():
            confirm_msg += (f"Rótulo: {derived_label}\n"
                            f"  (amigável: {friendly_name})\n")
        if self.verify_var.get():
            confirm_msg += f"Verificação: {hash_algo_sel}\n"
        confirm_msg += extra_warn
        confirm_msg += f"\nDeseja prosseguir?"
        confirm = self._popup_ask("⚠️ CONFIRMAÇÃO", confirm_msg)
        if not confirm:
            return
        self.is_running = True
        self.cancel_requested = False
        self._operation_start_time = time.time()
        self._operation_iso = self.iso_path
        self._operation_mode = self.mode_combo.get()
        self.start_btn.set_state(state=tk.DISABLED)
        self.cancel_btn.set_state(state=tk.NORMAL)
        self._set_led(COLORS['led_yellow'])
        # v3.6.0: pulso neon só em tarefa real (gravação)
        self._start_global_pulse()
        try:
            if self.neon_ball is not None:
                self.neon_ball.set_writing_mode(True)
        except Exception:
            pass
        self._update_progress(0, "Inicializando...")
        threading.Thread(target=self._operation_worker, daemon=True).start()

    def _operation_worker(self):
        success = False
        mounted_iso = None
        iso = self.iso_path
        self._last_was_dd_windows = False
        automount_disabled = False
        try:
            drive = self.selected_drive
            if drive is None:
                raise RuntimeError("Nenhum pendrive selecionado para a operação.")
            mode = self.mode_combo.get()
            filesystem = self.fs_combo.get()
            scheme = self.scheme_combo.get()
            quick = self.quick_var.get()
            verify = self.verify_var.get()
            hash_algo_sel = (self.hash_algo_combo.get()
                             if hasattr(self, 'hash_algo_combo') else 'SHA256')
            hash_algo = HASH_MAP.get(hash_algo_sel, 'sha256')
            tier = _detect_usb_tier(drive)
            try:
                buf_override = (self.buffer_combo.get()
                                if hasattr(self, 'buffer_combo')
                                else 'Auto (por tier USB)')
                chunk_override = (self.chunk_combo.get()
                                  if hasattr(self, 'chunk_combo') else 'Auto')
                reopen_str = (self.reopen_combo.get()
                              if hasattr(self, 'reopen_combo') else '5')
                align_override = (self.align_combo.get()
                                  if hasattr(self, 'align_combo')
                                  else 'Auto (1024 KB)')
                cluster_override = (self.cluster_combo.get()
                                    if hasattr(self, 'cluster_combo')
                                    else 'Auto')
                force_fsync = (self.fsync_var.get()
                               if hasattr(self, 'fsync_var') else True)
                leave_raw = (self.leave_raw_var.get()
                             if hasattr(self, 'leave_raw_var') else False)
            except Exception:
                buf_override = 'Auto (por tier USB)'
                chunk_override = 'Auto'
                reopen_str = '5'
                align_override = 'Auto (1024 KB)'
                cluster_override = 'Auto'
                force_fsync = True
                leave_raw = False
            buf_size = _get_optimal_buffer(tier, buf_override)
            try:
                reopen_attempts_max = int(reopen_str)
            except Exception:
                reopen_attempts_max = 5
            self.log(f"⚡ Buffer ({tier}): {buf_size // (1024**2)} MB",
                     is_info=True)
            self.log(f"🔪 Chunk: {chunk_override} | "
                     f"Reopen: {reopen_attempts_max} | "
                     f"Align: {align_override} | "
                     f"Cluster: {cluster_override} | "
                     f"fsync: {force_fsync} | "
                     f"leave_raw: {leave_raw}", is_info=True)
            if verify:
                self.log(f"🔐 Verificação: {hash_algo_sel}", is_info=True)
            def cancelled():
                return self.cancel_requested
            if IS_WINDOWS:
                automount_disabled = _disable_windows_automount(self.log)
            ok, err = _validate_iso_pre_flight(iso, self.log)
            if not ok:
                raise Exception("ISO inválida detectada no worker:\n" +
                                err[:300])
            if "DD" in mode:
                try:
                    is_win, _ = _detect_windows_iso(iso)
                    self._last_was_dd_windows = is_win
                except Exception:
                    self._last_was_dd_windows = False
                self.log("🔧 Modo DD: clonagem universal.", is_info=True)
                if leave_raw:
                    self.log("🔒 Modo RAW ativado pelo usuário.", is_warning=True)
                else:
                    self.log("🔄 Modo DD com REMONTAGEM AUTOMÁTICA ativado.",
                             is_success=True)
                self._update_progress(5, "Preparando dispositivo...")
                if not write_dd_image(
                    iso, drive['DevicePath'],
                    lambda p: self._update_progress(
                        10 + int(p * 0.85), f"Gravando: {p}%"),
                    lambda n: self.root.after(
                        0, lambda nn=n: self.current_file_label.config(
                            text=f"📄 {nn}")),
                    self.log, cancelled,
                    is_windows_iso=self._last_was_dd_windows,
                    buf_size=buf_size,
                    reopen_attempts_max=reopen_attempts_max,
                    force_fsync=force_fsync,
                    leave_raw=leave_raw):
                    if cancelled():
                        raise InterruptedError()
                    raise Exception("Falha na escrita DD.")
                if verify and not cancelled():
                    self._update_progress(96, f"Verificando {hash_algo_sel}...")
                    if not verify_dd_write(iso, drive['DevicePath'], self.log,
                                             cancelled, algo=hash_algo):
                        if cancelled():
                            raise InterruptedError()
                        raise Exception(
                            f"A verificação {hash_algo_sel} do DD falhou.")
                success = True
            else:
                self.log("📂 Modo Extração.", is_info=True)
                volume_label = _derive_volume_label(iso)
                friendly = _friendly_distro_name(iso)
                is_linux = _detect_linux_iso(iso)
                self.log(f"🏷️  Nome: {volume_label} ({friendly})",
                         is_info=True)
                if is_linux:
                    self.log("🐧 Distro Linux: aplicando tratamento robusto "
                             "de symlinks/dirs/case.", is_info=True)
                self._update_progress(5, "Formatando pendrive...")
                mount_point = format_usb(
                    drive, filesystem, scheme, quick, self.log, cancelled,
                    volume_label=volume_label,
                    align_override=align_override,
                    cluster_override=cluster_override)
                if not mount_point:
                    raise Exception("Falha na formatação.")
                pendrive_letter = (mount_point.rstrip(':') if IS_WINDOWS
                                   else mount_point)
                self.log(f"💾 Formatado: {mount_point} ({friendly})",
                         is_success=True)
                self._update_progress(15, "Montando ISO...")
                mounted_iso = mount_iso(iso, self.log)
                if not mounted_iso:
                    raise Exception("Falha ao montar ISO.")
                self.log(f"📀 ISO montada: {mounted_iso}", is_success=True)
                self._update_progress(20, "Copiando arquivos...")
                def file_prog(cur, total):
                    pct = 20 + int((cur / total) * 70)
                    self._update_progress(pct, f"Copiando {cur}/{total}...")
                dst = f"{mount_point}\\" if IS_WINDOWS else mount_point
                ok = copy_files_with_progress(
                    mounted_iso, dst, file_prog,
                    lambda n: self.root.after(
                        0, lambda nn=n: self.current_file_label.config(
                            text=f"📄 {nn}")),
                    self.log, cancelled, filesystem,
                    buf_size=buf_size)
                if not ok:
                    if cancelled():
                        raise InterruptedError()
                    raise Exception("Falha na cópia.")
                if not cancelled():
                    self._update_progress(90, "Verificando integridade...")
                    if not verify_copy_completeness(mounted_iso, dst, self.log):
                        raise Exception("Verificação detectou divergências.")
                if IS_WINDOWS and not cancelled():
                    self._update_progress(94, "Aplicando boot sector...")
                    if is_linux:
                        self.log("🐧 Aplicando MBR isohybrid do Linux...",
                                 is_info=True)
                    inject_boot_sector(pendrive_letter, mounted_iso, self.log,
                                        iso_path=iso)
                if verify and not cancelled():
                    self._update_progress(96, f"Calculando {hash_algo_sel}...")
                    h = hashlib.new(hash_algo)
                    with open(iso, 'rb') as f:
                        while True:
                            if cancelled():
                                raise InterruptedError()
                            chunk = f.read(4 * 1024 * 1024)
                            if not chunk:
                                break
                            h.update(chunk)
                    self.log(f"✅ {hash_algo_sel}: {h.hexdigest()}",
                             is_success=True)
                success = True
        except InterruptedError:
            self.log("❌ Operação cancelada.", is_error=True)
        except Exception as e:
            self.log(f"❌ ERRO: {e}", is_error=True)
            if self.debug_var.get():
                self.log(traceback.format_exc(), is_error=True)
        finally:
            if mounted_iso:
                dismount_iso(iso, self.log)
            if automount_disabled:
                _enable_windows_automount(self.log)
            try:
                neon_ball = self.neon_ball
                if neon_ball is not None:
                    self.root.after(
                        0, lambda ball=neon_ball: ball.set_writing_mode(False))
            except Exception:
                pass
            self.root.after(0, lambda s=success: self._finish_operation(s))

    def _update_progress(self, percent, msg):
        try:
            self.root.after(0, lambda p=percent, m=msg:
                            self._gui_update_progress(p, m))
        except Exception:
            pass

    def _gui_update_progress(self, percent, msg):
        self.progress['value'] = percent
        self.percent_label.config(text=f"{percent}%")
        self.status_label.config(text=msg, fg=COLORS['warning'])

    def _finish_operation(self, success):
        self.is_running = False
        self.start_btn.set_state(state=tk.NORMAL)
        self.cancel_btn.set_state(state=tk.DISABLED)
        op_time = datetime.now().strftime("%d/%m/%Y %H:%M")
        status = "Sucesso" if success else "Falha"
        self.config['last_operation'] = f"{status} em {op_time}"
        save_config(self.config)
        elapsed = ""
        if self._operation_start_time:
            dur = time.time() - self._operation_start_time
            elapsed = _format_eta(dur)
            self._operation_start_time = None
        self.root.update_idletasks()
        self.root.update()
        if success:
            self.trigger_reactive_pulse(3, 1800, "✅ CONCLUÍDO!")
            self.progress['value'] = 100
            self.percent_label.config(text="100%")
            self.status_label.config(text="✅ Concluído", fg=COLORS['success'])
            self._set_led(COLORS['led_green'])
            self._show_success_summary(elapsed)
        else:
            self.trigger_reactive_pulse(3, 1400)
            self.progress['value'] = 0
            self.percent_label.config(text="0%")
            self.status_label.config(text="❌ Erro - verifique o log",
                                     fg=COLORS['error'])
            self._set_led(COLORS['led_red'])
            self._show_error_summary()
        self.current_file_label.config(text="")
        self.root.after(3000, lambda: self._set_led(COLORS['led_off']))
        self._stop_global_pulse(delay_ms=3000)

    def _show_success_summary(self, elapsed: str = ""):
        log_tail = self._get_log_tail(18)
        iso_name = os.path.basename(self._operation_iso or "—")
        mode = self._operation_mode or "—"
        try:
            leave_raw_used = (self.leave_raw_var.get()
                              if hasattr(self, 'leave_raw_var') else False)
        except Exception:
            leave_raw_used = False
        is_linux = False
        try:
            is_linux = _detect_linux_iso(self._operation_iso)
        except Exception:
            pass
        header_msg = (f"Pendrive criado com sucesso! 🎉\n\n"
                      f"📄 ISO: {iso_name}\n"
                      f"⚙️  Modo: {mode}\n"
                      f"⚡ Tier USB: {self._current_usb_tier}\n")
        if elapsed:
            header_msg += f"⏱️  Duração: {elapsed}\n"
        header_msg += "\n"
        if "DD" in mode:
            if leave_raw_used:
                header_msg += (
                    "═══════════════════════════════════════════════\n"
                    "🔒 MODO RAW ATIVADO\n"
                    "═══════════════════════════════════════════════\n"
                    "O disco está OFFLINE (RAW).\n\n"
                    "🛠️  PARA USAR:\n"
                    "   1. Abra 'diskmgmt.msc'\n"
                    "   2. Selecione o disco\n"
                    "   3. Botão direito → 'Online'\n"
                    "═══════════════════════════════════════════════\n\n")
            else:
                header_msg += (
                    "═══════════════════════════════════════════════\n"
                    "✅ REMONTAGEM AUTOMÁTICA CONCLUÍDA\n"
                    "═══════════════════════════════════════════════\n"
                    "O pendrive foi trazido online e a letra\n"
                    "foi atribuída automaticamente.\n\n"
                    "🧪 TESTAR BOOT: F12/F8/F10/Esc na inicialização\n"
                    "═══════════════════════════════════════════════\n\n")
        elif is_linux:
            try:
                _lbl = _derive_volume_label(self._operation_iso)
                _fr = _friendly_distro_name(self._operation_iso)
                header_msg += (f"🐧 Distro Linux: {_fr}\n"
                               f"🏷️  Rótulo: {_lbl}\n\n"
                               f"✅ MBR isohybrid aplicado.\n"
                               f"✅ Symlinks e diretórios tratados.\n\n"
                               f"🧪 TESTAR BOOT:\n"
                               f"   • BIOS: F12/F8/F10/Esc na inicialização\n"
                               f"   • UEFI: escolha a entrada USB\n\n")
            except Exception:
                pass
        else:
            try:
                _lbl = _derive_volume_label(self._operation_iso)
                _fr = _friendly_distro_name(self._operation_iso)
                header_msg += (f"🏷️  Rótulo: {_lbl}\n"
                               f"📦 Distro: {_fr}\n\n"
                               f"✅ Teste bootando (F12/F8 no boot).\n\n")
            except Exception:
                pass
        header_msg += ("═══════════════════════════════════════════════\n"
                       "📋 RESUMO DAS ÚLTIMAS OPERAÇÕES:\n"
                       "═══════════════════════════════════════════════\n\n"
                       f"{log_tail}")
        self._popup_success("✅ Operação Concluída", header_msg)

    def _show_error_summary(self):
        log_tail = self._get_log_tail(25)
        iso_name = os.path.basename(self._operation_iso or "—")
        mode = self._operation_mode or "—"
        hints = []
        try:
            joined = '\n'.join(self._log_buffer[-40:]).lower()
            if 'muito pequena' in joined or 'placeholder' in joined:
                hints.append("• A ISO é inválida (arquivo pequeno/HTML)")
                hints.append("• Baixe novamente de uma fonte OFICIAL")
            if 'html' in joined:
                hints.append("• O arquivo é uma PÁGINA HTML, não ISO")
            if 'acesso negado' in joined or 'permission' in joined:
                hints.append("• Execute como ADMINISTRADOR/root")
            if 'espaço insuficiente' in joined:
                hints.append("• Pendrive muito pequeno")
            if 'ferramenta' in joined and 'não encontrada' in joined:
                hints.append("• Instale ferramentas mkfs")
            if 'bad file descriptor' in joined or 'handle inválido' in joined:
                hints.append("• Reconecte o pendrive USB")
            if 'fs' in joined and 'não é nativo' in joined:
                hints.append("• Use Recuperação/Reparo (Ctrl+R)")
            if 'sha256' in joined and ('divergente' in joined or 'falhou' in joined):
                hints.append("• SHA256 divergente — rebaixe a ISO")
        except Exception:
            pass
        msg = (f"❌ A operação falhou!\n\n"
               f"📄 ISO: {iso_name}\n"
               f"⚙️  Modo: {mode}\n\n"
               f"💡 POSSÍVEIS SOLUÇÕES:\n")
        if hints:
            msg += '\n'.join(hints) + "\n\n"
        else:
            msg += "• Verifique as mensagens abaixo\n\n"
        msg += (f"📋 DETALHES DO ERRO:\n\n{log_tail}")
        self._popup_error("❌ Erro na Operação", msg)

    def _set_led(self, color):
        self.led_canvas.itemconfig(self.led_id, fill=color)

    def _rebuild_all_widgets(self):
        try:
            current_geom = self.root.geometry()
        except Exception:
            current_geom = None
        log_content = ""
        try:
            if hasattr(self, 'log_text') and self.log_text.winfo_exists():
                log_content = self.log_text.get("1.0", tk.END)
        except Exception:
            log_content = ""
        prog_value = 0
        prog_percent_text = "0%"
        prog_status_text = "✅ Pronto"
        try:
            if hasattr(self, 'progress') and self.progress.winfo_exists():
                prog_value = float(self.progress['value'])
            if hasattr(self, 'percent_label') and self.percent_label.winfo_exists():
                prog_percent_text = self.percent_label.cget('text')
            if hasattr(self, 'status_label') and self.status_label.winfo_exists():
                prog_status_text = self.status_label.cget('text')
        except Exception:
            pass
        vals = {'iso': "", 'fs': 'NTFS', 'scheme': 'MBR', 'mode': 0,
                'quick': True, 'verify': False, 'hash_algo': 'SHA256',
                'debug': False, 'drive_sel': 0, 'distro_sel': 0,
                'windows_sel': 0, 'log_level': 'Detalhado',
                'buffer_override': 'Auto (por tier USB)',
                'chunk_override': 'Auto', 'reopen_attempts': '5',
                'align_override': 'Auto (1024 KB)',
                'cluster_override': 'Auto', 'force_fsync': True,
                'leave_raw': False,
                'current_tab': 0}
        try:
            if hasattr(self, 'iso_entry') and self.iso_entry.winfo_exists():
                vals['iso'] = self.iso_entry.get()
        except Exception:
            vals['iso'] = self.iso_path or ""
        for attr, key in (('fs_combo', 'fs'), ('scheme_combo', 'scheme'),
                          ('hash_algo_combo', 'hash_algo'),
                          ('log_level_combo', 'log_level'),
                          ('buffer_combo', 'buffer_override'),
                          ('chunk_combo', 'chunk_override'),
                          ('reopen_combo', 'reopen_attempts'),
                          ('align_combo', 'align_override'),
                          ('cluster_combo', 'cluster_override')):
            try:
                cb = getattr(self, attr, None)
                if cb is not None and cb.winfo_exists():
                    vals[key] = cb.get()
            except Exception:
                pass
        try:
            if hasattr(self, 'mode_combo') and self.mode_combo.winfo_exists():
                vals['mode'] = self.mode_combo.current()
        except Exception:
            pass
        for attr, key in (('quick_var', 'quick'), ('verify_var', 'verify'),
                          ('debug_var', 'debug'), ('fsync_var', 'force_fsync'),
                          ('leave_raw_var', 'leave_raw')):
            try:
                if hasattr(self, attr):
                    vals[key] = getattr(self, attr).get()
            except Exception:
                pass
        for attr, key in (('drive_combo', 'drive_sel'),
                          ('distro_combo', 'distro_sel'),
                          ('windows_combo', 'windows_sel')):
            try:
                cb = getattr(self, attr, None)
                if cb is not None and cb.winfo_exists():
                    vals[key] = max(0, cb.current())
            except Exception:
                pass
        try:
            if self._tab_bar is not None:
                vals['current_tab'] = self._tab_bar.current()
        except Exception:
            pass
        try:
            self.root.configure(bg=COLORS['bg'])
        except Exception:
            pass
        self._tooltips.clear()
        for w in list(self.root.winfo_children()):
            try:
                w.destroy()
            except Exception:
                pass
        self._build_ui()
        try:
            if current_geom:
                self.root.geometry(current_geom)
        except Exception:
            pass
        try:
            if log_content and hasattr(self, 'log_text'):
                self.log_text.delete("1.0", tk.END)
                self.log_text.insert("1.0", log_content)
                self.log_text.see(tk.END)
        except Exception:
            pass
        try:
            if hasattr(self, 'progress'):
                self.progress['value'] = prog_value
            if hasattr(self, 'percent_label'):
                self.percent_label.config(text=prog_percent_text)
            if hasattr(self, 'status_label'):
                if 'Concluído' in prog_status_text or 'Pronto' in prog_status_text:
                    fg = COLORS['success']
                elif 'Erro' in prog_status_text or 'erro' in prog_status_text:
                    fg = COLORS['error']
                else:
                    fg = COLORS['warning']
                self.status_label.config(text=prog_status_text, fg=fg)
        except Exception:
            pass
        try:
            if vals['iso'] and hasattr(self, 'iso_entry'):
                self.iso_entry.delete(0, tk.END)
                self.iso_entry.insert(0, vals['iso'])
            if hasattr(self, 'fs_combo'):
                self.fs_combo.set(vals['fs'])
            if hasattr(self, 'scheme_combo'):
                self.scheme_combo.set(vals['scheme'])
            if hasattr(self, 'mode_combo'):
                self.mode_combo.current(vals['mode'])
            if hasattr(self, 'quick_var'):
                self.quick_var.set(vals['quick'])
            if hasattr(self, 'verify_var'):
                self.verify_var.set(vals['verify'])
            if hasattr(self, 'hash_algo_combo'):
                self.hash_algo_combo.set(vals['hash_algo'])
            if hasattr(self, 'debug_var'):
                self.debug_var.set(vals['debug'])
            if hasattr(self, 'log_level_combo'):
                self.log_level_combo.set(vals['log_level'])
            if hasattr(self, 'buffer_combo'):
                self.buffer_combo.set(vals['buffer_override'])
            if hasattr(self, 'chunk_combo'):
                self.chunk_combo.set(vals['chunk_override'])
            if hasattr(self, 'reopen_combo'):
                self.reopen_combo.set(vals['reopen_attempts'])
            if hasattr(self, 'align_combo'):
                self.align_combo.set(vals['align_override'])
            if hasattr(self, 'cluster_combo'):
                self.cluster_combo.set(vals['cluster_override'])
            if hasattr(self, 'fsync_var'):
                self.fsync_var.set(vals['force_fsync'])
            if hasattr(self, 'leave_raw_var'):
                self.leave_raw_var.set(vals['leave_raw'])
            if hasattr(self, 'distro_combo'):
                self.distro_combo.current(vals['distro_sel'])
            if hasattr(self, 'windows_combo'):
                self.windows_combo.current(vals['windows_sel'])
        except Exception:
            pass
        try:
            if hasattr(self, 'drive_combo') and hasattr(self, 'drives') and self.drives:
                if vals['drive_sel'] < len(self.drives):
                    self.drive_combo.current(vals['drive_sel'])
                    self.selected_drive = self.drives[vals['drive_sel']]
        except Exception:
            pass
        try:
            if self._tab_bar is not None:
                self._tab_bar.select(vals['current_tab'], silent=True)
                self._on_tab_clicked(vals['current_tab'])
        except Exception:
            pass
        try:
            self.root.update_idletasks()
        except Exception:
            pass

    # ==================================================================
    # PAINEL DE RECUPERAÇÃO — modal (v3.6.0 com PgUp/PgDown)
    # ==================================================================
    def _open_usb_recovery(self):
        drive = self.selected_drive
        if not drive:
            self._popup_warning(
                "Sem pendrive selecionado",
                "Selecione um pendrive antes de abrir\n"
                "o painel de Recuperação/Reparo.")
            return
        disk_num = drive.get('DiskNumber', -1)
        if IS_WINDOWS and disk_num == 0:
            self._popup_error(
                "Bloqueado",
                "🚨 O disco 0 é o disco do sistema!\n"
                "Operações de reparo não são permitidas nele.")
            return

        colors = COLORS
        dlg = tk.Toplevel(self.root)
        dlg.title("🛠️  Recuperação e Reparo USB")
        dlg.configure(bg=colors['bg'])
        # v3.6.0: sem pulso global ao abrir painel
        def _on_recovery_close():
            self._close_modal(dlg)
        try:
            dlg.transient(self.root)
        except Exception:
            pass
        dlg.resizable(True, True)
        w, h = 720, 720
        try:
            sw = dlg.winfo_screenwidth()
            sh = dlg.winfo_screenheight()
            x = (sw - w) // 2
            y = max(20, (sh - h) // 2)
            dlg.geometry(f"{w}x{h}+{x}+{y}")
        except Exception:
            dlg.geometry("720x720")
        dlg.minsize(600, 480)
        self._make_modal(dlg)
        dlg.protocol("WM_DELETE_WINDOW", _on_recovery_close)
        dlg.bind('<Escape>', lambda e: _on_recovery_close())

        outer = tk.Frame(dlg, bg=colors['frame_bg'],
                         highlightbackground=colors['frame_border'],
                         highlightcolor=colors['accent'], highlightthickness=2)
        outer.pack(fill=tk.BOTH, expand=True, padx=8, pady=8)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(1, weight=1)

        header = tk.Frame(outer, bg=colors['frame_bg'])
        header.grid(row=0, column=0, sticky='ew', padx=14, pady=(12, 6))
        header.columnconfigure(1, weight=1)
        tk.Label(header, text="🛠️", font=('Segoe UI Emoji', 22, 'bold'),
                 fg=colors['error'], bg=colors['frame_bg']).grid(
                     row=0, column=0, padx=(0, 10))
        tk.Label(header, text="Recuperação e Reparo USB",
                 font=('Segoe UI', 13, 'bold'), fg=colors['fg'],
                 bg=colors['frame_bg'], anchor='w').grid(
                     row=0, column=1, sticky='ew')

        body_wrap = tk.Frame(outer, bg=colors['frame_bg'])
        body_wrap.grid(row=1, column=0, sticky='nsew', padx=14, pady=4)
        body_wrap.columnconfigure(0, weight=1)
        body_wrap.rowconfigure(0, weight=1)
        body_canvas = tk.Canvas(body_wrap, bg=colors['frame_bg'],
                                 highlightthickness=0)
        body_canvas.grid(row=0, column=0, sticky='nsew')
        body_sb = ttk.Scrollbar(body_wrap, orient=tk.VERTICAL,
                                 command=body_canvas.yview,
                                 style='Vertical.TScrollbar')
        body_sb.grid(row=0, column=1, sticky='ns')
        body_canvas.configure(yscrollcommand=body_sb.set)
        body = tk.Frame(body_canvas, bg=colors['frame_bg'])
        body.columnconfigure(0, weight=1)
        body.bind('<Configure>',
                  lambda e: body_canvas.configure(
                      scrollregion=body_canvas.bbox('all')))
        bw = body_canvas.create_window((0, 0), window=body, anchor='nw')
        body_canvas.bind('<Configure>',
                         lambda e: body_canvas.itemconfig(bw, width=e.width))

        def _wheel_evt(event):
            try:
                delta = int(-1 * (event.delta / 120)) if event.delta else 0
                if delta: body_canvas.yview_scroll(delta, "units")
            except Exception: pass
            return "break"
        for w_ in (body_canvas, body, outer, dlg):
            w_.bind('<MouseWheel>', _wheel_evt, add='+')
            w_.bind('<Button-4>', lambda e: body_canvas.yview_scroll(-3, 'units'), add='+')
            w_.bind('<Button-5>', lambda e: body_canvas.yview_scroll(3, 'units'), add='+')

        # ── v3.6.0: PgUp/PgDown no painel de Recuperação ──
        def _pgup_rec(e=None):
            try:
                body_canvas.yview_scroll(-8, "units")
            except Exception:
                pass
            return "break"
        def _pgdn_rec(e=None):
            try:
                body_canvas.yview_scroll(8, "units")
            except Exception:
                pass
            return "break"
        dlg.bind('<Prior>', _pgup_rec, add='+')
        dlg.bind('<Next>',  _pgdn_rec, add='+')
        body_canvas.bind('<Prior>', _pgup_rec, add='+')
        body_canvas.bind('<Next>',  _pgdn_rec, add='+')
        body.bind('<Prior>', _pgup_rec, add='+')
        body.bind('<Next>',  _pgdn_rec, add='+')

        target_card = tk.LabelFrame(
            body, text=" 🎯 Dispositivo Alvo ",
            font=('Segoe UI', 10, 'bold'), fg=colors['accent'],
            bg=colors['frame_bg'], relief=tk.FLAT, bd=0,
            highlightbackground=colors['frame_border'],
            highlightcolor=colors['accent'], highlightthickness=2,
            labelanchor='nw', padx=10, pady=8)
        target_card.grid(row=0, column=0, sticky='ew', pady=(0, 8))
        target_card.columnconfigure(0, weight=1)

        ident_row = tk.Frame(target_card, bg=colors['frame_bg'])
        ident_row.pack(fill=tk.X, pady=(0, 6))
        ident_btn = self._make_button(
            ident_row,
            "🔍 Identificar e Listar Pendrives",
            None,
            kind="primary",
            font=('Segoe UI', 10, 'bold'))
        ident_btn.pack(fill=tk.X, padx=2)

        combo_row = tk.Frame(target_card, bg=colors['frame_bg'])
        combo_row.pack(fill=tk.X, pady=(0, 6))
        tk.Label(combo_row, text="📀 Pendrive:",
                 font=('Segoe UI', 9, 'bold'),
                 fg=colors['label_fg'], bg=colors['frame_bg']).pack(side=tk.LEFT)
        rec_combo = ttk.Combobox(combo_row, state='readonly')
        rec_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(6, 0))

        rec_state = {'drive': drive, 'disk_num': disk_num}
        info_labels = {}
        for key, label, color in (
            ('disco', '💾 Disco:', None),
            ('tamanho', '📏 Tamanho:', None),
            ('letras', '🔌 Letras:', None),
            ('serial', '🔑 Serial:', colors['info']),
            ('tier', '⚡ Tier:', colors['accent']),
            ('device', '📂 Device:', None),
        ):
            r = tk.Frame(target_card, bg=colors['frame_bg'])
            r.pack(fill=tk.X, pady=1)
            tk.Label(r, text=label, font=('Segoe UI', 10, 'bold'),
                     fg=colors['label_fg'], bg=colors['frame_bg'],
                     width=12, anchor='w').pack(side=tk.LEFT)
            val_lbl = tk.Label(r, text="—", font=('Consolas', 10),
                               fg=color or colors['fg'],
                               bg=colors['frame_bg'],
                               anchor='w', justify=tk.LEFT,
                               wraplength=520)
            val_lbl.pack(side=tk.LEFT, fill=tk.X, expand=True)
            info_labels[key] = val_lbl

        def _refresh_info_from_state():
            d = rec_state['drive']
            try:
                size_gb = d.get('Size', 0) / (1024**3) if d.get('Size', 0) else 0
                info_labels['disco'].config(
                    text=f"{d.get('DiskNumber')} - {d.get('Model', '?')}")
                info_labels['tamanho'].config(text=f"{size_gb:.2f} GB")
                info_labels['letras'].config(
                    text=d.get('Letters', '—') or '—')
                info_labels['serial'].config(
                    text=d.get('SerialNumber', '—') or '—')
                tier_now = _detect_usb_tier(d)
                info_labels['tier'].config(text=tier_now)
                info_labels['device'].config(
                    text=d.get('DevicePath', '—'))
            except Exception:
                pass

        def _do_identify():
            self.log("[1/2] Identificando via API...", is_info=True)
            try:
                new_drives = get_usb_drives()
            except Exception as e:
                self.log("Erro API: " + str(e), is_error=True)
                new_drives = []
            if not new_drives:
                self.log("[2/2] Varredura shell universal...", is_info=True)
                try:
                    new_drives = _scan_shell_all_platforms(self.log)
                except Exception as e:
                    self.log("Falha shell scan: " + str(e), is_warning=True)
                    new_drives = []
            if not new_drives:
                rec_combo["values"] = ["Nenhum pendrive detectado"]
                rec_combo.set("")
                self.log("Nenhum pendrive encontrado.", is_warning=True)
                return
            self.drives = new_drives
            items = []
            for d in new_drives:
                sg = d.get("Size", 0) / (1024**3) if d.get("Size", 0) else 0
                items.append("Disco " + str(d.get("DiskNumber")) + " - "
                             + str(d.get("Model", "?")) + " - "
                             + str(round(sg, 1)) + " GB")
            rec_combo["values"] = items
            rec_combo.current(0)
            rec_state["drive"] = new_drives[0]
            rec_state["disk_num"] = new_drives[0].get("DiskNumber", -1)
            self.selected_drive = new_drives[0]
            self._current_usb_tier = _detect_usb_tier(new_drives[0])
            _refresh_info_from_state()
            self.log(str(len(new_drives)) + " dispositivo(s).", is_success=True)
            try:
                self.drive_combo["values"] = items
                self.drive_combo.current(0)
            except Exception:
                pass


        def _on_local_combo_change(event=None):
            idx = rec_combo.current()
            if 0 <= idx < len(self.drives):
                rec_state['drive'] = self.drives[idx]
                rec_state['disk_num'] = self.drives[idx].get('DiskNumber', -1)
                self.selected_drive = self.drives[idx]
                self._current_usb_tier = _detect_usb_tier(self.drives[idx])
                _refresh_info_from_state()
                self.log(f"🎯 Dispositivo alvo alterado: "
                         f"{self.drives[idx].get('Model','?')}", is_info=True)

        ident_btn.set_state(command=_do_identify)
        self._add_tip(ident_btn,
                      "🔍 Reexecuta a busca por pendrives USB\n"
                      "conectados neste momento.")
        rec_combo.bind('<<ComboboxSelected>>', _on_local_combo_change)
        self._add_tip(rec_combo,
                      "🎯 Selecione o pendrive que deseja reparar.")

        try:
            init_items = []
            for d in (self.drives or [drive]):
                sg = d.get('Size', 0) / (1024**3) if d.get('Size', 0) else 0
                letters = d.get('Letters') or ''
                suffix = f" ({letters}:)" if letters else ''
                init_items.append(f"🔌 Disco {d.get('DiskNumber')}{suffix} - "
                                  f"{d.get('Model', '?')} - {sg:.1f} GB")
            rec_combo['values'] = init_items
            if init_items:
                try:
                    idx_now = self.drives.index(drive) if self.drives else 0
                except Exception:
                    idx_now = 0
                rec_combo.current(idx_now)
        except Exception:
            pass
        _refresh_info_from_state()

        selection_card = tk.LabelFrame(
            body, text=" ⚡ Seleção Rápida ",
            font=('Segoe UI', 10, 'bold'),
            fg=colors['accent'], bg=colors['frame_bg'], relief=tk.FLAT, bd=0,
            highlightbackground=colors['frame_border'],
            highlightcolor=colors['accent'],
            highlightthickness=2, labelanchor='nw', padx=10, pady=8)
        selection_card.grid(row=1, column=0, sticky='ew', pady=(0, 8))
        selection_card.columnconfigure(0, weight=1)
        selection_card.columnconfigure(1, weight=1)
        selection_card.columnconfigure(2, weight=1)
        sel_iso = self._make_button(selection_card, "📂 Selecionar ISO",
                                     self._select_iso, kind='primary')
        sel_iso.grid(row=0, column=0, padx=3, sticky='ew')
        self._add_tip(sel_iso, "📂 Abre a janela do sistema para selecionar uma ISO/IMG.")
        sel_recent = self._make_button(selection_card, "📋 ISOs recentes",
                                        self._show_recent_isos)
        sel_recent.grid(row=0, column=1, padx=3, sticky='ew')
        self._add_tip(sel_recent, "📋 Mostra as últimas ISOs utilizadas.")
        sel_drive = self._make_button(selection_card, "🎯 Selecionar pendrive",
                                       self._manual_select_drive, kind='primary')
        sel_drive.grid(row=0, column=2, padx=3, sticky='ew')
        self._add_tip(sel_drive, "🎯 Abre a janela do sistema para seleção manual.")

        def _recovery_op_wrap(op_name, fn):
            def _wrapped():
                if self._recovery_active:
                    return
                self._recovery_active = True
                self._set_led(colors['led_yellow'])
                # v3.6.0: pulso só em operação real (Limpar/Formatar/Reparar)
                self._start_global_pulse()
                try:
                    if self.neon_ball is not None:
                        self.neon_ball.set_writing_mode(True)
                except Exception:
                    pass
                self.log(f"🛠️ Iniciando: {op_name}", is_info=True)
                try:
                    fn()
                except Exception as e:
                    self.log(f"❌ Falha em '{op_name}': {e}", is_error=True)
                finally:
                    try:
                        if self.neon_ball is not None:
                            self.neon_ball.set_writing_mode(False)
                    except Exception:
                        pass
                    self._set_led(colors['led_off'])
                    self._recovery_active = False
                    self._stop_global_pulse(delay_ms=1500)
                    self.log(f"🛠️ '{op_name}' finalizado.", is_info=True)
            return _wrapped

        quick_card = tk.LabelFrame(
            body, text=" ⚡ Ações Rápidas ",
            font=('Segoe UI', 10, 'bold'), fg=colors['accent'],
            bg=colors['frame_bg'], relief=tk.FLAT, bd=0,
            highlightbackground=colors['frame_border'],
            highlightcolor=colors['accent'], highlightthickness=2,
            labelanchor='nw', padx=10, pady=8)
        quick_card.grid(row=2, column=0, sticky='ew', pady=(0, 8))
        qr_grid = tk.Frame(quick_card, bg=colors['frame_bg'])
        qr_grid.pack(fill=tk.X)
        for i in range(2):
            qr_grid.columnconfigure(i, weight=1)

        def _do_chkdsk():
            d = rec_state['drive']
            letters = d.get('Letters', '') or ''
            if not letters:
                self._popup_warning("Sem letra",
                                    "Disco não tem letra de unidade.\n"
                                    "Chkdsk precisa de uma letra para operar.")
                return
            letter = letters.split(',')[0].strip().rstrip(':')
            cmd = f'chkdsk {letter}: /F /R /X'
            self.log(f"🛠️ chkdsk {letter}:", is_info=True)
            _launch_terminal(cmd, shell='cmd')
        b1 = self._make_button(qr_grid, "🔧 Chkdsk /F /R",
                                _recovery_op_wrap("Chkdsk", _do_chkdsk),
                                kind="primary")
        b1.grid(row=0, column=0, padx=3, pady=3, sticky='ew')
        self._add_tip(b1, "🔧 Executa chkdsk /F /R /X na unidade selecionada (Windows).")

        def _do_clear_readonly():
            if not IS_WINDOWS:
                self._popup_info("Não suportado",
                                  "Remover readonly só no Windows.")
                return
            dn = rec_state['disk_num']
            if dn is None or dn < 0:
                return
            script = (f"select disk {dn}\n"
                      "attributes disk clear readonly\n"
                      "exit\n")
            sp = CONFIG_DIR / f"_clr_ro_{os.getpid()}.txt"
            try:
                with open(sp, "w", encoding="ascii", newline="\r\n") as f:
                    f.write(script)
                r = run_hidden(["diskpart", "/s", str(sp)], timeout=60)
                try:
                    sp.unlink(missing_ok=True)
                except Exception:
                    pass
                if r.returncode == 0:
                    self.log("✅ Readonly removido.", is_success=True)
                    self._popup_success("OK", "Readonly removido!")
                else:
                    self.log("⚠️ Falha ao remover readonly.", is_warning=True)
            except Exception as e:
                self.log(f"❌ Erro: {e}", is_error=True)
        b2 = self._make_button(qr_grid, "🔓 Remover readonly",
                                _recovery_op_wrap("Remover readonly",
                                                   _do_clear_readonly),
                                kind="normal")
        b2.grid(row=0, column=1, padx=3, pady=3, sticky='ew')
        self._add_tip(b2, "🔓 Limpa o atributo read-only do disco (Windows).")

        def _do_clean_disk():
            dn = rec_state['disk_num']
            d = rec_state['drive']
            ok = UltimatePopup.ask(
                dlg, "⚠️ Limpar Disco",
                f"⚠️  ATENÇÃO!\n\n"
                f"Isto vai APAGAR TODAS as partições do:\n\n"
                f"   Disco {dn} — {d.get('Model', '?')}\n\n"
                f"Tem certeza?",
                kind="warning",
                buttons=("Sim, limpar", "Cancelar"))
            if not ok:
                return
            if IS_WINDOWS:
                script = (f"select disk {dn}\n"
                          "attributes disk clear readonly\n"
                          "clean\n"
                          "create partition primary\n"
                          "select partition 1\n"
                          "format fs=ntfs quick label=PENBOOT\n"
                          "assign\n"
                          "exit\n")
                sp = CONFIG_DIR / f"_clean_{os.getpid()}.txt"
                try:
                    with open(sp, "w", encoding="ascii", newline="\r\n") as f:
                        f.write(script)
                    r = run_hidden(["diskpart", "/s", str(sp)], timeout=120)
                    try:
                        sp.unlink(missing_ok=True)
                    except Exception:
                        pass
                    if r.returncode == 0:
                        self.log(f"✅ Disco {dn} limpo (RAW).",
                                 is_success=True)
                        self._popup_success("Disco recuperado",
                                             "RAW removido. Partição NTFS PENBOOT criada.")
                except Exception as e:
                    self.log(f"❌ Erro: {e}", is_error=True)
            else:
                dev = d.get('DevicePath', '')
                if dev:
                    _launch_terminal(f"sudo wipefs -a {dev}; sudo sync",
                                      shell='bash')
        b3 = self._make_button(qr_grid, "🧹 Limpar Disco (RAW)",
                                _recovery_op_wrap("Limpar disco",
                                                   _do_clean_disk),
                                kind="danger")
        b3.grid(row=1, column=0, padx=3, pady=3, sticky='ew')
        self._add_tip(b3, "🧹 Apaga tudo e cria partição NTFS limpa (Windows) ou wipefs (Linux).")

        def _do_rebuild_mbr():
            dn = rec_state['disk_num']
            ok = UltimatePopup.ask(
                dlg, "Reconstruir MBR",
                f"Reconstruir o MBR do disco {dn}?\n\n"
                f"Útil para pendrives que não bootam.",
                kind="question",
                buttons=("Sim, reconstruir", "Cancelar"))
            if not ok:
                return
            if IS_WINDOWS:
                script = (f"select disk {dn}\n"
                          "clean\n"
                          "convert mbr\n"
                          "create partition primary align=1024\n"
                          "select partition 1\n"
                          "active\n"
                          "assign\n"
                          "exit\n")
                sp = CONFIG_DIR / f"_mbr_{os.getpid()}.txt"
                try:
                    with open(sp, "w", encoding="ascii", newline="\r\n") as f:
                        f.write(script)
                    r = run_hidden(["diskpart", "/s", str(sp)], timeout=90)
                    try:
                        sp.unlink(missing_ok=True)
                    except Exception:
                        pass
                    if r.returncode == 0:
                        self.log("✅ MBR reconstruído.", is_success=True)
                        self._popup_success("MBR OK", "Reconstruído!")
                except Exception as e:
                    self.log(f"❌ Erro: {e}", is_error=True)
        b4 = self._make_button(qr_grid, "🔄 Reconstruir MBR",
                                _recovery_op_wrap("Reconstruir MBR",
                                                   _do_rebuild_mbr),
                                kind="normal")
        b4.grid(row=1, column=1, padx=3, pady=3, sticky='ew')
        self._add_tip(b4, "🔄 Recria o MBR, partição ativa e alinhamento (Windows).")

        fs_card = tk.LabelFrame(
            body, text=" 📁 Formatar com FS Específico ",
            font=('Segoe UI', 10, 'bold'), fg=colors['accent'],
            bg=colors['frame_bg'], relief=tk.FLAT, bd=0,
            highlightbackground=colors['frame_border'],
            highlightcolor=colors['accent'], highlightthickness=2,
            labelanchor='nw', padx=10, pady=8)
        fs_card.grid(row=3, column=0, sticky='ew', pady=(0, 8))
        fs_row = tk.Frame(fs_card, bg=colors['frame_bg'])
        fs_row.pack(fill=tk.X, pady=(0, 6))
        tk.Label(fs_row, text="Sistema de Arquivos:",
                 font=('Segoe UI', 10, 'bold'), fg=colors['label_fg'],
                 bg=colors['frame_bg']).pack(side=tk.LEFT)
        recov_fs_combo = ttk.Combobox(
            fs_row, values=FS_LIST, state='readonly', width=14)
        recov_fs_combo.set(self.fs_combo.get() if hasattr(self, 'fs_combo')
                            else 'NTFS')
        recov_fs_combo.pack(side=tk.LEFT, padx=8)
        self._add_tip(recov_fs_combo, "Sistema de arquivos alvo")

        btn_row = tk.Frame(fs_card, bg=colors['frame_bg'])
        btn_row.pack(fill=tk.X)
        for i in range(2):
            btn_row.columnconfigure(i, weight=1)

        def _do_format_via_terminal():
            """v3.6.1 - Formata o pendrive ALVO no FS do seletor."""
            d = rec_state["drive"]
            dn = rec_state["disk_num"]
            fs = recov_fs_combo.get().upper()
            if not d:
                self._popup_warning("Sem alvo", "Clique em Identificar.")
                return
            if dn is None or dn == -1:
                hits = _scan_shell_all_platforms(self.log)
                if hits:
                    rec_state["drive"] = hits[0]
                    rec_state["disk_num"] = hits[0].get("DiskNumber", -1)
                    dn = rec_state["disk_num"]
                    d = rec_state["drive"]
            model = str(d.get("Model", "?"))
            msg = ("Formatar Disco " + str(dn) + " (" + model + ")"
                   + " como " + fs + "? Dados serao APAGADOS.")
            ok = UltimatePopup.ask(dlg, "Formatar como " + fs, msg,
                                    kind="warning",
                                    buttons=("Sim, formatar", "Cancelar"))
            if not ok:
                return
            if IS_WINDOWS:
                if dn is None or dn == -1 or dn == 0:
                    self._popup_error("Bloqueado", "Disco invalido.")
                    return
                if fs not in ("NTFS", "FAT32", "EXFAT"):
                    self._popup_info("FS nao nativo",
                        fs + " nao e nativo do Windows.")
                    return
                lines = ["select disk " + str(dn),
                         "attributes disk clear readonly",
                         "clean",
                         "create partition primary",
                         "select partition 1",
                         "format fs=" + fs + " quick label=PENBOOT",
                         "assign",
                         "exit"]
                sp = CONFIG_DIR / ("_fmt_" + str(os.getpid()) + ".txt")
                try:
                    with open(sp, "w", encoding="ascii",
                              newline="\r\n") as f:
                        f.write("\n".join(lines))
                    self.log("Formatando Disco " + str(dn) + " como "
                             + fs + "...", is_info=True)
                    rr = run_hidden(["diskpart", "/s", str(sp)], timeout=600)
                    if rr.returncode == 0:
                        self.log("Formatado como " + fs + ".", is_success=True)
                        self._popup_success("OK",
                            "Disco " + str(dn) + " formatado como " + fs)
                        try:
                            self.refresh_drives()
                        except Exception:
                            pass
                    else:
                        self.log("DiskPart erro.", is_error=True)
                finally:
                    try:
                        sp.unlink(missing_ok=True)
                    except Exception:
                        pass
            else:
                dev = d.get("DevicePath", "")
                if not dev or not os.path.exists(dev):
                    self._popup_warning("Invalido", "Caminho: " + dev)
                    return
                fs_map = {"NTFS": "ntfs", "FAT32": "vfat", "EXFAT": "exfat",
                          "EXT4": "ext4", "EXT3": "ext3", "EXT2": "ext2"}
                mkfs_fs = fs_map.get(fs, fs.lower())
                part = dev + "1" if not dev[-1:].isdigit() else dev
                cmd = ("sudo umount " + dev + "* 2>/dev/null; "
                       "sudo mkfs." + mkfs_fs + " -F -L PENBOOT " + part
                       + "; sudo sync")
                _launch_terminal(cmd, shell="bash")


        b_fmt = self._make_button(btn_row, "📁 Formatar com FS",
                                   _recovery_op_wrap("Formatar FS",
                                                      _do_format_via_terminal),
                                   kind="primary")
        b_fmt.grid(row=0, column=0, padx=3, pady=2, sticky='ew')
        self._add_tip(b_fmt, "📁 Formata o pendrive com o FS escolhido.")

        def _do_diskpart():
            d = rec_state["drive"]
            dn = rec_state["disk_num"]
            if not d:
                self._popup_warning("Sem alvo",
                    "Clique em Identificar primeiro.")
                return
            if dn is None or dn == -1:
                hits = _scan_shell_all_platforms(self.log)
                if hits:
                    self.drives = hits
                    rec_state["drive"] = hits[0]
                    rec_state["disk_num"] = hits[0].get("DiskNumber", -1)
                    self.selected_drive = hits[0]
                    _refresh_info_from_state()
                    dn = rec_state["disk_num"]
                    d = rec_state["drive"]
            if IS_WINDOWS:
                _launch_terminal("diskpart", shell="cmd")
            else:
                dev = d.get("DevicePath", "")
                if dev:
                    _launch_terminal("sudo parted " + dev, shell="bash")


        term_card = tk.LabelFrame(
            body, text=" 🖥️ Terminal Personalizado ",
            font=('Segoe UI', 10, 'bold'), fg=colors['accent'],
            bg=colors['frame_bg'], relief=tk.FLAT, bd=0,
            highlightbackground=colors['frame_border'],
            highlightcolor=colors['accent'], highlightthickness=2,
            labelanchor='nw', padx=10, pady=8)
        term_card.grid(row=4, column=0, sticky='ew', pady=(0, 8))
        tk.Label(term_card, text="Comando (opcional):",
                 font=('Segoe UI', 9), fg=colors['label_fg'],
                 bg=colors['frame_bg']).pack(anchor='w')
        term_entry = tk.Entry(
            term_card, bg=colors['entry_bg'], fg=colors['entry_fg'],
            insertbackground=colors['fg'], relief=tk.FLAT, bd=2,
            highlightthickness=1,
            highlightbackground=colors['frame_border'],
            highlightcolor=colors['accent'], font=('Consolas', 10))
        term_entry.pack(fill=tk.X, ipady=5, pady=(2, 6))
        if IS_WINDOWS:
            term_entry.insert(0,
                              f"Get-CimInstance Win32_DiskDrive -Filter 'Index={disk_num}' "
                              f"| Select-Object Model,SerialNumber,Size")
        else:
            dev = drive.get('DevicePath', '/dev/sdX')
            term_entry.insert(0, f"sudo smartctl -a {dev} | less")
        term_btns = tk.Frame(term_card, bg=colors['frame_bg'])
        term_btns.pack(fill=tk.X)
        for i in range(3):
            term_btns.columnconfigure(i, weight=1)

        def _open_cmd_terminal():
            cmd_text = term_entry.get().strip() or None
            if IS_WINDOWS and cmd_text and (
                    cmd_text.startswith('Get-CimInstance') or
                    cmd_text.startswith('Get-WmiObject') or
                    '| Select-Object' in cmd_text):
                escaped = cmd_text.replace('"', '\\"')
                cmd_text = f'powershell.exe -NoProfile -Command "{escaped}"'
            _launch_terminal(cmd_text, shell='cmd')
        bc = self._make_button(term_btns, "🖥️ cmd",
                                _recovery_op_wrap("cmd", _open_cmd_terminal),
                                kind="normal")
        bc.grid(row=0, column=0, padx=3, pady=2, sticky='ew')
        self._add_tip(bc, "🖥️ Abre cmd (Windows) executando o comando acima.")

        def _open_ps_terminal():
            cmd_text = term_entry.get().strip() or None
            _launch_terminal(cmd_text, shell='powershell')
        bp = self._make_button(term_btns, "🖥️ PowerShell",
                                _recovery_op_wrap("PowerShell",
                                                   _open_ps_terminal),
                                kind="normal")
        bp.grid(row=0, column=1, padx=3, pady=2, sticky='ew')
        self._add_tip(bp, "🖥️ Abre PowerShell executando o comando acima.")

        def _open_default_terminal():
            _launch_terminal(None, shell='default')
        bd_ = self._make_button(term_btns, "🖥️ Terminal SO",
                                 _recovery_op_wrap("Terminal",
                                                    _open_default_terminal),
                                 kind="primary")
        bd_.grid(row=0, column=2, padx=3, pady=2, sticky='ew')
        self._add_tip(bd_, "🖥️ Abre APENAS o terminal do SO.")

        tips = tk.LabelFrame(
            body, text=" 💡 Dicas ",
            font=('Segoe UI', 10, 'bold'), fg=colors['info'],
            bg=colors['frame_bg'], relief=tk.FLAT, bd=0,
            highlightbackground=colors['frame_border'],
            highlightcolor=colors['info'], highlightthickness=1,
            labelanchor='nw', padx=10, pady=8)
        tips.grid(row=5, column=0, sticky='ew', pady=(0, 8))
        tips_txt = (
            "• 🔍 Identificar: reescaneia USB e atualiza o seletor\n"
            "• 🎯 Pendrive: alterne o dispositivo alvo pelo combo\n"
            "• 🔧 Chkdsk: repara sistema de arquivos (Windows)\n"
            "• 🧹 Limpar Disco: deixa em RAW para reformatação\n"
            "• 🔄 Reconstruir MBR: pendrive que não boota\n"
            "• 📁 Formatar FS: NTFS/FAT32/exFAT | ext4/3/2\n"
            "• 🔓 Remover readonly: discos write-protected\n"
            "• 🖥️ Terminal SO: abre o terminal SEM executar comando\n"
            "• ⌨️ PgUp/PgDown: rola o painel (v3.6.0)"
        )
        tk.Label(tips, text=tips_txt, justify=tk.LEFT, anchor='w',
                 fg=colors['label_fg'], bg=colors['frame_bg'],
                 font=('Consolas', 9)).pack(fill=tk.X)

        footer = tk.Frame(outer, bg=colors['frame_bg'])
        footer.grid(row=2, column=0, sticky='ew', padx=14, pady=(6, 12))
        close_btn = self._make_button(footer, "❌ Fechar",
                                       _on_recovery_close,
                                       kind="danger", width=160)
        close_btn.pack(side=tk.RIGHT)
        self._add_tip(close_btn, "❌ Fecha o painel de Recuperação/Reparo.")

        try:
            ident_btn.focus_set()
        except Exception:
            pass
        self.log("🛠️ Painel de Recuperação/Reparo aberto.", is_info=True)

    def _on_closing(self):
        if self.is_running:
            msg = ("Operação em andamento. Cancelar e sair?")
            if self.download_active:
                msg = ("Download em andamento. Cancelar e sair?")
            if self._popup_ask("Sair", msg):
                self.cancel_requested = True
                self.download_cancel_requested = True
                self.root.after(500, self.root.destroy)
        else:
            try:
                geom = self.root.geometry()
                self.config['window_geometry'] = geom
            except Exception:
                pass
            try:
                self.config['log_level'] = (self.log_level_combo.get()
                                            if hasattr(self, 'log_level_combo')
                                            else 'Detalhado')
                self.config['buffer_override'] = (
                    self.buffer_combo.get() if hasattr(self, 'buffer_combo')
                    else 'Auto (por tier USB)')
                self.config['chunk_override'] = (
                    self.chunk_combo.get() if hasattr(self, 'chunk_combo')
                    else 'Auto')
                self.config['reopen_attempts'] = (
                    self.reopen_combo.get() if hasattr(self, 'reopen_combo')
                    else '5')
                self.config['align_override'] = (
                    self.align_combo.get() if hasattr(self, 'align_combo')
                    else 'Auto (1024 KB)')
                self.config['cluster_override'] = (
                    self.cluster_combo.get() if hasattr(self, 'cluster_combo')
                    else 'Auto')
                self.config['force_fsync'] = (
                    self.fsync_var.get() if hasattr(self, 'fsync_var') else True)
                self.config['leave_raw_dd'] = (
                    self.leave_raw_var.get()
                    if hasattr(self, 'leave_raw_var') else False)
            except Exception:
                pass
            save_config({
                **self.config,
                'last_iso': self.iso_path,
                'filesystem': self.fs_combo.get(),
                'scheme': self.scheme_combo.get(),
                'mode': 'extract' if self.mode_combo.current() == 0 else 'dd',
                'quick_format': self.quick_var.get(),
                'verify': self.verify_var.get(),
                'hash_algo': (self.hash_algo_combo.get()
                              if hasattr(self, 'hash_algo_combo') else 'SHA256'),
                'debug': self.debug_var.get(),
                'theme': self.config.get('theme', 'matrix'),
                'leave_raw_dd': (self.leave_raw_var.get()
                                  if hasattr(self, 'leave_raw_var') else False),
                'ad_mode': self.ad_mode,
                'premium_unlocked': self.premium_unlocked,
            })
            self.root.destroy()

# ==================================================================
# 22. MAIN
# ==================================================================
def main():
    if not is_admin():
        response = messagebox.askyesno(
            "Privilégios necessários",
            f"{APP_NAME} precisa de privilégios de administrador.\n\n"
            "Reiniciar como administrador?")
        if response:
            run_as_admin()
        else:
            messagebox.showwarning(
                "Aviso",
                "O programa pode não funcionar corretamente sem privilégios "
                "elevados.")
    try:
        root = tk.Tk()
        DarkPenBoot(root)
        root.mainloop()
    except Exception as e:
        try:
            messagebox.showerror("Erro Fatal",
                                f"{e}\n\n{traceback.format_exc()}")
        except Exception:
            print(f"Erro fatal: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
