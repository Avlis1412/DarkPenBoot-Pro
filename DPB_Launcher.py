#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════╗
║   DARKPENBOOT PRO — LAUNCHER MULTI-VERSÃO v1.0              ║
║                                                              ║
║   • Seleciona entre as 3 versões do DarkPenBoot Pro          ║
║   • v3.4.0 é a ★ PRINCIPAL — o resto é DEMO                  ║
║   • Motor de processamento assíncrono (fila + workers)       ║
║   • Bloco dedicado de refinamento das 3 GUIs                 ║
║   • Independência total: subprocesso por versão              ║
║                                                              ║
║   Uso:   python DPB_Launcher.py                              ║
║   Autor: Adriano Rodrigues da Silva                          ║
╚══════════════════════════════════════════════════════════════╝
"""
from __future__ import annotations
import os
import sys
import re
import json
import time
import queue
import shutil
import subprocess
import threading
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ══════════════════════════════════════════════════════════════
# 1. CONSTANTES DO LAUNCHER
# ══════════════════════════════════════════════════════════════
LAUNCHER_VERSION = "1.0.1"
LAUNCHER_TITLE   = "🔌 DarkPenBoot Pro — Launcher Multi-Versão"
LAUNCHER_DIR     = Path(__file__).resolve().parent
LAUNCHER_CFG     = LAUNCHER_DIR / ".launcher_config.json"
LAUNCHER_LOG     = LAUNCHER_DIR / ".launcher_log.txt"
PROFILE_DIR      = LAUNCHER_DIR / ".launcher_profiles"

IS_WINDOWS = sys.platform.startswith("win")
CREATE_NEW_CONSOLE = 0x00000010 if IS_WINDOWS else 0

# ══════════════════════════════════════════════════════════════
# 2. REGISTRO DE VERSÕES (ordem importa — v3.4.0 primeiro)
# ══════════════════════════════════════════════════════════════
VERSION_REGISTRY: list[dict] = [
    {
        "id": "v340_star",
        "file": "DarkPenBoot_PRO1.py.v340.bak",
        "name": "★ DarkPenBoot v3.4.0 — PRINCIPAL",
        "short": "v3.4.0",
        "type": "principal",
        "declared_version": "3.4.0",
        "description": ("Versão carro-chefe. Tema Soft Dark, "
                        "NixOS 24.11/25.05, PREMIUM, SHA256."),
        "accent": "#00ff41",
        "badge": "★ PRINCIPAL",
    },
    {
        "id": "v340_pre20C",
        "file": "DarkPenBoot_PRO1.py.before_fix20C.bak",
        "name": "DarkPenBoot v3.4.0 (pré-fix 20C)",
        "short": "v3.4.0-pre",
        "type": "demo",
        "declared_version": "3.4.0-pre",
        "description": "Snapshot antes do fix 20C. Uso demonstrativo.",
        "accent": "#ffaa00",
        "badge": "DEMO",
    },
    {
        "id": "v351_canonical",
        "file": "DarkPenBoot_PRO1.py",
        "name": "DarkPenBoot v3.5.1 — CANÔNICO",
        "short": "v3.5.1",
        "type": "canonical",
        "declared_version": "3.5.1",
        "description": ("Código atual com motor de busca, 16 distros, "
                        "ToolTip corrigido e rodapé reorganizado."),
        "accent": "#00ccff",
        "badge": "CANÔNICO",
    },
]

# ══════════════════════════════════════════════════════════════
# 3. BLOCO DE REFINAMENTO DAS 3 INTERFACES GRÁFICAS
# ══════════════════════════════════════════════════════════════
VERSION_GUI_REFINEMENTS: dict[str, dict] = {
    "v340_star": {
        "theme": "soft_dark",
        "window_geometry": "480x820",
        "log_level": "Detalhado",
        "force_fsync": True,
        "leave_raw_dd": False,
        "buffer_override": "Auto (por tier USB)",
        "extra_env": {"DARKPENBOOT_PROFILE": "principal"},
    },
    "v340_pre20C": {
        "theme": "matrix",
        "window_geometry": "520x860",
        "log_level": "Debug",
        "force_fsync": False,
        "leave_raw_dd": True,
        "buffer_override": "16 MB",
        "extra_env": {"DARKPENBOOT_PROFILE": "demo-pre20c"},
    },
    "v351_canonical": {
        "theme": "cyberpunk",
        "window_geometry": "500x840",
        "log_level": "Detalhado",
        "force_fsync": True,
        "leave_raw_dd": False,
        "buffer_override": "Auto (por tier USB)",
        "extra_env": {"DARKPENBOOT_PROFILE": "canonical"},
    },
}

# ══════════════════════════════════════════════════════════════
# 4. CORES / ESTILO DO LAUNCHER
# ══════════════════════════════════════════════════════════════
C_BG        = "#0d0f14"
C_FRAME     = "#161a22"
C_BORDER    = "#232a36"
C_FG        = "#cdd6f4"
C_MUTED     = "#7a8390"
C_ACCENT    = "#89b4fa"
C_OK        = "#a6e3a1"
C_WARN      = "#f9e2af"
C_ERR       = "#f38ba8"
C_CARD      = "#1b2029"
C_CARD_SEL  = "#252c38"

# ══════════════════════════════════════════════════════════════
# 5. SCANNER DE METADADOS
# ══════════════════════════════════════════════════════════════
def scan_version_file(path: Path) -> dict:
    info = {
        "exists": False, "size": 0, "lines": 0,
        "app_version": "?", "has_motor": False,
        "has_16mirrors": False, "has_tooltip_fix": False,
        "has_duplication": False, "modified": "—",
    }
    if not path.exists():
        return info
    info["exists"] = True
    try:
        st = path.stat()
        info["size"] = st.st_size
        info["modified"] = datetime.fromtimestamp(
            st.st_mtime).strftime("%d/%m/%Y %H:%M")
        txt = path.read_text(encoding="utf-8", errors="replace")
        info["lines"] = txt.count("\n") + 1
        m = re.search(r'APP_VERSION\s*=\s*"([^"]+)"', txt)
        if m:
            info["app_version"] = m.group(1)
        info["has_motor"]       = ("_search_distros" in txt
                                    or "_resolve_latest_url" in txt)
        info["has_16mirrors"]   = ("mirror.ufscar.br" in txt
                                    and "mirrors.kernel.org" in txt)
        info["has_tooltip_fix"] = ("raw_text = (self.text_getter() if callable"
                                    in txt)
        info["has_duplication"] = (txt.count("# 13. ESCRITA DD") >= 2)
    except Exception:
        pass
    return info


# ══════════════════════════════════════════════════════════════
# 6. MOTOR DE PROCESSAMENTO — FILA ASSÍNCRONA
# ══════════════════════════════════════════════════════════════
class ProcessingEngine:
    def __init__(self):
        self._q: queue.Queue = queue.Queue()
        self._stop = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def submit(self, func, *args, **kwargs):
        self._q.put((func, args, kwargs))

    def _run(self):
        while not self._stop.is_set():
            try:
                func, args, kwargs = self._q.get(timeout=0.4)
            except queue.Empty:
                continue
            try:
                func(*args, **kwargs)
            except Exception as e:
                print(f"[ENGINE] job falhou: {e}", file=sys.stderr)
            finally:
                self._q.task_done()

    def stop(self):
        self._stop.set()


# ══════════════════════════════════════════════════════════════
# 7. CARD DE VERSÃO
# ══════════════════════════════════════════════════════════════
class VersionCard(tk.Frame):
    def __init__(self, parent, version: dict, on_click):
        super().__init__(parent, bg=C_CARD, highlightthickness=2,
                         highlightbackground=C_BORDER,
                         highlightcolor=version["accent"],
                         cursor="hand2")
        self.version = version
        self.on_click = on_click
        self.selected = False
        self._build()
        self._bind_all(self)

    def _build(self):
        v = self.version
        pad = 14

        top = tk.Frame(self, bg=C_CARD)
        top.pack(fill=tk.X, padx=pad, pady=(pad, 4))
        self.badge_lbl = tk.Label(top, text=v["badge"],
                                   font=("Segoe UI", 8, "bold"),
                                   fg=C_BG, bg=v["accent"],
                                   padx=6, pady=2)
        self.badge_lbl.pack(side=tk.LEFT)
        self.short_lbl = tk.Label(top, text=v["short"],
                                   font=("Consolas", 9, "bold"),
                                   fg=v["accent"], bg=C_CARD)
        self.short_lbl.pack(side=tk.RIGHT)

        self.title_lbl = tk.Label(self, text=v["name"],
                                   font=("Segoe UI", 11, "bold"),
                                   fg=C_FG, bg=C_CARD,
                                   anchor="w", justify=tk.LEFT,
                                   wraplength=260)
        self.title_lbl.pack(fill=tk.X, padx=pad, pady=(2, 4))

        self.desc_lbl = tk.Label(self, text=v["description"],
                                  font=("Segoe UI", 8),
                                  fg=C_MUTED, bg=C_CARD,
                                  anchor="w", justify=tk.LEFT,
                                  wraplength=260)
        self.desc_lbl.pack(fill=tk.X, padx=pad, pady=(0, 8))

        self.status_lbl = tk.Label(self, text="⏳ escaneando…",
                                    font=("Consolas", 8),
                                    fg=C_MUTED, bg=C_CARD,
                                    anchor="w", justify=tk.LEFT,
                                    wraplength=260)
        self.status_lbl.pack(fill=tk.X, padx=pad, pady=(0, pad))

    def update_meta(self, info: dict):
        if not info["exists"]:
            self.status_lbl.config(text="❌ arquivo ausente", fg=C_ERR)
            return
        bits = [
            f"📄 {info['lines']:,} linhas".replace(",", "."),
            f"📏 {info['size']/1024:.0f} KB",
            f"🏷️ v{info['app_version']}",
        ]
        flags = []
        if info.get("has_motor"):       flags.append("🔍 motor")
        if info.get("has_16mirrors"):   flags.append("🌐 16+ mirrors")
        if info.get("has_tooltip_fix"): flags.append("🛠️ fix ToolTip")
        if info.get("has_duplication"): flags.append("⚠️ duplicatas")
        line2 = " ".join(flags) if flags else "—"
        self.status_lbl.config(
            text=" · ".join(bits) + "\n" + line2,
            fg=C_OK if not info.get("has_duplication") else C_WARN,
        )

    def set_selected(self, sel: bool):
        self.selected = sel
        bg = C_CARD_SEL if sel else C_CARD
        self.configure(
            bg=bg,
            highlightbackground=self.version["accent"] if sel else C_BORDER,
            highlightthickness=2 if sel else 1)
        for w in (self.badge_lbl, self.short_lbl, self.title_lbl,
                  self.desc_lbl, self.status_lbl):
            try:
                w.configure(bg=bg)
            except Exception:
                pass

    def _bind_all(self, widget):
        widget.bind("<Button-1>", lambda e: self.on_click(self.version))
        for child in widget.winfo_children():
            child.bind("<Button-1>",
                        lambda e: self.on_click(self.version))
            if child.winfo_children():
                for sub in child.winfo_children():
                    sub.bind("<Button-1>",
                             lambda e: self.on_click(self.version))


# ══════════════════════════════════════════════════════════════
# 8. APLICAÇÃO PRINCIPAL
# ══════════════════════════════════════════════════════════════
class LauncherApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(f"{LAUNCHER_TITLE} v{LAUNCHER_VERSION}")
        self.root.configure(bg=C_BG)
        self.root.geometry("900x640")
        self.root.minsize(820, 560)

        self.engine = ProcessingEngine()
        self.version_meta: dict[str, dict] = {}
        self.cards: dict[str, VersionCard] = {}
        self.selected_id: str | None = None
        self.active_process = None
        self.proc_monitor_id = None

        self._style_ttk()
        self._build_ui()
        self._restore_geometry()

        # Scan inicial assíncrono
        self.engine.submit(self._scan_all)

        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

    # ─────────────────────────────────────────────────────
    def _style_ttk(self):
        s = ttk.Style()
        try:
            s.theme_use("clam")
        except Exception:
            pass
        s.configure("Vertical.TScrollbar",
                    background=C_FRAME, troughcolor=C_BG,
                    bordercolor=C_BORDER, arrowcolor=C_ACCENT,
                    gripcount=0, relief="flat")

    # ─────────────────────────────────────────────────────
    def _build_ui(self):
        # HEADER
        header = tk.Frame(self.root, bg=C_BG)
        header.pack(fill=tk.X, padx=18, pady=(14, 6))
        tk.Label(header, text="🔌", font=("Segoe UI Emoji", 22, "bold"),
                 fg=C_ACCENT, bg=C_BG).pack(side=tk.LEFT)
        tk.Label(header, text="DarkPenBoot Launcher",
                 font=("Segoe UI", 15, "bold"),
                 fg=C_FG, bg=C_BG).pack(side=tk.LEFT, padx=(8, 0))
        tk.Label(header, text=f"  v{LAUNCHER_VERSION}",
                 font=("Segoe UI", 9),
                 fg=C_MUTED, bg=C_BG).pack(side=tk.LEFT)
        tk.Label(header, text="★ Principal: v3.4.0",
                 font=("Segoe UI", 9, "italic"),
                 fg="#00ff41", bg=C_BG).pack(side=tk.RIGHT)

        # CARDS
        cards_wrap = tk.Frame(self.root, bg=C_BG)
        cards_wrap.pack(fill=tk.X, padx=14, pady=6)
        for i in range(len(VERSION_REGISTRY)):
            cards_wrap.columnconfigure(i, weight=1, uniform="cards")

        for idx, v in enumerate(VERSION_REGISTRY):
            card = VersionCard(cards_wrap, v, self._on_select)
            card.grid(row=0, column=idx, sticky="nsew", padx=6, pady=6)
            self.cards[v["id"]] = card

        # SEPARADOR
        sep = tk.Frame(self.root, bg=C_BORDER, height=1)
        sep.pack(fill=tk.X, padx=18, pady=(10, 4))

        # PAINEL DE DETALHES
        details = tk.Frame(self.root, bg=C_FRAME,
                           highlightthickness=1,
                           highlightbackground=C_BORDER)
        details.pack(fill=tk.X, padx=18, pady=4)
        inner = tk.Frame(details, bg=C_FRAME)
        inner.pack(fill=tk.X, padx=14, pady=10)

        self.details_title = tk.Label(
            inner, text="—", font=("Segoe UI", 11, "bold"),
            fg=C_FG, bg=C_FRAME, anchor="w")
        self.details_title.pack(fill=tk.X)
        self.details_sub = tk.Label(
            inner, text="—", font=("Consolas", 9),
            fg=C_MUTED, bg=C_FRAME, anchor="w", justify=tk.LEFT)
        self.details_sub.pack(fill=tk.X, pady=(4, 0))

        # BOTÕES DE AÇÃO
        actions = tk.Frame(self.root, bg=C_BG)
        actions.pack(fill=tk.X, padx=18, pady=(8, 4))
        for c in range(5):
            actions.columnconfigure(c, weight=1)

        self.btn_launch = self._mk_button(
            actions, "🚀  LANÇAR", self._launch_selected,
            bg=C_ACCENT, fg=C_BG, col=0)
        self.btn_admin = self._mk_button(
            actions, "🛡️  LANÇAR (Admin)", self._launch_admin,
            bg="#cba6f7", fg=C_BG, col=1)
        self.btn_refresh = self._mk_button(
            actions, "🔄  REFAZER SCAN", self._scan_async,
            bg=C_CARD, fg=C_FG, col=2)
        self.btn_folder = self._mk_button(
            actions, "📂  ABRIR PASTA", self._open_folder,
            bg=C_CARD, fg=C_FG, col=3)
        self.btn_stop = self._mk_button(
            actions, "⏹️  PARAR", self._stop_active,
            bg="#8c4451", fg=C_FG, col=4)

        # LOG
        logwrap = tk.Frame(self.root, bg=C_FRAME,
                           highlightthickness=1,
                           highlightbackground=C_BORDER)
        logwrap.pack(fill=tk.BOTH, expand=True, padx=18, pady=(8, 14))
        tk.Label(logwrap, text=" 📋 LOG DO LAUNCHER ",
                 font=("Segoe UI", 9, "bold"),
                 fg=C_ACCENT, bg=C_FRAME).pack(anchor="w",
                                                padx=10, pady=(6, 0))
        tf = tk.Frame(logwrap, bg=C_FRAME)
        tf.pack(fill=tk.BOTH, expand=True, padx=10, pady=(4, 10))
        tf.columnconfigure(0, weight=1)
        tf.rowconfigure(0, weight=1)
        self.log_text = tk.Text(
            tf, bg="#0a0c10", fg=C_FG,
            font=("Consolas", 8), wrap=tk.WORD,
            relief=tk.FLAT, bd=0, height=8,
            insertbackground=C_ACCENT)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        sb = ttk.Scrollbar(tf, orient=tk.VERTICAL,
                            command=self.log_text.yview,
                            style="Vertical.TScrollbar")
        sb.grid(row=0, column=1, sticky="ns")
        self.log_text.configure(yscrollcommand=sb.set)
        self.log_text.tag_config("err",  foreground=C_ERR)
        self.log_text.tag_config("warn", foreground=C_WARN)
        self.log_text.tag_config("ok",   foreground=C_OK)
        self.log_text.tag_config("info", foreground=C_ACCENT)
        self.log_text.configure(state="disabled")

        self.status_bar = tk.Label(
            self.root, text="Pronto.",
            font=("Segoe UI", 8), fg=C_MUTED,
            bg=C_BG, anchor="w")
        self.status_bar.pack(fill=tk.X, padx=20, pady=(0, 8))

        # ★ SELEÇÃO INICIAL — AQUI (após TODOS os widgets existirem)
        self._on_select(VERSION_REGISTRY[0])

    # ─────────────────────────────────────────────────────
    def _mk_button(self, parent, text, cmd, bg, fg, col):
        b = tk.Button(parent, text=text, command=cmd,
                      bg=bg, fg=fg, font=("Segoe UI", 10, "bold"),
                      relief=tk.FLAT, bd=0, cursor="hand2",
                      activebackground=C_ACCENT,
                      activeforeground=C_BG,
                      padx=10, pady=8)
        b.grid(row=0, column=col, padx=4, sticky="ew")
        return b

    # ─────────────────────────────────────────────────────
    def log(self, msg: str, kind: str = "info"):
        ts = datetime.now().strftime("%H:%M:%S")
        line = f"[{ts}] {msg}\n"
        def _append():
            try:
                self.log_text.configure(state="normal")
                self.log_text.insert(tk.END, line, kind)
                self.log_text.see(tk.END)
                self.log_text.configure(state="disabled")
            except Exception:
                pass
        try:
            self.root.after(0, _append)
        except Exception:
            pass

    # ─────────────────────────────────────────────────────
    def _scan_async(self):
        self.log("🔍 Varrendo as 3 versões…", "info")
        self.engine.submit(self._scan_all)

    def _scan_all(self):
        for v in VERSION_REGISTRY:
            path = LAUNCHER_DIR / v["file"]
            info = scan_version_file(path)
            self.version_meta[v["id"]] = info
            def _upd(vid=v["id"], inf=info):
                card = self.cards.get(vid)
                if card:
                    card.update_meta(inf)
            self.root.after(0, _upd)
            status = "OK" if info["exists"] else "AUSENTE"
            self.log(f"  • {v['short']}: {status} "
                     f"({info['lines']} linhas, v{info['app_version']})",
                     "ok" if info["exists"] else "err")
        self.root.after(0, lambda: self.status_bar.config(
            text=f"Scan concluído — {datetime.now():%H:%M:%S}"))
        self.log("✅ Scan concluído.", "ok")

    # ─────────────────────────────────────────────────────
    def _on_select(self, version: dict):
        self.selected_id = version["id"]
        for vid, card in self.cards.items():
            card.set_selected(vid == self.selected_id)

        # Guard defensivo: só atualiza painel se ele existir
        if getattr(self, "details_title", None) is not None:
            self.details_title.config(text=version["name"],
                                       fg=version["accent"])
        if getattr(self, "details_sub", None) is not None:
            info = self.version_meta.get(version["id"], {})
            bits = []
            if info.get("exists"):
                bits.append(f"📄 {info['lines']} linhas")
                bits.append(f"📏 {info['size']/1024:.1f} KB")
                bits.append(f"🏷️  v{info['app_version']}")
                bits.append(f"🕐 {info['modified']}")
            else:
                bits.append("❌ arquivo não encontrado")
            self.details_sub.config(text=" · ".join(bits))

        self.log(f"Selecionado: {version['short']}", "info")

    # ─────────────────────────────────────────────────────
    def _selected_version(self):
        if not self.selected_id:
            return None
        return next((v for v in VERSION_REGISTRY
                     if v["id"] == self.selected_id), None)

    # ─────────────────────────────────────────────────────
    def _launch_selected(self, admin: bool = False):
        v = self._selected_version()
        if not v:
            messagebox.showwarning("Launcher", "Selecione uma versão.")
            return
        path = LAUNCHER_DIR / v["file"]
        if not path.exists():
            messagebox.showerror("Launcher",
                                  f"Arquivo não encontrado:\n{path}")
            return
        if self.active_process and self.active_process.poll() is None:
            messagebox.showwarning(
                "Launcher",
                "Já existe uma versão em execução. Pare antes de lançar.")
            return

        refinements = VERSION_GUI_REFINEMENTS.get(v["id"], {})
        profile_env = dict(refinements.get("extra_env", {}))
        env = {**os.environ, **profile_env,
               "DARKPENBOOT_LAUNCHED_BY": f"launcher/{LAUNCHER_VERSION}"}

        try:
            PROFILE_DIR.mkdir(exist_ok=True)
            (PROFILE_DIR / f"{v['id']}.json").write_text(
                json.dumps(refinements, indent=2, ensure_ascii=False),
                encoding="utf-8")
        except Exception:
            pass

        # Elevação (UAC) — Windows
        if admin and IS_WINDOWS:
            self.log(f"🛡️ Solicitando elevação para {v['short']}…", "warn")
            try:
                import ctypes
                from ctypes import wintypes
                sh = ctypes.windll.shell32
                sh.ShellExecuteW.argtypes = [
                    wintypes.HWND, wintypes.LPCWSTR, wintypes.LPCWSTR,
                    wintypes.LPCWSTR, wintypes.LPCWSTR, ctypes.c_int
                ]
                sh.ShellExecuteW.restype = wintypes.HINSTANCE
                r = sh.ShellExecuteW(
                    None, "runas", sys.executable,
                    f'"{path}"', str(LAUNCHER_DIR), 1)
                if int(r) > 32:
                    self.log("✅ Pedido de elevação enviado.", "ok")
                else:
                    self.log(f"❌ Falha ao elevar (código {r}).", "err")
            except Exception as e:
                self.log(f"❌ Erro na elevação: {e}", "err")
            return

        try:
            proc = subprocess.Popen(
                [sys.executable, str(path)],
                cwd=str(LAUNCHER_DIR),
                env=env,
                creationflags=CREATE_NEW_CONSOLE,
            )
        except Exception as e:
            self.log(f"❌ Falha ao lançar: {e}", "err")
            messagebox.showerror("Launcher", f"Falha ao lançar:\n{e}")
            return

        self.active_process = proc
        self.log(f"🚀 {v['short']} lançada (PID {proc.pid}).", "ok")
        self.status_bar.config(
            text=f"Em execução: {v['short']} (PID {proc.pid})")
        self._start_monitor(proc, v)

    def _launch_admin(self):
        self._launch_selected(admin=True)

    # ─────────────────────────────────────────────────────
    def _start_monitor(self, proc, version: dict):
        def _poll():
            rc = proc.poll()
            if rc is None:
                self.proc_monitor_id = self.root.after(500, _poll)
                return
            self.proc_monitor_id = None
            self.active_process = None
            kind = "ok" if rc == 0 else "err"
            self.log(f"⏹️ {version['short']} encerrada "
                     f"(código {rc}).", kind)
            self.status_bar.config(
                text=f"{version['short']} encerrada às "
                     f"{datetime.now():%H:%M:%S}")
        self.proc_monitor_id = self.root.after(500, _poll)

    # ─────────────────────────────────────────────────────
    def _stop_active(self):
        if (not self.active_process
                or self.active_process.poll() is not None):
            self.log("Nada em execução.", "warn")
            return
        if not messagebox.askyesno(
                "Launcher",
                "Encerrar o processo em execução?\n"
                "(pode corromper operação em andamento)"):
            return
        try:
            self.active_process.terminate()
            self.log("⏹️ Terminate enviado.", "warn")
        except Exception as e:
            self.log(f"❌ Falha ao parar: {e}", "err")

    # ─────────────────────────────────────────────────────
    def _open_folder(self):
        try:
            if IS_WINDOWS:
                os.startfile(str(LAUNCHER_DIR))
            elif sys.platform == "darwin":
                subprocess.Popen(["open", str(LAUNCHER_DIR)])
            else:
                subprocess.Popen(["xdg-open", str(LAUNCHER_DIR)])
            self.log("📂 Pasta aberta no gerenciador.", "info")
        except Exception as e:
            self.log(f"❌ Não foi possível abrir pasta: {e}", "err")

    # ─────────────────────────────────────────────────────
    def _restore_geometry(self):
        try:
            if LAUNCHER_CFG.exists():
                cfg = json.loads(LAUNCHER_CFG.read_text(encoding="utf-8"))
                g = cfg.get("geometry")
                if g and re.match(r"^\d+x\d+[+-]\d+[+-]\d+$", g):
                    self.root.geometry(g)
        except Exception:
            pass

    def _on_close(self):
        try:
            LAUNCHER_CFG.write_text(
                json.dumps({"geometry": self.root.geometry()}, indent=2),
                encoding="utf-8")
        except Exception:
            pass
        try:
            self.engine.stop()
        except Exception:
            pass
        self.root.destroy()


# ══════════════════════════════════════════════════════════════
# 9. MAIN
# ══════════════════════════════════════════════════════════════
def main():
    root = tk.Tk()
    app = LauncherApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()             
 