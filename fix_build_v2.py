import os

def fix_buildozer_spec():
    caminho = 'buildozer.spec'
    if not os.path.exists(caminho):
        print(f"❌ Erro: {caminho} não encontrado.")
        return
    
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # 1. Forçar Kivy 2.2.1 para evitar o bug do libthorvg
    if 'kivy==2.3.0' in conteudo:
        conteudo = conteudo.replace('kivy==2.3.0', 'kivy==2.2.1')
        print("✅ Kivy alterado para 2.2.1")
    elif 'kivy==2.2.1' not in conteudo:
        conteudo = conteudo.replace('kivy,', 'kivy==2.2.1,').replace('kivy\n', 'kivy==2.2.1\n')
        print("✅ Kivy forçado para 2.2.1")

    # 2. Reduzir log_level para evitar truncamento
    conteudo = conteudo.replace('log_level = 2', 'log_level = 1')

    # 3. Excluir pastas de ambientes virtuais pesados
    if 'kivy_venv' not in conteudo.split('source.exclude_patterns =')[1].split('\n')[0]:
        conteudo = conteudo.replace(
            'source.exclude_patterns = ',
            'source.exclude_patterns = kivy_venv,venv312,'
        )
        print("✅ Pastas kivy_venv e venv312 excluídas do build")

    # 4. Forçar apenas arquitetura arm64-v8a (mais rápido e evita erro de memória)
    if 'android.archs = arm64-v8a, armeabi-v7a' in conteudo:
        conteudo = conteudo.replace(
            'android.archs = arm64-v8a, armeabi-v7a',
            'android.archs = arm64-v8a'
        )
        print("✅ Arquitetura reduzida para apenas arm64-v8a")

    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print("✅ buildozer.spec corrigido com sucesso.")

def fix_workflow_github():
    caminho = '.github/workflows/build.yml'
    if not os.path.exists(caminho):
        print(f"❌ Erro: {caminho} não encontrado.")
        return

    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # 1. Remover o -v do comando (Essa é a causa do log gigante!)
    conteudo = conteudo.replace(
        'yes | buildozer -v android debug',
        'yes | buildozer android debug'
    )
    print("✅ Flag -v removida do buildozer")

    # 2. Invalidar o cache (v4 para v5)
    conteudo = conteudo.replace(
        "key: buildozer-v2-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}",
        "key: buildozer-v5-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}"
    )
    conteudo = conteudo.replace(
        "key: buildozer-v3-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}",
        "key: buildozer-v5-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}"
    )
    conteudo = conteudo.replace(
        "key: buildozer-v4-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}",
        "key: buildozer-v5-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}"
    )
    print("✅ Cache do GitHub invalidado para v5")

    # 3. Garantir que o Cython não seja menor que 3
    conteudo = conteudo.replace(
        'pip install --upgrade "cython<3" buildozer',
        'pip install --upgrade cython buildozer'
    )

    # 4. Adicionar dependências de sistema ausentes
    if 'libltdl-dev' not in conteudo:
        conteudo = conteudo.replace(
            'libtinfo5 cmake libffi-dev libssl-dev automake',
            'libtinfo5 cmake libffi-dev libssl-dev automake libltdl-dev python3-dev'
        )
        print("✅ Dependências libltdl-dev e python3-dev adicionadas")

    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print("✅ build.yml corrigido com sucesso.")

if __name__ == "__main__":
    print("🚀 Iniciando correção DEFINITIVA...")
    fix_buildozer_spec()
    fix_workflow_github()
    print("🎉 Tudo pronto! Agora faça o commit e push.")