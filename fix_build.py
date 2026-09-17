import os

def corrigir_buildozer_spec():
    caminho = 'buildozer.spec'
    if not os.path.exists(caminho):
        print(f"❌ Erro: {caminho} não encontrado.")
        return
    
    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # 1. Mudar a versão do Kivy para 2.2.1 (remove a dependência do libthorvg)
    conteudo = conteudo.replace('kivy==2.3.0', 'kivy==2.2.1')

    # 2. Reduzir verbosidade do log (já feito, mas garantindo)
    conteudo = conteudo.replace('log_level = 2', 'log_level = 1')
    
    # 3. Excluir ambientes virtuais pesados (já feito, mas garantindo)
    if 'kivy_venv' not in conteudo.split('source.exclude_patterns =')[1].split('\n')[0]:
        conteudo = conteudo.replace(
            'source.exclude_patterns = ',
            'source.exclude_patterns = kivy_venv,venv312,'
        )
    
    # 4. Garantir que apenas arm64-v8a seja compilado
    if 'android.archs = arm64-v8a, armeabi-v7a' in conteudo:
        conteudo = conteudo.replace(
            'android.archs = arm64-v8a, armeabi-v7a',
            'android.archs = arm64-v8a'
        )

    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print("✅ buildozer.spec atualizado (kivy==2.2.1, arm64-v8a apenas).")

def corrigir_workflow_github():
    caminho = '.github/workflows/build.yml'
    if not os.path.exists(caminho):
        print(f"❌ Erro: {caminho} não encontrado.")
        return

    with open(caminho, 'r', encoding='utf-8') as f:
        conteudo = f.read()

    # 1. Invalidar o cache (v4) para forçar download limpo
    conteudo = conteudo.replace(
        "key: buildozer-v3-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}",
        "key: buildozer-v4-${{ runner.os }}-${{ hashFiles('buildozer.spec') }}"
    )

    # 2. Garantir que o Cython está na versão 3 (Kivy 2.2.1 também funciona)
    conteudo = conteudo.replace(
        'pip install --upgrade "cython<3" buildozer',
        'pip install --upgrade cython buildozer'
    )

    # 3. Adicionar dependências de sistema
    if 'libltdl-dev' not in conteudo:
        conteudo = conteudo.replace(
            'libtinfo5 cmake libffi-dev libssl-dev automake',
            'libtinfo5 cmake libffi-dev libssl-dev automake libltdl-dev python3-dev'
        )

    # 4. Remover o -v para não truncar o log
    conteudo = conteudo.replace(
        'yes | buildozer -v android debug',
        'yes | buildozer android debug'
    )

    with open(caminho, 'w', encoding='utf-8') as f:
        f.write(conteudo)
    print("✅ build.yml atualizado (cache v4, sem -v).")

if __name__ == "__main__":
    print("🚀 Iniciando script de correção DEFINITIVO (v2)...")
    corrigir_buildozer_spec()
    corrigir_workflow_github()
    print("🎉 Correções aplicadas com sucesso!")