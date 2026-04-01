# buddy-reroll-skill

Reset Claude Code `/buddy` local state and re-hatch with a chosen seed.

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

Install and reroll with a fixed seed:

```bash
npx buddy-reroll-skill reroll --seed user-2224
```

Install and reroll with random seed:

```bash
npx buddy-reroll-skill reroll --random
```

## Direct script usage

```bash
python3 ~/.claude/skills/buddy-reroll/scripts/reroll_buddy.py --seed user-2224
python3 ~/.claude/skills/buddy-reroll/scripts/reroll_buddy.py --random
```
