# DarkPenBoot Pro

**Criador Profissional de Pendrives Bootaveis Universais**

Windows | Linux | macOS | Android (Termux) | OTG Mobile

![Versao](https://img.shields.io/badge/versao-3.6.1-blue)
![Python](https://img.shields.io/badge/python-3.8+-yellow)

**Autor:** Adriano Rodrigues da Silva
**GitHub:** [@Avlis1412](https://github.com/Avlis1412)

---

## Novidades v3.6.1 (2026-09-16)

### Adicionado
- Varredura shell universal: `_scan_shell_all_platforms()`
  - Windows: PowerShell + CIM (`Win32_DiskDrive`)
  - Linux/macOS: `lsblk -J` + fallback `/dev/sd*`
  - Termux/Android: `/storage`, `/mnt/media_rw`, `/dev/block/sd*`
- Constantes visuais v3.6.1: `GUI_TEXTURE_ENABLED`,
  `ORB_TRANSLUCENCY`, `ORB_GLASS_EDGE`, `LOGO_GLOW_ENABLED`
- Helpers de cor: `_blend_color`, `_rgb_tuple_to_hex`,
  `_lighten_hex`, `_darken_hex`

### Modificado
- `refresh_drives()` - pulso neon + oscilacao do orb
- `_do_identify()` - fallback shell se API falhar
- `_do_diskpart()` - revarredura se perder o alvo
- `_do_format_via_terminal()` - formata o FS do seletor
- `ClickableLogo._update_colors()` - glow + shadow

### Corrigido
- `SyntaxError` em `download_with_fallback`

---

## Estatisticas do projeto

Gerado automaticamente em 2026-09-16 por `deploy.py`.

| Metrica | Valor |
|---------|-------|
| Arquivos | 49 |
| Diretorios | 20 |
| Linhas totais | 20,183 |
| Tamanho total | 0.85 MB |
| Erros de sintaxe | 0 |

### Por extensao (top 8 por linhas)

| Ext | Arquivos | Linhas | Tamanho |
|-----|----------|--------|---------|
| `.py` | 16 | 14,030 | 595.9 KB |
| `.md` | 17 | 3,980 | 184.8 KB |
| `.nix` | 3 | 497 | 24.3 KB |
| `.ps1` | 2 | 401 | 15.8 KB |
| `.yml` | 2 | 368 | 14.0 KB |
| `.sh` | 1 | 305 | 12.0 KB |
| `.toml` | 1 | 240 | 10.6 KB |
| `(sem ext)` | 2 | 131 | 3.0 KB |

### Maiores arquivos

| Arquivo | Linhas | Tamanho |
|---------|--------|---------|
| `DarkPenBoot_PRO1.py` | 9,995 | 439.2 KB |
| `darkpenboot_kivy.py` | 1,984 | 78.6 KB |
| `DPB_Launcher.py` | 684 | 30.5 KB |
| `deploy.py` | 598 | 20.8 KB |
| `docs\ARQUITETURA.md` | 447 | 17.4 KB |
| `docs\NIXOS.md` | 421 | 12.7 KB |
| `CHANGELOG.md` | 387 | 11.7 KB |
| `.github\skills\speckit-checklist\SKILL.md` | 383 | 22.1 KB |
| `.github\skills\speckit-specify\SKILL.md` | 345 | 18.2 KB |
| `build.sh` | 305 | 12.0 KB |

---

## Recursos

| Recurso | Descricao |
|---------|-----------|
| Multi-FS | NTFS, FAT32, exFAT, ext4/3/2, JHFS+, APFS |
| 7 temas | Matrix, Crimson, Nord, Cyberpunk, Monokai, Light, Soft Dark |
| ~35 distros | Debian, Ubuntu, Fedora, Arch, NixOS, etc |
| Hashes | SHA256, SHA512, SHA1, MD5, SHA3-256, BLAKE2b |
| Downloads | Fallback curl -> wget -> urllib + mirrors |
| Recuperacao USB | Chkdsk, MBR rebuild, format FS |
| Mobile | Kivy + Buildozer (Android) |
| Soft Dark | Tema que reduz fadiga visual |

---

## Como usar

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Executar

```bash
python DarkPenBoot_PRO1.py
```

### 3. Build e deploy

```bash
python deploy.py --build      # compila .exe
python deploy.py --push       # commit + push
python deploy.py --all        # tudo
```
