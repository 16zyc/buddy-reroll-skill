#!/usr/bin/env python3
import argparse
import hashlib
import json
import random
import string
import time
from pathlib import Path


def make_seed(random_mode: bool, explicit_seed: str | None) -> str:
    if explicit_seed:
        return explicit_seed
    if random_mode:
        suffix = "".join(random.choices(string.digits, k=8))
        return f"user-{suffix}"
    raise ValueError("Provide --seed or --random.")


def backup_file(src: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    dst = backup_dir / f"{src.name}.backup.{stamp}"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return dst


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reset local Claude /buddy companion state and set seed."
    )
    parser.add_argument("--seed", help="Seed string, e.g. user-2224")
    parser.add_argument("--random", action="store_true", help="Generate random seed")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only")
    args = parser.parse_args()

    seed = make_seed(args.random, args.seed)
    seed_hash = hashlib.sha256(seed.encode("utf-8")).hexdigest()

    home = Path.home()
    claude_dir = home / ".claude"
    global_file = home / ".claude.json"
    settings_file = claude_dir / "settings.json"
    backups_dir = claude_dir / "backups"

    if not global_file.exists():
        raise FileNotFoundError(f"Missing file: {global_file}")
    if not settings_file.exists():
        raise FileNotFoundError(f"Missing file: {settings_file}")

    global_data = json.loads(global_file.read_text(encoding="utf-8"))
    settings_data = json.loads(settings_file.read_text(encoding="utf-8"))

    if args.dry_run:
        print("[dry-run] No files were modified.")
    else:
        backup_global = backup_file(global_file, backups_dir)
        backup_settings = backup_file(settings_file, backups_dir)

        global_data["userID"] = seed_hash
        if "companion" in global_data:
            del global_data["companion"]
        settings_data["userID"] = seed

        global_file.write_text(
            json.dumps(global_data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        settings_file.write_text(
            json.dumps(settings_data, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        print(f"Backed up: {backup_global}")
        print(f"Backed up: {backup_settings}")

    print(f"Seed: {seed}")
    print(f"SHA256(seed): {seed_hash}")
    print("Next:")
    print("1) Start a fresh Claude session")
    print("2) Run /buddy")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
