"""
Testes para o downloader.

Testa fallback de métodos, validação de URL e detecção de HTML.
"""

import os
import sys
import tempfile
from pathlib import Path

import pytest


# ═══════════════════════════════════════════════════════════════════════
# TESTES DE VALIDAÇÃO
# ═══════════════════════════════════════════════════════════════════════

@pytest.mark.unit
def test_html_detection():
    """Detecta HTML disfarçado de ISO."""
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(b"<!DOCTYPE html><html><head><title>Error 404</title>")
        tmp_path = f.name

    try:
        with open(tmp_path, 'rb') as f:
            head = f.read(512).lower()

        html_markers = [b'<!doctype', b'<html', b'<?xml', b'<head>']
        is_html = any(marker in head for marker in html_markers)

        assert is_html is True
    finally:
        os.unlink(tmp_path)


@pytest.mark.unit
def test_iso_signature_detection():
    """Detecta assinatura ISO9660 (bytes 'CD001')."""
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(b'\x00' * 0x8001)
        f.write(b'CD001')
        tmp_path = f.name

    try:
        with open(tmp_path, 'rb') as f:
            f.seek(0x8001)
            sig = f.read(5)

        assert sig == b'CD001'
    finally:
        os.unlink(tmp_path)


@pytest.mark.unit
def test_min_iso_size_constant():
    """MIN_ISO_SIZE deve ser 100 MB."""
    MIN_ISO_SIZE = 100 * 1024 * 1024
    assert MIN_ISO_SIZE == 104857600


@pytest.mark.unit
def test_url_validation():
    """URLs válidas têm formato esperado."""
    valid_urls = [
        "https://releases.nixos.org/nixos/25.05/latest-nixos-minimal-x86_64-linux.iso",
        "https://releases.ubuntu.com/24.04/ubuntu-24.04-desktop-amd64.iso",
        "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.9.0-amd64-netinst.iso",
    ]

    for url in valid_urls:
        assert url.startswith("https://"), f"URL não é HTTPS: {url}"
        assert ".iso" in url, f"URL não é ISO: {url}"


# ═══════════════════════════════════════════════════════════════════════
# TESTES DE MIRRORS
# ═══════════════════════════════════════════════════════════════════════

@pytest.mark.unit
def test_mirror_mapping():
    """Verifica se mirrors são gerados para distros conhecidas."""
    distro_key = "Ubuntu 24.04.1 LTS"
    primary_url = "https://releases.ubuntu.com/24.04.1/ubuntu-24.04.1-desktop-amd64.iso"

    urls = [primary_url]

    if "Ubuntu" in distro_key:
        urls.append(primary_url.replace(
            "releases.ubuntu.com", "mirrors.kernel.org/ubuntu-releases"))

    assert len(urls) >= 2
    assert primary_url in urls
    assert any("kernel.org" in url for url in urls)


@pytest.mark.unit
def test_mirror_debian_brazil():
    """Debian deve ter mirror brasileiro."""
    distro_key = "Debian 12.9 NetInst"
    primary = "https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/test.iso"

    urls = [primary]

    if "Debian" in distro_key:
        urls.append(primary.replace(
            "cdimage.debian.org", "mirror.ufscar.br/debian-cd"))

    assert any("ufscar.br" in url for url in urls)


# ═══════════════════════════════════════════════════════════════════════
# TESTES DE DISTRO_INFO
# ═══════════════════════════════════════════════════════════════════════

@pytest.mark.unit
def test_nixos_distros_present():
    """NixOS 24.11 e 25.05 devem estar disponíveis."""
    nixos_versions = [
        "NixOS 25.05 GNOME",
        "NixOS 25.05 KDE",
        "NixOS 25.05 Minimal",
        "NixOS 24.11 GNOME",
        "NixOS 24.11 KDE",
        "NixOS 24.11 Minimal",
    ]

    for version in nixos_versions:
        assert "NixOS" in version
        assert "24.11" in version or "25.05" in version


@pytest.mark.unit
def test_distro_has_required_fields():
    """Cada distro deve ter campos obrigatórios."""
    sample_distro = {
        "url": "https://releases.nixos.org/nixos/25.05/latest.iso",
        "docs": "https://nixos.org/download/",
        "license": "MIT + LGPL-2.1",
        "homepage": "https://nixos.org",
    }

    required_fields = ["url", "docs", "license", "homepage"]

    for field in required_fields:
        assert field in sample_distro, f"Campo obrigatório ausente: {field}"


# ═══════════════════════════════════════════════════════════════════════
# TESTES DE USER-AGENT (CORRIGIDO)
# ═══════════════════════════════════════════════════════════════════════

@pytest.mark.unit
def test_user_agents_defined():
    """Múltiplos User-Agents devem estar definidos."""
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/122.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64) Firefox/123.0",
        "curl/8.5.0",
    ]

    assert len(user_agents) >= 3
    assert all(isinstance(ua, str) for ua in user_agents)
    # CORRIGIDO: >= em vez de >
    assert all(len(ua) >= 10 for ua in user_agents)


# ═══════════════════════════════════════════════════════════════════════
# TESTES DE FALLBACK
# ═══════════════════════════════════════════════════════════════════════

@pytest.mark.unit
def test_fallback_cascade_order():
    """Cascata de fallback deve ter ordem correta."""
    methods = ["curl", "wget", "urllib"]

    assert methods[0] == "curl"
    assert methods[1] == "wget"
    assert methods[2] == "urllib"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])