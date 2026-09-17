Aqui está o `ARQUITETURA.md` reescrito em estilo **técnico direto**, sem os comentários "gerados por IA" (aqueles rótulos tipo "Decisão arquitetural:", "Por que existe:", excesso de emojis e tom de marketing).

## 📄 Novo conteúdo para `docs/ARQUITETURA.md`

Copie tudo abaixo, cole no arquivo e salve:

```markdown
# Arquitetura — DarkPenBoot Pro

Documento técnico sobre a organização interna do projeto: como as camadas
se comunicam, quais decisões foram tomadas e por quê.

---

## Visão Geral

O DarkPenBoot Pro é distribuído como um script Python único, mas internamente
segue uma arquitetura em camadas. A escolha de arquivo único é deliberada:
facilita distribuição e evita problemas de importação no Buildozer.

```
┌──────────────────────────────────────────────┐
│  UI         Tkinter (desktop) · Kivy (mobile)│
├──────────────────────────────────────────────┤
│  Core       download · gravação · formatação │
├──────────────────────────────────────────────┤
│  Platform   windows · linux · mac · android  │
├──────────────────────────────────────────────┤
│  System     subprocess · ctypes · fsync      │
├──────────────────────────────────────────────┤
│  Constants  temas · distros · limites · URLs │
└──────────────────────────────────────────────┘
```

Cada camada só depende das camadas abaixo. Não há dependência circular.

---

## Camadas

### Constants

Fica no topo do `DarkPenBoot_PRO1.py`. Só dados, nenhuma lógica.

| Constante | Uso |
|---|---|
| `APP_NAME`, `APP_VERSION` | Metadados |
| `THEMES` | Sete temas em formato dict |
| `DISTRO_INFO` | Distros Linux com URLs oficiais |
| `WINDOWS_OPTIONS` | Links da Microsoft |
| `MIN_ISO_SIZE` | Mínimo de 100 MB para aceitar ISO |
| `BROWSER_UA` | User-Agent usado nos downloads |
| `SKIP_DIRS`, `SKIP_FILES` | Filtros de arquivos temporários |

Mudar uma cor, URL ou limite em um único lugar reflete em todo o app.

### System

Utilitários que dependem do SO mas são usados por todas as plataformas.

- `run_hidden()` — executa comandos sem abrir janela (Windows)
- `_get_all_drive_letters()` — lista drives via `kernel32.GetLogicalDrives()`
- `_long_path()` — suporta caminhos > 260 caracteres no Windows
- `_get_free_space()` — espaço livre em qualquer SO
- `_force_assign_letter_to_iso()` — força letra de unidade em ISO montada

O código específico de SO fica isolado aqui para que a camada Core não
precise saber se está no Windows ou Linux.

### Platform

Cada SO tem funções com sufixo próprio:

- `_get_usb_drives_windows()`, `_get_usb_drives_linux()`, `_get_usb_drives_mac()`
- `_format_usb_windows()`, `_format_usb_linux()`, `_format_usb_mac()`
- `_mount_iso_windows()`, `_mount_iso_linux()`, `_mount_iso_mac()`

Uma função fábrica escolhe a implementação correta:

```python
def get_usb_drives():
    if IS_ANDROID or IS_TERMUX:
        return _get_usb_drives_android()
    if IS_WINDOWS:
        return _get_usb_drives_windows()
    elif IS_LINUX:
        return _get_usb_drives_linux()
    elif IS_MAC:
        return _get_usb_drives_mac()
    return []
```

| SO | Detecção USB | Formatação | Gravação DD | Montagem ISO |
|---|---|---|---|---|
| Windows | PowerShell + WMI | `diskpart` | `CreateFileW` | `Mount-DiskImage` |
| Linux | `lsblk -J` | `parted` + `mkfs` | `os.open(O_DIRECT)` | `mount -o loop` |
| macOS | `diskutil -plist` | `diskutil` | `os.open(rdisk)` | `hdiutil attach` |
| Android | `/storage` + `/dev/block` | via terminal | requer root | montagem nativa |

### Core

Lógica de negócio independente de SO.

#### Downloader

Cinco camadas em sequência, cada uma tentada antes de passar para a próxima:

```
curl (UA Chrome)
curl (UA Firefox)
wget
urllib (SSL verificado)
urllib (SSL desabilitado)
```

Depois de baixar:
1. Verifica se é maior que 100 MB
2. Verifica se não é uma página HTML (isso indica erro de URL)
3. Calcula SHA256 e compara com o esperado (se registrado)
4. Se falhar, renomeia para `.parcial` em vez de apagar

#### Formatador USB

Ordem de operações no Windows:

```
1. Detectar disco alvo (bloquear disco 0)
2. Desmontar partições existentes
3. clean (apaga tabela de partição)
4. convert mbr|gpt
5. create partition primary align=1024
6. format fs=ntfs|fat32|exfat quick
7. active (só para MBR)
8. assign (letra)
9. aguardar drive aparecer
```

#### Escritor DD

Blocos de 16 MB, com checagem de cancelamento a cada 512 KB:

```python
with open(iso_path, "rb") as src:
    while chunk := src.read(buf_size):
        for sub_chunk in split(chunk, 512 * 1024):
            if cancel_requested():
                return False
            device.write(sub_chunk)
