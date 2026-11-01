# Capturas de tela e imagens para os estudos de caso

Os estudos de caso do portfólio descrevem experiências profissionais sem expor o ambiente de terceiros. **Este pacote não inclui capturas de produção.**

## Como incluir imagens posteriormente

1. Confirme que a publicação da imagem é permitida e que você tem autorização para divulgá-la.
2. Use uma cópia editada, nunca o original com dados sensíveis. Remova ou substitua nomes de clientes, CNPJ, CPF, e-mails, telefones, credenciais, nomes de usuários, URLs, domínios, endereços IP, identificadores de máquinas, números de documentos e caminhos internos.
3. Prefira **capturas demonstrativas com dados fictícios**, quando possível. Oculte notificações do sistema e metadados que identifiquem terceiros.
4. Revise a imagem ampliada antes de incluir no repositório. Não confie apenas em tarjas translúcidas ou em recortes que possam deixar dados visíveis.
5. Nomeie claramente a evidência, adicione uma legenda e informe quando o conteúdo foi anonimizado ou simulado. Não apresente simulação como tela de produção.

## Organização sugerida

```text
docs/
  imagens/
    painel-interno/
      dashboard-publico.png
      servicos-publico.png
    automacao-fiscal/
      tela-publica.png
      indicadores-publicos.png
```

Após colocar os arquivos na pasta correta, adicione os links relativos nos estudos de caso, por exemplo:

```markdown
![Tela demonstrativa do portal interno](../docs/imagens/painel-interno/dashboard-publico.png)
```

Esses caminhos são **exemplos**, não arquivos incluídos neste repositório. Links para imagens não foram ativados para evitar referências quebradas.

## Sobre as métricas divulgadas

As contagens agregadas do projeto de automação fiscal foram informadas em **01/11/2026**. Antes de torná-las públicas, confirme se sua divulgação é permitida e mantenha evidência privada do painel de onde foram obtidas. Não publique nomes, listas, arquivos de clientes ou relatórios reais.
