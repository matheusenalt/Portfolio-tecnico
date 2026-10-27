#!/usr/bin/env python3
"""Backup seguro e restore de um banco SQLite DE LABORATÓRIO.

Não reutilize para produção sem adaptação, política de retenção e testes próprios.
"""

import argparse
import hashlib
import json
import os
import shutil
import sqlite3
import tempfile
from datetime import datetime, timezone
from pathlib import Path


def digest(path: Path) -> str:
    sha = hashlib.sha256()
    with path.open("rb") as file:
        for block in iter(lambda: file.read(1024 * 1024), b""):
            sha.update(block)
    return sha.hexdigest()


def assert_db_integrity(path: Path) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Banco ausente: {path}")
    conn = sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True)
    try:
        status = conn.execute("PRAGMA quick_check").fetchone()[0]
        if status != "ok":
            raise ValueError(f"Falha de integridade SQLite: {status}")
    finally:
        conn.close()


def init_demo(database: Path):
    database.parent.mkdir(parents=True, exist_ok=True)
    if database.exists():
        raise FileExistsError(f"O banco já existe: {database}. Não será sobrescrito.")
    conn = sqlite3.connect(database)
    try:
        conn.executescript("""
            CREATE TABLE inventory (
                id INTEGER PRIMARY KEY,
                item TEXT NOT NULL,
                quantity INTEGER NOT NULL CHECK (quantity >= 0)
            );
            INSERT INTO inventory (item, quantity) VALUES
              ('Exemplo A', 15), ('Exemplo B', 3), ('Exemplo C', 21);
        """)
        conn.commit()
    finally:
        conn.close()
    assert_db_integrity(database)
    return database


def create_backup(database: Path, backup_dir: Path):
    assert_db_integrity(database)
    backup_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    target = backup_dir / f"snapshot-{timestamp}.sqlite3"
    manifest_path = backup_dir / f"snapshot-{timestamp}.manifest.json"
    with tempfile.NamedTemporaryFile(dir=backup_dir, suffix=".partial", delete=False) as tmp:
        temp_path = Path(tmp.name)
    try:
        source = sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True)
        destination = sqlite3.connect(temp_path)
        try:
            source.backup(destination)
        finally:
            destination.close()
            source.close()
        assert_db_integrity(temp_path)
        if target.exists() or manifest_path.exists():
            raise FileExistsError("Nome de snapshot já existente; não sobrescrever.")
        os.replace(temp_path, target)
        manifest = {
            "format": "sqlite-demo-v1",
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
            "backup_file": target.name,
            "sha256": digest(target),
            "size_bytes": target.stat().st_size,
        }
        # Arquivo de manifesto criado com modo exclusivo, não sobrepõe existentes.
        with manifest_path.open("x", encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        return manifest_path
    finally:
        temp_path.unlink(missing_ok=True)


def verify(manifest_path: Path):
    with manifest_path.open(encoding="utf-8") as handle:
        manifest = json.load(handle)
    if manifest.get("format") != "sqlite-demo-v1":
        raise ValueError("Formato de manifesto incompatível")
    filename = manifest.get("backup_file", "")
    if not filename or Path(filename).name != filename or not filename.endswith(".sqlite3"):
        raise ValueError("Nome de arquivo inválido no manifesto")
    target = manifest_path.parent / filename
    if target.stat().st_size != manifest["size_bytes"]:
        raise ValueError("Tamanho do backup não corresponde ao manifesto")
    if digest(target) != manifest["sha256"]:
        raise ValueError("SHA-256 não corresponde ao manifesto")
    assert_db_integrity(target)
    return target


def restore(manifest_path: Path, destination: Path):
    backup = verify(manifest_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # 'xb' impede sobrescrever, mesmo se o arquivo for criado entre verificações.
    created = False
    try:
        with destination.open("xb") as output:
            created = True
            with backup.open("rb") as source:
                shutil.copyfileobj(source, output)
        assert_db_integrity(destination)
        if digest(destination) != digest(backup):
            raise ValueError("Falha na verificação da cópia restaurada")
    except Exception:
        # Nunca apagar um arquivo preexistente se 'xb' recusou a operação.
        if created:
            destination.unlink(missing_ok=True)
        raise
    return destination


def main():
    parser = argparse.ArgumentParser(description="Laboratório de backup SQLite com SHA-256")
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="cria uma base sintética sem sobrescrever")
    init.add_argument("--database", type=Path, default=Path("data/demo.sqlite3"))
    backup = commands.add_parser("backup", help="cria snapshot e manifesto")
    backup.add_argument("--database", type=Path, default=Path("data/demo.sqlite3"))
    backup.add_argument("--backup-dir", type=Path, default=Path("backups"))
    check = commands.add_parser("verify", help="verifica manifesto, SHA e quick_check")
    check.add_argument("manifest", type=Path)
    rest = commands.add_parser("restore", help="restaura em NOVO arquivo")
    rest.add_argument("manifest", type=Path)
    rest.add_argument("--destination", type=Path, required=True)
    args = parser.parse_args()
    try:
        if args.command == "init":
            result = init_demo(args.database)
        elif args.command == "backup":
            result = create_backup(args.database, args.backup_dir)
        elif args.command == "verify":
            result = verify(args.manifest)
        else:
            result = restore(args.manifest, args.destination)
        print(f"OK: {result}")
    except (OSError, sqlite3.DatabaseError, ValueError, KeyError) as exc:
        parser.exit(1, f"ERRO: {exc}\n")


if __name__ == "__main__":
    main()
