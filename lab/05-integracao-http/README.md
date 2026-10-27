# Laboratório 05 · Agente de integração HTTP e revisão de registros

**Status:** laboratório de demonstração com dados fictícios, API HTTP local e agente de sincronização. Reproduz **conceitos gerais**, não regras de negócios, tabelas ou endpoints de sistemas empresariais.

## O que demonstra

- Agente Python que lê registros de uma fonte sintética JSON.
- Regra fictícia de validação que separa eventos `accepted` e `review`.
- Envio de resultados com `POST /events` em **localhost**.
- API Python que valida o formato, salva registros em SQLite e consolida contagens.
- **Idempotência:** o mesmo `record_id` pode ser reenviado sem criar uma segunda linha.
- Testes automatizados do caminho agente → API → banco e do modo `dry-run`.

## Como executar

Use dois terminais, ambos na pasta `lab/05-integracao-http`:

```bash
# Terminal 1
python3 api.py
```

```bash
# Terminal 2
python3 agent.py --dry-run   # valida sem enviar
python3 agent.py             # envia para localhost
python3 agent.py             # repete, IDs não duplicam
curl -s http://127.0.0.1:8091/events
```

Resultado esperado após o primeiro envio: **4 registros únicos**, sendo **2 aceitos** e **2 para revisão**. `data/events.sqlite3` é gerado localmente e não deve ser enviado ao GitHub.

## Testes

```bash
# Na raiz do repositório:
python3 -m unittest discover -s lab/05-integracao-http/tests -p 'test_*.py' -v
```

## Segurança e limitações

A API só escuta em `127.0.0.1` e o agente recusa destinos externos. **Não implementei autenticação, HTTPS ou retry de fila**: este material não é uma solução de produção e não deve ser publicado como serviço na internet. Os arquivos não contêm dados de clientes nem códigos ou consultas de sistemas fiscais.
