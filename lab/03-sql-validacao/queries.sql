-- Consultas independentes para o catalogo FICTÍCIO do laboratório.
-- Execute sobre a base SQLite gerada por seed.py, nunca no banco da empresa.

-- SKUs repetidos:
SELECT sku, COUNT(*) AS ocorrencias
FROM products
GROUP BY sku
HAVING COUNT(*) > 1;

-- Nomes em branco:
SELECT id, sku FROM products WHERE TRIM(name) = '';

-- Preços com valor negativo:
SELECT id, sku, price_cents FROM products WHERE price_cents < 0;

-- Referências inexistentes em movimentos:
SELECT m.id, m.product_id
FROM stock_movements AS m
LEFT JOIN products AS p ON m.product_id = p.id
WHERE p.id IS NULL;
