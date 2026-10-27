#!/usr/bin/env python3
"""Agente de integração de exemplo que envia somente eventos artificiais para localhost."""

import argparse
import json
from pathlib import Path
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


def classify(record: dict):
    """Regra FICTÍCIA: exemplifica separação entre processamento e revisão."""
    if not isinstance(record, dict):
        raise ValueError("registro inválido")
    identifier = record.get("id")
    if not isinstance(identifier, str) or not identifier.startswith("LAB-"):
        raise ValueError("somente IDs de teste LAB-*")
    valid_label = isinstance(record.get("label"), str) and bool(record["label"].strip())
    valid_category = isinstance(record.get("category"), str) and bool(record["category"].strip())
    quantity = record.get("quantity")
    valid_qty = type(quantity) is int and quantity >= 0
    if valid_label and valid_category and valid_qty:
        return {"record_id": identifier, "decision": "accepted", "reason": "valid_demo_record"}
    return {"record_id": identifier, "decision": "review", "reason": "missing_or_invalid_field"}


def sync(records: list, base_url: str, dry_run=False):
    parsed = urlsplit(base_url)
    if parsed.scheme != "http" or parsed.hostname not in ("localhost", "127.0.0.1"):
        raise ValueError("O laboratório só permite HTTP em localhost")
    outcomes = []
    for record in records:
        event = classify(record)
        outcomes.append(event)
        if not dry_run:
            request = Request(
                base_url.rstrip("/") + "/events",
                data=json.dumps(event).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(request, timeout=3) as response:
                if response.status != 200:
                    raise RuntimeError(f"Status inesperado: {response.status}")
    return outcomes


def main():
    parser = argparse.ArgumentParser(description="Agente HTTP local para dados sintéticos")
    parser.add_argument("--file", type=Path, default=Path("sample_records.json"))
    parser.add_argument("--url", default="http://127.0.0.1:8091")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    records = json.loads(args.file.read_text(encoding="utf-8"))
    events = sync(records, args.url, args.dry_run)
    print(json.dumps({"dry_run": args.dry_run, "events": events}, indent=2))


if __name__ == "__main__":
    main()
