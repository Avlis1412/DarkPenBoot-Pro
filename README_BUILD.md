# Build - DarkPenBoot Pro v3.6.1

> Atualizado em 2026-09-16

# 🏗️ Guia de Build — DarkPenBoot Pro

Este documento explica **como gerar os executáveis** do DarkPenBoot Pro
para todas as plataformas suportadas.

---

## 📋 Índice

- Filosofia NixOS
- Métodos de Build
- Requisitos por Plataforma
- Build Linux
- Build macOS
- Build Windows
- Build Android
- Build via Nix
- Verificação SHA256
- Troubleshooting

---

## 🟣 Filosofia NixOS

O build deste projeto segue princípios do **NixOS**:

- 🔄 **Reprodutibilidade** — mesmo código, mesmo binário
- 🔒 **Isolamento** — cada build em ambiente limpo
- 📦 **Declaratividade** — tudo explícito em arquivos `.yml` e `.nix`
- ✅ **Verificabilidade** — SHA256 de cada artefato

> **NixOS®** é marca registrada da **NixOS Foundation**.
> Este projeto **NÃO** é afiliado à NixOS Foundation.

---

## 🚀 Métodos de Build

| Método | Quando usar | Vantagem |
| -------- | ------------- | ---------- |
| 🎯 **GitHub Actions** | Sempre que possível | Zero config local, 4 plataformas em paralelo |
| 🔧 **Build local** | Durante desenvolvimento | Rápido, sem esperar fila |
| ❄️ **Nix** | Máxima reprodutibilidade | Hash garante mesmo output |

---

## 💻 Requisitos por Plataforma

### **Requisitos mínimos comuns**

| Ferramenta | Versão mínima | Como verificar |
| ------------ | :-------------: | ---------------- |
| Python | 3.9+ | `python --version` |
| Git | 2.30+ | `git --version` |

### **Requisitos específicos**

| Plataforma | Adicional |
| ------------ | ----------- |
| 🪟 **Windows** | PowerShell 5.1+, PyInstaller |
| 🐧 **Linux** | `python3-tk`, `p7zip-full`, `parted` |
| 🍏 **macOS** | Xcode Command Line Tools |
| 📱 **Android** | JDK 17, Buildozer, Cython |
| ❄️ **Nix** | Nix 2.18+, flakes habilitados |

---

## 🐧 Build Linux

### **Passo 1 — Instalar dependências**

**Ubuntu/Debian:**

```bash
sudo apt update
sudo apt install -y \
    python3 python3-pip python3-tk \
    p7zip-full curl wget file \
    git make
```
