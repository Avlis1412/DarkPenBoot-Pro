"""Configuracao e links compartilhados da interface Android."""

from pathlib import Path

APP_NAME = "DarkPenBoot Pro"
APP_VERSION = "3.5.0"
APP_AUTHOR = "Adriano Rodrigues da Silva"
GITHUB_URL = "https://github.com/Avlis1412"
NIXOS_URL = "https://nixos.org"
NIXOS_GOVERNANCE_URL = "https://nixos.org/governance/"
NIXOS_DOWNLOAD_URL = "https://nixos.org/download/"
NIXOS_CONSTITUTION_URL = "https://github.com/NixOS/org/blob/main/doc/constitution.md"
PREMIUM_CHECKOUT_URL = "https://github.com/Avlis1412/DarkPenBoot-Pro#premium"

BASE_DIR = Path("/sdcard/DarkPenBootPro")
DOWNLOAD_DIR = BASE_DIR / "downloads"
LOG_DIR = BASE_DIR / "logs"
CONFIG_FILE = BASE_DIR / "config.json"

for directory in (BASE_DIR, DOWNLOAD_DIR, LOG_DIR):
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except OSError:
        pass

DEFAULT_CONFIG = {
    "theme": "soft_dark",
    "last_distro": "NixOS 25.05 Minimal",
    "last_iso": "",
    "verify_sha256": True,
}

LEGAL_NOTICE = (
    "NixOS® é marca registrada da NixOS Foundation. "
    "O DarkPenBoot Pro não é afiliado, endossado ou patrocinado pela "
    "NixOS Foundation. Consulte apenas os links oficiais de governança e download."
)
