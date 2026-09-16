# DarkPenBoot Pro — Constituição do Projeto

Versão: 1.0.0
Ratificada em: 2026-09-15
Última emenda: 2026-09-15
Autor: Adriano Rodrigues da Silva

---

## 🎯 Artigo I — Princípio da Integridade de Mídia (NÃO-NEGOCIÁVEL)

Toda operação de escrita em dispositivo USB DEVE:

1. Validar a ISO **antes** de qualquer formatação (assinatura ISO9660/UDF/ZIP)
2. Rejeitar arquivos HTML/XML mesmo que `>MIN_ISO_SIZE`
3. Verificar SHA256 quando o hash oficial estiver registrado
4. Bloquear escrita em `PhysicalDrive0` no Windows (disco do sistema)
5. Re-verificar o dispositivo alvo por SerialNumber imediatamente antes da gravação

**Justificativa:** danos catastróficos ao usuário são irreversíveis. Um pendrive
formatado erroneamente não pode ser recuperado por esta ferramenta.

---

## 🎯 Artigo II — Compatibilidade Multiplataforma

O código DEVE rodar em:

- Windows 10/11 (x64, ARM64)
- Linux (qualquer distro com Python 3.9+)
- macOS 12+
- Android/Termux (sem ROOT para operações de usuário)
- iOS/iSH (leitura apenas)

**NENHUMA** funcionalidade core pode depender de bibliotecas exclusivas de um SO.
Ferramentas externas (`diskpart`, `parted`, `diskutil`, `mkfs.*`) são aceitáveis
desde que o código degrade graciosamente quando ausentes.

---

## 🎯 Artigo III — Tipagem Estática Rigorosa

Todo o código DEVE:

1. Passar em `mypy --strict` (a partir da v3.5.0)
2. Passar em `Pylance` com `Basic` no mínimo, `Strict` como meta
3. **ZERO** warnings de `reportOptional*` (`reportOptionalMemberAccess`,
   `reportOptionalSubscript`, `reportOptionalIterable`)
4. Usar `Optional[T]` explicitamente sempre que um valor puder ser `None`
5. **NUNCA** usar `# type: ignore` sem comentário justificando

**Meta de cobertura de tipo:** > 95% dos símbolos públicos anotados.

---

## 🎯 Artigo IV — Governança da Marca NixOS

Toda menção a NixOS DEVE:

1. Incluir o texto: *"NixOS® é marca registrada da NixOS Foundation"*
2. Deixar explícito: *"DarkPenBoot Pro NÃO é afiliado, endossado ou patrocinado pela NixOS Foundation"*
3. Linkar a governança oficial: `https://nixos.org/governance/`
4. Não editar, gerar ou validar arquivos `configuration.nix` do usuário
5. Não executar `nixos-rebuild`, `nix-env` nem qualquer comando Nix

**Justificativa:** respeito à [política de marca registrada](https://nixos.org/governance/)
recém-emitida pela NixOS Foundation.

---

## 🎯 Artigo V — Download Robusto e Auditável

Todo download de ISO DEVE:

1. Tentar **múltiplas URLs** (primária + mirrors oficiais)
2. Tentar **múltiplos métodos** (`curl` → `wget` → `urllib`)
3. Detectar **resposta HTML/XML** mascarada como ISO
4. Detectar **estagnação** (> 120s sem progresso) e abortar
5. Registrar em log: URL usada, tamanho, tempo, hash (se aplicável)
6. Suportar **cancelamento** com limpeza de arquivo parcial
7. Nunca reescrever o arquivo `.parcial` em caso de falha de hash

---

## 🎯 Artigo VI — Interface e Acessibilidade

Toda interface DEVE:

1. Ser **totalmente navegável por teclado** (Tab, Setas, Enter, Esc, F1)
2. Ter **tooltips** em todos os controles
3. Respeitar **contraste mínimo** WCAG AA (4.5:1)
4. Aplicar a **filosofia Soft Dark** em todos os 7 temas
5. **NUNCA** animar a menos de 14ms por frame (60fps)
6. **SEMPRE** oferecer ao usuário feedback visual antes de operações destrutivas

---

## 🎯 Artigo VII — Simplicidade e Não-Duplicação

O código DEVE:

1. Ter **exatamente uma** definição por função/classe pública
2. Cada módulo lógico em **um único lugar** do arquivo
3. Nenhuma cópia de seção (regressão v3.4.0 documentada)
4. Comentários explicando o **porquê**, não o **o quê**
5. Sem código morto (`grep` deve retornar zero para funções não chamadas)

**Métrica:** `grep -c "def nome_função" arquivo.py` deve retornar `1` para
toda função.

---

## 🎯 Artigo VIII — Testes Obrigatórios

Toda nova funcionalidade DEVE ter:

1. **Teste unitário** para a lógica pura
2. **Teste de integração** para fluxos com I/O
3. **Teste E2E** (manual documentado) para fluxos com hardware

**Cobertura mínima:** 40% no MVP v3.5.0, 70% até v4.0.0.

Ferramentas obrigatórias:

- `pytest` para testes
- `pytest-cov` para cobertura
- `pytest-mock` para isolar sistema de arquivos e rede
- `hypothesis` para property-based testing de sanitização de caminhos

---

## 🎯 Artigo IX — Licenciamento e Créditos

Toda dependência externa DEVE:

1. Estar listada em `THIRD_PARTY_LICENSES.md`
2. Ter sua licença respeitada nos termos
3. Ser mencionada na aba 📚 Fontes do app
4. Autor do projeto principal: **Adriano Rodrigues da Silva**
5. Código do projeto: licença a definir (recomendado MIT ou GPL-3.0)

---

## 📊 Critérios de Aceitação da Constituição

Antes de merge para `main`:

- [ ] `python -m mypy DarkPenBoot_PRO1.py --strict` → 0 erros
- [ ] `python -m pytest --cov=. --cov-fail-under=40` → passa
- [ ] `python -c "import ast; ast.parse(open('DarkPenBoot_PRO1.py').read())"` → OK
- [ ] `grep -c "def download_with_fallback" DarkPenBoot_PRO1.py` → 1
- [ ] `grep -c "class ClickableLogo" DarkPenBoot_PRO1.py` → 1
- [ ] Zero ocorrências de `# type: ignore` sem comentário

---

## 🚦 Governança

| Papel | Responsável | Escopo |
| ------- | ------------- | -------- |
| Autor / Maintainer | Adriano Rodrigues da Silva | Todas as decisões |
| Revisor técnico (futuro) | A definir | PRs de terceiros |
| Comunidade | GitHub Issues | Bug reports, feature requests |

Emendas a esta Constituição requerem:

1. Issue aberta com tag `constitution-amendment`
2. Descrição do princípio afetado
3. Justificativa técnica + impacto
4. Aprovação do Maintainer
5. Atualização do campo "Última emenda"

---

**Versão semântica:** este documento segue [SemVer](https://semver.org/lang/pt-BR/):

- MAJOR: remoção de princípio
- MINOR: adição de princípio
- PATCH: esclarecimento de texto