```

Se o Windows invalidar o handle no meio da gravação (errno 9), o writer
tenta reabrir o dispositivo e continuar de onde parou. Máximo de 5 tentativas.

### UI

#### Desktop (Tkinter)

Widgets customizados:

| Widget | Herda de | Função |
|---|---|---|
| `RoundedButton` | `tk.Canvas` | Botão com cantos arredondados e foco neon |
| `NeonThemeBall` | `tk.Canvas` | Orb 3D que troca tema |
| `NeonTabBar` | `tk.Frame` | Abas com persistência visual |
| `UltimatePopup` | `tk.Toplevel` | Popups responsivos com scroll |
| `ToolTip` | classe própria | Tooltips com posicionamento inteligente |
| `ClickableLogo` | `tk.Frame` | Logo que abre as instruções |

Temas são um dicionário global. `COLORS` aponta para o tema ativo e é
mutado quando o usuário troca.

O pulso neon global funciona assim:
- `GLOBAL_PULSE_STATE` é um dict compartilhado
- Cada widget registra um callback em `_PULSE_SUBSCRIBERS`
- `_global_pulse_tick()` avança a fase e redesenha os inscritos

#### Mobile (Kivy)

`DarkPenBootKivyApp` com `ScreenManager`. Seis telas: Home, Download,
ISO, USB, Log, About. Botões customizados via `canvas.before`.

---

## Segurança

Bloqueios implementados:

| Bloqueio | Implementação |
|---|---|
| Disco 0 (sistema) | `if disk_num == 0: return None` |
| ISO muito pequena | `if size < MIN_ISO_SIZE: abort` |
| HTML disfarçado de ISO | `_is_html_response()` → renomeia para `.html_error` |
| SHA256 divergente | arquivo renomeado para `.parcial` |
| Path traversal | `_sanitize_fat_relpath()` |

O aplicativo não apaga arquivos fora do pendrive selecionado, não envia
dados para servidores, não usa telemetria e não armazena credenciais.

---

## Empacotamento

### Windows (.exe)

```
pyinstaller --onefile --windowed --name DarkPenBoot DarkPenBoot_PRO1.py
```

`--onefile` gera um único arquivo `.exe`. `--windowed` esconde o console.

### Linux / macOS

Mesmo comando sem `--windowed`.

### Android (.apk)

Buildozer + Kivy:

```
buildozer android debug
```

---

## Reprodutibilidade do Build

O `build.yml` do GitHub Actions segue princípios inspirados no NixOS:

| Princípio | Aplicação no projeto |
|---|---|
| Reprodutibilidade | Versões fixas (`python-version: '3.11'`) |
| Declaratividade | O workflow descreve todo o processo |
| Isolamento | Cada runner é ambiente limpo |
| Verificabilidade | SHA256 dos artefatos gerados |
| Multi-plataforma | Quatro runners em paralelo |

Não é uma dependência de NixOS. É a mesma ideia de build determinístico,
aplicada a um projeto Python comum.

---

## Performance

Tempos medidos em máquina local (USB 3.0, ISO de 2 GB):

| Operação | Tempo |
|---|---|
| Extração com 7-Zip | ~45 s |
| Cópia para USB 3 | ~25 s |
| Cópia para USB 2 | ~3 min |
| Gravação DD em USB 3 | ~40 s |
| Verificação SHA256 | ~8 s |

Otimizações aplicadas:

- Buffer adaptativo por tier USB (USB 3: 32 MB, USB 2: 4 MB)
- Cancelamento verificado a cada 512 KB, não a cada byte
- Detecção de travamento (aborta se o download ficar parado por 3 min)
- Cópia em streaming — nunca carrega o arquivo todo na memória

---

## Fluxo de Gravação (modo Extrair)

```
1. Valida ISO
     tamanho > 100 MB
     assinatura ISO9660/UDF presente
     SHA256 (opcional)

2. Re-verifica o pendrive alvo
     serial igual ao selecionado
     não é o disco 0

3. Desabilita automount (Windows)

4. Formata
     clean
     convert MBR ou GPT
     create partition align=1024
     format fs=... quick

5. Monta a ISO

6. Copia arquivos
     symlinks tratados
     FAT: sanitiza nomes + checa duplicatas case-insensitive
     buffer ajustado ao tier USB

7. Aplica boot sector
     bootsect.exe (Windows)
     MBR isohybrid (Linux)

8. Verifica integridade (tamanhos e contagem de arquivos)

9. Reativa automount e mostra resumo
```

---

## Testes

Estrutura em três níveis:

- Unitários: `tests/test_checksums.py`, `tests/test_config.py`
- Integração: `tests/test_download.py`
- End-to-end: gravação real em pendrive (manual)

Executar:

```
python -m pytest tests/ -v
python -m pytest tests/ --cov=. --cov-report=html
```

---

## Referências

- PyInstaller — https://pyinstaller.org/
- Tkinter — https://docs.python.org/3/library/tkinter.html
- Kivy — https://kivy.org/doc/stable/
- Buildozer — https://buildozer.readthedocs.io/
- NixOS — https://nixos.org/governance/
```
