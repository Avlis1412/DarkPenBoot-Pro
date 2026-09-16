# ═══════════════════════════════════════════════════════════════════════════
# DARKPENBOOT PRO — flake.nix
# Build reprodutível multi-plataforma via Nix
# ═══════════════════════════════════════════════════════════════════════════
#
# Uso:
#   nix develop              # Entra no ambiente de desenvolvimento
#   nix build                # Compila o binário
#   nix flake show           # Lista todos os outputs
#   nix flake check          # Roda verificações
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │ FILOSOFIA NIXOS APLICADA                                                │
# │                                                                         │
# │ Este flake implementa os princípios do NixOS:                           │
# │   • REPRODUTIBILIDADE — mesmo input, mesmo output (hash garante)        │
# │   • DECLARATIVIDADE  — tudo em um arquivo, nada implícito               │
# │   • ISOLAMENTO       — deps isoladas do sistema host                    │
# │   • MULTI-PLATAFORMA — Linux, macOS nativos                             │
# │                                                                         │
# │ NixOS® é marca registrada da NixOS Foundation — sem afiliação.          │
# │ Referência: https://nixos.org/governance/                               │
# └─────────────────────────────────────────────────────────────────────────┘
#
{
  description = "DarkPenBoot Pro v3.5.0 — Criador de Pendrives Bootáveis Multi-Plataforma";

  # ─── INPUTS (dependências externas, tudo declarado) ──────────────────
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";

    # NixOS 25.05 (mais recente) para features futuras
    nixpkgs-unstable.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  # ─── OUTPUTS (o que este flake produz) ───────────────────────────────
  outputs = { self, nixpkgs, nixpkgs-unstable, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pkgs-unstable = import nixpkgs-unstable { inherit system; };

        # Versão do software (sincronizada com APP_VERSION)
        version = "3.5.0";

        # ─── Python + dependências ────────────────────────────────────
        # INSPIRAÇÃO NIXOS: declaramos TUDO que o software precisa.
        python = pkgs.python311.withPackages (ps: with ps; [
          # Bibliotecas base
          # (tkinter vem embutido no python311 do nixpkgs)

          # Bibliotecas opcionais para UI moderna
          pillow          # Processamento de imagem (ícones)
          requests        # HTTP (fallback para downloads)

          # Ferramentas de build
          pyinstaller     # Empacotar Python em binário
        ]);

      in
      {
        # ═══════════════════════════════════════════════════════════════
        # PACOTES — Binários finais
        # ═══════════════════════════════════════════════════════════════
        packages = {

          # ─── Build padrão (Linux/macOS executável) ────────────────
          default = pkgs.stdenv.mkDerivation {
            pname = "darkpenboot";
            inherit version;

            src = ./.;

            nativeBuildInputs = [ python pkgs.makeWrapper ];

            # FASE DE BUILD: roda PyInstaller
            buildPhase = ''
              echo "═══════════════════════════════════════════════════════"
              echo "  DarkPenBoot Pro v${version} — Build NixOS reprodutível"
              echo "═══════════════════════════════════════════════════════"
              echo ""
              echo "🟣 Inspirado em NixOS — nixos.org"
              echo "🟣 NixOS® é marca da NixOS Foundation (sem afiliação)"
              echo ""

              # Detecta o script principal
              if [ -f "DarkPenBoot_PRO1.py" ]; then
                MAIN_SCRIPT="DarkPenBoot_PRO1.py"
              elif [ -f "darkpenboot.py" ]; then
                MAIN_SCRIPT="darkpenboot.py"
              else
                echo "❌ Script principal não encontrado!"
                exit 1
              fi

              echo "📦 Empacotando: $MAIN_SCRIPT"

              # Roda PyInstaller em modo onefile (mais portável)
              pyinstaller \
                --onefile \
                --windowed \
                --name darkpenboot \
                --distpath dist \
                --workpath build \
                --specpath . \
                --noconfirm \
                --clean \
                "$MAIN_SCRIPT"

              echo "✅ Build concluído!"
              ls -lh dist/
            '';

            # FASE DE INSTALAÇÃO: copia binário para $out
            installPhase = ''
              mkdir -p $out/bin
              cp dist/darkpenboot $out/bin/
              chmod +x $out/bin/darkpenboot

              # Cria um wrapper para garantir PATH correto
              makeWrapper $out/bin/darkpenboot $out/bin/darkpenboot-wrapped \
                --prefix PATH : ${pkgs.lib.makeBinPath [
                  pkgs.curl
                  pkgs.wget
                  pkgs.p7zip
                ]}
            '';

            meta = with pkgs.lib; {
              description = "Criador de pendrives bootáveis multi-plataforma";
              homepage = "https://github.com/Avlis1412/DarkPenBoot-Pro";
              license = licenses.mit;
              platforms = platforms.unix;
              maintainers = [ ];
            };
          };

          # ─── Preparação para build Windows ────────────────────────
          windows-prep = pkgs.stdenv.mkDerivation {
            pname = "darkpenboot-windows-prep";
            inherit version;
            src = ./.;

            buildInputs = with pkgs; [
              mingw-w64
              wineWowPackages.stable
            ];

            buildPhase = ''
              echo "═══════════════════════════════════════════════════════"
              echo "  Preparação para build Windows"
              echo "═══════════════════════════════════════════════════════"
              echo ""
              echo "⚠️  Cross-compile Python + PyInstaller é complexo."
              echo "💡 Use GitHub Actions para .exe confiável."
              echo "📄 Veja: .github/workflows/build.yml"
              echo ""
            '';

            installPhase = ''
              mkdir -p $out/share/darkpenboot-windows-prep
              cp -r . $out/share/darkpenboot-windows-prep/
            '';
          };

          # ─── Preparação para build Android ────────────────────────
          android-prep = pkgs.stdenv.mkDerivation {
            pname = "darkpenboot-android-prep";
            inherit version;
            src = ./.;

            buildInputs = with pkgs; [
              openjdk17
              androidenv.androidPkgs.androidsdk
              androidenv.androidPkgs.platform-tools
              gradle
            ];

            buildPhase = ''
              echo "═══════════════════════════════════════════════════════"
              echo "  Preparação para build Android"
              echo "═══════════════════════════════════════════════════════"
              echo ""
              echo "📱 UI Tkinter NÃO funciona no Android."
              echo "💡 Para APK, use a versão Kivy:"
              echo "   python darkpenboot_kivy.py"
              echo "📄 Veja: buildozer.spec e .github/workflows/build.yml"
              echo ""
            '';

            installPhase = ''
              mkdir -p $out/share/darkpenboot-android-prep
            '';
          };
        };

        # ═══════════════════════════════════════════════════════════════
        # SHELLS — Ambientes de desenvolvimento
        # ═══════════════════════════════════════════════════════════════
        devShells = {

          # ─── Shell padrão (com todas as ferramentas) ──────────────
          default = pkgs.mkShell {
            buildInputs = [
              python
              pkgs.curl
              pkgs.wget
              pkgs.p7zip
              pkgs.unzip
              pkgs.file
              pkgs.git
              pkgs.jq
            ];

            shellHook = ''
              echo "═══════════════════════════════════════════════════════"
              echo "  🚀 DarkPenBoot Pro v${version} — Ambiente NixOS"
              echo "═══════════════════════════════════════════════════════"
              echo ""
              echo "🟣 Filosofia NixOS: build reprodutível + declarativo"
              echo "🟣 NixOS® é marca da NixOS Foundation (sem afiliação)"
              echo ""
              echo "Python:       $(python --version)"
              echo "PyInstaller:  $(pyinstaller --version 2>/dev/null || echo 'N/A')"
              echo "curl:         $(curl --version | head -1)"
              echo ""
              echo "📋 Comandos disponíveis:"
              echo "   nix build                → binário Linux/macOS"
              echo "   nix build .#windows-prep → prep. Windows"
              echo "   nix develop              → este shell"
              echo "   ./build.sh               → build automatizado"
              echo ""
              echo "═══════════════════════════════════════════════════════"
            '';
          };

          # ─── Shell mínimo (só Python) ─────────────────────────────
          minimal = pkgs.mkShell {
            buildInputs = [ python ];
            shellHook = ''
              echo "🐍 Python minimal shell — DarkPenBoot Pro"
              python --version
            '';
          };
        };

        # ═══════════════════════════════════════════════════════════════
        # APPS — Entry points (nix run)
        # ═══════════════════════════════════════════════════════════════
        apps = {
          default = {
            type = "app";
            program = "${self.packages.${system}.default}/bin/darkpenboot-wrapped";
          };
        };

        # ═══════════════════════════════════════════════════════════════
        # CHECKS — Testes automatizados (nix flake check)
        # ═══════════════════════════════════════════════════════════════
        checks = {
          # Verifica que o script Python compila (sem erros de sintaxe)
          syntax-check = pkgs.runCommand "darkpenboot-syntax-check" {
            buildInputs = [ python ];
          } ''
            echo "🔍 Verificando sintaxe Python..."

            # Verifica o script principal (desktop)
            if [ -f "${./.}/DarkPenBoot_PRO1.py" ]; then
              python -m py_compile "${./.}/DarkPenBoot_PRO1.py"
              echo "✅ Sintaxe OK: DarkPenBoot_PRO1.py"
            fi

            # Verifica o script Kivy (mobile)
            if [ -f "${./.}/darkpenboot_kivy.py" ]; then
              python -m py_compile "${./.}/darkpenboot_kivy.py"
              echo "✅ Sintaxe OK: darkpenboot_kivy.py"
            fi

            touch $out
          '';
        };
      }
    ) // {
      # ═════════════════════════════════════════════════════════════════
      # OUTPUTS ADICIONAIS (fora do eachDefaultSystem)
      # ═════════════════════════════════════════════════════════════════

      # ─── Overlay para projetos que consomem este flake ─────────────
      overlays.default = final: prev: {
        darkpenboot = self.packages.${prev.system}.default;
      };
    };
}