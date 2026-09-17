import os

def debug_buildozer_spec():
    caminho = 'buildozer.spec'
    if not os.path.exists(caminho):
        print(f"❌ Erro: {caminho} não encontrado.")
        return
    
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # 1. Aumentar o log para 2 TEMPORARIAMENTE para vermos o erro real
    if 'log_level = 1' in conteudo:
        conteudo = conteudo.replace('log_level = 1', 'log_level = 2')
        print("⚠️ log_level alterado para 2 (temporário para debug)")
    
    # 2. Garantir que os venvs continuam excluídos
    if 'kivy_venv' not in conteudo.split('source.exclude_patterns =')[1].split('\n')[0]:
        conteudo = conteudo.replace(
            'source.exclude_patterns = ',
            'source.exclude_patterns = kivy_venv,venv312,'
        )

    # 3. Manter apenas arm64-v8a
    if 'android.archs = arm64-v8a, armeabi-v7a' in conteudo:
        conteudo = conteudo.replace(
            'android.archs = arm64-v8a, armeabi-v7a',
            'android.archs = arm64-v8a'
        )

    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print("✅ buildozer.spec atualizado para debug.")

def fix_workflow_dependencies():
    caminho = '.github/workflows/build.yml'
    if not os.path.exists(caminho):
        print(f"❌ Erro: {caminho} não encontrado.")
        return

    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # Adicionar libtool-bin se não existir
    if 'libtool-bin' not in conteudo:
        conteudo = conteudo.replace(
            'libltdl-dev python3-dev',
            'libltdl-dev python3-dev libtool-bin'
        )
        print("✅ libtool-bin adicionado às dependências do sistema")

    # Limpar o cache novamente (v6)
    conteudo = conteudo.replace(
        "key: buildozer-v5-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}",
        "key: buildozer-v6-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}"
    )

    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print("✅ build.yml atualizado (cache v6, libtool-bin).")

if __name__ == "__main__":
    print("🚀 Iniciando correção de DEPURAÇÃO...")
    debug_buildozer_spec()
    fix_workflow_dependencies()
    print("🎉 Pronto! Faça o commit e push para vermos o erro real.")