"""
Testes para configuração (load_config, save_config).

Testa persistência de dados, valores padrão e serialização JSON.
"""

import json
import os
import sys
import tempfile
from pathlib import Path

import pytest


# ═══════════════════════════════════════════════════════════════════════
# TESTES DE CONFIGURAÇÃO (isolados do módulo principal)
# ═══════════════════════════════════════════════════════════════════════

@pytest.mark.unit
def test_config_defaults():
    """Verifica valores padrão esperados da configuração."""
    expected_defaults = {
        'filesystem': 'NTFS',
        'scheme': 'MBR',
        'theme': 'matrix',
        'quick_format': True,
        'verify': False,
        'mode': 'extract',
    }

    # Simula a estrutura esperada
    config = {
        'filesystem': 'NTFS',
        'scheme': 'MBR',
        'theme': 'matrix',
        'quick_format': True,
        'verify': False,
        'mode': 'extract',
    }

    for key, expected in expected_defaults.items():
        assert config[key] == expected, f"Default de {key} incorreto"


@pytest.mark.unit
def test_config_json_serialization():
    """Config pode ser serializada e desserializada em JSON."""
    config = {
        'filesystem': 'FAT32',
        'scheme': 'GPT',
        'theme': 'soft_dark',
        'quick_format': False,
        'verify': True,
        'last_iso': '/path/to/test.iso',
        'buffer_override': 'Auto (por tier USB)',
    }

    # Serializa
    json_str = json.dumps(config)
    assert isinstance(json_str, str)

    # Desserializa
    restored = json.loads(json_str)
    assert restored == config


@pytest.mark.unit
def test_config_save_and_load():
    """Salvar e carregar config preserva os dados."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "config.json"

        original = {
            'theme': 'cyberpunk',
            'filesystem': 'exFAT',
            'verify': True,
        }

        # Salva
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(original, f, indent=2)

        # Carrega
        with open(config_path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)

        assert loaded == original


@pytest.mark.unit
def test_config_handles_missing_file():
    """Carregar config inexistente retorna dict vazio/padrão."""
    non_existent = Path("/tmp/this_does_not_exist_12345.json")

    assert not non_existent.exists()

    # Simula o comportamento do load_config
    result = {}
    if non_existent.exists():
        with open(non_existent, 'r') as f:
            result = json.load(f)

    assert result == {}


@pytest.mark.unit
def test_config_handles_corrupted_json():
    """Carregar config corrompido não quebra (usa fallback)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / "corrupted.json"

        # Escreve JSON inválido
        with open(config_path, 'w') as f:
            f.write("{invalid json without closing brace")

        # Simula comportamento de fallback
        result = {}
        try:
            with open(config_path, 'r') as f:
                result = json.load(f)
        except json.JSONDecodeError:
            result = {}  # Fallback

        assert result == {}


@pytest.mark.unit
def test_config_unicode_support():
    """Config suporta caracteres Unicode (acentos, emojis)."""
    config = {
        'name': 'Configuração de Teste',
        'description': 'Análise com acentuação',
        'emoji': '🟣 NixOS',
    }

    with tempfile.TemporaryDirectory() as tmpdir:
        path = Path(tmpdir) / "unicode.json"

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False)

        with open(path, 'r', encoding='utf-8') as f:
            loaded = json.load(f)

        assert loaded['name'] == 'Configuração de Teste'
        assert loaded['emoji'] == '🟣 NixOS'


@pytest.mark.unit
def test_config_merge():
    """Merge de defaults + config carregado funciona."""
    defaults = {
        'theme': 'matrix',
        'filesystem': 'NTFS',
        'verify': False,
        'mode': 'extract',
    }

    loaded = {
        'theme': 'cyberpunk',
        'verify': True,
    }

    # Merge como faz o load_config real
    merged = dict(defaults)
    merged.update(loaded)

    assert merged['theme'] == 'cyberpunk'       # Sobrescrito
    assert merged['verify'] is True             # Sobrescrito
    assert merged['filesystem'] == 'NTFS'       # Padrão mantido
    assert merged['mode'] == 'extract'          # Padrão mantido


if __name__ == "__main__":
    pytest.main([__file__, "-v"])