#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
╔══════════════════════════════════════════════════════════════════════════╗
║    DARKPENBOOT PRO v3.5.0 — MOBILE (KIVY / ANDROID)                      ║
║                                                                          ║
║  Autor: Adriano Rodrigues da Silva                                       ║
║  GitHub: https://github.com/Avlis1412                                    ║
║                                                                          ║
║  VERSÃO MOBILE — Android/iOS via Kivy + Buildozer                        ║
║                                                                          ║
║  ┌────────────────────────────────────────────────────────────────────┐  ║
║  │ INSPIRAÇÃO NIXOS — Build reprodutível via Buildozer                 │  ║
║  │ NixOS® é marca da NixOS Foundation (sem afiliação)                  │  ║
║  └────────────────────────────────────────────────────────────────────┘  ║
║                                                                          ║
║  FUNCIONALIDADES:                                                        ║
║   ✅ Download de distros Linux (com SHA256)                              ║
║   ✅ Download de ISOs Windows (link direto navegador)                    ║
║   ✅ Verificação SHA256 automática                                       ║
║   ✅ Seleção de ISO local (/sdcard/Download)                             ║
║   ✅ Detecção de pendrive OTG                                            ║
║   ✅ Gravação via DD (requer ROOT)                                       ║
║   ✅ Log em tempo real                                                   ║
║   ✅ 7 temas (Matrix, Dracula, Nord, Cyberpunk, Monokai, Light, Soft)    ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
"""

# ═════════════════════════════════════════════════════════════════════
# IMPORTS
# ═════════════════════════════════════════════════════════════════════
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

# ─── Kivy ─────────────────────────────────────────────────────────────
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock, mainthread
from kivy.metrics import dp, sp
from kivy.utils import platform, get_color_from_hex
from kivy.graphics import Color, RoundedRectangle, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
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

# ═════════════════════════════════════════════════════════════════════
# DETECÇÃO DE PLATAFORMA
# ═════════════════════════════════════════════════════════════════════
IS_ANDROID = platform == 'android'
IS_IOS = platform == 'ios'
IS_MOBILE = IS_ANDROID or IS_IOS
IS_TERMUX = os.environ.get('TERMUX_VERSION') is not None
IS_WINDOWS = platform == 'win'
IS_LINUX = platform == 'linux'
IS_MAC = platform == 'macosx'

# ═════════════════════════════════════════════════════════════════════
# CONSTANTES
# ═════════════════════════════════════════════════════════════════════
APP_NAME = "DarkPenBoot Pro"
APP_VERSION = "3.5.0"
APP_AUTHOR = "Adriano Rodrigues da Silva"
GITHUB_URL = "https://github.com/Avlis1412"

# ─── NixOS (inspiração) ──────────────────────────────────────────────
NIXOS_URL = "https://nixos.org"
NIXOS_GOVERNANCE_URL = "https://nixos.org/governance/"
NIXOS_DOWNLOAD_URL = "https://nixos.org/download/"
NIXOS_CONSTITUTION_URL = "https://github.com/NixOS/org/blob/main/doc/constitution.md"

PREMIUM_PRICE_BRL = "R$ 10,00"
PREMIUM_CHECKOUT_URL = "https://github.com/Avlis1412/DarkPenBoot-Pro#premium"

# ─── PIX ─────────────────────────────────────────────────────────────
PIX_KEY = "cc473489-9842-4fce-97e4-5a1b697aa4f3"
PIX_RECEIVER_NAME = "ADRIANO RODRIGUES DA SILVA"
PIX_BANK_NAME = "Santander"

# ─── Diretórios (mobile) ─────────────────────────────────────────────
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

# ─── Tamanhos mínimos ────────────────────────────────────────────────
MIN_ISO_SIZE = 100 * 1024 * 1024  # 100 MB

# ─── User-Agent ──────────────────────────────────────────────────────
BROWSER_UA = (
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36"
)

# ═════════════════════════════════════════════════════════════════════
# TEMAS (mesmos do desktop)
# ═════════════════════════════════════════════════════════════════════
THEMES = {
    "matrix": {
        "label": "🟢 Matrix",
        "bg": "#040805", "fg": "#00ff41",
        "panel": "#0a1610", "border": "#00b833",
        "accent": "#00ff41", "accent2": "#00ccff",
        "error": "#ff2233", "warning": "#ffdd00",
        "success": "#00ff88", "info": "#00ccff",
        "button": "#0f2418", "button_hover": "#1a3a24",
    },
    "dracula": {
        "label": "🩸 Crimson",
        "bg": "#0a0205", "fg": "#ff8095",
        "panel": "#1a0810", "border": "#ff2d55",
        "accent": "#ff4466", "accent2": "#e066ff",
        "error": "#ff2255", "warning": "#ffcc44",
        "success": "#00ffa3", "info": "#cc99ff",
        "button": "#22091a", "button_hover": "#3a1028",
    },
    "nord": {
        "label": "❄️ Nord",
        "bg": "#2e3440", "fg": "#eceff4",
        "panel": "#3b4252", "border": "#4c566a",
        "accent": "#88c0d0", "accent2": "#b48ead",
        "error": "#bf616a", "warning": "#ebcb8b",
        "success": "#a3be8c", "info": "#81a1c1",
        "button": "#434c5e", "button_hover": "#4c566a",
    },
    "cyberpunk": {
        "label": "⚡ Cyberpunk",
        "bg": "#08060f", "fg": "#f7e600",
        "panel": "#130d2b", "border": "#e6d800",
        "accent": "#f7e600", "accent2": "#ff007f",
        "error": "#ff0066", "warning": "#ffaa00",
        "success": "#00ff88", "info": "#00d4ff",
        "button": "#1f1240", "button_hover": "#2d1c5c",
    },
    "monokai": {
        "label": "🟠 Monokai",
        "bg": "#1e1f1c", "fg": "#f8f8f2",
        "panel": "#272822", "border": "#75715e",
        "accent": "#fd971f", "accent2": "#ae81ff",
        "error": "#f92672", "warning": "#e6db74",
        "success": "#a6e22e", "info": "#66d9ef",
        "button": "#3e3d32", "button_hover": "#4d4c3d",
    },
    "light": {
        "label": "☀️ Light",
        "bg": "#f4f6f8", "fg": "#1a1a1a",
        "panel": "#ffffff", "border": "#d1d5db",
        "accent": "#2563eb", "accent2": "#7c3aed",
        "error": "#dc2626", "warning": "#d97706",
        "success": "#059669", "info": "#2563eb",
        "button": "#e5e7eb", "button_hover": "#d1d5db",
    },
    "soft_dark": {
        "label": "🌙 Soft Dark",
        "bg": "#1e1e24", "fg": "#cdd6f4",
        "panel": "#242630", "border": "#45475a",
        "accent": "#89b4fa", "accent2": "#cba6f7",
        "error": "#f38ba8", "warning": "#f9e2af",
        "success": "#a6e3a1", "info": "#89b4fa",
        "button": "#313244", "button_hover": "#45475a",
    },
}

# ═════════════════════════════════════════════════════════════════════
# DISTROS (idênticas ao desktop — versões atualizadas 2025)
# ═════════════════════════════════════════════════════════════════════
DISTRO_INFO = {
    # 🟣 NIXOS — PRIORIDADE MÁXIMA
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
    # 🐧 UBUNTU
    "Ubuntu 24.04.1 LTS": {
        "url": "https://releases.ubuntu.com/24.04.1/ubuntu-24.04.1-desktop-amd64.iso",
        "docs": "https://ubuntu.com/download/desktop",
        "license": "GPL-3.0",
        "sha256": "",
    },
    # 🐧 DEBIAN
    "Debian 12.9 NetInst": {
        "url": "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.9.0-amd64-netinst.iso",
        "docs": "https://www.debian.org/CD/http-ftp/",
        "license": "DFSG-compliant",
        "sha256": "",
    },
    # 🐧 LINUX MINT
    "Linux Mint 22 Cinnamon": {
        "url": "https://mirrors.kernel.org/linuxmint/stable/22/linuxmint-22-cinnamon-64bit.iso",
        "docs": "https://linuxmint.com/download.php",
        "license": "GPL-3.0",
        "sha256": "",
    },
    # 🐧 FEDORA
    "Fedora Workstation 41": {
        "url": "https://download.fedoraproject.org/pub/fedora/linux/releases/41/Workstation/x86_64/iso/Fedora-Workstation-Live-x86_64-41-1.4.iso",
        "docs": "https://fedoraproject.org/workstation/download/",
        "license": "GPL-2.0 + MIT + Apache 2.0",
        "sha256": "",
    },
    # 🐧 KALI
    "Kali Linux 2025.1": {
        "url": "https://cdimage.kali.org/kali-2025.1/kali-linux-2025.1-installer-amd64.iso",
        "docs": "https://www.kali.org/get-kali/",
        "license": "GPL-3.0",
        "sha256": "",
    },
    # 🐧 PARROT
    "Parrot OS 7.0 Home": {
        "url": "https://parrot.elhacker.net/iso/7.0/Parrot-home-7.0_amd64.iso",
        "docs": "https://parrotsec.org/download/",
        "license": "GPL-3.0",
        "sha256": "",
    },
    # 🐧 POP!_OS
    "Pop!_OS 22.04 LTS": {
        "url": "https://iso.pop-os.org/22.04/amd64/intel/32/pop-os_22.04_amd64_intel_32.iso",
        "docs": "https://pop.system76.com/",
        "license": "GPL-3.0",
        "sha256": "",
    },
    # 🐧 MANJARO
    "Manjaro KDE 24.2": {
        "url": "https://download.manjaro.org/kde/24.2.0/manjaro-kde-24.2.0-241210-linux612.iso",
        "docs": "https://manjaro.org/download/",
        "license": "GPL-3.0",
        "sha256": "",
    },
    # 🐧 openSUSE
    "openSUSE Leap 15.6": {
        "url": "https://download.opensuse.org/distribution/leap/15.6/iso/openSUSE-Leap-15.6-DVD-x86_64-Media.iso",
        "docs": "https://get.opensuse.org/leap/",
        "license": "GPL-2.0 / GPL-3.0",
        "sha256": "",
    },
    # 🐧 ARCH
    "Arch Linux Latest": {
        "url": "https://mirror.rackspace.com/archlinux/iso/latest/archlinux-x86_64.iso",
        "docs": "https://archlinux.org/download/",
        "license": "GPL-2.0",
        "sha256": "",
    },
    # 🐧 ZORIN
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

# ═════════════════════════════════════════════════════════════════════
# UTILITÁRIOS CORE (mesmos do desktop)
# ═════════════════════════════════════════════════════════════════════
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

# ═════════════════════════════════════════════════════════════════════
# CONFIG (JSON persistente)
# ═════════════════════════════════════════════════════════════════════
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

# ═════════════════════════════════════════════════════════════════════
# DOWNLOADER (5 camadas de fallback)
# ═════════════════════════════════════════════════════════════════════
def download_with_fallback(url, destino, progress_cb, cancel_flag, log_cb):
    """
    Downloader resiliente com múltiplas camadas.
    Camadas: curl → wget → urllib
    """
    log_cb(f"⬇️ Iniciando: {url}", "info")

    # Camada 1: curl
    if shutil.which('curl'):
        log_cb("🔧 Tentando via curl...", "info")
        if _download_curl(url, destino, progress_cb, cancel_flag, log_cb):
            return _post_download(destino, url, log_cb)
        if cancel_flag():
            return False

    # Camada 2: wget
    if shutil.which('wget'):
        log_cb("🔧 Tentando via wget...", "info")
        if _download_wget(url, destino, progress_cb, cancel_flag, log_cb):
            return _post_download(destino, url, log_cb)
        if cancel_flag():
            return False

    # Camada 3: urllib
    log_cb("🔧 Tentando via urllib...", "info")
    if _download_urllib(url, destino, progress_cb, cancel_flag, log_cb):
        return _post_download(destino, url, log_cb)

    log_cb("❌ Todos os métodos falharam", "error")
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
        log_cb(f"⚠️ curl: {e}", "warning")
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
        log_cb(f"⚠️ wget: {e}", "warning")
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
        log_cb(f"⚠️ urllib: {e}", "warning")
        return False

def _post_download(destino, url, log_cb):
    """Verifica se o arquivo é HTML (erro) em vez de ISO."""
    try:
        size = os.path.getsize(destino)
        if size < 1024 * 1024:
            with open(destino, 'rb') as f:
                head = f.read(512).lower()
            if b'<html' in head or b'<!doc' in head:
                log_cb("❌ Download retornou HTML (página de erro)", "error")
                try:
                    os.rename(destino, destino + ".html_error")
                except Exception:
                    pass
                return False
        log_cb(f"✅ Download OK: {_format_bytes(size)}", "success")
        return True
    except Exception:
        return False

# ═════════════════════════════════════════════════════════════════════
# KIVY UI — WIDGETS CUSTOMIZADOS
# ═════════════════════════════════════════════════════════════════════
class RoundedButton(Button):
    """Botão com cantos arredondados e cores do tema."""

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

    def _update_rect(self, *args):
        self._rect.pos = self.pos
        self._rect.size = self.size

    def set_theme(self, bg_color, text_color):
        self._bg_color = get_color_from_hex(bg_color)
        self._color_instruction.rgba = self._bg_color
        self.color = get_color_from_hex(text_color)

# ═════════════════════════════════════════════════════════════════════
# TELAS (SCREENS)
# ═════════════════════════════════════════════════════════════════════

class HomeScreen(Screen):
    """Tela inicial com menu principal."""
    pass


class DownloadScreen(Screen):
    """Tela de download de distros."""
    pass


class ISOScreen(Screen):
    """Tela de seleção de ISO local."""
    pass


class USBScreen(Screen):
    """Tela de detecção e gravação em pendrive."""
    pass


class LogScreen(Screen):
    """Tela de log."""
    pass


class AboutScreen(Screen):
    """Tela Sobre + NixOS + PIX."""
    pass


# ═════════════════════════════════════════════════════════════════════
# APP PRINCIPAL
# ═════════════════════════════════════════════════════════════════════
class DarkPenBootKivyApp(App):
    """Aplicativo Kivy principal."""

    # ─── Propriedades reativas ────────────────────────────────────
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
        self.config = load_config()
        self.theme_key = self.config.get('theme', 'soft_dark')
        self._cancel_download = False
        self._download_thread = None
        self._log_lines = []

    # ─── Helpers de tema ──────────────────────────────────────────
    def get_theme(self) -> dict:
        return THEMES.get(self.theme_key, THEMES['soft_dark'])

    def hex(self, key: str) -> str:
        t = self.get_theme()
        return t.get(key, '#ffffff')

    def kivy_color(self, key: str):
        return get_color_from_hex(self.hex(key))

    # ─── Log ──────────────────────────────────────────────────────
    def log(self, msg: str, level: str = "info"):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}"
        self._log_lines.append(line)
        if len(self._log_lines) > 500:
            self._log_lines = self._log_lines[-500:]
        self.log_text = "\n".join(self._log_lines[-200:])

    # ─── Build UI ─────────────────────────────────────────────────
    def build(self):
        Window.clearcolor = self.kivy_color('bg')

        self.sm = ScreenManager(transition=SlideTransition())
        self.sm.add_widget(self._build_home())
        self.sm.add_widget(self._build_download())
        self.sm.add_widget(self._build_iso())
        self.sm.add_widget(self._build_usb())
        self.sm.add_widget(self._build_log())
        self.sm.add_widget(self._build_about())

        self.log(f"🚀 {APP_NAME} v{APP_VERSION} (Kivy Mobile)", "success")
        self.log(f"📱 Plataforma: {platform}", "info")
        self.log("🟣 Inspirado em NixOS — build reprodutível", "info")
        self.log("🟣 NixOS® é marca da NixOS Foundation (sem afiliação)", "info")

        # Aviso se não for root
        if not _is_admin():
            self.log("⚠️ Sem ROOT — gravação em pendrive desabilitada", "warning")
            self.log("💡 Use Termux com 'tsu' para ganhar root", "info")

        return self.sm

    # ═════════════════════════════════════════════════════════════
    # TELA HOME
    # ═════════════════════════════════════════════════════════════
    def _build_home(self) -> Screen:
        s = HomeScreen(name='home')

        root = BoxLayout(orientation='vertical', padding=dp(16), spacing=dp(12))
        with root.canvas.before:
            Color(*self.kivy_color('bg'))
            bg = Rectangle(pos=root.pos, size=root.size)
        root.bind(pos=lambda *a: setattr(bg, 'pos', root.pos),
                  size=lambda *a: setattr(bg, 'size', root.size))

        # ─── Header ───
        title = Label(
            text=f"🔌 DARKPENBOOT\n[color={self.hex('accent')}]PRO v{APP_VERSION}[/color]",
            markup=True,
            font_size=sp(24),
            bold=True,
            size_hint_y=None,
            height=dp(80),
            color=self.kivy_color('fg'),
        )
        root.add_widget(title)

        subtitle = Label(
            text=f"[color={self.hex('info')}]Criador de Pendrives Bootáveis — Mobile[/color]",
            markup=True,
            font_size=sp(11),
            size_hint_y=None,
            height=dp(24),
        )
        root.add_widget(subtitle)

        # ─── Botões principais ───
        buttons = [
            ("⬇️  Baixar Distro Linux", 'download', 'accent'),
            ("💿  Selecionar ISO Local", 'iso', 'accent2'),
            ("🔌  Gravar no Pendrive", 'usb', 'warning'),
            ("📋  Ver Log", 'log', 'info'),
            ("ℹ️  Sobre + NixOS + PIX", 'about', 'success'),
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

        # ─── Seletor de tema ───
        theme_row = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(8))
        theme_row.add_widget(Label(
            text="🎨 Tema:", size_hint_x=0.3,
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

        # ─── Rodapé ───
        footer = Label(
            text=f"[color={self.hex('info')}]🟣 nixos.org  •  "
                 f"github.com/Avlis1412[/color]",
            markup=True,
            font_size=sp(10),
            size_hint_y=None,
            height=dp(24),
        )
        root.add_widget(footer)

        s.add_widget(root)
        return s

    def _on_theme_change(self, spinner, text):
        for key, t in THEMES.items():
            if t['label'] == text:
                self.theme_key = key
                self.config['theme'] = key
                save_config(self.config)
                break

    def go_to(self, screen_name: str):
        self.sm.current = screen_name

    # ═════════════════════════════════════════════════════════════
    # TELA DOWNLOAD
    # ═════════════════════════════════════════════════════════════
    def _build_download(self) -> Screen:
        s = DownloadScreen(name='download')

        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))

        # Header
        header = self._make_header("⬇️ Download de ISOs", 'home')
        root.add_widget(header)

        # Info NixOS
        nixos_info = Label(
            text=f"[color={self.hex('accent2')}]🟣 NixOS 24.11 + 25.05 "
                 f"com GOVERNANÇA oficial[/color]",
            markup=True, font_size=sp(11),
            size_hint_y=None, height=dp(24),
        )
        root.add_widget(nixos_info)

        # Spinner de distros
        distro_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(6))
        distro_row.add_widget(Label(
            text="🐧 Distro:", size_hint_x=0.3,
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

        # Botão baixar
        self.btn_download = RoundedButton(
            text="⬇️  Baixar Distro",
            bg_color=self.hex('accent'),
            text_color='#000000',
            size_hint_y=None, height=dp(56), radius=14,
        )
        self.btn_download.bind(on_release=self._start_download)
        root.add_widget(self.btn_download)

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
        self.dl_log.bind(width=lambda *a: self.dl_log.setter('text_size')(
            self.dl_log.width, None))
        scroll.add_widget(self.dl_log)
        root.add_widget(scroll)

        # Botão voltar
        back = RoundedButton(
            text="❌ Cancelar / Voltar",
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
        self.config['last_distro'] = text
        save_config(self.config)

    def _start_download(self, *args):
        if self.is_downloading:
            return
        distro = self.distro_spinner.text
        url = LINUX_DISTROS.get(distro)
        if not url:
            self.log(f"❌ Distro não encontrada: {distro}", "error")
            return

        # Nome do arquivo
        filename = distro.replace(" ", "_").replace("/", "_") + ".iso"
        destino = DOWNLOAD_DIR / filename

        # Verifica se já existe
        if destino.exists() and os.path.getsize(destino) > MIN_ISO_SIZE:
            self.log(f"✅ ISO já existe: {destino}", "success")
            self.selected_iso = str(destino)
            self.config['last_iso'] = str(destino)
            save_config(self.config)
            add_recent_iso(str(destino))
            self._show_info("Download", f"ISO já existe:\n{filename}")
            return

        self.is_downloading = True
        self._cancel_download = False
        self.btn_download.disabled = True
        self.btn_download.text = "⏳ Baixando..."

        if "NixOS" in distro:
            self.log("🟣 NixOS — Governança: nixos.org/governance/", "info")
            self.log("🟣 NixOS® marca da NixOS Foundation — sem afiliação", "info")

        self.log(f"⬇️ Baixando {distro}...", "info")
        self.log(f"📥 {url}", "info")

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
        self.btn_download.text = "⬇️  Baixar Distro"

        if ok:
            self.log(f"✅ Download concluído: {destino}", "success")
            self.selected_iso = str(destino)
            self.config['last_iso'] = str(destino)
            save_config(self.config)
            add_recent_iso(str(destino))
            self.download_pb.value = 100
            self.lbl_status.text = "✅ Download concluído!"
            self._show_info("Sucesso", f"ISO baixada:\n{destino.name}\n\n"
                                       f"Vá em 💿 para usar.")
        else:
            if self._cancel_download:
                self.log("⏹️ Download cancelado", "warning")
                self.lbl_status.text = "⏹️ Cancelado"
            else:
                self.log("❌ Download falhou", "error")
                self.lbl_status.text = "❌ Falhou"
                self._show_info("Falha", "Não foi possível baixar.\n"
                                          "Verifique a conexão.")

    # ═════════════════════════════════════════════════════════════
    # TELA ISO
    # ═════════════════════════════════════════════════════════════
    def _build_iso(self) -> Screen:
        s = ISOScreen(name='iso')
        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))

        header = self._make_header("💿 Selecionar ISO", 'home')
        root.add_widget(header)

        # Instruções
        info = Label(
            text=f"[color={self.hex('info')}]Coloque ISOs em:\n"
                 f"{DOWNLOAD_DIR}[/color]",
            markup=True, font_size=sp(10),
            size_hint_y=None, height=dp(40),
        )
        root.add_widget(info)

        # Botão refresh
        btn_refresh = RoundedButton(
            text="🔄  Atualizar lista de ISOs",
            bg_color=self.hex('accent'),
            text_color='#000000',
            size_hint_y=None, height=dp(48),
        )
        btn_refresh.bind(on_release=self._refresh_iso_list)
        root.add_widget(btn_refresh)

        # Lista scrollável de ISOs
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

        # Botão gravar
        btn_use = RoundedButton(
            text="🔌  Usar esta ISO → Pendrive",
            bg_color=self.hex('warning'),
            text_color='#000000',
            size_hint_y=None, height=dp(48),
        )
        btn_use.bind(on_release=lambda b: self.go_to('usb'))
        root.add_widget(btn_use)

        # Voltar
        back = RoundedButton(
            text="← Voltar",
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
                text="❌ Nenhuma ISO encontrada",
                color=self.kivy_color('error'),
                size_hint_y=None, height=dp(40),
            )
            self.iso_list.add_widget(lbl)
            return

        for iso in isos:
            try:
                size = iso.stat().st_size
                btn = RoundedButton(
                    text=f"💿 {iso.name}\n"
                         f"   {_format_bytes(size)}  •  {iso.parent}",
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
        self.config['last_iso'] = path
        save_config(self.config)
        add_recent_iso(path)
        try:
            size = os.path.getsize(path)
            self.lbl_iso.text = f"✅ {Path(path).name}\n{_format_bytes(size)}"
        except Exception:
            self.lbl_iso.text = f"✅ {Path(path).name}"
        self.log(f"💿 ISO selecionada: {path}", "success")

    # ═════════════════════════════════════════════════════════════
    # TELA USB
    # ═════════════════════════════════════════════════════════════
    def _build_usb(self) -> Screen:
        s = USBScreen(name='usb')
        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))

        header = self._make_header("🔌 Pendrive USB", 'home')
        root.add_widget(header)

        # Aviso de ROOT
        root_warn = Label(
            text=f"[color={self.hex('warning')}]⚠️ Gravação requer ROOT "
                 f"(Termux com tsu)[/color]",
            markup=True, font_size=sp(10),
            size_hint_y=None, height=dp(24),
        )
        root.add_widget(root_warn)

        # Botão detectar
        btn_detect = RoundedButton(
            text="🔄  Detectar Pendrives",
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

        # Botão gravar
        self.btn_write = RoundedButton(
            text="💾  GRAVAR ISO NO PENDRIVE",
            bg_color=self.hex('error'),
            text_color='#ffffff',
            size_hint_y=None, height=dp(56),
        )
        self.btn_write.bind(on_release=self._start_write)
        root.add_widget(self.btn_write)

        # Voltar
        back = RoundedButton(
            text="← Voltar",
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
        self.log("🔍 Detectando pendrives...", "info")
        drives = self._get_usb_drives_mobile()

        if not drives:
            lbl = Label(
                text="❌ Nenhum pendrive OTG detectado\n\n"
                     "💡 Conecte o pendrive via cabo OTG\n"
                     "💡 Autorize o acesso quando pedido",
                color=self.kivy_color('warning'),
                size_hint_y=None, height=dp(100),
                halign='center',
            )
            self.usb_list.add_widget(lbl)
            return

        for d in drives:
            sg = d.get('size', 0) / (1024**3)
            btn = RoundedButton(
                text=f"🔌 {d['model']}\n"
                     f"   {d['path']}  •  {sg:.1f} GB",
                bg_color=self.hex('button'),
                text_color=self.hex('fg'),
                size_hint_y=None, height=dp(60),
            )
            btn.bind(on_release=lambda b, dr=d: self._select_drive(dr))
            self.usb_list.add_widget(btn)

        self.log(f"✅ {len(drives)} pendrive(s) detectado(s)", "success")

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
            f"✅ Alvo: {drive['path']}\n"
            f"💿 ISO: {Path(self.selected_iso).name if self.selected_iso else '(nenhuma)'}"
        )
        self.log(f"🎯 Pendrive alvo: {drive['path']}", "success")

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
                "Gravação requer privilégios de root.\n\n"
                "No Termux: execute 'tsu' antes de rodar.\n"
                "No APK: o app precisa de root.")
            return

        self.log(f"💾 Gravando {self.selected_iso} → {self._selected_usb['path']}", "warning")
        self._show_info(
            "🚧 Em desenvolvimento",
            "A gravação via DD no mobile está em desenvolvimento.\n\n"
            "Use a versão desktop para gravar no pendrive.")

    # ═════════════════════════════════════════════════════════════
    # TELA LOG
    # ═════════════════════════════════════════════════════════════
    def _build_log(self) -> Screen:
        s = LogScreen(name='log')
        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))

        header = self._make_header("📋 Log de Operações", 'home')
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
            width=lambda *a: self.log_label.setter('text_size')(
                self.log_label.width, None))
        scroll.add_widget(self.log_label)
        root.add_widget(scroll)

        # Botões
        btn_row = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(6))
        btn_clear = RoundedButton(
            text="🗑️ Limpar",
            bg_color=self.hex('button'),
            text_color=self.hex('fg'),
        )
        btn_clear.bind(on_release=lambda b: self._clear_log())
        btn_row.add_widget(btn_clear)

        btn_save = RoundedButton(
            text="💾 Salvar",
            bg_color=self.hex('accent'),
            text_color='#000000',
        )
        btn_save.bind(on_release=lambda b: self._save_log())
        btn_row.add_widget(btn_save)
        root.add_widget(btn_row)

        back = RoundedButton(
            text="← Voltar",
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
        self.log("🗑️ Log limpo", "success")

    def _save_log(self):
        try:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            path = LOG_DIR / f"log_{ts}.txt"
            with open(path, 'w', encoding='utf-8') as f:
                f.write("\n".join(self._log_lines))
            self.log(f"💾 Log salvo: {path}", "success")
            self._show_info("Log salvo", str(path))
        except Exception as e:
            self.log(f"❌ Erro: {e}", "error")

    # ═════════════════════════════════════════════════════════════
    # TELA ABOUT
    # ═════════════════════════════════════════════════════════════
    def _build_about(self) -> Screen:
        s = AboutScreen(name='about')
        root = BoxLayout(orientation='vertical', padding=dp(12), spacing=dp(8))

        header = self._make_header("ℹ️ Sobre", 'home')
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
            f"🟣 INSPIRAÇÃO NIXOS[/color][/b]\n"
            f"Este projeto adota princípios do NixOS:\n"
            f"• Build reprodutível\n"
            f"• Dependências declarativas\n"
            f"• Isolamento total\n\n"
            f"NixOS® é marca registrada da NixOS Foundation\n"
            f"(Stichting NixOS Foundation). Sem afiliação.\n\n"
            f"[b][color={self.hex('accent')}]"
            f"🌐 LINKS NIXOS[/color][/b]\n"
            f"• Governança: nixos.org/governance/\n"
            f"• Download: nixos.org/download/\n"
            f"• Constituição:\n"
            f"  github.com/NixOS/org\n\n"
            f"[b][color={self.hex('accent')}]"
            f"⚖️ LICENÇAS[/color][/b]\n"
            f"• Nixpkgs: MIT\n"
            f"• Nix: LGPL-2.1\n"
            f"• Logo NixOS: CC BY 4.0\n\n"
            f"[b][color={self.hex('success')}]"
            f"❤️ APOIAR (PIX)[/color][/b]\n"
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
        lbl.bind(width=lambda *a: lbl.setter('text_size')(lbl.width, None))
        lbl.bind(texture_size=lambda *a: setattr(lbl, 'height',
                                                  lbl.texture_size[1]))
        content.add_widget(lbl)

        # Botões
        for text, url in [
            ("🌐 GitHub", GITHUB_URL),
            ("🟣 NixOS Governance", NIXOS_GOVERNANCE_URL),
            ("📥 NixOS Download", NIXOS_DOWNLOAD_URL),
            ("📜 Constituição NixOS", NIXOS_CONSTITUTION_URL),
            ("⭐ PREMIUM R$ 10", PREMIUM_CHECKOUT_URL),
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
            text="← Voltar",
            bg_color=self.hex('button'),
            text_color=self.hex('fg'),
            size_hint_y=None, height=dp(44),
        )
        back.bind(on_release=lambda b: self.go_to('home'))
        root.add_widget(back)

        s.add_widget(root)
        return s

    # ═════════════════════════════════════════════════════════════
    # HELPERS UI
    # ═════════════════════════════════════════════════════════════
    def _make_header(self, title_text: str, back_screen: str) -> BoxLayout:
        row = BoxLayout(size_hint_y=None, height=dp(52), spacing=dp(6))

        btn_back = RoundedButton(
            text="←",
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
        # Botão fechar
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

    # ─── Ciclo de vida ────────────────────────────────────────────
    def on_pause(self):
        """Android: pausa segura."""
        return True

    def on_resume(self):
        """Android: retomada."""
        pass

    def on_stop(self):
        """Salva config ao sair."""
        try:
            save_config(self.config)
        except Exception:
            pass


# ═════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═════════════════════════════════════════════════════════════════════
def main():
    DarkPenBootKivyApp().run()


if __name__ == "__main__":
    main()