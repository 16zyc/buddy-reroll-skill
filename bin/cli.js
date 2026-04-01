#!/usr/bin/env node
const path = require("path");
const { spawnSync } = require("child_process");

const repoRoot = path.resolve(__dirname, "..");
const installScript = path.join(repoRoot, "install.sh");
const targetScript = path.join(
  process.env.HOME || "",
  ".claude",
  "skills",
  "buddy-reroll",
  "scripts",
  "reroll_buddy.py"
);

function run(cmd, args, opts = {}) {
  const ret = spawnSync(cmd, args, {
    stdio: "inherit",
    ...opts,
  });
  if (ret.status !== 0) {
    process.exit(ret.status || 1);
  }
}

function hasArg(name) {
  return process.argv.slice(2).includes(name);
}

function argValue(name) {
  const args = process.argv.slice(2);
  const i = args.indexOf(name);
  if (i >= 0 && i + 1 < args.length) return args[i + 1];
  return null;
}

function printHelp() {
  console.log("buddy-reroll-skill");
  console.log("");
  console.log("Install skill only:");
  console.log("  npx buddy-reroll-skill install");
  console.log("");
  console.log("Install and reroll with seed:");
  console.log("  npx buddy-reroll-skill reroll --seed user-2224");
  console.log("");
  console.log("Install and reroll random:");
  console.log("  npx buddy-reroll-skill reroll --random");
}

const cmd = process.argv[2];

if (!cmd || cmd === "--help" || cmd === "-h") {
  printHelp();
  process.exit(0);
}

if (cmd === "install") {
  run("bash", [installScript], { cwd: repoRoot });
  process.exit(0);
}

if (cmd === "reroll") {
  run("bash", [installScript], { cwd: repoRoot });

  const args = [];
  const seed = argValue("--seed");
  if (seed) {
    args.push("--seed", seed);
  } else if (hasArg("--random")) {
    args.push("--random");
  } else {
    args.push("--random");
  }
  if (hasArg("--dry-run")) {
    args.push("--dry-run");
  }

  run("python3", [targetScript, ...args]);
  process.exit(0);
}

printHelp();
process.exit(1);
