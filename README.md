# 🚀 DarkPenBoot Pro

**Criador Profissional de Pendrives Bootaveis Universais**

Windows · Linux · macOS · Android (Termux) · OTG Mobile

![Versao](https://img.shields.io/badge/versao-3.6.1-blue)
![Python](https://img.shields.io/badge/python-3.8+-yellow)
![Plataformas](https://img.shields.io/badge/plataformas-Windows%20%7C%20Linux%20%7C%20macOS%20%7C%20Android-green)

**Autor:** Adriano Rodrigues da Silva
**GitHub:** [@Avlis1412](https://github.com/Avlis1412)

---

## 🆕 Novidades v3.6.1 (2026-09-16)

### Adicionado
- 🔍 **Varredura shell universal** — `_scan_shell_all_platforms()`
  - Windows: PowerShell + CIM (`Win32_DiskDrive`)
  - Linux/macOS: `lsblk -J` + fallback `/dev/sd*`
  - Termux/Android: `/storage`, `/mnt/media_rw`, `/dev/block/sd*`
- 🎨 Constantes visuais v3.6.1
- 🧮 Helpers de cor (`_blend_color`, `_lighten_hex`, `_darken_hex`)

### Modificado
- ♻️ `refresh_drives()` — pulso neon + oscilacao do orb
- ♻️ `_do_identify()` — fallback shell se API falhar
- ♻️ `_do_diskpart()` — revarredura se perder o alvo
- ♻️ `_do_format_via_terminal()` — formata o FS do seletor

### Corrigido
- 🐛 `SyntaxError` em `download_with_fallback`

---

## 📦 Executaveis Disponiveis

_Nenhuma versao compilada ainda. Rode `.\deploy.ps1 -Build`._

---

## 🎯 Recursos

| Recurso | Descricao |
|---------|-----------|
| 💿 Multi-FS | NTFS, FAT32, exFAT, ext4/3/2, JHFS+, APFS |
| 🎨 7 temas | Matrix, Crimson, Nord, Cyberpunk, Monokai, Light, Soft Dark |
| 🌐 ~35 distros | Debian, Ubuntu, Fedora, Arch, NixOS, etc |
| 🔐 Hashes | SHA256, SHA512, SHA1, MD5, SHA3-256, BLAKE2b |
| 📥 Downloads | Fallback curl → wget → urllib + mirrors |
| 🛠️ Recuperacao USB | Chkdsk, MBR rebuild, format FS |
| 📱 Mobile | Kivy + Buildozer (Android) |
| 🌙 Soft Dark | Tema que reduz fadiga visual |

---

## 🚀 Como usar

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Executar
```bash
python DarkPenBoot_PRO1.py
```

### 3. Build e deploy
```powershell
.\deploy.ps1 -Build      # compila EXE versionado
.\deploy.ps1             # só docs + push
```

