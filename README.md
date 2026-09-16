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

- **Varredura shell universal** - `_scan_shell_all_platforms()` detecta pendrives mesmo quando a API falha.
  - Windows: PowerShell + CIM (Win32_DiskDrive)
  - Linux/macOS: `lsblk -J` + fallback `/dev/sd*`
  - Termux/Android: `/storage`, `/mnt/media_rw`, `/dev/block/sd*`
- **Constantes visuais v3.6.1**:
  - `GUI_TEXTURE_ENABLED`, `ORB_TRANSLUCENCY`, `ORB_GLASS_EDGE`
  - `LOGO_GLOW_ENABLED`, `LOGO_SHADOW_ENABLED`
- **Helpers de cor**:
  - `_blend_color(rgb, bg_rgb, alpha)`
  - `_rgb_tuple_to_hex(rgb)`
  - `_lighten_hex(hex, amount)` / `_darken_hex(hex, amount)`

### Modificado

- `refresh_drives()` - Dispara pulso neon + oscilacao do orb
- `_do_identify()` - Fallback shell se API falhar
- `_do_diskpart()` - Revarredura se perder o alvo
- `_do_format_via_terminal()` - Formata o FS do seletor
- `ClickableLogo._update_colors()` - Glow + shadow

### Corrigido

- `SyntaxError` em `download_with_fallback` (`fnattempt_url` invalido)

### Estatisticas

| Item | Valor |
|------|-------|
| Linhas | ~9.763 |
| Patches | 7/10 |
| Python | 3.8+ |

---

# 🔌 DARKPENBOOT PRO

## Criador de Pendrives Bootáveis Multi-Plataforma

[![Version](https://img.shields.io/badge/version-3.5.0-blue?style=for-the-badge)](https://github.com/Avlis1412/DarkPenBoot-Pro/releases)
[![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-yellow?style=for-the-badge&logo=python)](https://www.python.org)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-purple?style=for-the-badge)
[![Build](https://github.com/Avlis1412/DarkPenBoot-Pro/actions/workflows/build.yml/badge.svg)](https://github.com/Avlis1412/DarkPenBoot-Pro/actions/workflows/build.yml)

Crie pendrives bootáveis de forma simples, rápida e segura.
Suporte a Windows, Linux, macOS, Android e NixOS — tudo em uma ferramenta.

Download • Recursos • Como Usar • NixOS • Build

---

## 📥 Download

| Plataforma | Arquivo | Link |
| :----------: | :-------: | :----: |
| 🪟 Windows | `DarkPenBoot.exe` | [⬇️ Baixar](https://github.com/Avlis1412/DarkPenBoot-Pro/releases/latest) |
| 🐧 Linux | `darkpenboot` (binário) | [⬇️ Baixar](https://github.com/Avlis1412/DarkPenBoot-Pro/releases/latest) |
| 🍏 macOS | `DarkPenBoot` (binário) | [⬇️ Baixar](https://github.com/Avlis1412/DarkPenBoot-Pro/releases/latest) |
| 📱 Android | `darkpenboot-*.apk` | [⬇️ Baixar](https://github.com/Avlis1412/DarkPenBoot-Pro/releases/latest) |

> 🔐 Cada download vem com arquivo `.sha256` para verificação.

### Verificação SHA256

```bash
# Linux/macOS
sha256sum -c darkpenboot.sha256

# Windows PowerShell
$esperado = (Get-Content DarkPenBoot.exe.sha256).Split()[0]
$calculado = (Get-FileHash DarkPenBoot.exe -Algorithm SHA256).Hash
if ($esperado -eq $calculado) { Write-Host "✅ Hash OK" -ForegroundColor Green }
```
