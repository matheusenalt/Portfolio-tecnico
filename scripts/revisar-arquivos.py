#!/usr/bin/env python3
"""Auxilia a revisão pré-publicação sem ler arquivos ignorados pelo Git.

Heurística simples: não substitui secret scanner nem revisão manual.
"""

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATTERNS = {
    "possível chave privada": re.compile(r"-----BEGIN (?:OPENSSH|RSA|EC|DSA|PRIVATE) PRIVATE KEY-----"),
    "possível token GitHub": re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}\b"),
    "possível senha literal": re.compile(r"(?im)^\s*(?:password|senha|secret)\s*[:=]\s*['\"][^'\"]{4,}['\"]"),
}


def main():
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(ROOT), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            stderr=subprocess.DEVNULL,
        )
        files = [ROOT / p.decode("utf-8") for p in raw.split(b"\0") if p]
    except (FileNotFoundError, subprocess.CalledProcessError):
        files = [p for p in ROOT.rglob("*") if p.is_file() and ".git" not in p.parts]
        print("AVISO: Git não disponível; lista de arquivos pode incluir artefatos locais.")

    findings = []
    for path in files:
        try:
            if path.stat().st_size > 1_000_000:
                continue
            content = path.read_text(encoding="utf-8")
        except (UnicodeError, OSError):
            continue
        for label, pattern in PATTERNS.items():
            if pattern.search(content):
                findings.append((path.relative_to(ROOT), label))
    for path, description in findings:
        print(f"REVISAR: {path}: {description}")
    print(f"Arquivos inspecionados: {len(files)}")
    if findings:
        raise SystemExit(1)
    print("Sem correspondências nas heurísticas simples. Faça também a revisão manual.")


if __name__ == "__main__":
    main()
