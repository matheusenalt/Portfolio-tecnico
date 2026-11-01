# 01 · Plataforma interna em Linux

**Área:** infraestrutura Linux, serviços web, colaboração e operação  
**Situação:** implantação realizada; sustentação e documentação técnica  
**Tecnologias:** Linux, VPS, SSH, Docker Compose, proxy reverso/HTTPS, serviços web

## Contexto

O suporte técnico dependia de informações e procedimentos distribuídos entre ferramentas distintas. A proposta foi organizar um **portal interno de serviços e conhecimento** para facilitar o trabalho da equipe, a consulta a documentos e a continuidade dos atendimentos.

## Minha atuação

- Propus e trabalhei na estruturação de um ambiente interno unificado em uma VPS Linux.
- Participei da implantação, configuração e integração de serviços web para arquivos, colaboração e chamados.
- Organizei recursos voltados à **base de conhecimento, arquivos, atividades e informações de suporte**, conforme as necessidades da operação.
- Atuei em verificações de disponibilidade, acesso, logs, conectividade, HTTPS e comportamento dos serviços.
- Preparei documentação técnica e orientações de uso, para que outras pessoas pudessem compreender e manter o ambiente.
- Trabalhei com rotinas de backup e recuperação, em conjunto com a estrutura descrita no [estudo de caso 03](03-backup-continuidade.md).

O projeto envolveu trabalho colaborativo. Este relato se concentra nas minhas iniciativas, configurações, validações e documentação, sem atribuir a mim a autoria de componentes de terceiros.

## Visão da solução (simplificada)

```text
Equipe de suporte
       |
       v
Portal interno / acesso web
       |
       +--> Arquivos e documentação
       +--> Base de conhecimento
       +--> Recursos de colaboração
       +--> Atendimento / chamados
       |
       v
Serviços em Linux + containers
       |
       +--> Configuração de acesso / HTTPS
       +--> Logs e verificações operacionais
       +--> Rotinas de cópia e recuperação
```

Esse desenho é **conceitual**: não reproduz endereços, configurações nem a topologia interna real.

## Como foi validado

Acompanhei o funcionamento dos serviços, autenticação, acessibilidade das aplicações, logs e testes progressivos das funções. Documentação de manutenção e recuperação foi tratada como parte da entrega, não como atividade posterior.

## Resultados e aprendizados

- Organização dos serviços e informações antes dispersos, facilitando o acesso no cotidiano do suporte.
- Melhoria da rastreabilidade técnica por meio de documentação, procedimentos e registros de verificação.
- Experiência prática com implantação, sustentação e continuidade de uma stack Linux baseada em serviços web.

**Demonstração independente:** [Linux, Docker e proxy reverso](../lab/01-linux-docker/README.md). O laboratório utiliza código de demonstração e não reproduz a infraestrutura real.

### Capturas e evidências

Capturas do painel poderão ser adicionadas **após autorização e revisão dos dados exibidos**. Veja [como preparar imagens públicas](../docs/IMAGENS-PROJETOS.md). Nenhuma imagem de produção foi incluída nesta versão.

> **Limite de divulgação:** estudo de caso descritivo e anonimizado. Os arquivos corporativos, as credenciais e as configurações reais não fazem parte deste repositório.
