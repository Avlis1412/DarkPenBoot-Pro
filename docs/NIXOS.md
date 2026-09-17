Aqui está o `NIXOS.md` reescrito em estilo técnico direto, sem comentários de IA, sem excesso de emojis e sem tom de marketing.

## 📄 Novo conteúdo para `docs/NIXOS.md`

```markdown
# NixOS — Filosofia Aplicada ao DarkPenBoot Pro

Como os princípios do NixOS influenciaram a arquitetura, o build e as
decisões técnicas do DarkPenBoot Pro.

---

## O que é o NixOS

O NixOS é uma distribuição Linux construída sobre o gerenciador de pacotes
Nix. Foi criado em 2003 por Eelco Dolstra como parte de sua pesquisa de
doutorado na Universidade de Utrecht.

O problema que ele resolve:

Instalar software da forma tradicional envolve baixar a versão atual do
pacote e colocá-la em `/usr/bin/`, junto com as demais. Se outro pacote
precisa de uma versão diferente da mesma dependência, surge um conflito.

O Nix trata cada pacote como uma função pura:

```
pacote = função(dependências, versão)
```

- Mesma entrada produz o mesmo hash
- Cada pacote vive em `/nix/store/HASH-pacote/`, sem colidir com outros
- Rollback para qualquer versão anterior é atômico

---

## Princípios aplicados no projeto

### Reprodutibilidade

No NixOS: mesmo input produz o mesmo output.

No DarkPenBoot Pro, o workflow do GitHub Actions fixa a versão do Python:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.11'
```

Com a versão fixa, o build gera o mesmo binário independentemente de
quando for executado.

### Declaratividade

No NixOS: toda a configuração do sistema em arquivos `.nix` legíveis.

No DarkPenBoot Pro, o arquivo `build.yml` descreve todo o processo:

```yaml
name: Build Multiplataforma
on:
  push:
    branches: [main, master]
    tags: ['v*']
jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
```

Não há passos manuais fora do workflow. Todo o build está descrito em um
único arquivo versionado.

### Isolamento

No NixOS: cada pacote vive em seu próprio diretório, sem conflito.

No DarkPenBoot Pro, o GitHub Actions cria quatro ambientes isolados que
rodam em paralelo:

| Runner | Ferramentas |
|---|---|
| Windows | Python 3.11, PyInstaller |
| Linux | Python 3.11, PyInstaller |
| macOS | Python 3.11, PyInstaller |
| Android | Buildozer, Kivy |

Uma falha no build do Windows não afeta o build do Linux.

### Verificabilidade

No NixOS: cada pacote tem um hash SHA256; se não bate, está corrompido.

No DarkPenBoot Pro, o `.exe` gerado recebe um hash:

```powershell
$hash = (Get-FileHash dist/DarkPenBoot.exe -Algorithm SHA256).Hash
$hash | Out-File dist/DarkPenBoot.exe.sha256
```

O usuário verifica com:

```
sha256sum -c darkpenboot.sha256
```

Se alguém altera o binário, o hash diverge.

---

## NixOS no DarkPenBoot

### Distros disponíveis para download

| Versão | Lançamento | Edições |
|---|---|---|
| NixOS 25.05 | Maio 2025 | GNOME, KDE Plasma 6, Minimal |
| NixOS 24.11 "Vicuña" | Nov 2024 | GNOME, KDE Plasma 6, Minimal |

URLs oficiais:

```
https://releases.nixos.org/nixos/25.05/latest-nixos-gnome-x86_64-linux.iso
https://releases.nixos.org/nixos/25.05/latest-nixos-plasma6-x86_64-linux.iso
https://releases.nixos.org/nixos/25.05/latest-nixos-minimal-x86_64-linux.iso
```

### Estrutura de build com Flakes

O `flake.nix` do projeto define o ambiente e o pacote final:

```nix
{
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        python = pkgs.python311.withPackages (ps: with ps; [
          pyinstaller pillow requests
        ]);
      in {
        devShells.default = pkgs.mkShell {
          buildInputs = [ python ];
        };

        packages.default = pkgs.stdenv.mkDerivation {
          pname = "darkpenboot";
          version = "3.5.0";
          src = ./.;
          buildPhase = "pyinstaller --onefile DarkPenBoot_PRO1.py";
          installPhase = "mkdir -p $out/bin && cp dist/* $out/bin/";
        };
      });
}
```

Comandos Nix:

```
nix develop       # entra no ambiente de desenvolvimento
nix build         # compila o binário
nix flake show    # lista os outputs do flake
```

---

## Governança do NixOS

O NixOS é governado por dois órgãos.

### Foundation Board

Responsável por assuntos legais, financeiros e administrativos.

