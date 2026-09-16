# ═══════════════════════════════════════════════════════════════════════════
# DARKPENBOOT PRO — nix/android.nix
# ═══════════════════════════════════════════════════════════════════════════
#
# Ambiente de build Android para o DarkPenBoot Pro (Kivy + Buildozer).
#
# Uso:
#   nix-shell nix/android.nix
#
# Ou importe em um flake.nix:
#   imports = [ ./nix/android.nix ];
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ INSPIRAÇÃO NIXOS                                                        │
# │                                                                         │
# │ Este arquivo aplica os princípios do NixOS:                             │
# │   • REPRODUTIBILIDADE — mesmas versões sempre                          │
# │   • DECLARATIVIDADE  — tudo em 1 arquivo                                │
# │   • ISOLAMENTO       — SDK/NDK em ambiente próprio                      │
# │                                                                         │
# │ NixOS® é marca da NixOS Foundation (sem afiliação).                     │
# │ Referência: https://nixos.org/governance/                               │
# └─────────────────────────────────────────────────────────────────────────┘
#
{ pkgs ? import <nixpkgs> {} }:

let
  # ─── Versão do Python usada pelo Kivy/Buildozer ──────────────────────
  python = pkgs.python311;

  # ─── Pacotes Python necessários para o build Android ─────────────────
  pythonEnv = python.withPackages (ps: with ps; [
    # Framework mobile
    kivy

    # Build system
    cython
    buildozer

    # Bibliotecas usadas pelo app
    pillow
    requests

    # Utilitários
    pip
    setuptools
    wheel
  ]);

in
pkgs.mkShell rec {
  name = "darkpenboot-android";

  # ─── Ferramentas do sistema ──────────────────────────────────────────
  buildInputs = with pkgs; [
    # ─── Java (obrigatório para Gradle) ───
    openjdk17

    # ─── Android SDK & Tools ───
    androidenv.androidPkgs.androidsdk
    androidenv.androidPkgs.platform-tools
    androidenv.androidPkgs.emulator

    # ─── Gradle (build system Android) ───
    gradle

    # ─── Python + Kivy ───
    pythonEnv

    # ─── Ferramentas de build C/C++ ───
    # (Kivy compila extensões nativas)
    autoconf
    automake
    libtool
    pkg-config
    cmake
    ninja
    gnumake

    # ─── Bibliotecas nativas que o Kivy usa ───
    zlib
    libffi
    openssl
    ncurses
    sqlite

    # ─── Ferramentas gerais ───
    git
    zip
    unzip
    wget
    curl
    file
    which
  ];

  # ─── Variáveis de ambiente ───────────────────────────────────────────
  ANDROID_HOME = "${pkgs.androidenv.androidPkgs.androidsdk}/share/android-sdk";
  ANDROID_SDK_ROOT = "${pkgs.androidenv.androidPkgs.androidsdk}/share/android-sdk";
  ANDROID_NDK_HOME = "${pkgs.androidenv.androidPkgs.androidsdk}/share/android-sdk/ndk-bundle";

  GRADLE_USER_HOME = "$PWD/.gradle-home";

  # ─── Mensagem ao entrar no shell ─────────────────────────────────────
  shellHook = ''
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo "  📱 DarkPenBoot Pro — Android Build Environment"
    echo "═══════════════════════════════════════════════════════════"
    echo ""
    echo "🟣 Inspirado em NixOS — build reprodutível"
    echo "🟣 NixOS® é marca da NixOS Foundation (sem afiliação)"
    echo ""
    echo "📦 Ferramentas disponíveis:"
    echo "   • Java:    $(java -version 2>&1 | head -1)"
    echo "   • Python:  $(python --version)"
    echo "   • Kivy:    $(python -c 'import kivy; print(kivy.__version__)' 2>/dev/null || echo 'N/A')"
    echo "   • Gradle:  $(gradle --version 2>/dev/null | grep Gradle | head -1 || echo 'N/A')"
    echo "   • SDK:     $ANDROID_HOME"
    echo ""
    echo "🚀 Comandos disponíveis:"
    echo "   buildozer android debug     → Gera APK de debug"
    echo "   buildozer android release   → Gera APK de release"
    echo "   buildozer android clean     → Limpa artefatos"
    echo ""
    echo "📄 Configuração: buildozer.spec"
    echo ""
    echo "═══════════════════════════════════════════════════════════"
    echo ""

    # Cria diretório do Gradle se não existir
    mkdir -p "$GRADLE_USER_HOME"
  '';
}