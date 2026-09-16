#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patcher v3.6.1c — Ultra-safe
- Aplica UM patch de cada vez
- Valida sintaxe após CADA patch
- Se um patch quebra, só ELE é revertido (rollback individual)
- Salva no final com o que deu certo
"""
import re, sys, shutil, datetime, ast
from pathlib import Path

TARGET = Path("DarkPenBoot_PRO1.py")
NL = chr(92) + "n"


def apply_patch(src, name, pattern, replacement, use_regex=False):
    """Aplica um patch. Valida sintaxe. Rollback individual se falhar."""
    try:
        if use_regex:
            new_src, n = re.subn(pattern, replacement, src, count=1,
                                  flags=re.DOTALL)
        else:
            if pattern in src:
                new_src = src.replace(pattern, replacement, 1)
                n = 1
            else:
                n = 0
                new_src = src
    except Exception as e:
        print(f"  ⚠️  [{name}] Erro no regex: {e}")
        return src, False

    if n == 0:
        print(f"  ⚠️  [{name}] padrão NÃO encontrado (pulando)")
        return src, False

    # Valida sintaxe
    try:
        ast.parse(new_src)
    except SyntaxError as e:
        print(f"  ❌ [{name}] QUEBROU sintaxe linha {e.lineno}: {e.msg}")
        print(f"     → {(e.text or '').strip()[:100]}")
        print(f"     → DESFAZENDO este patch")
        return src, False  # rollback individual

    print(f"  ✅ [{name}] aplicado")
    return new_src, True


# ══════════════════════════════════════════════════════════════
# PATCHES
# ══════════════════════════════════════════════════════════════

# P0 — Fix SyntaxError original
P0 = (
    '                except TypeError:\n'
    '                    \n'
    '                    ok = fnattempt_url, destino\n'
    '                except TypeError:\n'
    '                    ok = fn(attempt_url, destino, progress_cb, cancel_flag)',
    '                except TypeError:\n'
    '                    ok = fn(attempt_url, destino, progress_cb, cancel_flag)'
)

# P1 — Constantes visuais v3.6.1
P1 = (
    'PIX_ACCOUNT_INFO = "Agência 3449 • C/C 01081019-8"',
    'PIX_ACCOUNT_INFO = "Agência 3449 • C/C 01081019-8"\n'
    '\n'
    'GUI_TEXTURE_ENABLED  = True\n'
    'GUI_TEXTURE_STEP     = 26\n'
    'GUI_TEXTURE_ALPHA    = 0.08\n'
    'ORB_TRANSLUCENCY     = 0.78\n'
    'ORB_GLASS_EDGE       = True\n'
    'LOGO_GLOW_ENABLED    = True\n'
    'LOGO_SHADOW_ENABLED  = True\n'
    '\n'
    '\n'
    'def _blend_color(rgb, bg_rgb, alpha):\n'
    '    alpha = max(0.0, min(1.0, float(alpha)))\n'
    '    return tuple(\n'
    '        int(c * alpha + b * (1.0 - alpha))\n'
    '        for c, b in zip(rgb, bg_rgb)\n'
    '    )\n'
    '\n'
    '\n'
    'def _rgb_tuple_to_hex(rgb) -> str:\n'
    '    r, g, b = (max(0, min(255, int(c))) for c in rgb)\n'
    '    return f"#{r:02x}{g:02x}{b:02x}"\n'
    '\n'
    '\n'
    'def _lighten_hex(hex_color: str, amount: int = 20) -> str:\n'
    '    try:\n'
    '        r, g, b = _theme_rgb(hex_color)\n'
    '        return _rgb_tuple_to_hex((r + amount, g + amount, b + amount))\n'
    '    except Exception:\n'
    '        return hex_color\n'
    '\n'
    '\n'
    'def _darken_hex(hex_color: str, amount: int = 20) -> str:\n'
    '    try:\n'
    '        r, g, b = _theme_rgb(hex_color)\n'
    '        return _rgb_tuple_to_hex((r - amount, g - amount, b - amount))\n'
    '    except Exception:\n'
    '        return hex_color'
)

# P3 — _scan_shell_all_platforms
P3 = (
    'def get_disk_number_by_letter(letter: str) -> int:',
    'def _scan_shell_all_platforms(log_func=None) -> list:\n'
    '    """v3.6.1 - Varredura universal via shell."""\n'
    '    found = []\n'
    '    if IS_WINDOWS:\n'
    '        try:\n'
    '            ps = "Get-CimInstance Win32_DiskDrive | "\n'
    '            ps += "Where-Object { $_.InterfaceType -eq \'USB\' } | "\n'
    '            ps += "Select-Object Index,Model,Size,InterfaceType,"\n'
    '            ps += "SerialNumber,PNPDeviceID | ConvertTo-Json -Compress"\n'
    '            r = run_hidden(["powershell", "-NoProfile", "-Command", ps],\n'
    '                           timeout=30)\n'
    '            if r.returncode == 0 and r.stdout.strip():\n'
    '                import json as _j\n'
    '                data = _j.loads(r.stdout)\n'
    '                if not isinstance(data, list):\n'
    '                    data = [data]\n'
    '                for d in data:\n'
    '                    found.append({\n'
    '                        "DiskNumber": d.get("Index"),\n'
    '                        "Model": (d.get("Model") or "?").strip(),\n'
    '                        "Size": int(d.get("Size") or 0),\n'
    '                        "Letters": "",\n'
    '                        "BusType": "USB",\n'
    '                        "DevicePath": "\\\\\\\\.\\\\PhysicalDrive" + str(d.get("Index")),\n'
    '                        "SerialNumber": (d.get("SerialNumber") or "").strip(),\n'
    '                        "PNPDeviceID": (d.get("PNPDeviceID") or "").strip(),\n'
    '                    })\n'
    '        except Exception:\n'
    '            pass\n'
    '    elif IS_LINUX or IS_TERMUX or IS_ANDROID:\n'
    '        try:\n'
    '            cmd = "lsblk -J -o NAME,TYPE,SIZE,MODEL,TRAN,SERIAL,RM 2>/dev/null"\n'
    '            r = run_hidden(["sh", "-c", cmd], timeout=15)\n'
    '            if r.returncode == 0 and r.stdout.strip():\n'
    '                import json as _j\n'
    '                data = _j.loads(r.stdout)\n'
    '                for dev in data.get("blockdevices", []):\n'
    '                    if dev.get("type") != "disk":\n'
    '                        continue\n'
    '                    name = dev.get("name", "")\n'
    '                    if not name:\n'
    '                        continue\n'
    '                    is_usb = (str(dev.get("tran") or "").lower() == "usb"\n'
    '                              or dev.get("rm") in (True, "1", 1))\n'
    '                    if not is_usb:\n'
    '                        continue\n'
    '                    try:\n'
    '                        size = _parse_size(str(dev.get("size", "0")))\n'
    '                    except Exception:\n'
    '                        size = 0\n'
    '                    found.append({\n'
    '                        "DiskNumber": name,\n'
    '                        "Model": (dev.get("model") or "Unknown USB").strip(),\n'
    '                        "Size": size,\n'
    '                        "Letters": "",\n'
    '                        "BusType": "USB",\n'
    '                        "DevicePath": "/dev/" + name,\n'
    '                        "SerialNumber": (dev.get("serial") or "").strip(),\n'
    '                        "PNPDeviceID": "",\n'
    '                    })\n'
    '        except Exception:\n'
    '            pass\n'
    '    if log_func:\n'
    '        log_func("Varredura shell: " + str(len(found)) + " dispositivo(s).",\n'
    '                 is_info=True)\n'
    '    return found\n'
    '\n'
    '\n'
    'def get_disk_number_by_letter(letter: str) -> int:'
)

# P4 — refresh_drives com pulso
P4_REGEX = r'(    def refresh_drives\(self\):.*?)(?=\n    def )'
P4_REPL = (
    '    def refresh_drives(self):\n'
    '        self._start_global_pulse()\n'
    '        self.trigger_reactive_pulse(2, 1100, "ATUALIZANDO PENDRIVES...")\n'
    '        try:\n'
    '            self.log("Procurando pendrives USB...", is_info=True)\n'
    '            self.drives = get_usb_drives()\n'
    '            if not self.drives:\n'
    '                self.drive_combo["values"] = ["Nenhum pendrive detectado"]\n'
    '                self.drive_combo.set("")\n'
    '                self.log("Nenhum pendrive encontrado.", is_warning=True)\n'
    '                return\n'
    '            items = []\n'
    '            for d in self.drives:\n'
    '                sg = d["Size"] / (1024**3) if d["Size"] > 0 else 0\n'
    '                items.append("Disco " + str(d["DiskNumber"]) + " - "\n'
    '                             + str(d["Model"]) + " - " + str(round(sg, 1)) + " GB")\n'
    '            self.drive_combo["values"] = items\n'
    '            self.drive_combo.current(0)\n'
    '            self.selected_drive = self.drives[0] if self.drives else None\n'
    '            self._current_usb_tier = _detect_usb_tier(self.selected_drive)\n'
    '            self.log(str(len(self.drives)) + " pendrive(s) encontrado(s).",\n'
    '                     is_success=True)\n'
    '        except Exception as e:\n'
    '            self.log("Falha ao atualizar pendrives: " + str(e), is_warning=True)\n'
    '        finally:\n'
    '            self._stop_global_pulse(delay_ms=1500)\n'
    '\n'
)

# P5 — _do_identify com fallback shell
P5_REGEX = r'(        def _do_identify\(\):.*?)(?=\n        def _on_local_combo_change)'
P5_REPL = (
    '        def _do_identify():\n'
    '            self.log("[1/2] Identificando via API...", is_info=True)\n'
    '            try:\n'
    '                new_drives = get_usb_drives()\n'
    '            except Exception as e:\n'
    '                self.log("Erro API: " + str(e), is_error=True)\n'
    '                new_drives = []\n'
    '            if not new_drives:\n'
    '                self.log("[2/2] Varredura shell universal...", is_info=True)\n'
    '                try:\n'
    '                    new_drives = _scan_shell_all_platforms(self.log)\n'
    '                except Exception as e:\n'
    '                    self.log("Falha shell scan: " + str(e), is_warning=True)\n'
    '                    new_drives = []\n'
    '            if not new_drives:\n'
    '                rec_combo["values"] = ["Nenhum pendrive detectado"]\n'
    '                rec_combo.set("")\n'
    '                self.log("Nenhum pendrive encontrado.", is_warning=True)\n'
    '                return\n'
    '            self.drives = new_drives\n'
    '            items = []\n'
    '            for d in new_drives:\n'
    '                sg = d.get("Size", 0) / (1024**3) if d.get("Size", 0) else 0\n'
    '                items.append("Disco " + str(d.get("DiskNumber")) + " - "\n'
    '                             + str(d.get("Model", "?")) + " - "\n'
    '                             + str(round(sg, 1)) + " GB")\n'
    '            rec_combo["values"] = items\n'
    '            rec_combo.current(0)\n'
    '            rec_state["drive"] = new_drives[0]\n'
    '            rec_state["disk_num"] = new_drives[0].get("DiskNumber", -1)\n'
    '            self.selected_drive = new_drives[0]\n'
    '            self._current_usb_tier = _detect_usb_tier(new_drives[0])\n'
    '            _refresh_info_from_state()\n'
    '            self.log(str(len(new_drives)) + " dispositivo(s).", is_success=True)\n'
    '            try:\n'
    '                self.drive_combo["values"] = items\n'
    '                self.drive_combo.current(0)\n'
    '            except Exception:\n'
    '                pass\n'
    '\n'
)

# P6 — _do_diskpart com revarredura
P6_REGEX = r'(        def _do_diskpart\(\):.*?)(?=\n        term_card =)'
P6_REPL = (
    '        def _do_diskpart():\n'
    '            d = rec_state["drive"]\n'
    '            dn = rec_state["disk_num"]\n'
    '            if not d:\n'
    '                self._popup_warning("Sem alvo",\n'
    '                    "Clique em Identificar primeiro.")\n'
    '                return\n'
    '            if dn is None or dn == -1:\n'
    '                hits = _scan_shell_all_platforms(self.log)\n'
    '                if hits:\n'
    '                    self.drives = hits\n'
    '                    rec_state["drive"] = hits[0]\n'
    '                    rec_state["disk_num"] = hits[0].get("DiskNumber", -1)\n'
    '                    self.selected_drive = hits[0]\n'
    '                    _refresh_info_from_state()\n'
    '                    dn = rec_state["disk_num"]\n'
    '                    d = rec_state["drive"]\n'
    '            if IS_WINDOWS:\n'
    '                _launch_terminal("diskpart", shell="cmd")\n'
    '            else:\n'
    '                dev = d.get("DevicePath", "")\n'
    '                if dev:\n'
    '                    _launch_terminal("sudo parted " + dev, shell="bash")\n'
    '\n'
)

# P7 — _do_format_via_terminal (SIMPLIFICADO — sem f-strings complexas)
P7_REGEX = r'(        def _do_format_via_terminal\(\):.*?)(?=\n        b_fmt = self\._make_button)'
P7_REPL = (
    '        def _do_format_via_terminal():\n'
    '            d = rec_state["drive"]\n'
    '            dn = rec_state["disk_num"]\n'
    '            fs = recov_fs_combo.get().upper()\n'
    '            if not d:\n'
    '                self._popup_warning("Sem alvo", "Clique em Identificar.")\n'
    '                return\n'
    '            if dn is None or dn == -1:\n'
    '                hits = _scan_shell_all_platforms(self.log)\n'
    '                if hits:\n'
    '                    rec_state["drive"] = hits[0]\n'
    '                    rec_state["disk_num"] = hits[0].get("DiskNumber", -1)\n'
    '                    dn = rec_state["disk_num"]\n'
    '                    d = rec_state["drive"]\n'
    '            model = str(d.get("Model", "?"))\n'
    '            msg = ("Formatar Disco " + str(dn) + " (" + model + ")"\n'
    '                   + " como " + fs + "? Todos os dados serao APAGADOS.")\n'
    '            ok = UltimatePopup.ask(dlg, "Formatar como " + fs, msg,\n'
    '                                    kind="warning",\n'
    '                                    buttons=("Sim, formatar", "Cancelar"))\n'
    '            if not ok:\n'
    '                return\n'
    '            if IS_WINDOWS:\n'
    '                if dn is None or dn == -1 or dn == 0:\n'
    '                    self._popup_error("Bloqueado", "Disco invalido.")\n'
    '                    return\n'
    '                if fs not in ("NTFS", "FAT32", "EXFAT"):\n'
    '                    self._popup_info("FS nao nativo",\n'
    '                        fs + " nao e nativo do Windows.")\n'
    '                    return\n'
    '                lines = ["select disk " + str(dn),\n'
    '                         "attributes disk clear readonly",\n'
    '                         "clean",\n'
    '                         "create partition primary",\n'
    '                         "select partition 1",\n'
    '                         "format fs=" + fs + " quick label=PENBOOT",\n'
    '                         "assign",\n'
    '                         "exit"]\n'
    '                sp = CONFIG_DIR / ("_fmt_" + str(os.getpid()) + ".txt")\n'
    '                try:\n'
    '                    with open(sp, "w", encoding="ascii",\n'
    '                              newline="\\r\\n") as f:\n'
    '                        f.write("\\n".join(lines))\n'
    '                    self.log("Formatando Disco " + str(dn) + " como "\n'
    '                             + fs + "...", is_info=True)\n'
    '                    rr = run_hidden(["diskpart", "/s", str(sp)], timeout=600)\n'
    '                    if rr.returncode == 0:\n'
    '                        self.log("Disco formatado como " + fs + ".",\n'
    '                                 is_success=True)\n'
    '                        self._popup_success("OK",\n'
    '                            "Disco " + str(dn) + " formatado como " + fs + ".")\n'
    '                        try:\n'
    '                            self.refresh_drives()\n'
    '                        except Exception:\n'
    '                            pass\n'
    '                    else:\n'
    '                        self.log("DiskPart erro.", is_error=True)\n'
    '                finally:\n'
    '                    try:\n'
    '                        sp.unlink(missing_ok=True)\n'
    '                    except Exception:\n'
    '                        pass\n'
    '            else:\n'
    '                dev = d.get("DevicePath", "")\n'
    '                if not dev or not os.path.exists(dev):\n'
    '                    self._popup_warning("Invalido", "Caminho: " + dev)\n'
    '                    return\n'
    '                fs_map = {"NTFS": "ntfs", "FAT32": "vfat", "EXFAT": "exfat",\n'
    '                          "EXT4": "ext4", "EXT3": "ext3", "EXT2": "ext2"}\n'
    '                mkfs_fs = fs_map.get(fs, fs.lower())\n'
    '                part = dev + "1" if not dev[-1:].isdigit() else dev\n'
    '                cmd = ("sudo umount " + dev + "* 2>/dev/null; "\n'
    '                       "sudo mkfs." + mkfs_fs + " -F -L PENBOOT " + part\n'
    '                       + "; sudo sync")\n'
    '                _launch_terminal(cmd, shell="bash")\n'
    '\n'
)

# P8 — Orb translúcido (só parte interna do _draw)
P8_REGEX = r'(        alpha = ORB_TRANSLUCENCY\n.*?)(?=\n        if self\._focused)'
# Não substituímos P8 por regex; usamos um approach mais conservador.

# P9 — Logo glow (aproximação por simple replace)
P9_FIND = (
    '        if GLOBAL_PULSE_STATE[\'active\']:\n'
    '            base = COLORS[\'accent\']\n'
    '            c1 = self._pulse(base, 220)\n'
    '            c2 = self._pulse(COLORS[\'accent2\'], 200)\n'
    '            self._icon_lbl.configure(fg=c1)\n'
    '            self._text_lbl.configure(fg=c1)\n'
    '            self._ver_lbl.configure(fg=c2)\n'
    '            self._hint_lbl.configure(fg=c2)'
)
P9_REPL = (
    '        if GLOBAL_PULSE_STATE[\'active\']:\n'
    '            base = COLORS[\'accent\']\n'
    '            c1 = self._pulse(base, 240)\n'
    '            c2 = self._pulse(COLORS[\'accent2\'], 220)\n'
    '            try:\n'
    '                c_glow = _lighten_hex(c1, 30)\n'
    '                c_shadow = _darken_hex(c2, 40)\n'
    '            except Exception:\n'
    '                c_glow = c1\n'
    '                c_shadow = c2\n'
    '            self._icon_lbl.configure(fg=c1)\n'
    '            self._text_lbl.configure(fg=c_glow)\n'
    '            self._ver_lbl.configure(fg=c2)\n'
    '            self._hint_lbl.configure(fg=c_shadow)'
)


def main():
    print()
    print("=" * 62)
    print("  DARKPENBOOT PRO — PATCHER v3.6.1c (ultra-safe)")
    print("=" * 62)

    if not TARGET.exists():
        print(f"❌ Não encontrado: {TARGET}")
        sys.exit(1)

    src = TARGET.read_text(encoding="utf-8")
    orig_lines = src.count("\n") + 1
    print(f"\nArquivo: {TARGET}")
    print(f"Linhas:  {orig_lines}")
    print(f"Sintaxe: ", end="")
    try:
        ast.parse(src)
        print("OK")
    except SyntaxError as e:
        print(f"ERRO linha {e.lineno}: {e.msg}")
        sys.exit(1)

    # Backup
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = TARGET.parent / f"{TARGET.stem}_v361c_BACKUP_{ts}.py"
    shutil.copy2(TARGET, bak)
    print(f"Backup:  {bak.name}\n")

    # Patches — (nome, dados, usar_regex)
    PATCHES = [
        ("P0-FixSyntax",     P0,     False),
        ("P1-Constantes",    P1,     False),
        ("P3-ShellScan",     P3,     False),
        ("P4-RefreshDrive",  P4_REGEX, True),
        ("P5-Identify",      P5_REGEX, True),
        ("P6-Diskpart",      P6_REGEX, True),
        ("P7-FormatFS",      P7_REGEX, True),
        ("P9-LogoGlow",      (P9_FIND, P9_REPL), False),
    ]

    current = src
    ok_count = 0
    fails = []

    for name, data, use_regex in PATCHES:
        if isinstance(data, tuple):
            pattern, replacement = data
        else:
            pattern = data
            replacement = data

        current, ok = apply_patch(current, name, pattern, replacement, use_regex)
        if ok:
            ok_count += 1
        else:
            fails.append(name)

    # Salvar
    print()
    if ok_count > 0:
        TARGET.write_text(current, encoding="utf-8")
        new_lines = current.count("\n") + 1
        print(f"✅ Arquivo salvo: {TARGET}")
        print(f"   Linhas: {orig_lines} → {new_lines} (Δ {new_lines - orig_lines:+d})")
    else:
        print("⚠️  Nenhum patch aplicado — arquivo NÃO foi modificado.")
        sys.exit(1)

    print()
    print("=" * 62)
    print(f"  Aplicados: {ok_count}/{len(PATCHES)}")
    if fails:
        print(f"  Falharam:  {', '.join(fails)}")
    print("=" * 62)
    print()
    print("Para testar:")
    print(f"  python {TARGET.name}")
    print()
    print(f"Para restaurar backup:")
    print(f"  Copy-Item '{bak.name}' '{TARGET.name}' -Force")
    print()


if __name__ == "__main__":
    main()