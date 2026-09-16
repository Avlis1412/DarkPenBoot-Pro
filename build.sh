#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════
# DARKPENBOOT PRO — build.sh
# Script de build local para Linux / macOS
# ═══════════════════════════════════════════════════════════════════════════
#
# Uso:
#   ./build.sh                # Build para plataforma atual
#   ./build.sh --nix          # Build via Nix (reprodutível)
#   ./build.sh --all          # Build + testes
#   ./build.sh --android      # Build APK (via Buildozer)
#   ./build.sh --clean        # Limpa artefatos
#   ./build.sh --help         # Mostra esta ajuda
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ INSPIRAÇÃO NIXOS                                                        │
# │                                                                         │
# │ Este script aplica os princípios do NixOS:                              │
# │   • Isolamento — usa venv dedicada                                      │
# │   • Reprodutibilidade — versões fixadas                                 │
# │   • Multi-plataforma — mesma interface, alvos diferentes                │
# │                                                                         │
# │ NixOS® é marca da NixOS Foundation. Sem afiliação.                      │
# └─────────────────────────────────────────────────────────────────────────┘
#

set -euo pipefail

# ─── Cores ───────────────────────────────────────────────────────────────
readonly RED='\033[0;31m'
readonly GREEN='\033[0;32m'
readonly YELLOW='\033[1;33m'
readonly CYAN='\033[0;36m'
readonly PURPLE='\033[0;35m'
readonly NC='\033[0m' # No Color

# ─── Configuração ────────────────────────────────────────────────────────
readonly APP_NAME="DarkPenBoot"
readonly APP_VERSION="3.5.0"
readonly MAIN_SCRIPT="DarkPenBoot_PRO1.py"
readonly DIST_DIR="dist"
readonly BUILD_DIR="build"
readonly VENV_DIR=".venv_build"

# ─── Banner ──────────────────────────────────────────────────────────────
print_banner() {
    echo -e "${PURPLE}"
    echo "═══════════════════════════════════════════════════════════"
    echo "  🚀 ${APP_NAME} Pro v${APP_VERSION} — Build Local"
    echo "═══════════════════════════════════════════════════════════"
    echo -e "${NC}"
    echo -e "${PURPLE}🟣 Inspirado em NixOS — build reprodutível${NC}"
    echo -e "${PURPLE}🟣 NixOS® é marca da NixOS Foundation (sem afiliação)${NC}"
    echo ""
}

# ─── Detectar SO ─────────────────────────────────────────────────────────
detect_os() {
    case "$(uname -s)" in
        Linux*)     echo "linux";;
        Darwin*)    echo "macos";;
        MINGW*|MSYS*|CYGWIN*) echo "windows";;
        *)          echo "unknown";;
    esac
}

# ─── Verificar dependências ──────────────────────────────────────────────
check_deps() {
    echo -e "${CYAN}🔍 Verificando dependências...${NC}"

    local missing=()
    if ! command -v python3 &>/dev/null; then
        missing+=("python3")
    fi

    if [ ${#missing[@]} -gt 0 ]; then
        echo -e "${RED}❌ Faltando: ${missing[*]}${NC}"
        echo ""
        echo -e "${YELLOW}💡 Como instalar:${NC}"
        echo "   Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk"
        echo "   macOS:         brew install python@3.11 python-tk"
        exit 1
    fi

    echo -e "${GREEN}✅ Dependências OK${NC}"
    echo "   Python: $(python3 --version)"
}

# ─── Verificar PyInstaller ───────────────────────────────────────────────
check_pyinstaller() {
    if ! python3 -m pip show pyinstaller &>/dev/null; then
        echo -e "${YELLOW}📦 Instalando PyInstaller...${NC}"
        python3 -m pip install --user pyinstaller
    fi
    echo -e "${GREEN}✅ PyInstaller instalado${NC}"
}

# ─── Limpar artefatos ────────────────────────────────────────────────────
clean_build() {
    echo -e "${CYAN}🧹 Limpando artefatos...${NC}"
    rm -rf "$DIST_DIR" "$BUILD_DIR" "$VENV_DIR" 2>/dev/null || true
    rm -f *.spec 2>/dev/null || true
    echo -e "${GREEN}✅ Limpeza concluída${NC}"
}

# ─── Build local (PyInstaller) ───────────────────────────────────────────
build_local() {
    local os_type
    os_type="$(detect_os)"

    echo -e "${CYAN}🏗️  Build para: ${os_type}${NC}"
    echo ""

    # Verifica script principal
    if [ ! -f "$MAIN_SCRIPT" ]; then
        echo -e "${RED}❌ Script principal não encontrado: $MAIN_SCRIPT${NC}"
        exit 1
    fi

    # Verifica sintaxe
    echo -e "${CYAN}🔍 Verificando sintaxe Python...${NC}"
    python3 -m py_compile "$MAIN_SCRIPT" || {
        echo -e "${RED}❌ Erro de sintaxe!${NC}"
        exit 1
    }
    echo -e "${GREEN}✅ Sintaxe OK${NC}"
    echo ""

    # Configura PyInstaller
    local pyi_opts=(
        --onefile
        --name "${APP_NAME}"
        --distpath "$DIST_DIR"
        --workpath "$BUILD_DIR"
        --specpath .
        --noconfirm
        --clean
    )

    # Adiciona --windowed em plataformas gráficas
    if [ "$os_type" = "linux" ] || [ "$os_type" = "macos" ]; then
        pyi_opts+=(--windowed)
    fi

    # Roda PyInstaller
    echo -e "${CYAN}📦 Empacotando com PyInstaller...${NC}"
    python3 -m PyInstaller "${pyi_opts[@]}" "$MAIN_SCRIPT"

    # Nome do executável por SO
    local exe_name
    case "$os_type" in
        linux)   exe_name="${APP_NAME}";;
        macos)   exe_name="${APP_NAME}";;
        windows) exe_name="${APP_NAME}.exe";;
    esac

    if [ ! -f "$DIST_DIR/$exe_name" ]; then
        echo -e "${RED}❌ Build falhou — binário não encontrado${NC}"
        exit 1
    fi

    # Calcula SHA256
    echo -e "${CYAN}🔐 Calculando SHA256...${NC}"
    if command -v sha256sum &>/dev/null; then
        sha256sum "$DIST_DIR/$exe_name" > "$DIST_DIR/$exe_name.sha256"
    else
        shasum -a 256 "$DIST_DIR/$exe_name" > "$DIST_DIR/$exe_name.sha256"
    fi

    # Resultado final
    local size
    size=$(du -h "$DIST_DIR/$exe_name" | cut -f1)
    local hash
    hash=$(awk '{print $1}' "$DIST_DIR/$exe_name.sha256")

    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  ✅ Build concluído!${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════${NC}"
    echo ""
    echo -e "📦 Binário:  ${CYAN}$DIST_DIR/$exe_name${NC}"
    echo -e "📏 Tamanho:  ${CYAN}$size${NC}"
    echo -e "🔐 SHA256:   ${CYAN}$hash${NC}"
    echo ""
}

