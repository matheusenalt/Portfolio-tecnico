# Laboratório 03 · SQL, qualidade de dados e validação funcional

**Status:** banco de dados totalmente sintético, código demonstrativo e testes automatizados. Não usa tabelas ou regras de ERP corporativo.

## Objetivo

Simular quatro problemas comuns de integridade de cadastro: SKU duplicado, nome vazio, preço negativo e movimento referenciando produto inexistente. O banco SQLite foi deliberadamente criado **sem algumas restrições**, para permitir identificar falhas de um legado fictício.

## Passo a passo

```bash
cd lab/03-sql-validacao
python3 seed.py
python3 audit.py
python3 audit.py --strict
```

A auditoria padrão deve encontrar **4 anomalias intencionais**. No modo `--strict`, o programa retorna código de saída 1 quando existem falhas, o que pode ser usado em um pipeline CI para barrar um conjunto de dados inválido. Este retorno 1 é **esperado** antes das correções.

## Como testar o reparo apenas no exemplo

```bash
python3 - <<'PY'
import sqlite3
with sqlite3.connect('data/catalogo_demo.sqlite3') as db:
    db.executescript('''
        UPDATE products SET sku='SKU-003' WHERE id=3;
        UPDATE products SET name='Carregador' WHERE id=4;
        UPDATE products SET price_cents=200 WHERE id=5;
        DELETE FROM stock_movements WHERE product_id=999;
    ''')
PY
python3 audit.py --strict
```

O relatório final deve indicar 0 anomalias. **Não replique estes `UPDATE/DELETE` em sistemas reais**: em produção, ajustes requerem autorização, backup e avaliação do esquema.

## Testes independentes

```bash
# Da raiz do repositório:
python3 -m unittest discover -s lab/03-sql-validacao/tests -p 'test_*.py' -v
```

Os testes cobrem o resultado esperado do dataset, a correção em dados sintéticos e a recusa de abrir uma base inexistente.

## Relação com a experiência

Este exercício ilustra análise de dados, investigação e validação de resultados; ele **não replica regras fiscais** nem demonstra acesso a dados de terceiros. Veja o [estudo anonimizado](../../cases/04-diagnostico-qa.md).
