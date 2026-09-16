#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DarkPenBoot Pro - Analise + README + Build + Deploy
====================================================
Uso:
    python deploy.py              -> limpa + analisa + regenera README
    python deploy.py --build      -> + compila .exe
    python deploy.py --push       -> + commit + push
    python deploy.py --all        -> tudo
    python deploy.py --dry-run    -> simula (nao escreve nada)
    python deploy.py --no-clean   -> pula a fase de limpeza
"""
import sys, os, re, ast, shutil, subprocess, datetime
from pathlib import Path
from collections import defaultdict

# ---------------- CONFIG ----------------
VERSION = "3.6.1"
DATE = datetime.datetime.now().strftime("%Y-%m-%d")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
BRANCH = "main"
REMOTE = "origin"
MAIN_SCRIPT = "DarkPenBoot_PRO1.py"

DO_BUILD  = ("--build" in sys.argv) or ("--all" in sys.argv)
DO_PUSH   = ("--push"  in sys.argv) or ("--all" in sys.argv)
DRY_RUN   = "--dry-run" in sys.argv
NO_CLEAN  = "--no-clean" in sys.argv

# ---------------- HELPERS ----------------
def info(m): print("[INFO] " + m)
def ok(m):   print("[OK]   " + m)
def warn(m): print("[WARN] " + m)
def err(m):  print("[ERR]  " + m)

def head(m):
    print()
    print("=" * 62)
    print("  " + m)
    print("=" * 62)

def run(cmd, check=False, capture=False):
    if DRY_RUN:
        warn("[DRY]  " + " ".join(str(c) for c in cmd))
        return None
    if capture:
        return subprocess.run(cmd, capture_output=True, text=True)
    r = subprocess.run(cmd)
    if check and r.returncode != 0:
        err("Falhou: " + " ".join(str(c) for c in cmd))
        sys.exit(1)
    return r

def backup(p):
    p = Path(p)
    if p.exists() and not DRY_RUN:
        bak = p.with_suffix(p.suffix + ".bak_" + TS)
        shutil.copy2(p, bak)
        info("Backup: " + bak.name)

# ---------------- FILTROS ----------------
SKIP_DIRS = {
    ".git", "__pycache__", ".venv", "venv", "kivy_venv", "env",
    ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "build", "dist", "node_modules", ".idea", ".vscode",
    ".specify", ".launcher_profiles", "meu-projeto",
}
SKIP_SUFFIXES = (".egg-info",)
BINARY_EXTS = {
    ".pyc", ".pyo", ".exe", ".dll", ".so", ".dylib",
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".bmp", ".svg",
    ".zip", ".tar", ".gz", ".7z", ".rar",
    ".pdf", ".mp3", ".mp4", ".wav", ".ogg",
    ".db", ".sqlite", ".lock",
}

def should_skip_dir(name):
    if name in SKIP_DIRS:
        return True
    for s in SKIP_SUFFIXES:
        if name.endswith(s):
            return True
    return False

# ---------------- 0. LIMPEZA ----------------
TEMP_FILES = {
    "diag.py", "diag2.py",
    "fix_final.py", "fix_final_v361.py", "fix_tk_methods.py",
    "fix_rodape.py", "fix_pgup.py", "fix_p4_p7.py",
    "fix_remaining.ps1", "fix_remaining.py",
    "kivy_patcher_v361.py", "patcher_v360.py", "patcher_v361c.py",
    "update_docs_v361.py", "patcher_consolidado_v361.py",
    "project_tree.txt", "para_apagar.txt",
    ".launcher_config.json", ".launcher_log.txt",
}

def cleanup_backups(root):
    """Remove todos os *.bak_*, *.bak e *_BACKUP_*.py do projeto (recursivo)."""
    removed = []
    patterns = ("*.bak_*", "*.bak", "*_BACKUP_*.py")
    for pat in patterns:
        for f in root.rglob(pat):
            if not f.is_file():
                continue
            # nao apaga dentro de venv/.git
            parts = set(f.parts)
            if parts & {".git", "kivy_venv", "venv", ".venv"}:
                continue
            if DRY_RUN:
                removed.append(str(f.relative_to(root)))
                continue
            try:
                f.unlink()
                removed.append(str(f.relative_to(root)))
            except OSError:
                pass
    return removed

def cleanup_tempfiles(root):
    """Remove scripts temporarios conhecidos."""
    removed = []
    for name in TEMP_FILES:
        f = root / name
        if f.exists() and f.is_file():
            if DRY_RUN:
                removed.append(name)
                continue
            try:
                f.unlink()
                removed.append(name)
            except OSError:
                pass
    return removed

def fix_bom(root):
    """Remove BOM (U+FEFF) do inicio de arquivos .py."""
    fixed = []
    for p in root.rglob("*.py"):
        parts = set(p.parts)
        if parts & {".git", "kivy_venv", "venv", ".venv", "__pycache__"}:
            continue
        try:
            raw = p.read_bytes()
        except OSError:
            continue
        if raw.startswith(b"\xef\xbb\xbf"):
            if DRY_RUN:
                fixed.append(str(p.relative_to(root)))
                continue
            try:
                p.write_bytes(raw[3:])
                fixed.append(str(p.relative_to(root)))
            except OSError:
                pass
    return fixed

# ---------------- 1. ANALISE ----------------
def analyze_tree(root):
    stats = {
        "total_files": 0,
        "total_dirs": 0,
        "total_lines": 0,
        "total_bytes": 0,
        "by_ext": defaultdict(lambda: {"files": 0, "lines": 0, "bytes": 0}),
        "files": [],
    }

    def walk(path):
        try:
            entries = sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
        except (PermissionError, OSError):
            return
        for e in entries:
            if e.is_dir():
                if should_skip_dir(e.name):
                    continue
                stats["total_dirs"] += 1
                walk(e)
            else:
                if ".bak_" in e.name or e.name.endswith(".bak"):
                    continue
                stats["total_files"] += 1
                try:
                    size = e.stat().st_size
                except OSError:
                    size = 0
                stats["total_bytes"] += size
                ext = e.suffix.lower() or "(sem ext)"
                nlines = 0
                if ext not in BINARY_EXTS:
                    try:
                        with open(e, "r", encoding="utf-8", errors="ignore") as f:
                            nlines = sum(1 for _ in f)
                    except Exception:
                        nlines = 0
                stats["by_ext"][ext]["files"] += 1
                stats["by_ext"][ext]["lines"] += nlines
                stats["by_ext"][ext]["bytes"] += size
                stats["total_lines"] += nlines
                rel = str(e.relative_to(root))
                stats["files"].append((rel, size, nlines, ext))

    walk(root)
    return stats

def print_top_level(root):
    print()
    print("Diretorios de topo:")
    print("-" * 62)
    try:
        entries = sorted(root.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
    except OSError:
        return
    for e in entries:
        if e.is_dir():
            if should_skip_dir(e.name):
                continue
            try:
                n = sum(1 for x in e.rglob("*") if x.is_file())
            except OSError:
                n = 0
            print("  " + e.name + "/  (" + str(n) + " arquivos)")
        else:
            try:
                kb = e.stat().st_size / 1024
            except OSError:
                kb = 0
            print("  " + e.name + "  (" + ("%.1f" % kb) + " KB)")
    print("-" * 62)

def print_ext_stats(stats):
    print()
    print("Estatisticas por extensao:")
    print("-" * 62)
    print("  " + "Ext".ljust(12) + "Files".rjust(8) + "Lines".rjust(14) + "Size".rjust(14))
    ordered = sorted(stats["by_ext"].items(), key=lambda kv: kv[1]["lines"], reverse=True)
    for ext, s in ordered[:12]:
        kb = s["bytes"] / 1024
        print("  " + ext.ljust(12)
              + str(s["files"]).rjust(8)
              + ("{:,}".format(s["lines"])).rjust(14)
              + ("%.1f KB" % kb).rjust(14))
    print("-" * 62)

def print_biggest_files(stats):
    print()
    print("Top 10 arquivos por linhas:")
    print("-" * 62)
    top = sorted(stats["files"], key=lambda f: f[2], reverse=True)[:10]
    for rel, size, nlines, ext in top:
        kb = size / 1024
        print("  " + ("{:,}".format(nlines)).rjust(8) + " linhas  "
              + ("%.1f KB" % kb).rjust(10) + "  " + rel)
    print("-" * 62)

# ---------------- 2. DIAGNOSTICO ----------------
def diagnose_python(root, rels):
    print()
    print("Diagnostico de sintaxe Python:")
    print("-" * 62)
    py_files = [r for r in rels if r.endswith(".py")]
    errors = 0
    for rel in py_files:
        full = root / rel
        try:
            src = full.read_text(encoding="utf-8", errors="ignore")
            ast.parse(src, filename=str(full))
        except SyntaxError as e:
            errors += 1
            print("  [ERR] " + rel + ": linha " + str(e.lineno) + " - " + str(e.msg))
        except Exception as e:
            print("  [WARN] " + rel + ": " + str(e))
    if errors == 0:
        print("  [OK]  " + str(len(py_files)) + " arquivos Python - sintaxe OK")
    else:
        print("  " + str(errors) + " arquivo(s) com erro de sintaxe")
    print("-" * 62)
    return errors

# ---------------- 3. README ----------------
def build_readme(stats, diag_errors, root):
    total_files = stats["total_files"]
    total_dirs = stats["total_dirs"]
    total_lines = stats["total_lines"]
    mb = stats["total_bytes"] / (1024 * 1024)

    top_exts = sorted(stats["by_ext"].items(), key=lambda kv: kv[1]["lines"], reverse=True)[:8]
    top_files = sorted(stats["files"], key=lambda f: f[2], reverse=True)[:10]

    L = []
    L.append("# DarkPenBoot Pro")
    L.append("")
    L.append("**Criador Profissional de Pendrives Bootaveis Universais**")
    L.append("")
    L.append("Windows | Linux | macOS | Android (Termux) | OTG Mobile")
    L.append("")
    L.append("![Versao](https://img.shields.io/badge/versao-" + VERSION + "-blue)")
    L.append("![Python](https://img.shields.io/badge/python-3.8+-yellow)")
    L.append("")
    L.append("**Autor:** Adriano Rodrigues da Silva")
    L.append("**GitHub:** [@Avlis1412](https://github.com/Avlis1412)")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Novidades v" + VERSION + " (" + DATE + ")")
    L.append("")
    L.append("### Adicionado")
    L.append("- Varredura shell universal: `_scan_shell_all_platforms()`")
    L.append("  - Windows: PowerShell + CIM (`Win32_DiskDrive`)")
    L.append("  - Linux/macOS: `lsblk -J` + fallback `/dev/sd*`")
    L.append("  - Termux/Android: `/storage`, `/mnt/media_rw`, `/dev/block/sd*`")
    L.append("- Constantes visuais v3.6.1: `GUI_TEXTURE_ENABLED`,")
    L.append("  `ORB_TRANSLUCENCY`, `ORB_GLASS_EDGE`, `LOGO_GLOW_ENABLED`")
    L.append("- Helpers de cor: `_blend_color`, `_rgb_tuple_to_hex`,")
    L.append("  `_lighten_hex`, `_darken_hex`")
    L.append("")
    L.append("### Modificado")
    L.append("- `refresh_drives()` - pulso neon + oscilacao do orb")
    L.append("- `_do_identify()` - fallback shell se API falhar")
    L.append("- `_do_diskpart()` - revarredura se perder o alvo")
    L.append("- `_do_format_via_terminal()` - formata o FS do seletor")
    L.append("- `ClickableLogo._update_colors()` - glow + shadow")
    L.append("")
    L.append("### Corrigido")
    L.append("- `SyntaxError` em `download_with_fallback`")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Estatisticas do projeto")
    L.append("")
    L.append("Gerado automaticamente em " + DATE + " por `deploy.py`.")
    L.append("")
    L.append("| Metrica | Valor |")
    L.append("|---------|-------|")
    L.append("| Arquivos | " + str(total_files) + " |")
    L.append("| Diretorios | " + str(total_dirs) + " |")
    L.append("| Linhas totais | " + "{:,}".format(total_lines) + " |")
    L.append("| Tamanho total | " + ("%.2f MB" % mb) + " |")
    L.append("| Erros de sintaxe | " + str(diag_errors) + " |")
    L.append("")
    L.append("### Por extensao (top 8 por linhas)")
    L.append("")
    L.append("| Ext | Arquivos | Linhas | Tamanho |")
    L.append("|-----|----------|--------|---------|")
    for ext, s in top_exts:
        kb = s["bytes"] / 1024
        L.append("| `" + ext + "` | " + str(s["files"]) + " | "
                 + "{:,}".format(s["lines"]) + " | " + ("%.1f KB" % kb) + " |")
    L.append("")
    L.append("### Maiores arquivos")
    L.append("")
    L.append("| Arquivo | Linhas | Tamanho |")
    L.append("|---------|--------|---------|")
    for rel, size, nlines, ext in top_files:
        kb = size / 1024
        L.append("| `" + rel + "` | " + "{:,}".format(nlines) + " | "
                 + ("%.1f KB" % kb) + " |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Recursos")
    L.append("")
    L.append("| Recurso | Descricao |")
    L.append("|---------|-----------|")
    L.append("| Multi-FS | NTFS, FAT32, exFAT, ext4/3/2, JHFS+, APFS |")
    L.append("| 7 temas | Matrix, Crimson, Nord, Cyberpunk, Monokai, Light, Soft Dark |")
    L.append("| ~35 distros | Debian, Ubuntu, Fedora, Arch, NixOS, etc |")
    L.append("| Hashes | SHA256, SHA512, SHA1, MD5, SHA3-256, BLAKE2b |")
    L.append("| Downloads | Fallback curl -> wget -> urllib + mirrors |")
    L.append("| Recuperacao USB | Chkdsk, MBR rebuild, format FS |")
    L.append("| Mobile | Kivy + Buildozer (Android) |")
    L.append("| Soft Dark | Tema que reduz fadiga visual |")
    L.append("")
    L.append("---")
    L.append("")
    L.append("## Como usar")
    L.append("")
    L.append("### 1. Instalar dependencias")
    L.append("")
    L.append("```bash")
    L.append("pip install -r requirements.txt")
    L.append("```")
    L.append("")
    L.append("### 2. Executar")
    L.append("")
    L.append("```bash")
    L.append("python " + MAIN_SCRIPT)
    L.append("```")
    L.append("")
    L.append("### 3. Build e deploy")
    L.append("")
    L.append("```bash")
    L.append("python deploy.py --build      # compila .exe")
    L.append("python deploy.py --push       # commit + push")
    L.append("python deploy.py --all        # tudo")
    L.append("```")
    L.append("")
    return "\n".join(L)

def write_readme(root, new_content):
    p = root / "README.md"
    old = ""
    if p.exists():
        old = p.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"##\s+.*Vers[oõ]es\s+Anteriores.*", old, re.IGNORECASE)
    if m:
        final = new_content + "\n\n---\n\n" + old[m.start():]
    else:
        final = new_content
    if not DRY_RUN:
        p.write_text(final, encoding="utf-8")
    return len(final.splitlines())

# ---------------- 4. BUILD ----------------
def build_exe(root):
    head("[BUILD] Compilando executaveis")
    r = subprocess.run([sys.executable, "-m", "pip", "show", "pyinstaller"],
                       capture_output=True, text=True)
    if "Name: pyinstaller" not in r.stdout:
        warn("PyInstaller nao instalado. Instalando...")
        run([sys.executable, "-m", "pip", "install", "pyinstaller"])

    for d in ["build", "dist"]:
        full = root / d
        if full.exists() and not DRY_RUN:
            shutil.rmtree(full, ignore_errors=True)
            info("Removido: " + d + "/")

    spec = root / "DarkPenBoot.spec"
    if spec.exists():
        info("Usando DarkPenBoot.spec")
        run(["pyinstaller", "--clean", "--noconfirm", "DarkPenBoot.spec"])
    else:
        info("Criando build automatico")
        cmd = ["pyinstaller", "--onefile", "--windowed",
               "--name", "DarkPenBoot_PRO_" + VERSION]
        icon = root / "assets" / "icon.ico"
        if icon.exists():
            cmd.append("--icon=" + str(icon))
        cmd.append(str(root / MAIN_SCRIPT))
        run(cmd)

    dist = root / "dist"
    if dist.exists() and not DRY_RUN:
        for f in dist.iterdir():
            if f.is_file():
                mb = f.stat().st_size / (1024 * 1024)
                ok("Artefato: " + f.name + " (" + ("%.2f MB" % mb) + ")")

# ---------------- 5. GIT ----------------
def git_deploy(root, do_build):
    head("[GIT] Commit e push")

    if not (root / ".git").exists():
        warn(".git nao encontrado - pulando")
        return

    # 1. Adiciona modificados/deletados JA rastreados
    run(["git", "add", "-u"])

    # 2. Adiciona novos arquivos
    files = ["README.md", "deploy.py"]
    for f in ["CHANGELOG.md", "pyproject.toml", "README_BUILD.md"]:
        if (root / f).exists():
            files.append(f)
    for f in files:
        if (root / f).exists():
            run(["git", "add", f])

    # 3. Forca o .exe (ignorado pelo .gitignore)
    if do_build and (root / "dist").exists():
        for exe in (root / "dist").glob("*.exe"):
            info("Force add (ignorado pelo .gitignore): " + exe.name)
            run(["git", "add", "-f", str(exe)])

    msg_lines = [
        "docs(v" + VERSION + "): limpeza + analise + README + build",
        "",
        "- limpeza: backups .bak_*, temporarios, BOM corrigido",
        "- README.md: estatisticas reais do projeto",
        "- deploy.py: pipeline + limpeza + BOM fix + build",
    ]
    if do_build:
        msg_lines.append("- dist/: executavel recompilado")
    msg_lines.append("")
    msg_lines.append("Data: " + DATE)
    msg = "\n".join(msg_lines)

    if DRY_RUN:
        warn("[DRY] git commit -m <msg>")
        warn("[DRY] git push " + REMOTE + " " + BRANCH)
        return

    r = subprocess.run(["git", "diff", "--cached", "--quiet"])
    if r.returncode == 0:
        warn("Nada para commitar")
    else:
        run(["git", "commit", "-m", msg])
        ok("Commit realizado")

    r = subprocess.run(["git", "push", REMOTE, BRANCH])
    if r.returncode == 0:
        ok("Push concluido")
    else:
        warn("Push falhou - verifique credenciais")

# ---------------- MAIN ----------------
def main():
    root = Path.cwd()

    head("DARKPENBOOT PRO - ANALISE + README + BUILD + DEPLOY v" + VERSION)
    print("  CWD:    " + str(root))
    print("  Data:   " + DATE)
    print("  Build:  " + ("sim" if DO_BUILD else "nao"))
    print("  Push:   " + ("sim" if DO_PUSH else "nao"))
    print("  DryRun: " + ("sim" if DRY_RUN else "nao"))
    print("  Limpar: " + ("nao" if NO_CLEAN else "sim"))

    if not (root / MAIN_SCRIPT).exists():
        err(MAIN_SCRIPT + " nao encontrado em " + str(root))
        sys.exit(1)

    # 0. LIMPEZA
    if NO_CLEAN:
        head("[0/5] LIMPEZA - Ignorada (--no-clean)")
    else:
        head("[0/5] LIMPEZA - Backups, temporarios e BOM")

        baks = cleanup_backups(root)
        if baks:
            ok(str(len(baks)) + " backups removidos:")
            for b in baks[:25]:
                print("     - " + b)
            if len(baks) > 25:
                print("     ... + " + str(len(baks) - 25) + " outros")
        else:
            info("Nenhum backup encontrado")

        temps = cleanup_tempfiles(root)
        if temps:
            ok(str(len(temps)) + " temporarios removidos:")
            for t in temps:
                print("     - " + t)
        else:
            info("Nenhum temporario encontrado")

        boms = fix_bom(root)
        if boms:
            ok(str(len(boms)) + " BOM (U+FEFF) corrigidos:")
            for b in boms:
                print("     - " + b)
        else:
            info("Nenhum BOM encontrado")

    # 1. ANALISE
    head("[1/5] ANALISE - Varredura de diretorios e arquivos")
    stats = analyze_tree(root)
    ok(str(stats["total_files"]) + " arquivos, " + str(stats["total_dirs"]) + " diretorios")
    ok("{:,}".format(stats["total_lines"]) + " linhas, "
       + ("%.2f MB" % (stats["total_bytes"] / (1024 * 1024))))
    print_top_level(root)
    print_ext_stats(stats)
    print_biggest_files(stats)

    # 2. DIAG
    head("[2/5] DIAG - Verificacao de teor (sintaxe Python)")
    diag_errors = diagnose_python(root, [f[0] for f in stats["files"]])

    # 3. README
    head("[3/5] README - Geracao com estatisticas reais")
    content = build_readme(stats, diag_errors, root)
    nlines = write_readme(root, content)
    ok("README.md regenerado (" + str(nlines) + " linhas)")

    # 4. BUILD
    if DO_BUILD:
        build_exe(root)
    else:
        head("[4/5] BUILD - Ignorado (use --build ou --all)")

    # 5. GIT
    if DO_PUSH:
        git_deploy(root, DO_BUILD)
    else:
        head("[5/5] GIT - Ignorado (use --push ou --all)")

    head("OK - Pipeline concluido")
    print("  Proximos passos:")
    print("    python deploy.py --build   # compilar .exe")
    print("    python deploy.py --push    # commit + push")
    print("    python deploy.py --all     # tudo de uma vez")
    print("    python deploy.py --no-clean # pular limpeza")
    print()

if __name__ == "__main__":
    main()