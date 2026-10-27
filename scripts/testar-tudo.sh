#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

printf '\n[1/5] API HTTP\n'
python3 -m unittest discover -s lab/01-linux-docker/tests -p 'test_*.py' -v
printf '\n[2/5] Backup e restore\n'
python3 -m unittest discover -s lab/02-backup-restauracao/tests -p 'test_*.py' -v
printf '\n[3/5] SQL e auditoria\n'
python3 -m unittest discover -s lab/03-sql-validacao/tests -p 'test_*.py' -v
printf '\n[4/5] Integração HTTP\n'
python3 -m unittest discover -s lab/05-integracao-http/tests -p 'test_*.py' -v
printf '\n[5/5] Verificação sintática de scripts shell\n'
bash -n scripts/testar-tudo.sh lab/04-diagnostico-linux/check_host.sh
printf '\nOK: verificações locais concluídas.\n'