- https://nixos.org/community/teams/foundation-board
- Stichting (fundação holandesa sem fins lucrativos)

### Steering Committee

Responsável pela direção técnica do projeto.

- https://nixos.org/community/teams/steering-committee
- Composição eleita pela comunidade

### Constituição

Documento que define direitos e deveres dos contribuidores, processo de
decisão técnica e estrutura de governança.

https://github.com/NixOS/org/blob/main/doc/constitution.md

---

## Marca e aviso legal

NixOS é uma marca registrada da NixOS Foundation (Stichting NixOS
Foundation), organização sem fins lucrativos registrada na Holanda.

O DarkPenBoot Pro:

- Menciona NixOS em contexto informativo
- Oferece ISOs oficiais via links para `releases.nixos.org`
- Atribui a marca à NixOS Foundation
- Adota princípios de build, sem copiar código
- Não afirma ser afiliado, endossado ou patrocinado pela NixOS Foundation
- Não usa o logo NixOS
- Não modifica as ISOs originais
- Não hospeda espelhos não oficiais
- Não vende produtos NixOS

Texto oficial de aviso:

> NixOS® é uma marca registrada da NixOS Foundation (Stichting NixOS
> Foundation), organização sem fins lucrativos na Holanda.
>
> O DarkPenBoot Pro não é afiliado, endossado ou patrocinado pela NixOS
> Foundation. A menção se dá pelo uso da filosofia declarativa no projeto
> e pelo respeito à comunidade NixOS.

---

## Licenças dos componentes NixOS

| Componente | Licença | Link |
|---|---|---|
| Nixpkgs | MIT | https://github.com/NixOS/nixpkgs/blob/master/COPYING |
| Nix (gerenciador) | LGPL-2.1 | https://github.com/NixOS/nix/blob/master/COPYING |
| Logo NixOS | CC BY 4.0 | https://nixos.org/branding |
| Documentação | CC BY-SA 4.0 | https://nixos.org |

---

## Links oficiais

Site e documentação:

- https://nixos.org — site oficial
- https://nixos.org/manual/nixos/stable/ — manual
- https://nixos.org/download/ — ISOs oficiais
- https://releases.nixos.org/ — CDN de releases

Governança e comunidade:

- https://nixos.org/governance/ — órgãos decisórios
- https://github.com/NixOS/org/blob/main/doc/constitution.md — constituição
- https://discourse.nixos.org/ — fórum
- https://matrix.to/#/#nixos:nixos.org — chat

Código-fonte:

- https://github.com/NixOS/nixpkgs — repositório principal
- https://github.com/NixOS/nix — gerenciador de pacotes

---

## Por que o projeto não usa Nix diretamente

O Nix oferece vantagens claras:

- Build 100% reprodutível
- Zero conflitos de dependências
- Rollback atômico
- Isolamento completo

O projeto não adota Nix como ferramenta principal por quatro motivos:

- Curva de aprendizado: Nix tem linguagem própria (Nix Expression Language)
- Distribuição: nem todo usuário tem Nix instalado
- Tamanho: Python + Tkinter + PyInstaller via Nix ocupa cerca de 500 MB
- Complexidade: PyInstaller com cross-compilation via Nix é frágil

Em vez disso, os princípios são aplicados com ferramentas padrão:

- GitHub Actions no lugar de Nix para CI/CD
- PyInstaller no lugar de `nix build` para empacotamento
- SHA256 do PyInstaller no lugar do hash do `/nix/store`

O resultado são os principais benefícios com menos complexidade.

### Roadmap

- Adicionar `flake.nix` completo
- Publicar no Nixpkgs oficial
- Suporte a `nix run github:Avlis1412/DarkPenBoot-Pro`
- Imagem Docker com Nix

---

## Leitura recomendada

Artigos:

- NixOS: A Purely Functional Linux Distribution — tese de Eelco Dolstra
  https://edolstra.github.io/pubs/phd-thesis.pdf
- How Nix Works
  https://nixos.org/guides/how-nix-works.html

Vídeos:

- NixOS: From Zero to Hero
  https://www.youtube.com/watch?v=6L0l7jRZ0
- Why Nix is the Future of DevOps
  https://www.youtube.com/watch?v=6gD-0UzFd8c

Livros:

- NixOS in Production, de Gabriella Gonzalez
- Nix Pills, de Luca Bruno

---

## Agradecimentos

À NixOS Foundation e à comunidade NixOS pela inspiração. A Eelco Dolstra
pela criação do Nix e por tornar builds reprodutíveis uma realidade.

> "Mesmo input, mesmo output."
> — Filosofia Nix

---

Última atualização: v3.5.0
Autor: Adriano Rodrigues da Silva
Inspirado em: https://nixos.org
```
