# Segurança e divulgação responsável

Este repositório é público e reúne **estudos de caso anonimizados**, **indicadores agregados declarados pelo autor** e **laboratórios com dados fictícios**. Indicadores e imagens de contexto profissional exigem verificação de permissão de divulgação antes da publicação.

## O que não entra aqui

- Senhas, tokens, chaves SSH, certificados privados e arquivos `.env` reais.
- Backups, bases de clientes, XMLs fiscais, documentos internos ou amostras de produção.
- IPs operacionais, endereços internos, acessos ou qualquer informação que permita identificar a infraestrutura de terceiros.
- Código-fonte proprietário ou configurações corporativas de produção.
- Capturas de tela de produção sem autorização e anonimização rigorosa.

Para preparar imagens públicas, consulte [docs/IMAGENS-PROJETOS.md](docs/IMAGENS-PROJETOS.md).

## Laboratórios

Os exemplos são para desenvolvimento local. Não são serviços endurecidos para exposição pública nem implementações de backup para produção. Cada laboratório informa seus próprios limites.

## Revisão antes de publicar

O script abaixo faz uma verificação simples de padrões de segredos nos arquivos que o Git considera publicáveis:

```bash
python3 scripts/revisar-arquivos.py
```

Ele **não substitui revisão manual**. Consulte `git status` e `git diff --cached` antes de enviar arquivos para o repositório.

## Relatar um problema

Se identificar informação sensível publicada por engano, não abra uma issue incluindo o conteúdo. Entre em contato pelo e-mail do perfil e indique apenas o caminho do arquivo e a natureza do problema.
