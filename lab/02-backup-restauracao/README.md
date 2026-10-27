# Laboratório 02 · Backup, SHA-256 e restauração

**Status:** exemplo autoral reproduzível com SQLite e dados artificiais. O banco e o script não foram extraídos de ambiente profissional.

## Objetivo

Demonstrar uma rotina com **cópia consistente** usando `sqlite3.backup()`, manifesto JSON, hash SHA-256, validação `PRAGMA quick_check` e restauração para **novo destino**, sem sobrescrever o banco original.

## Execução (Python 3.10+, sem bibliotecas extras)

Da raiz do repositório:

```bash
cd lab/02-backup-restauracao
python3 backup_lab.py init
python3 backup_lab.py backup
ls backups/
```

O segundo comando imprime o caminho completo do manifesto gerado, por exemplo `backups/snapshot-...manifest.json`. Copie **esse caminho real** e utilize nos próximos comandos:

```bash
python3 backup_lab.py verify backups/SEU_MANIFESTO.manifest.json
python3 backup_lab.py restore backups/SEU_MANIFESTO.manifest.json --destination restaurados/teste.sqlite3
```

O exemplo `SEU_MANIFESTO` é **um placeholder**; substitua pelo arquivo mostrado no seu terminal. `data/`, `backups/` e `restaurados/` estão ignorados pelo Git via `.gitignore` (bases e backups não devem ser publicados).

## Testes automatizados

```bash
# Na raiz do repositório:
python3 -m unittest discover -s lab/02-backup-restauracao/tests -p 'test_*.py' -v
```

Os testes cobrem snapshot/restore, impedimento de sobrescrita, detecção de arquivo adulterado e recusa de criar banco existente.

## Limites

Esse exercício é intencionalmente simplificado. Ele não implementa **retenção, criptografia, armazenamento externo, rotação de segredos, SFTP, agendamento ou recuperação de Docker**. Essas práticas aparecem como experiências descritas no [case histórico](../../cases/03-backup-continuidade.md), mas não foram copiadas para este laboratório. Não use esta implementação como rotina de backup de produção.
