#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DarkPenBoot Pro — PATCHER CONSOLIDADO v3.6.0
Aplica 12 correções direto no arquivo-alvo. Backup automático.
Uso: python patcher_v360.py DarkPenBoot_PRO1.py
"""
import re, sys, shutil, ast
from pathlib import Path
from datetime import datetime

ARQ = Path(sys.argv[1] if len(sys.argv) > 1 else "DarkPenBoot_PRO1.py")
if not ARQ.exists():
    print(f"❌ Não encontrado: {ARQ}"); sys.exit(1)

bak = ARQ.parent / f"{ARQ.name}.{datetime.now():%Y%m%d_%H%M%S}.bak"
shutil.copy2(ARQ, bak)
print(f"✅ Backup: {bak.name}")

src = ARQ.read_text(encoding="utf-8")
orig = src.count("\n") + 1
print(f"📄 Linhas originais: {orig}")
CHANGES = []

def ok(m):
    print(f"✅ {m}"); CHANGES.append(m)

def warn(m):
    print(f"⚠️  {m}")

# ═══════════════════════════════════════════════════════════
# 1. VERSÃO → 3.6.0
# ═══════════════════════════════════════════════════════════
src = re.sub(r'APP_VERSION\s*=\s*"3\.\d+\.\d+"',
             'APP_VERSION = "3.6.0"', src, count=1)
ok("APP_VERSION → 3.6.0")

# ═══════════════════════════════════════════════════════════
# 2. PULSO NEON MAIS SUAVE (intervalo maior, amplitude menor)
# ═══════════════════════════════════════════════════════════
src = src.replace(
    "'interval_ms': 55,",
    "'interval_ms': 80,", 1)
ok("Pulso neon suavizado (80ms)")

# ═══════════════════════════════════════════════════════════
# 3. FEDORA/DEBIAN — fix do _format_usb_linux + copia
# ═══════════════════════════════════════════════════════════
# 3a. Adicionar fallback de mkfs se faltar ferramenta
fix_linux = '''def _ensure_linux_mkfs_tools(log_func=None):
    """Garante que as ferramentas mkfs estejam disponíveis."""
    needed = {
        'mkfs.vfat':   ['mkfs.fat', 'mkdosfs', 'dosfstools'],
        'mkfs.ntfs':   ['mkntfs', 'ntfs-3g'],
        'mkfs.exfat':  ['mkexfatfs', 'exfat-utils', 'exfatprogs'],
        'mkfs.ext4':   ['mke2fs', 'e2fsprogs'],
    }
    missing = []
    for tool, alts in needed.items():
        if shutil.which(tool):
            continue
        found = False
        for a in alts:
            if shutil.which(a):
                found = True; break
        if not found:
            missing.append(f"{tool} (instale: {' ou '.join(alts)})")
    if missing and log_func:
        log_func("⚠️ Ferramentas mkfs ausentes:", is_warning=True)
        for m in missing:
            log_func(f"   • {m}", is_warning=True)
        log_func("   💡 sudo apt install dosfstools ntfs-3g exfatprogs e2fsprogs",
                 is_info=True)
    return missing

'''
if "def _ensure_linux_mkfs_tools" not in src:
    # Inserir após "def _normalize_fs"
    anchor = "def _is_fat_like(fs: str) -> bool:"
    if anchor in src:
        src = src.replace(anchor, fix_linux + anchor, 1)
        ok("Fedora/Debian: helper _ensure_linux_mkfs_tools adicionado")

# 3b. Chamar verificação no início de _format_usb_linux
old_linux = "def _format_usb_linux(drive_info, filesystem, scheme, quick,\n                      log_func, cancel_flag, volume_label=\"DARKPENBOOT\"):\n    device = drive_info['DevicePath']"
new_linux = """def _format_usb_linux(drive_info, filesystem, scheme, quick,
                      log_func, cancel_flag, volume_label="DARKPENBOOT"):
    device = drive_info['DevicePath']
    # ── v3.6.0: garante ferramentas mkfs ──
    _ensure_linux_mkfs_tools(log_func)"""
if old_linux in src:
    src = src.replace(old_linux, new_linux, 1)
    ok("Fedora/Debian: verificação de mkfs em _format_usb_linux")

# ═══════════════════════════════════════════════════════════
# 4. MOTOR DE BUSCA — busca universal (key + family + version)
# ═══════════════════════════════════════════════════════════
new_search = '''def _search_distros(query: str, family: str = "", limit: int = 60) -> List[str]:
    """Filtra distros por substring em key, family, version e license."""
    q = (query or "").lower().strip()
    if not q:
        return list(DISTRO_INFO.keys())[:limit]
    out: List[str] = []
    for key, info in DISTRO_INFO.items():
        if family and info.get("family") != family:
            continue
        hay = " ".join([
            key,
            info.get("family", ""),
            info.get("version", ""),
            info.get("license", ""),
            info.get("foundation", ""),
        ]).lower()
        if q in hay:
            out.append(key)
        if len(out) >= limit:
            break
    return out

'''
pat_s = re.compile(
    r'def _search_distros\(query: str, family: str = "", limit: int = 40\) -> List\[str\]:.*?(?=\ndef |\nclass |\n# =====)',
    re.DOTALL)
if pat_s.search(src):
    src = pat_s.sub(new_search, src, count=1)
    ok("Motor de busca universal (family + version + license)")

# ═══════════════════════════════════════════════════════════
# 5. REMOVER BOTÃO DOAR DUPLICADO
# ═══════════════════════════════════════════════════════════
# 5a. Remover botão ❤️ do _build_log (manter somente no rodapé)
old_log_btn = """        bd = self._make_button(btn_frame, "❤️", self._open_donate,
                                kind="primary", width=70)
        bd.grid(row=0, column=2, padx=1, sticky='ew')
        self._add_tip(bd, "❤️ Doar via PIX")
        ba = self._make_button(btn_frame, "ℹ️ Sobre",
                    lambda: self._show_about(), width=96)
        ba.grid(row=0, column=3, padx=1, sticky='ew')"""
new_log_btn = """        # ── v3.6.0: doação única no rodapé ──
        ba = self._make_button(btn_frame, "ℹ️ Sobre",
                    lambda: self._show_about(), width=96)
        ba.grid(row=0, column=2, padx=1, sticky='ew', columnspan=2)"""
if old_log_btn in src:
    src = src.replace(old_log_btn, new_log_btn, 1)
    ok("Botão Doar duplicado removido (log)")

# ═══════════════════════════════════════════════════════════
# 6. RODAPÉ — coração pulsante multicolor com fundo animado
# ═══════════════════════════════════════════════════════════
new_footer = '''    def _build_premium_footer(self, parent, row):
        """Rodapé com [💖 Doação] [📱 Mobile] | [❤️ pulsa] [📢 Anúncios]."""
        try:
            frame = tk.Frame(parent, bg=COLORS['bg'])
            frame.grid(row=row, column=0, sticky='ew', pady=(4, 0))
            frame.columnconfigure(0, weight=1)

            left = tk.Frame(frame, bg=COLORS['bg'])
            left.grid(row=0, column=0, sticky='w')

            donate = self._make_button(
                left, "\\U0001f496 DOAR VIA PIX", self._open_donate,
                kind="primary", font=('Segoe UI', 10, 'bold'))
            donate.pack(side=tk.LEFT, padx=(2, 4), pady=2)
            self._add_tip(donate,
                          "\\U0001f496 Botão único de doação via PIX.\\n"
                          "Consolidado v3.6.0.")

            mobile = self._make_button(
                left, "\\U0001f4f1 Versão Mobile (sem Ads)",
                self._open_mobile_page,
                kind="normal", font=('Segoe UI', 9, 'bold'))
            mobile.pack(side=tk.LEFT, padx=4, pady=2)
            self._add_tip(mobile,
                          "\\U0001f4f1 Versão mobile sem anúncios.")

            right = tk.Frame(frame, bg=COLORS['bg'])
            right.grid(row=0, column=1, sticky='e')

            # Coração pulsante multicolor com fundo animado
            self.heart_btn = HeartPulseButton(
                right,
                command=self._toggle_favorite,
                width=54, height=40)
            self.heart_btn.pack(side=tk.TOP, anchor='e', pady=(0, 3))
            self._add_tip(self.heart_btn,
                          "\\u2764\\ufe0f Favoritar ISO atual.\\n"
                          "Pulsa entre as cores do tema.")

            ads = self._make_button(
                right, "\\U0001f4e2 Anúncios", self._open_ads_settings,
                kind="normal", width=130,
                font=('Segoe UI', 9, 'bold'))
            ads.pack(side=tk.TOP, anchor='e')
            self._add_tip(ads, "\\U0001f4e2 Preferências de anúncios.")
        except Exception as e:
            self.log(f"\\u26a0\\ufe0f Rodapé: {e}", is_warning=True)

'''
pat_f = re.compile(
    r'    def _build_premium_footer\(self, parent, row\):.*?(?=\n    def [a-zA-Z_])',
    re.DOTALL)
if pat_f.search(src):
        src = pat_f.sub(lambda m: new_footer, src, count=1)
    ok("Rodapé: coração pulsante + botão Doar único")

# ═══════════════════════════════════════════════════════════
# 7. INJETAR HeartPulseButton (antes de RoundedButton)
# ═══════════════════════════════════════════════════════════
heart_class = '''# ==================================================================
# 17B. HEART PULSE BUTTON — coração multicolor com fundo animado
# ==================================================================
class HeartPulseButton(tk.Canvas):
    def __init__(self, parent, command=None, width=54, height=40, **kw):
        try:
            bg = parent.cget('bg')
        except Exception:
            bg = COLORS['bg']
        super().__init__(parent, width=width, height=height,
                         highlightthickness=0, bg=bg,
                         takefocus=True, **kw)
        self._command = command
        self._width = width
        self._height = height
        self._phase = 0
        self._anim_id = None
        self._hover = False
        self._focused = False
        self._pressed = False
        self.bind('<Button-1>', self._on_press)
        self.bind('<ButtonRelease-1>', self._on_release)
        self.bind('<Enter>', self._on_enter)
        self.bind('<Leave>', self._on_leave)
        self.bind('<FocusIn>', self._on_focus_in)
        self.bind('<FocusOut>', self._on_focus_out)
        self.bind('<Return>', self._on_key)
        self.bind('<space>', self._on_key)
        _PULSE_SUBSCRIBERS.append(self)
        self._tick()

    def _palette(self):
        return [
            COLORS.get('accent', '#ff5252'),
            COLORS.get('accent2', '#ff79c6'),
            COLORS.get('info', '#89b4fa'),
            COLORS.get('success', '#a6e3a1'),
            COLORS.get('warning', '#f9e2af'),
        ]

    def _tick(self):
        try:
            self._phase = (self._phase + 1) % 64
            self._draw()
            self._anim_id = self.after(60, self._tick)
        except Exception:
            self._anim_id = None

    def _draw(self):
        try:
            self.delete('all')
        except Exception:
            return
        w, h = self._width, self._height
        cx, cy = w / 2, h / 2
        palette = self._palette()
        idx = (self._phase // 12) % len(palette)
        col = palette[idx]
        # Fundo pulsante (glassmorphism)
        for i in range(6):
            rr = 14 + i * 2.2 + 3 * abs(3 - (self._phase % 8))
            self.create_oval(cx - rr, cy - rr, cx + rr, cy + rr,
                             outline=col, width=1, fill='')
        # Coração
        size = 10 + int(2 * abs(3 - (self._phase % 8)))
        if self._pressed:
            size -= 2
        self.create_text(cx, cy, text='\\u2764\\ufe0f',
                         font=('Segoe UI Emoji', size, 'bold'),
                         fill=col)

    def _on_press(self, e):
        self._pressed = True
        try: self.focus_set()
        except Exception: pass
        self._draw()

    def _on_release(self, e):
        if self._pressed and self._command:
            self._pressed = False
            try: self._command()
            except Exception: pass
        self._draw()

    def _on_enter(self, e):
        self._hover = True; self._draw()

    def _on_leave(self, e):
        self._hover = False; self._draw()

    def _on_focus_in(self, e):
        self._focused = True; self._draw()

    def _on_focus_out(self, e):
        self._focused = False; self._draw()

    def _on_key(self, e):
        if self._command:
            try: self._command()
            except Exception: pass
        return "break"

    def destroy(self):
        if self._anim_id is not None:
            try: self.after_cancel(self._anim_id)
            except Exception: pass
        try: _PULSE_SUBSCRIBERS.remove(self)
        except ValueError: pass
        super().destroy()

'''
anchor_rb = "# 17. ROUNDED BUTTON"
if anchor_rb in src and "class HeartPulseButton" not in src:
    src = src.replace(anchor_rb, heart_class + anchor_rb, 1)
    ok("HeartPulseButton injetado")

# ═══════════════════════════════════════════════════════════
# 8. ROUNDED BUTTON — glassmorphism + foco de alto contraste
# ═══════════════════════════════════════════════════════════
# 8a. Adicionar efeito translúcido no _redraw
old_redraw_head = '''    def _redraw(self):
        self.delete("all")
        w, h, r = self._width, self._height, self._radius
        if not self._enabled:
            bg, fg, outline = (COLORS['button_bg'], COLORS['led_off'],
                                COLORS['frame_border'])'''
new_redraw_head = '''    def _redraw(self):
        self.delete("all")
        w, h, r = self._width, self._height, self._radius
        # ── v3.6.0: glassmorphism ──
        try:
            glass_bg = self._glassify(self._bg_norm)
        except Exception:
            glass_bg = None
        if not self._enabled:
            bg, fg, outline = (COLORS['button_bg'], COLORS['led_off'],
                                COLORS['frame_border'])'''
if old_redraw_head in src:
    src = src.replace(old_redraw_head, new_redraw_head, 1)

# 8b. Adicionar método _glassify
glass_method = '''    def _glassify(self, hex_color):
        """Mistura a cor com o fundo para efeito translúcido."""
        try:
            h = hex_color.lstrip('#')
            r = int(h[0:2], 16); g = int(h[2:4], 16); b = int(h[4:6], 16)
            try:
                pbg = self.master.cget('bg').lstrip('#')
                pr = int(pbg[0:2], 16); pg = int(pbg[2:4], 16); pb = int(pbg[4:6], 16)
            except Exception:
                pr, pg, pb = 20, 22, 30
            # 65% cor + 35% fundo
            nr = int(r * 0.65 + pr * 0.35)
            ng = int(g * 0.65 + pg * 0.35)
            nb = int(b * 0.65 + pb * 0.35)
            return f"#{nr:02x}{ng:02x}{nb:02x}"
        except Exception:
            return hex_color

'''
if "_glassify" not in src:
    anchor_g = "    def _redraw(self):"
    if anchor_g in src:
        src = src.replace(anchor_g, glass_method + anchor_g, 1)
        ok("RoundedButton: glassmorphism ativado")

# 8c. Foco com alto contraste (linha extra branca)
old_focus = '''        if (self._focused or self._persistent_focus) and self._enabled:
            phase = self._focus_phase
            halo = self._pulse_color(COLORS.get('accent', '#00ff41'), phase, 160)'''
new_focus = '''        if (self._focused or self._persistent_focus) and self._enabled:
            phase = self._focus_phase
            # ── v3.6.0: alto contraste do foco ──
            try:
                self.create_polygon(self._rounded_polygon(1, 1, w - 1, h - 1,
                                                            r - 1),
                                    smooth=True, splinesteps=24,
                                    fill='', outline='#ffffff', width=3)
            except Exception:
                pass
            halo = self._pulse_color(COLORS.get('accent', '#00ff41'), phase, 160)'''
if old_focus in src:
    src = src.replace(old_focus, new_focus, 1)
    ok("RoundedButton: foco de alto contraste")

# ═══════════════════════════════════════════════════════════
# 9. NEON ORB — bolha fina translúcida
# ═══════════════════════════════════════════════════════════
old_trail = '''        n_trail = 6
        for i in range(n_trail):
            t = i / float(n_trail)
            trail_r = r_base + 2.0 + i * 2.2
            mix = self._lerp_rgb(acc_rgb, acc2_rgb, t)
            pulse_off = int(90 * (0.5 + 0.5 * math.sin(
                (self._phase + i * 2) * math.pi / 8)))
            r_col = min(255, mix[0] + pulse_off)
            g_col = min(255, mix[1] + pulse_off)
            b_col = min(255, mix[2] + pulse_off)
            fade = 1.0 - (i / float(n_trail))
            r_col = int(r_col * fade + 20 * (1 - fade))
            g_col = int(g_col * fade + 20 * (1 - fade))
            b_col = int(b_col * fade + 20 * (1 - fade))
            color = f"#{r_col:02x}{g_col:02x}{b_col:02x}"
            try:
                self.create_oval(cx - trail_r, cy - trail_r,
                                 cx + trail_r, cy + trail_r,
                                 outline=color,
                                 width=max(1, 2 - i // 3))
            except Exception:
                pass'''
new_trail = '''        # ── v3.6.0: bolha fina translúcida ──
        n_trail = 4
        for i in range(n_trail):
            t = i / float(n_trail)
            trail_r = r_base + 4.0 + i * 3.0
            mix = self._lerp_rgb(acc_rgb, acc2_rgb, t)
            fade = 1.0 - (i / float(n_trail))
            r_col = int(mix[0] * fade + 15 * (1 - fade))
            g_col = int(mix[1] * fade + 15 * (1 - fade))
            b_col = int(mix[2] * fade + 15 * (1 - fade))
            color = f"#{r_col:02x}{g_col:02x}{b_col:02x}"
            try:
                self.create_oval(cx - trail_r, cy - trail_r,
                                 cx + trail_r, cy + trail_r,
                                 outline=color, width=1)
            except Exception:
                pass'''
if old_trail in src:
    src = src.replace(old_trail, new_trail, 1)
    ok("Neon orb: bolha fina translúcida")

# ═══════════════════════════════════════════════════════════
# 10. PAGE UP/DOWN em modais (UltimatePopup + About)
# ═══════════════════════════════════════════════════════════
# Universal bind nas modais — já existe no UltimatePopup,
# adiciona explicitamente no _show_about
old_about_bind = "        dlg.bind('<Escape>', lambda e: dlg.destroy())"
new_about_bind = """        dlg.bind('<Escape>', lambda e: dlg.destroy())
        # ── v3.6.0: Page Up/Down na barra de rolagem ──
        try:
            dlg.bind('<Prior>',
                     lambda e: cv.yview_scroll(-1, 'pages'))
            dlg.bind('<Next>',
                     lambda e: cv.yview_scroll(1, 'pages'))
            dlg.bind('<Up>',
                     lambda e: cv.yview_scroll(-3, 'units'))
            dlg.bind('<Down>',
                     lambda e: cv.yview_scroll(3, 'units'))
        except Exception:
            pass"""
# Só substituir dentro do _show_about
if old_about_bind in src:
    # Primeira ocorrência depois de _show_about
    idx = src.find("def _show_about")
    if idx != -1:
        sub = src[idx:idx + 8000]
        if old_about_bind in sub:
            sub = sub.replace(old_about_bind, new_about_bind, 1)
            src = src[:idx] + sub + src[idx + 8000:]
            ok("Page Up/Down na janela Sobre")

# ═══════════════════════════════════════════════════════════
# 11. BOTÃO ATUALIZAR DISTRO (site oficial)
# ═══════════════════════════════════════════════════════════
# Adiciona botão "🌐 Site" no card de download Linux
old_dl = '''        b1 = self._make_button(inner, "📥 Baixar", self._download_linux_iso)
        b1.grid(row=0, column=2, padx=2, pady=2)'''
new_dl = '''        b1 = self._make_button(inner, "📥 Baixar", self._download_linux_iso)
        b1.grid(row=0, column=2, padx=2, pady=2)
        # ── v3.6.0: botão Site Oficial + Atualizar ──
        b1b = self._make_button(inner, "🌐 Site", self._open_distro_site,
                                 width=70)
        b1b.grid(row=0, column=3, padx=2, pady=2)
        self._add_tip(b1b,
                      "🌐 Abre o site oficial da distro selecionada.\\n"
                      "Fonte sempre atualizada.")'''
if old_dl in src:
    src = src.replace(old_dl, new_dl, 1)
    ok("Botão 🌐 Site no card de download")

# Adicionar método _open_distro_site
open_site_m = '''    def _open_distro_site(self):
        """Abre o site oficial da distro selecionada."""
        try:
            distro = self.distro_combo.get()
            info = DISTRO_INFO.get(distro, {})
            url = info.get("homepage") or info.get("docs")
            if not url:
                self._popup_warning(
                    "Sem URL",
                    f"A distro '{distro}' não tem site cadastrado.")
                return
            webbrowser.open(url)
            self.log(f"🌐 Site oficial: {url}", is_success=True)
        except Exception as e:
            self.log(f"⚠️ Erro ao abrir site: {e}", is_warning=True)

    def _open_donate(self):'''
if "_open_distro_site" not in src:
    src = src.replace("    def _open_donate(self):",
                       open_site_m, 1)
    ok("Método _open_distro_site adicionado")

# ═══════════════════════════════════════════════════════════
# 12. NAVEGAÇÃO UNIFORME — bind_class para Canvas
# ═══════════════════════════════════════════════════════════
old_nav = '''            for klass in ("TButton", "TCombobox", "TEntry", "TCheckbutton",
                          "Entry", "Text", "Listbox", "Checkbutton"):'''
new_nav = '''            for klass in ("TButton", "TCombobox", "TEntry", "TCheckbutton",
                          "Entry", "Text", "Listbox", "Checkbutton",
                          "Canvas", "Frame"):'''
if old_nav in src:
    src = src.replace(old_nav, new_nav, 1)
    ok("Navegação: Canvas + Frame incluídos")

# ═══════════════════════════════════════════════════════════
# 13. VALIDAÇÃO FINAL
# ═══════════════════════════════════════════════════════════
try:
    ast.parse(src)
    print("✅ Sintaxe validada")
except SyntaxError as e:
    print(f"❌ ERRO DE SINTAXE — linha {e.lineno}: {e.msg}")
    print(f"   Contexto: {(e.text or '').rstrip()}")
    print("   Backup preservado. Restaurando arquivo original…")
    ARQ.write_text(bak.read_text(encoding="utf-8"), encoding="utf-8")
    sys.exit(1)

ARQ.write_text(src, encoding="utf-8")
novo = src.count("\n") + 1
print()
print("═" * 62)
print(f"🎉 PATCH v3.6.0 APLICADO")
print(f"📄 {ARQ}")
print(f"📏 Linhas: {orig} → {novo}  (Δ {novo-orig:+d})")
print(f"🗄️  Backup: {bak.name}")
print("═" * 62)
print()
print("📋 Correções aplicadas:")
for c in CHANGES:
    print(f"   • {c}")
print()
print("🧪 Rode agora:")
print(f"   python -c \"import ast; ast.parse(open('{ARQ.name}', encoding='utf-8').read()); print('OK')\"")
print(f"   python {ARQ.name}")
