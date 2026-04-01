---
name: buddy-reroll
description: Reset local Claude Code /buddy companion state and re-hatch with a chosen or random seed by updating ~/.claude.json and ~/.claude/settings.json. Use when the user asks to reroll buddy, re-hatch companion, switch buddy seed, or recover from a stuck companion result.
---

# Buddy Reroll

Reset local companion state safely and quickly.

Default mode is random:

```bash
python3 scripts/reroll_buddy.py
```

Run the bundled script:

```bash
python3 scripts/reroll_buddy.py
```

Use a specific seed only when user explicitly asks for one:

```bash
python3 scripts/reroll_buddy.py --seed 0000693
```

Target a species / rarity (auto-search seed):

```bash
python3 scripts/reroll_buddy.py --target dragon --rarity legendary
```

By default, account UUID will be cleared to fully reset buddy:

```bash
python3 scripts/reroll_buddy.py --seed 0000693
```

## Workflow

1. Back up `~/.claude.json` and `~/.claude/settings.json` into `~/.claude/backups`.
2. Set `~/.claude.json.userID` to plain `seed`.
3. Remove `~/.claude.json.companion` so buddy can hatch again.
4. Set `~/.claude/settings.json.userID` to the plain seed string.
5. Print the exact command to launch Claude and hatch again.

## Commands

Default random reroll (recommended):

`python3 scripts/reroll_buddy.py`

Use a specific seed:

```bash
python3 scripts/reroll_buddy.py --seed 0000693
```

Find seed by target:

```bash
python3 scripts/reroll_buddy.py --target dragon --rarity legendary
```

Keep account UUID (not recommended):

```bash
python3 scripts/reroll_buddy.py --seed 0000693 --keep-account-uuid
```

Show full debug info:

```bash
python3 scripts/reroll_buddy.py --seed 0000693 --verbose
```

Inspect without writing:

```bash
python3 scripts/reroll_buddy.py --dry-run
```

## Notes

- This skill only edits local files under `~/.claude`.
- If the companion still does not change, run `/buddy` again in a fresh Claude session.
- Use backup files in `~/.claude/backups` to restore previous state.
- If user does not provide a seed, default to random mode.
- account UUID is removed by default so seed fully controls species.
- Response style: do not add narrative summaries like "Your new buddy is ...".
- Response style: return concise result lines only (seed/species/rarity + next step).
- Script output is concise by default; use `--verbose` only when debugging.
