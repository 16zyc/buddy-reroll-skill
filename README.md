# buddy-reroll-skill

Reset Claude Code `/buddy` local state and re-hatch with a chosen seed.

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
npx buddy-reroll-skill reroll --seed user-2224
```

Install and reroll with a fixed seed:

```bash
npx buddy-reroll-skill reroll --seed user-2224
```

Install and reroll with random seed:

```bash
npx buddy-reroll-skill reroll --random
```

Install then use short command:

```bash
buddy-reroll --seed user-2224
```

Windows:

```powershell
buddy-reroll --seed user-2224
```

## Direct script usage

```bash
python3 ~/.claude/skills/buddy-reroll/scripts/reroll_buddy.py --seed user-2224
python3 ~/.claude/skills/buddy-reroll/scripts/reroll_buddy.py --random
```
