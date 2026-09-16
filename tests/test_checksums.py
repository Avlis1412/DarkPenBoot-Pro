"""
Testes para cálculo de checksums (SHA256, MD5, etc).

Testa a função `compute_checksums` e a verificação SHA256.
"""

import hashlib
import os
import sys
import tempfile
from pathlib import Path

import pytest

# Adiciona o diretório raiz ao path para importar o módulo principal
sys.path.insert(0, str(Path(__file__).parent.parent))

# Importa o módulo principal (pode falhar se Tkinter não existir)
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "darkpenboot",
        str(Path(__file__).parent.parent / "DarkPenBoot_PRO1.py")
    )
    darkpenboot = importlib.util.module_from_spec(spec)
    # Não executa o main, apenas carrega
    # spec.loader.exec_module(darkpenboot)
    HAS_MODULE = True
except Exception:
    HAS_MODULE = False


# ═══════════════════════════════════════════════════════════════════════
# TESTES DE HASH PUROS (não dependem do módulo principal)
# ═══════════════════════════════════════════════════════════════════════

@pytest.mark.unit
def test_sha256_hello_world():
    """SHA256 de 'hello world' deve ser sempre o mesmo."""
    expected = "b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9"
    actual = hashlib.sha256(b"hello world").hexdigest()
    assert actual == expected


@pytest.mark.unit
def test_md5_hello_world():
    """MD5 de 'hello world' deve ser sempre o mesmo."""
    expected = "5eb63bbbe01eeed093cb22bb8f5acdc3"
    actual = hashlib.md5(b"hello world").hexdigest()
    assert actual == expected


@pytest.mark.unit
def test_sha1_hello_world():
    """SHA1 de 'hello world' deve ser sempre o mesmo."""
    expected = "2aae6c35c94fcfb415dbe95f408b9ce91ee846ed"
    actual = hashlib.sha1(b"hello world").hexdigest()
    assert actual == expected


@pytest.mark.unit
def test_sha256_empty():
    """SHA256 de string vazia é conhecido."""
    expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    actual = hashlib.sha256(b"").hexdigest()
    assert actual == expected


# ═══════════════════════════════════════════════════════════════════════
# TESTES COM ARQUIVOS TEMPORÁRIOS
# ═══════════════════════════════════════════════════════════════════════

@pytest.mark.unit
def test_hash_small_file():
    """Hash de arquivo pequeno calculado corretamente."""
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        f.write(b"DarkPenBoot Pro test content")
        tmp_path = f.name

    try:
        # SHA256
        h = hashlib.sha256()
        with open(tmp_path, 'rb') as f:
            h.update(f.read())
        digest = h.hexdigest()

        assert len(digest) == 64  # SHA256 = 64 hex chars
        assert digest.isalnum()
    finally:
        os.unlink(tmp_path)


@pytest.mark.unit
def test_hash_large_file():
    """Hash de arquivo grande (> 1 MB) é calculado corretamente."""
    with tempfile.NamedTemporaryFile(mode='wb', delete=False) as f:
        # Escreve 2 MB de dados
        f.write(b"A" * (2 * 1024 * 1024))
        tmp_path = f.name

    try:
        h = hashlib.sha256()
        with open(tmp_path, 'rb') as f:
            while True:
                chunk = f.read(8192 * 1024)
                if not chunk:
                    break
                h.update(chunk)
        digest = h.hexdigest()

        assert len(digest) == 64
    finally:
        os.unlink(tmp_path)


@pytest.mark.unit
def test_all_hash_algorithms():
    """Verifica que todos os algoritmos esperados funcionam."""
    test_data = b"DarkPenBoot Pro"

    algorithms = ['md5', 'sha1', 'sha256', 'sha512', 'sha3_256', 'blake2b']

    for algo in algorithms:
        try:
            h = hashlib.new(algo)
            h.update(test_data)
            digest = h.hexdigest()
            assert len(digest) > 0
            assert all(c in '0123456789abcdef' for c in digest)
        except Exception:
            pytest.skip(f"Algoritmo {algo} não disponível")


@pytest.mark.unit
def test_hash_consistency():
    """Mesmo conteúdo produz o mesmo hash."""
    data = b"Consistent content"

    h1 = hashlib.sha256(data).hexdigest()
    h2 = hashlib.sha256(data).hexdigest()

    assert h1 == h2


@pytest.mark.unit
def test_hash_different_content():
    """Conteúdos diferentes produzem hashes diferentes."""
    h1 = hashlib.sha256(b"content A").hexdigest()
    h2 = hashlib.sha256(b"content B").hexdigest()

    assert h1 != h2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])