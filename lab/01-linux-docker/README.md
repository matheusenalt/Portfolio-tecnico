# Laboratório 01 · Linux, Docker Compose e proxy reverso

**Status:** laboratório demonstrativo, executável em máquina local com Docker Compose. Não é a configuração usada em qualquer ambiente profissional.

## Objetivo

Mostrar um serviço HTTP simples em Python (somente biblioteca padrão), com proxy reverso Caddy, containers em rede privada, usuário não privilegiado na API, healthcheck e testes automatizados.

## Arquivos

- `app/server.py` — API JSON `/`, `/health`, `/api/status`.
- `app/Dockerfile` — imagem Python com usuário sem privilégios.
- `compose.yaml` — serviço API + Caddy, rede bridge, publicação local.
- `Caddyfile` — reverse proxy por HTTP **apenas no localhost**.
- `tests/test_api.py` — testes da API com servidor temporário.

## Rodar com Docker

```bash
cd lab/01-linux-docker
docker compose up --build -d
docker compose ps
curl -i http://127.0.0.1:8080/health
curl -s http://127.0.0.1:8080/api/status
# limpeza:
docker compose down
```

A porta só é publicada em `127.0.0.1:8080`. O Caddy roteia para `api:8000` na rede interna. Não expõe o serviço à internet.

## Rodar testes sem Docker

```bash
python3 -m unittest discover -s lab/01-linux-docker/tests -p 'test_*.py' -v
```

Execute da **raiz do repositório**. Os testes criam um servidor local e verificam health, status e resposta 404.

## Validações/limites

- `/health` responde HTTP 200 e JSON.
- Uma rota inexistente responde HTTP 404.
- O status inclui uptime e horário UTC.
- `docker compose ps` deve mostrar API saudável.
- Este lab **não implementa autenticação, TLS externo, observabilidade ou hardening de produção**. Para exposição pública, são necessárias outras camadas e políticas.
