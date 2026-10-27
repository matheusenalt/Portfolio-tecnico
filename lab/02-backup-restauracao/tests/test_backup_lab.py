"""Testes para demonstrar backup, adulteração detectada e restore seguro."""

import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from backup_lab import create_backup, init_demo, restore, verify  # noqa: E402


class TestBackup(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.database = self.root / "origem.sqlite3"
        init_demo(self.database)

    def test_backup_manifest_and_restore(self):
        manifest = create_backup(self.database, self.root / "backups")
        snapshot = verify(manifest)
        self.assertTrue(snapshot.exists())
        with manifest.open(encoding="utf-8") as handle:
            self.assertEqual(json.load(handle)["format"], "sqlite-demo-v1")
        destination = self.root / "restore.sqlite3"
        restore(manifest, destination)
        with sqlite3.connect(destination) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM inventory").fetchone()[0], 3)
        self.assertTrue(self.database.exists())

    def test_never_overwrite_existing_restore(self):
        manifest = create_backup(self.database, self.root / "backups")
        with self.assertRaises(FileExistsError):
            restore(manifest, self.database)
        with sqlite3.connect(self.database) as conn:
            self.assertEqual(conn.execute("SELECT COUNT(*) FROM inventory").fetchone()[0], 3)

    def test_modified_file_fails_hash_validation(self):
        manifest = create_backup(self.database, self.root / "backups")
        snapshot = verify(manifest)
        with snapshot.open("ab") as handle:
            handle.write(b"tampering")
        with self.assertRaises(ValueError):
            verify(manifest)

    def test_init_does_not_overwrite_database(self):
        with self.assertRaises(FileExistsError):
            init_demo(self.database)


if __name__ == "__main__":
    unittest.main()
