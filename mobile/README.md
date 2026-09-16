# Interface Mobile

A pasta `mobile/` separa a camada Kivy de Android da lógica desktop Tkinter.

## Componentes

- `config.py`: caminhos, links oficiais, defaults e aviso legal.
- `theme.py`: paleta mobile de contraste moderado.
- `widgets.py`: botões e páginas com rolagem vertical consistente.
- `screens.py`: Home, Ajuda e Sobre, com navegação por `ScreenManager`.
- `app.py`: entrypoint modular para executar a interface.

## Execução local

```bash
python -m mobile.app
```

## Android

Use `requirements-mobile.txt` e mantenha as permissões mínimas no `buildozer.spec`:

- `INTERNET` para downloads.
- `READ_EXTERNAL_STORAGE`/`WRITE_EXTERNAL_STORAGE` somente em Android legado.
- acesso USB/ROOT apenas quando a gravação raw for explicitamente solicitada.

A gravação de dispositivo deve continuar exigindo confirmação explícita e validação do caminho alvo.
