---
name: buddy-reroll
description: Reset local Claude Code /buddy companion state and re-hatch with a chosen or random seed by updating ~/.claude.json and ~/.claude/settings.json. Use when the user asks to reroll buddy, re-hatch companion, switch buddy seed, or recover from a stuck companion result.
---

# Buddy Reroll

Reset local companion state safely and quickly.

Run the bundled script:

```bash
python3 scripts/reroll_buddy.py --seed user-2224
```

Or use a random seed:

```bash
python3 scripts/reroll_buddy.py --random
```

## Workflow

1. Back up `~/.claude.json` and `~/.claude/settings.json` into `~/.claude/backups`.
2. Set `~/.claude.json.userID` to `sha256(seed)`.
3. Remove `~/.claude.json.companion` so buddy can hatch again.
4. Set `~/.claude/settings.json.userID` to the plain seed string.
5. Print the exact command to launch Claude and hatch again.

## Commands

Use a specific seed:

```bash
python3 scripts/reroll_buddy.py --seed user-2224
```

Use a random seed:

```bash
python3 scripts/reroll_buddy.py --random
```

Inspect without writing:

```bash
python3 scripts/reroll_buddy.py --seed user-2224 --dry-run
```

## Notes

- This skill only edits local files under `~/.claude`.
- If the companion still does not change, run `/buddy` again in a fresh Claude session.
- Use backup files in `~/.claude/backups` to restore previous state.
