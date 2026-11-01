# 02 · Automação de classificação e sincronização fiscal

**Área:** automação, dados fiscais, banco de dados e suporte técnico  
**Situação:** solução utilizada e acompanhada em contexto profissional  
**Tecnologias:** Firebird, SQL, processamento em lote, logs e validação de resultados

## Contexto

A conferência de informações fiscais de produtos exigia atividades manuais repetitivas, com necessidade de identificar registros que poderiam ser processados e aqueles que exigiam análise humana. A iniciativa buscou **reduzir retrabalho, padronizar a conferência e tornar o processamento rastreável**.

## Minha atuação

- Identifiquei a necessidade operacional no atendimento e trabalhei no desenvolvimento de uma solução de apoio à classificação e sincronização fiscal.
- Analisei registros em bases de dados e utilizei consultas SQL/Firebird para diagnóstico e validação.
- Estruturei e acompanhei processos de análise em lote, com distinção entre itens processados e casos que exigiam revisão.
- Trabalhei com registros de execução, verificações e medidas de segurança antes de operações com potencial de alterar informações.
- Acompanhei resultados, exceções e ajustes junto ao fluxo de suporte e aos demais profissionais envolvidos.

## Resultado registrado

| Indicador | Acumulado informado em 01/11/2026 |
|---|---:|
| Itens sincronizados | **267.854** |
| Clientes processados | **98** |

Esses são **valores agregados informados pelo autor**, consultados no painel operacional na data indicada; não representam clientes identificados nem auditoria independente. Não foi incluída uma estimativa de horas economizadas, pois ela dependeria de metodologia e evidências específicas.

## Fluxo simplificado

```text
Leitura de registros em base local
                |
                v
      Análise de classificação
                |
           +----+----+
           |         |
           v         v
     Processável   Revisão manual
           |         |
           v         v
    Sincronização   Registro da exceção
           |
           v
     Log / conferência
```

O desenho é ilustrativo e **não contém estrutura real de banco, algoritmos internos ou regras proprietárias**.

## O que esse trabalho demonstra

- Transformação de uma atividade manual recorrente em um fluxo de automação assistida.
- Capacidade de lidar com grande volume de registros e acompanhar exceções.
- Diagnóstico com SQL, validação de resultados e atenção a riscos de alteração de dados.
- Documentação de processo e comunicação técnica para suporte e desenvolvimento.

**Demonstrações independentes:** [Auditoria SQL](../lab/03-sql-validacao/README.md) e [Integração HTTP](../lab/05-integracao-http/README.md). Esses laboratórios usam dados fictícios.

### Capturas e evidências

Há possibilidade de acrescentar **capturas de interface e indicadores consolidados**, desde que autorizadas, com anonimização prévia e sem detalhes de clientes ou ambientes. Consulte o [guia para imagens públicas](../docs/IMAGENS-PROJETOS.md). Nenhuma captura de produção foi adicionada nesta versão.

> **Separação de projetos:** esta é uma experiência de automação fiscal em ambiente profissional. O [Sol Fiscal](https://github.com/matheusenalt/sol/tree/main/Sol-Fiscal) é uma ferramenta pessoal, apresentada em outro repositório; não é uma publicação do código corporativo descrito aqui.
