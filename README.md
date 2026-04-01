# buddy-reroll-skill

Reset Claude Code `/buddy` local state and re-hatch with a random seed by default, a chosen seed, or a target species/rarity search.

## Important

- Do not run `npx ...` directly inside the Claude chat input box.
- Run install/reroll in your system terminal (zsh/PowerShell/CMD) to avoid Claude usage/login limits.
- `/buddy-reroll` is not a built-in Claude slash command. If typed in Claude chat, it is treated as a normal model request and can fail due to account usage limits.

## Install (Git clone, ex-skill style)

Project-level:

```bash
mkdir -p .claude/skills
git clone https://github.com/16zyc/buddy-reroll-skill .claude/skills/buddy-reroll
bash .claude/skills/buddy-reroll/install.sh
```

Global:

```bash
git clone https://github.com/16zyc/buddy-reroll-skill ~/.claude/skills/buddy-reroll
bash ~/.claude/skills/buddy-reroll/install.sh
```

## Install / run with npm (npx)

Install skill files only:

```bash
npx buddy-reroll-skill install
```

Install and reroll (default random):

```bash
npx buddy-reroll-skill reroll
```

Install and reroll with a fixed seed:

```bash
npx buddy-reroll-skill reroll --seed 0000693
```

Install and reroll with random seed:

```bash
npx buddy-reroll-skill reroll --random
```

Install and reroll by target:

```bash
npx buddy-reroll-skill reroll --target dragon --rarity legendary
```

By default, account UUID will be cleared so seed fully controls species.
If you want to keep account UUID, pass `--keep-account-uuid`:

```bash
npx buddy-reroll-skill reroll --seed 0000693 --keep-account-uuid
```

Install then use short command:

```bash
buddy-reroll
```

Windows:

```powershell
buddy-reroll --random
```

## Direct script usage

```bash
python3 ~/.claude/skills/buddy-reroll/scripts/reroll_buddy.py --random
python3 ~/.claude/skills/buddy-reroll/scripts/reroll_buddy.py --seed 0000693
python3 ~/.claude/skills/buddy-reroll/scripts/reroll_buddy.py --target dragon --rarity legendary
python3 ~/.claude/skills/buddy-reroll/scripts/reroll_buddy.py --seed 0000693 --keep-account-uuid
python3 ~/.claude/skills/buddy-reroll/scripts/reroll_buddy.py --seed 0000693 --verbose
```

Default output is concise. Use `--verbose` to print seed/species/rarity/debug details.
