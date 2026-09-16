# Changelog - DarkPenBoot Pro

Todas as mudancas notaveis deste projeto sao documentadas aqui.

Formato baseado em [Keep a Changelog](https://keepachangelog.com/).

---

## [3.6.1] - 2026-09-16

### Adicionado

- `_scan_shell_all_platforms()` - Varredura universal via shell
  - Windows: PowerShell + CIM (Win32_DiskDrive)
- Constantes visuais v3.6.1: `GUI_TEXTURE_ENABLED`,
  `ORB_TRANSLUCENCY`, `ORB_GLASS_EDGE`, `LOGO_GLOW_ENABLED`
- Helpers: `_blend_color`, `_rgb_tuple_to_hex`,
  `_lighten_hex`, `_darken_hex`

### Modificado

- `refresh_drives()` - Dispara pulso neon + oscilacao do orb
- `_do_identify()` - Fallback shell se API falhar
- `_do_diskpart()` - Revarredura se perder o alvo
- `_do_format_via_terminal()` - Formata o FS do seletor
- `ClickableLogo._update_colors()` - Glow + shadow

### Corrigido

- `SyntaxError` em `download_with_fallback`

---

# 📋 Changelog — DarkPenBoot Pro

Todas as mudanças notáveis deste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/)
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## 📖 Legenda

| Ícone | Significado |
|:-----:|-------------|
| ✨ | Adicionado — Novas funcionalidades |
| 🔧 | Alterado — Mudanças em funcionalidades existentes |
| ⚠️ | Descontinuado — Funcionalidades que serão removidas |
| 🗑️ | Removido — Funcionalidades removidas |
| 🐛 | Corrigido — Correções de bugs |
| 🔐 | Segurança — Correções relacionadas a segurança |

---

## [Não Lançado]

### Planejado
- Suporte completo a Nix Flakes no repositório
- Compilação cross-platform via GitHub Actions para Android
- Sistema de plugins para adicionar distros customizadas
- CLI (Command-Line Interface) independente da GUI
- Modo portable (rodar de qualquer pasta)
- Suporte a Windows PE e ISOs híbridas
- Testes automatizados com cobertura > 80%

---

## [3.5.0] — 2026-09-15

### ✨ Adicionado

- **Downloader reescrito** com 5 camadas de fallback:
  1. `curl` com User-Agent de Chrome
  2. `curl` com User-Agent de Firefox
  3. `wget` com retry
  4. `urllib` com SSL permissivo
  5. Redirecionamento para navegador (último recurso)
- **URLs de distros Linux atualizadas** — 30+ distros com URLs verificadas em 2025
- **Mirrors oficiais automáticos**: kernel.org, fi.debian.org, mirror.ufscar.br
- **Detecção de HTML disfarçado** — rejeita páginas de erro em vez de ISOs
- **Verificação HEAD** — valida URL antes de baixar
- **Retry com backoff exponencial** — 5s entre tentativas
- **Referer `nixos.org`** — contorna bloqueios de CDN
- **User-Agent rotativo** — 5 UAs diferentes
- **Bloco de inspiração NixOS** no header do código
- **Menções explícitas ao NixOS** (15+ referências)
- **Aba 📚 Fontes** com créditos e licenças
- **Hyperlink NixOS** na janela Sobre
- **Botão PREMIUM** (R$ 10) com checkout
- **Verificação SHA256** automática pós-download

### 🔧 Alterado

- `AD_BANNER_TEXT` agora menciona NixOS Governance
- Detecção de stall aumentada para 180s (era 120s)
- Timeout de download aumentado para 2h (era 30s)
- `_download_linux_iso` usa novo downloader
- Aba Fontes reformulada com seção NixOS dedicada

### 🐛 Corrigido

- Downloads de distros Linux que estavam falhando por URLs desatualizadas
- Detecção de arquivos HTML baixados por engano
- Falta de verificação SHA256 em downloads
- URLs de mirrors brasileiros para Debian e Kali

### 🔐 Segurança

- Adicionado `Referer` legítimo para contornar bloqueios
- Validação `Content-Type` em HEAD requests
- Bloqueio de redirects suspeitos (> 15 redirecionamentos)

---

## [3.4.0] — 2026-09-10

### ✨ Adicionado