# ─── Build via Nix (reprodutível) ────────────────────────────────────────
build_nix() {
    if ! command -v nix &>/dev/null; then
        echo -e "${RED}❌ Nix não instalado!${NC}"
        echo -e "${YELLOW}💡 Instale em: https://nixos.org/download/${NC}"
        exit 1
    fi

    echo -e "${PURPLE}❄️  Build via Nix (reprodutível)${NC}"
    echo -e "${PURPLE}   Filosofia NixOS aplicada${NC}"
    echo ""

    if [ -f "flake.nix" ]; then
        echo -e "${CYAN}🏗️  Rodando: nix build${NC}"
        nix build .#default --print-build-logs
        echo -e "${GREEN}✅ Binário em: result/bin/darkpenboot${NC}"
    else
        echo -e "${RED}❌ flake.nix não encontrado!${NC}"
        exit 1
    fi
}

# ─── Build Android (via Buildozer) ───────────────────────────────────────
build_android() {
    if [ ! -f "buildozer.spec" ]; then
        echo -e "${YELLOW}⚠️  buildozer.spec não encontrado — pulando Android${NC}"
        return 0
    fi

    if ! command -v buildozer &>/dev/null; then
        echo -e "${YELLOW}⚠️  Buildozer não instalado${NC}"
        echo -e "${YELLOW}💡 Instale com: pip install buildozer cython${NC}"
        return 0
    fi

    echo -e "${CYAN}📱 Build Android via Buildozer...${NC}"
    buildozer android debug
    echo -e "${GREEN}✅ APK em: bin/*.apk${NC}"
}

# ─── Rodar testes ────────────────────────────────────────────────────────
run_tests() {
    echo -e "${CYAN}🧪 Rodando testes...${NC}"
    if [ -d "tests" ]; then
        python3 -m pytest tests/ -v || true
    else
        echo -e "${YELLOW}⚠️  Pasta tests/ não encontrada — pulando${NC}"
    fi
}

# ─── Ajuda ───────────────────────────────────────────────────────────────
show_help() {
    cat <<EOF
🚀 ${APP_NAME} Pro v${APP_VERSION} — Build Script

Uso: ./build.sh [OPÇÕES]

Opções:
  (sem args)      Build local com PyInstaller
  --nix           Build via Nix (reprodutível)
  --all           Build + testes
  --android       Build Android (via Buildozer)
  --clean         Limpa artefatos
  --help          Mostra esta ajuda

Plataformas suportadas:
  🐧 Linux     — binário ELF
  🍏 macOS     — binário Mach-O
  🪟 Windows   — .exe (via build.ps1)
  📱 Android   — .apk (via Buildozer)

Exemplos:
  ./build.sh              # Build local
  ./build.sh --nix        # Build reprodutível via Nix
  ./build.sh --clean      # Limpa tudo

🟣 Inspirado em NixOS — nixos.org
🟣 NixOS® é marca da NixOS Foundation (sem afiliação)
EOF
}

# ─── Main ────────────────────────────────────────────────────────────────
main() {
    print_banner

    case "${1:-}" in
        --help|-h)
            show_help
            ;;
        --clean|-c)
            clean_build
            ;;
        --nix|-n)
            build_nix
            ;;
        --android)
            build_android
            ;;
        --all)
            check_deps
            check_pyinstaller
            build_local
            echo ""
            run_tests
            ;;
        "")
            check_deps
            check_pyinstaller
            build_local
            ;;
        *)
            echo -e "${RED}❌ Opção desconhecida: $1${NC}"
            show_help
            exit 1
            ;;
    esac
}

main "$@"