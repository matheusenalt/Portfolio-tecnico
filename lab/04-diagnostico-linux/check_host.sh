#!/usr/bin/env bash
# Informações gerais em modo leitura; não instala, modifica ou transmite dados.
set -euo pipefail

printf '%s\n' '=== Diagnóstico local (laboratório) ==='
printf 'Data UTC: '
date -u '+%Y-%m-%dT%H:%M:%SZ'
printf '\nKernel:\n'
uname -sr
printf '\nUptime:\n'
if command -v uptime >/dev/null 2>&1; then uptime; else echo 'uptime indisponível'; fi
printf '\nPartição raiz:\n'
if command -v df >/dev/null 2>&1; then df -h /; else echo 'df indisponível'; fi
printf '\nMemória:\n'
if command -v free >/dev/null 2>&1; then free -h; else echo 'free indisponível'; fi
printf '\nFerramentas instaladas:\n'
for cmd in python3 docker git curl; do
  if command -v "$cmd" >/dev/null 2>&1; then
    printf '[OK] %s\n' "$cmd"
  else
    printf '[--] %s\n' "$cmd"
  fi
done
printf '\nConcluído (somente leitura). Não publique logs de máquinas reais.\n'