- **Tema 🌙 Soft Dark** — reduz fadiga visual em sessões longas
- **NixOS 24.11 "Vicuña"** — 3 edições (GNOME, KDE Plasma 6, Minimal)
- **NixOS 25.05** — 3 edições (GNOME, KDE Plasma 6, Minimal)
- **Aba 📚 Fontes** com créditos, licenças e trademark NixOS
- **Botão ⭐ PREMIUM (R$ 10)** com checkout
- **Verificação SHA256** automática pós-download
- **Hyperlink NixOS** na janela Sobre (atribuição legal)
- **Aviso legal NixOS** no rodapé da aba Fontes

### 🔧 Alterado

- `DISTRO_INFO` reformulado com campo `license`, `homepage`, `foundation`
- Seção NixOS no `DISTRO_INFO` com links de governança
- Título do app atualizado para v3.4.0

### 🐛 Corrigido

- Detecção de ISO Windows que estava confundindo com Linux
- Aviso de copyright NixOS agora aparece corretamente

---

## [3.3.0] — 2026-09-05

### ✨ Adicionado

- **Pulso Neon Global** — toda a UI pulsa durante operações
- **Orb 3D com rastro de neon** — seletor de tema animado
- **Logo clicável** — clique no logo abre popup de instruções
- **Aba 📖 Ajuda** — guia completo com atalhos
- **Seletor Extract vs RAW** — radio buttons explicativos
- **Popup de instruções (F1)** — guia rápido de uso
- **Atalhos de teclado**:
  - `F1` — Popup de ajuda
  - `Ctrl+O` — Selecionar ISO
  - `Ctrl+Enter` — Iniciar gravação
  - `Ctrl+R` — Painel de Recuperação
  - `Ctrl+L` — Limpar log
  - `Ctrl+S` — Salvar log
- **Tooltips em todos os controles** — ajuda contextual
- **Painel de Recuperação com pulso reforçado**

### 🔧 Alterado

- `ClickableLogo` agora tem animação de pulso
- `NeonThemeBall` redesenhado com rastro esférico
- `RoundedButton` responde ao pulso global

### 🐛 Corrigido

- Modo DD que deixava pendrive em RAW/offline por padrão
- Downloads com SSL context em alguns servidores
- Combobox de drive não atualizava após refresh

---

## [3.2.0] — 2026-08-28

### ✨ Adicionado

- **Painel de Recuperação USB** (Ctrl+R) com:
  - Botão **Identificar** para reescanear pendrives
  - Combobox para trocar drive sem fechar janela
  - `Chkdsk /F /R /X`
  - Limpar disco (RAW)
  - Reconstruir MBR/GPT
  - Formatar com FS específico
  - Abrir terminal (cmd/PowerShell/Parted)
- **Opção "Deixar RAW"** na aba Avançado
- **Remontagem automática** após DD — disco volta online com letra
- **Download com User-Agent de navegador real**
- **Downloads com SSL context** para contornar certs inválidos

### 🔧 Alterado

- Modo DD padrão agora remonta pendrive automaticamente
- DD passou a usar `_bring_online_and_assign` no final
- UI ganhou opção explícita "Deixar RAW"

### 🐛 Corrigido

- **Modo DD não deixa mais o pendrive em RAW/sumido**
- Pendrive reaparece no Explorer após gravação DD
- Letra de unidade é atribuída automaticamente

---

## [3.1.0] — 2026-08-15

### ✨ Adicionado

- Suporte a **Android/Termux** (detecção via `TERMUX_VERSION`)
- Suporte a **OTG Mobile**
- Buffer adaptativo por **tier USB** (USB2 vs USB3)
- Detecção de stalls (aborta se travar por 120s)
- Verificação de espaço livre antes de copiar
- Tratamento robusto de **symlinks** em ISOs Linux

### 🔧 Alterado

- `copy_files_with_progress` agora trata symlinks
- Detecção de FAT32 com aviso para arquivos > 4 GB
- Cache de arquivos recentes (últimas 5 ISOs)

---

## [3.0.0] — 2026-08-01

### ✨ Adicionado

