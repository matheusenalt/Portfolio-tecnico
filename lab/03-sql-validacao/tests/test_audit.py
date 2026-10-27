"""Casos de teste SQL em banco de dados efêmero, sem dependências externas."""

import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from audit import audit  # noqa: E402
from seed import seed  # noqa: E402


class TestSQLAudit(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.database = Path(self.temp.name) / "sample.sqlite3"
        seed(self.database)

    def test_detects_four_known_anomalies(self):
        report = audit(self.database)
        self.assertEqual(report["summary"]["products"], 6)
        self.assertEqual(report["summary"]["issues"], 4)
        self.assertEqual(
            {issue["type"] for issue in report["issues"]},
            {"sku_duplicado", "nome_em_branco", "preco_negativo", "movimento_sem_produto"},
        )

    def test_corrections_on_synthetic_fixture_resolve_issues(self):
        with sqlite3.connect(self.database) as conn:
            conn.executescript("""
                UPDATE products SET sku='SKU-003' WHERE id=3;
                UPDATE products SET name='Carregador' WHERE id=4;
                UPDATE products SET price_cents=200 WHERE id=5;
                DELETE FROM stock_movements WHERE product_id=999;
            """)
        self.assertEqual(audit(self.database)["summary"]["issues"], 0)

    def test_missing_database_must_not_be_created(self):
        database = Path(self.temp.name) / "missing.sqlite3"
        with self.assertRaises(FileNotFoundError):
            audit(database)
        self.assertFalse(database.exists())


if __name__ == "__main__":
    unittest.main()
