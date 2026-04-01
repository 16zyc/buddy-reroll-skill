#!/usr/bin/env python3
import argparse
import json
import os
import random
import string
import time
from pathlib import Path

RARITY_ORDER = ["common", "uncommon", "rare", "epic", "legendary"]
RARITY_WEIGHTS = {"common": 60, "uncommon": 25, "rare": 10, "epic": 4, "legendary": 1}
SPECIES = [
    "duck",
    "goose",
    "blob",
    "cat",
    "dragon",
    "octopus",
    "owl",
    "penguin",
    "turtle",
    "snail",
    "ghost",
    "axolotl",
    "capybara",
    "cactus",
    "robot",
    "rabbit",
    "mushroom",
    "chonk",
]
BUDDY_SALT = "friend-2026-401"


def make_seed(random_mode: bool, explicit_seed: str | None) -> str:
    if explicit_seed:
        return explicit_seed
    if random_mode or not explicit_seed:
        return "".join(random.choices(string.digits, k=7))
    raise ValueError("unable to build seed")


def backup_file(src: Path, backup_dir: Path) -> Path:
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    dst = backup_dir / f"{src.name}.backup.{stamp}"
    dst.write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    return dst


def home_candidates() -> list[Path]:
    cands: list[Path] = []
    for key in ("HOME", "USERPROFILE"):
        raw = os.environ.get(key, "").strip()
        if raw:
            cands.append(Path(raw))
    cands.append(Path.home())

    uniq: list[Path] = []
    seen: set[str] = set()
    for p in cands:
        k = str(p.resolve()) if p.exists() else str(p)
        if k not in seen:
            seen.add(k)
            uniq.append(p)
    return uniq


def locate_claude_paths() -> tuple[Path, Path, Path]:
    candidates: list[tuple[Path, Path, Path]] = []
    for home in home_candidates():
        claude_dir = home / ".claude"
        candidates.append(
            (home / ".claude.json", claude_dir / "settings.json", claude_dir / "backups")
        )

    for global_file, settings_file, backups_dir in candidates:
        if global_file.exists() and settings_file.exists():
            return global_file, settings_file, backups_dir

    first_global, first_settings, first_backups = candidates[0]
    return first_global, first_settings, first_backups


def to_uint32(v: int) -> int:
    return v & 0xFFFFFFFF


def to_int32(v: int) -> int:
    v &= 0xFFFFFFFF
    return v if v < 0x80000000 else v - 0x100000000


def imul32(a: int, b: int) -> int:
    return to_int32((to_uint32(a) * to_uint32(b)) & 0xFFFFFFFF)


def fnv1a_32(text: str) -> int:
    h = to_int32(2166136261)
    for ch in text:
        h = to_int32(h ^ ord(ch))
        h = imul32(h, 16777619)
    return to_uint32(h)


class Mulberry32:
    def __init__(self, seed: int):
        self.state = to_int32(seed)

    def random(self) -> float:
        self.state = to_int32(self.state + 1831565813)
        t = imul32(self.state ^ (to_uint32(self.state) >> 15), 1 | self.state)
        t = to_int32(t + imul32(t ^ (to_uint32(t) >> 7), 61 | t) ^ t)
        return to_uint32(t ^ (to_uint32(t) >> 14)) / 4294967296


def calc_buddy(seed: str) -> tuple[str, str]:
    rng = Mulberry32(fnv1a_32(seed + BUDDY_SALT))
    r = rng.random() * 100
    rarity = "common"
    for key in RARITY_ORDER:
        r -= RARITY_WEIGHTS[key]
        if r < 0:
            rarity = key
            break
    species = SPECIES[int(rng.random() * len(SPECIES))]
    return rarity, species