- **Reescrita completa da UI** com Tkinter
- **7 temas visuais** (Matrix, Crimson, Nord, Cyberpunk, Monokai, Light, Soft Dark)
- **Animações neon** em widgets customizados
- **Popup customizado** (`UltimatePopup`) com scroll responsivo
- **Config JSON** persistente em `~/.darkpenboot/config.json`
- **Log em tempo real** com cores por nível
- **Doação via PIX** integrada
- **Suporte a múltiplos SOs**:
  - Windows (PowerShell + diskpart)
  - Linux (lsblk + parted + mkfs)
  - macOS (diskutil + hdiutil)
  - Android/Termux

### 🔧 Alterado

- Migração de `print()` para UI gráfica
- Formatação USB agora usa `diskpart` no Windows (mais confiável)
- Detecção USB via WMI (Windows) e `lsblk -J` (Linux)

### 🗑️ Removido

- CLI standalone (virou parte da GUI)
- Dependência de `tkinter.ttk.Notebook` (substituído por `NeonTabBar`)

---

## [2.0.0] — 2026-07-15

### ✨ Adicionado

- **Suporte a Linux** além de Windows
- **Detecção de pendrive** multiplataforma
- **Formatação multi-FS**: NTFS, FAT32, exFAT, ext4, ext3, ext2
- **Gravação via DD** bit-a-bit
- **Verificação de hash** pós-gravação (MD5, SHA1, SHA256, SHA512)
- **Download de distros** Linux

### 🔧 Alterado

- Substituído `wmic` (deprecated) por PowerShell CIM
- Melhor tratamento de erros de permissão

---

## [1.0.0] — 2026-07-01

### ✨ Adicionado

- **Versão inicial** do DarkPenBoot Pro
- Suporte básico a Windows
- Detecção de pendrives USB
- Formatação em NTFS/FAT32
- Gravação de ISO via 7-Zip

---

## 🔮 Roadmap Público

### v3.6.0 — Planejado para Q4 2026
- [ ] Publicar no PyPI (`pip install darkpenboot`)
- [ ] Publicar no Nixpkgs oficial
- [ ] Imagem Docker com Nix
- [ ] Suporte a Windows PE
- [ ] Múltiplos pendrives simultâneos

### v4.0.0 — Planejado para Q1 2027
- [ ] Reescrita da UI com **Tauri** (Rust + Web)
- [ ] Interface web via Flask/FastAPI
- [ ] Suporte a iOS (BeeWare)
- [ ] API REST para integração
- [ ] Sistema de plugins para distros

---

## 📊 Estatísticas do Projeto

| Versão | Data | Arquivos | Linhas | Downloads |
|--------|------|:--------:|:------:|:---------:|
| v3.5.0 | 2026-09-15 | 24 | ~15.000 | 0 |
| v3.4.0 | 2026-09-10 | 22 | ~14.500 | — |
| v3.3.0 | 2026-09-05 | 20 | ~13.500 | — |
| v3.2.0 | 2026-08-28 | 18 | ~12.000 | — |
| v3.1.0 | 2026-08-15 | 15 | ~10.000 | — |
| v3.0.0 | 2026-08-01 | 12 | ~8.000 | — |
| v2.0.0 | 2026-07-15 | 8 | ~4.000 | — |
| v1.0.0 | 2026-07-01 | 3 | ~1.500 | — |

---

## 🤝 Contribuidores

Agradecimentos a todos que contribuíram:

- **Adriano Rodrigues da Silva** ([@Avlis1412](https://github.com/Avlis1412)) — Criador e mantenedor

Quer aparecer aqui? Veja [CONTRIBUTING.md](CONTRIBUTING.md) para saber como contribuir!

---

## 📚 Links Relacionados

- [Repositório](https://github.com/Avlis1412/DarkPenBoot-Pro)
- [Issues](https://github.com/Avlis1412/DarkPenBoot-Pro/issues)
- [Pull Requests](https://github.com/Avlis1412/DarkPenBoot-Pro/pulls)
- [Releases](https://github.com/Avlis1412/DarkPenBoot-Pro/releases)
- [MIT License](LICENSE)

---

## 🟣 Inspiração NixOS

Este changelog segue a filosofia do NixOS de **documentar cada mudança** de forma clara e rastreável.

> "NixOS® é marca da NixOS Foundation (sem afiliação)."
> Referência: [nixos.org/governance](https://nixos.org/governance/)

---

**[⬆️ Voltar ao topo](#-changelog--darkpenboot-pro)**