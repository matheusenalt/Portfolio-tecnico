<div align="center">

# Portfólio Técnico | Matheus Sena

**Infraestrutura Linux • Suporte Técnico • Docker • SQL • Automação**

Projetos e laboratórios que mostram minha experiência com sustentação de sistemas, diagnóstico de incidentes, implantação de serviços e rotinas de continuidade operacional.

![Linux](https://img.shields.io/badge/Linux-Administra%C3%A7%C3%A3o%20e%20suporte-FCC624?logo=linux&logoColor=black&style=flat-square)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white&style=flat-square)
![Python](https://img.shields.io/badge/Python-Laborat%C3%B3rios-3776AB?logo=python&logoColor=white&style=flat-square)
![SQL](https://img.shields.io/badge/SQL-Firebird%20%7C%20SQLite-4479A1?style=flat-square)
![CI](https://img.shields.io/badge/Testes-GitHub%20Actions-2088FF?logo=githubactions&logoColor=white&style=flat-square)

[**Projetos**](#-projetos-e-experi%C3%AAncias) · [**Laboratórios**](#-laborat%C3%B3rios-pr%C3%A1ticos) · [**Executar**](#-como-executar) · [**Contato**](#-contato)

</div>

---

## 🎯 Sobre mim

Sou estudante de **Segurança da Informação** e atuo com suporte técnico a sistemas empresariais. No dia a dia, trabalho com atendimento, análise de erros, bancos de dados e validação de soluções. Também participei de projetos de infraestrutura em VPS Linux, implantação de serviços com Docker, organização de acessos e rotinas de backup.

Meu foco profissional é evoluir para **Infraestrutura Linux, Operações Cloud e Suporte N2**. Este repositório reúne parte desse caminho: os desafios práticos que enfrentei e laboratórios independentes para demonstrar como aplico os conceitos.

### Tecnologias com as quais já trabalhei

| Área | Ferramentas e práticas |
|---|---|
| **Infraestrutura** | Linux, Debian, VPS, SSH, Docker, Docker Compose, Caddy, HTTP/HTTPS |
| **Bancos e sistemas** | SQL, Firebird, SQLite (em laboratório), PHP, JavaScript |
| **Operação** | Troubleshooting, logs, diagnóstico de incidentes, suporte N1–N3, documentação técnica |
| **Continuidade** | Backup, recuperação, SHA-256, SFTP, VirtualBox |
| **Automação e testes** | Bash, Python, validação funcional, testes automatizados e GitHub Actions |

> **Como ler este repositório:** os **estudos de caso** relatam atividades reais de forma anonimizada. Os **laboratórios** são implementações independentes, com dados fictícios, criadas para experimentar e demonstrar conceitos. Nenhum código, banco ou configuração de produção de terceiros está publicado aqui.

---

## 🧩 Projetos e experiências

Os projetos abaixo representam situações que surgiram no meu trabalho com suporte e infraestrutura. Cada página explica o contexto, minha atuação, como foi conduzida a validação e o que aprendi.

| Projeto | O que foi feito | Tecnologias principais | Situação |
|---|---|---|---|
| [**01 · Plataforma interna em Linux**](cases/01-plataforma-linux.md) | Implantação e sustentação de serviços web, organização de acessos e documentação operacional | Linux, VPS, Docker, Caddy | Implantação realizada |
| [**02 · Automação de análise de dados**](cases/02-automacao-dados.md) | Diagnóstico de bases, apoio à automação de cadastros e tratamento de exceções | Firebird, SQL, HTTP | Implantação acompanhada |
| [**03 · Backup e continuidade**](cases/03-backup-continuidade.md) | Cópias externas, integridade de arquivos, execução e testes de recuperação | Linux, SFTP, SHA-256, VM | Testes históricos registrados |
| [**04 · Investigação de falhas**](cases/04-diagnostico-qa.md) | Reprodução de erros, consultas SQL, validação de correções e comunicação com desenvolvimento | SQL, PHP, JavaScript | Atividade recorrente |
| [**05 · Integração documental**](cases/05-poc-integracao.md) | Requisitos, desenho de integração e protótipo de fluxo documental | APIs, modelagem, documentação | Prova de conceito parcial |

### Meu papel nesses projetos

Minha atuação envolveu principalmente **implantação, suporte, diagnóstico, validação, automação de rotinas e documentação**. Parte do trabalho ocorreu em conjunto com outros profissionais. Por isso, descrevo a minha participação técnica em vez de atribuir a mim o desenvolvimento integral dos sistemas.

---

## 🧪 Laboratórios práticos

Para não depender de ambientes internos, preparei versões pequenas e independentes de problemas técnicos que estudo e encontro no suporte. É possível baixar o repositório e executá-las localmente.

| Laboratório | O que demonstra | Como executar |
|---|---|---|
| [**01 · Linux + Docker**](lab/01-linux-docker/README.md) | Serviço HTTP Python, proxy Caddy, healthcheck e Compose | Docker ou Python |
| [**02 · Backup e restauração**](lab/02-backup-restauracao/README.md) | Snapshot SQLite, manifesto SHA-256, verificação e restore | Python |
| [**03 · Auditoria SQL**](lab/03-sql-validacao/README.md) | Identificação de registros inconsistentes em base fictícia | Python + SQLite |
| [**04 · Diagnóstico Linux**](lab/04-diagnostico-linux/README.md) | Script de checagem de host, armazenamento e memória | Bash |
| [**05 · Integração HTTP**](lab/05-integracao-http/README.md) | Agente, API, registros de eventos e idempotência | Python |

### Arquitetura do laboratório Docker

```text
      Navegador / curl
             |
      localhost:8080
             |
             v
       +-------------+
       |    Caddy    |  proxy reverso
       +-------------+
             |
         rede Docker
             |
             v
       +-------------+
       | API Python  |  /health  /api/status
       +-------------+
```

O serviço é publicado apenas em `127.0.0.1`, para execução local. O [README do laboratório 01](lab/01-linux-docker/README.md) detalha os comandos e as limitações técnicas do exemplo.

---

## 📁 Estrutura do repositório

```text
Portfolio-tecnico/
├── README.md                  # Apresentação e índice
├── SECURITY.md                # Publicação responsável e limites de segurança
├── CHANGELOG.md               # Evolução do repositório
├── LICENSE                    # Licença do código de demonstração
├── Makefile                   # Atalhos de validação
├── .github/workflows/ci.yml   # Testes automatizados
├── cases/                     # Experiências profissionais (anonimizadas)
│   ├── 01-plataforma-linux.md
│   ├── 02-automacao-dados.md
│   ├── 03-backup-continuidade.md
│   ├── 04-diagnostico-qa.md
│   └── 05-poc-integracao.md
├── lab/                       # Laboratórios independentes
│   ├── 01-linux-docker/
│   ├── 02-backup-restauracao/
│   ├── 03-sql-validacao/
│   ├── 04-diagnostico-linux/
│   └── 05-integracao-http/
├── docs/roadmap.md            # Próximos estudos
└── scripts/                   # Testes e revisão de arquivos
```

---

## 🚀 Como executar

**Pré-requisitos:** Python 3.10+ e Git. Para o laboratório de Docker, é necessário ter Docker Engine e Docker Compose. Para o diagnóstico de host, use um ambiente Linux com Bash.

### 1. Clonar

```bash
git clone https://github.com/matheusenalt/Portfolio-tecnico.git
cd Portfolio-tecnico
```

### 2. Executar os testes

```bash
bash scripts/testar-tudo.sh
```

O script roda os testes automatizados dos laboratórios em Python e verifica a sintaxe do script Bash. Também existe uma execução automática configurada em [GitHub Actions](.github/workflows/ci.yml).

### 3. Subir o exemplo com Docker

```bash
cd lab/01-linux-docker
docker compose up --build -d
curl http://127.0.0.1:8080/health
docker compose down
```

Para backup, SQL e integração HTTP, siga os comandos nos respectivos READMEs. Os testes Python **não exigem conexão com provedores Cloud**.

---

## ✅ Validações e segurança

- **Testes locais:** 13 testes automatizados passaram na preparação deste pacote, cobrindo API, backup/restauração, auditoria e integração.
- **CI:** pipeline configurado para rodar novamente a cada push e pull request. O resultado mais recente pode ser consultado na aba *Actions* do GitHub.
- **Docker:** a execução com Compose requer validação no ambiente onde for utilizada; o teste da stack containerizada não foi realizado neste pacote.
- **Dados de terceiros:** nenhum cliente, credencial, endereço interno ou banco real deve entrar no repositório. Veja [SECURITY.md](SECURITY.md).

Estes scripts foram feitos para **estudo e demonstração local**, não para implantação direta em produção.

---

## 📌 Próximas evoluções

Minha prioridade de estudo é aprofundar administração Linux, observabilidade, redes e fundamentos de Cloud. O plano de evolução está em [docs/roadmap.md](docs/roadmap.md). Os laboratórios serão atualizados conforme novos testes e cenários forem concluídos.

---

## 📬 Contato

- **LinkedIn:** [linkedin.com/in/matheus-sena-a83a88389](https://www.linkedin.com/in/matheus-sena-a83a88389/)
- **GitHub:** [github.com/matheusenalt](https://github.com/matheusenalt)
- **E-mail:** matheusena234@gmail.com

**Matheus Sena** · Segurança da Informação · Linux / Infraestrutura / Suporte Técnico
