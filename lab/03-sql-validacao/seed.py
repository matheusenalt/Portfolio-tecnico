#!/usr/bin/env python3
"""Cria um banco sintético com inconsistências intencionais para teste."""

import argparse
import sqlite3
from pathlib import Path


def seed(database: Path):
    database.parent.mkdir(parents=True, exist_ok=True)
    if database.exists():
        raise FileExistsError(f"Banco já existe: {database}")
    conn = sqlite3.connect(database)
    try:
        conn.executescript("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                sku TEXT NOT NULL,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                price_cents INTEGER NOT NULL
            );
            CREATE TABLE stock_movements (
                id INTEGER PRIMARY KEY,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL
            );
            CREATE INDEX idx_sku ON products (sku);
            INSERT INTO products (id, sku, name, category, price_cents) VALUES
              (1, 'SKU-001', 'Cabo USB', 'Acessorios', 2500),
              (2, 'SKU-002', 'Mouse', 'Perifericos', 4500),
              (3, 'SKU-002', 'Teclado', 'Perifericos', 9000),
              (4, 'SKU-004', '  ', 'Acessorios', 1200),
              (5, 'SKU-005', 'Adaptador', 'Acessorios', -200),
              (6, 'SKU-006', 'Hub USB', 'Acessorios', 7000);
            INSERT INTO stock_movements (id, product_id, quantity) VALUES
              (1, 1, 5), (2, 1, -2), (3, 999, 1);
        """)
        conn.commit()
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description="Base sintética para auditoria de SQL")
    parser.add_argument("--database", type=Path, default=Path("data/catalogo_demo.sqlite3"))
    args = parser.parse_args()
    try:
        seed(args.database)
        print(f"Base de teste criada: {args.database} (anomalias intencionais)")
    except OSError as error:
        parser.exit(1, f"ERRO: {error}\n")


if __name__ == "__main__":
    main()
