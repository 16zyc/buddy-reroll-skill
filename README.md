# buddy-reroll-skill

快速重置 Claude `/buddy`。

## 能做什么

- 默认随机重置（清理旧 companion，重新孵化）
- 指定 seed 重置
- 按物种/稀有度自动找 seed（例如 `dragon + legendary`）
- 默认执行“完全重置”（会清理 account UUID 覆盖）

## 下载与安装

### 方式 1：一条命令安装（推荐）

```bash
npx -y github:16zyc/buddy-reroll-skill install
```

### 方式 2：Git 下载后安装

```bash
git clone https://github.com/16zyc/buddy-reroll-skill ~/.claude/skills/buddy-reroll
bash ~/.claude/skills/buddy-reroll/install.sh
```

Windows:

```powershell
git clone https://github.com/16zyc/buddy-reroll-skill $HOME/.claude/skills/buddy-reroll
powershell -ExecutionPolicy Bypass -File $HOME/.claude/skills/buddy-reroll/install.ps1 -Force
```

## 常用命令

```bash
buddy-reroll
buddy-reroll --seed 0000693
buddy-reroll --target dragon --rarity legendary
```

调试详细输出（可选）：

```bash
buddy-reroll --verbose
```
