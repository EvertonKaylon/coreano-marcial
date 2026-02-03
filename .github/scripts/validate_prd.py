#!/usr/bin/env python3
"""Validate presence of PRD and basic Constitution compliance in changed specs."""
import sys
from pathlib import Path


def fail(msg: str):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(1)


repo_root = Path(__file__).resolve().parents[2]
prd = repo_root / "docs" / "PRD.md"
constitution = repo_root / ".specify" / "memory" / "constitution.md"

if not prd.exists():
    fail("docs/PRD.md not found in repo")

if not constitution.exists():
    fail(".specify/memory/constitution.md not found in repo")

content = prd.read_text(encoding="utf8")
if "Constitution" not in content and "Constitution Compliance" not in content:
    # be permissive but fail if no hint of Constitution mention
    fail("docs/PRD.md does not mention 'Constitution' or 'Constitution Compliance'")

print("PRD and Constitution files present and PRD mentions Constitution (basic check)")
sys.exit(0)
