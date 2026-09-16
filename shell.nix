# ═══════════════════════════════════════════════════════════════════════════
# DARKPENBOOT PRO — shell.nix
# Ambiente de desenvolvimento simples via Nix
# ═══════════════════════════════════════════════════════════════════════════
#
# Uso:
#   nix-shell
#
# Este é um ambiente SIMPLIFICADO para desenvolvimento rápido.
# Para o build completo multi-plataforma, use flake.nix (nix develop).
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ INSPIRAÇÃO NIXOS                                                        │
# │                                                                         │
# │ Um shell.nix é a forma mais simples de criar ambientes reprodutíveis.   │
# │ Todos que rodarem `nix-shell` terão EXATAMENTE as mesmas versões:       │
# │   • Python 3.11                                                         │
# │   • PyInstaller 6.x                                                     │
# │   • Pillow, requests                                                    │
# │   • curl, wget, 7-Zip                                                   │
# │                                                                         │
# │ NixOS® é marca da NixOS Foundation. Sem afiliação.                      │
# └─────────────────────────────────────────────────────────────────────────┘
#
{ pkgs ? import <nixpkgs> {} }:

pkgs.mkShell {
  name = "darkpenboot-dev";

  buildInputs = with pkgs; [
    # ─── Python + ferramentas ───
    python311
    python311Packages.pip
    python311Packages.pyinstaller
    python311Packages.pillow
    python311Packages.requests

    # ─── Ferramentas de sistema (usadas pelo DarkPenBoot) ───
    curl       # Download HTTP/HTTPS
    wget       # Download HTTP/HTTPS (fallback)
    p7zip      # 7-Zip (extração de ISOs)
    unzip      # Extração ZIP
    file       # Detectar tipo de arquivo
    jq         # Processar JSON

    # ─── Para desenvolvimento ───
    git        # Controle de versão
    gnumake    # Make
  ];

  shellHook = ''
    echo "═══════════════════════════════════════════════════════════"
    echo "  🚀 DarkPenBoot Pro — Ambiente nix-shell"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "🟣 Build reprodutível inspirado em NixOS"
    echo "🟣 NixOS® marca da NixOS Foundation (sem afiliação)"
    echo ""
    echo "Python:      $(python --version)"
    echo "PyInstaller: $(pyinstaller --version 2>/dev/null || echo 'N/A')"
    echo "curl:        $(curl --version | head -1)"
    echo ""
    echo "📋 Comandos úteis:"
    echo "   pyinstaller --onefile --windowed DarkPenBoot_PRO1.py"
    echo "   python DarkPenBoot_PRO1.py"
    echo ""
    echo "═══════════════════════════════════════════════════════════"
  '';
}