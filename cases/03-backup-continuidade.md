# 03 · Backup e continuidade operacional

**Área:** Linux, rotinas agendadas e recuperação  
**Situação:** coleta externa automatizada e ensaio histórico de recuperação documentado  
**Tecnologias:** Linux, SFTP, SHA-256, VirtualBox, armazenamento externo

## Problema

Manter os dados em um único ambiente aumenta o impacto de falhas. O objetivo foi apoiar uma rotina de cópias externas com verificações de integridade e instruções de recuperação.

## O que fiz

- Trabalhei na estruturação de uma VM Linux para executar a coleta externa de backups.
- Configurei e acompanhei rotinas de transferência por SFTP e conferência por SHA-256.
- Investiguei problemas de conectividade, montagem de disco e execução de serviços.
- Organizei procedimentos de restauração e de verificação após a recuperação.

## Fluxo de referência

```text
Serviço em VPS
      |
      v
Backup + checksum
      |
      v
Coleta externa (SFTP)
      |
      v
VM Linux / armazenamento
      |
      v
Verificação de integridade
```

## Validação

Existem registros de testes de transferência e de um ensaio de recuperação realizado em setembro de 2026. Isso documenta aquela validação específica, mas não substitui testes periódicos a cada mudança no ambiente.

**Demonstração relacionada:** [Backup, integridade e restauração](../lab/02-backup-restauracao/README.md).
