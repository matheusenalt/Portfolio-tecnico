#!/usr/bin/env python3
"""Auditoria de consistência para base SQLite FICTÍCIA."""

import argparse
import json
import sqlite3
from pathlib import Path


def audit(database: Path):
    if not database.is_file():
        raise FileNotFoundError(f"Base inexistente: {database}. Execute seed.py primeiro.")
    conn = sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    try:
        issues = []
        def query(sql):
            return [dict(r) for r in conn.execute(sql).fetchall()]

        checks = [
            ("sku_duplicado", "SELECT sku, COUNT(*) AS ocorrencias FROM products GROUP BY sku HAVING COUNT(*) > 1"),
            ("nome_em_branco", "SELECT id, sku FROM products WHERE TRIM(name) = ''"),
            ("preco_negativo", "SELECT id, sku, price_cents FROM products WHERE price_cents < 0"),
            ("movimento_sem_produto", "SELECT m.id, m.product_id FROM stock_movements m LEFT JOIN products p ON p.id = m.product_id WHERE p.id IS NULL"),
        ]
        for issue_type, sql in checks:
            for row in query(sql):
                issues.append({"type": issue_type, "details": row})
        return {
            "source": "synthetic-sqlite-demo",
            "summary": {
                "products": conn.execute("SELECT COUNT(*) FROM products").fetchone()[0],
                "movements": conn.execute("SELECT COUNT(*) FROM stock_movements").fetchone()[0],
                "issues": len(issues),
            },
            "issues": issues,
        }
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Auditoria SQL com relatório JSON")
    parser.add_argument("--database", type=Path, default=Path("data/catalogo_demo.sqlite3"))
    parser.add_argument("--strict", action="store_true", help="retorna 1 se encontrar anomalias")
    args = parser.parse_args()
    try:
        result = audit(args.database)
    except (OSError, sqlite3.DatabaseError) as exc:
        parser.exit(2, f"ERRO: {exc}\n")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if args.strict and result["summary"]["issues"]:
        parser.exit(1)


if __name__ == "__main__":
    main()
