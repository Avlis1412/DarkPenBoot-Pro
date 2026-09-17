# -*- coding: utf-8 -*-
"""Analise do codigo-fonte do DarkPenBoot Pro."""
import os
import ast
from pathlib import Path

PROJECT = r"C:\Users\adria_0kkmcbe\OneDrive\Desktop\DarkPenBoot-Pro"
IGNORE_DIRS = {'.git', 'venv312', 'venv312_mobile', '__pycache__',
               '.vscode', 'darkpenboot.egg-info', 'build', 'dist',
               '.buildozer', 'releases', 'docs', 'tests', 'mobile'}

def analyze_python(fp):
    try:
        with open(fp, 'r', encoding='utf-8') as f:
            src = f.read()
        lines = src.count('\n') + 1
        tree = ast.parse(src)
        imports, funcs, classes = set(), 0, 0
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for n in node.names:
                    imports.add(n.name.split('.')[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split('.')[0])
            elif isinstance(node, ast.FunctionDef):
                funcs += 1
            elif isinstance(node, ast.ClassDef):
                classes += 1
        return lines, sorted(imports), funcs, classes, None
    except SyntaxError as e:
        return 0, [], 0, 0, f"SyntaxError: {e}"
    except Exception as e:
        return 0, [], 0, 0, str(e)

def read_buildozer_source():
    """Le qual é o source.include_extensions e source.dir do buildozer.spec."""
    spec = os.path.join(PROJECT, "buildozer.spec")
    if not os.path.exists(spec):
        return None, None
    src_dir, main_py = ".", "main.py"
    with open(spec, 'r', encoding='utf-8', errors='replace') as f:
        for line in f:
            line = line.strip()
            if line.startswith("source.dir"):
                src_dir = line.split("=", 1)[1].strip()
            elif line.startswith("source.include_exts"):
                pass
    return src_dir, main_py

def main():
    print(">>> Analise do codigo-fonte")
    print("=" * 60)
    src_dir, main_py = read_buildozer_source()
    print(f"Buildozer source.dir  : {src_dir}")
    print(f"Buildozer main.py     : {main_py}")
    print("=" * 60)

    py_files = []
    for root, dirs, files in os.walk(PROJECT):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS and not d.startswith('.')]
        for f in files:
            if f.endswith('.py'):
                py_files.append(os.path.join(root, f))

    total_lines = 0
    for fp in sorted(py_files):
        rel = os.path.relpath(fp, PROJECT)
        lines, imports, funcs, classes, err = analyze_python(fp)
        total_lines += lines
        if err:
            print(f"[ERRO] {rel}")
            print(f"       {err}")
            continue
        size_kb = os.path.getsize(fp) / 1024
        print(f"\n[PY] {rel}")
        print(f"     {lines} linhas | {funcs} funcs | {classes} classes | {size_kb:.1f} KB")
        if imports:
            print(f"     imports: {', '.join(imports[:12])}")
        is_main = rel == main_py
        print(f"     {'★ ENTRY POINT (buildozer)' if is_main else ''}")

    print("\n" + "=" * 60)
    print(f"TOTAL: {len(py_files)} arquivo(s), {total_lines} linhas de codigo Python")

    # Verificacao de encoding
    print("\n>>> Verificacao de encoding (BOM U+FEFF):")
    for fp in sorted(py_files):
        rel = os.path.relpath(fp, PROJECT)
        with open(fp, 'rb') as f:
            first = f.read(3)
        if first == b'\xef\xbb\xbf':
            print(f"  [BOM] {rel}")
    print("  (nada listado = todos limpos)")

if __name__ == "__main__":
    main()