def find_seed_for_target(
    target_species: str,
    target_rarity: str | None,
    max_attempts: int,
) -> str:
    for i in range(1, max_attempts + 1):
        seed = str(i).zfill(7)
        rarity, species = calc_buddy(seed)
        if species != target_species:
            continue
        if target_rarity and rarity != target_rarity:
            continue
        return seed
    rarity_hint = f" + {target_rarity}" if target_rarity else ""
    raise RuntimeError(
        f"No seed found for {target_species}{rarity_hint} in first {max_attempts} attempts."
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Reset local Claude /buddy companion state and set seed (defaults to random)."
    )
    parser.add_argument("--seed", help="Seed string, e.g. 0000693")
    parser.add_argument("--random", action="store_true", help="Generate random seed (default behavior)")
    parser.add_argument("--target", choices=SPECIES, help="Target species, e.g. dragon")
    parser.add_argument("--rarity", choices=RARITY_ORDER, help="Optional rarity filter with --target")
    parser.add_argument(
        "--clear-account-uuid",
        action="store_true",
        help="Deprecated alias. accountUuid is cleared by default now.",
    )
    parser.add_argument(
        "--keep-account-uuid",
        action="store_true",
        help="Keep oauthAccount.accountUuid (not recommended).",
    )
    parser.add_argument(
        "--max-attempts",
        type=int,
        default=5_000_000,
        help="Max seeds to scan when using --target (default: 5000000)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Preview changes only")
    parser.add_argument("--verbose", action="store_true", help="Print detailed debug output")
    args = parser.parse_args()

    if args.seed and args.target:
        raise ValueError("Use either --seed or --target, not both.")
    if args.rarity and not args.target:
        raise ValueError("--rarity requires --target.")

    if args.target:
        seed = find_seed_for_target(args.target, args.rarity, args.max_attempts)
    else:
        seed = make_seed(args.random, args.seed)

    global_file, settings_file, backups_dir = locate_claude_paths()

    if not global_file.exists():
        raise FileNotFoundError(f"Missing file: {global_file}")
    if not settings_file.exists():
        raise FileNotFoundError(f"Missing file: {settings_file}")

    global_data = json.loads(global_file.read_text(encoding="utf-8"))
    settings_data = json.loads(settings_file.read_text(encoding="utf-8"))

    oauth = global_data.get("oauthAccount", {})
    oauth_uuid = oauth.get("accountUuid") if isinstance(oauth, dict) else None

    clear_account_uuid = (not args.keep_account_uuid) or args.clear_account_uuid

    if clear_account_uuid and isinstance(oauth, dict) and "accountUuid" in oauth:
        oauth = dict(oauth)
        oauth.pop("accountUuid", None)
        global_data["oauthAccount"] = oauth
        oauth_uuid = None

    effective_id = oauth_uuid if oauth_uuid else seed
    predicted_rarity, predicted_species = calc_buddy(effective_id)

    if args.dry_run:
        if args.verbose:
            print("[dry-run] No files were modified.")
    else:
        backup_global = backup_file(global_file, backups_dir)
        backup_settings = backup_file(settings_file, backups_dir)

        global_data["userID"] = seed
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

        if args.verbose:
            print(f"Backed up: {backup_global}")
            print(f"Backed up: {backup_settings}")

    if args.verbose:
        if oauth_uuid:
            print("[warn] oauthAccount.accountUuid exists and may override userID in /buddy species calc.")
            print(f"[warn] accountUuid: {oauth_uuid}")
            print("[warn] Use --keep-account-uuid only if you intentionally want account-bound species.")
            print(f"[info] Effective ID used for prediction: accountUuid ({oauth_uuid})")
        else:
            print(f"[info] Effective ID used for prediction: seed ({seed})")

        print(f"Seed: {seed}")
        print(f"Predicted species: {predicted_species}")
        print(f"Predicted rarity: {predicted_rarity}")
        print(f"Global file: {global_file}")
        print(f"Settings file: {settings_file}")
        print("Next:")
        print("1) Start a fresh Claude session")
        print("2) Run /buddy")
    else:
        if args.dry_run:
            print("已模拟重置刷新。")
        else:
            print("已重置刷新。")
        print("请新开会话后运行 /buddy。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
