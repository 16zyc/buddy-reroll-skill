#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="buddy-reroll"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FORCE="${FORCE:-0}"

TARGETS=()
TARGETS+=("$HOME/.claude/skills/${SKILL_NAME}")
TARGETS+=("${CODEX_HOME:-$HOME/.codex}/skills/${SKILL_NAME}")
BIN_DIR="$HOME/.local/bin"

sync_to_target() {
  local target_dir="$1"
  local target_root
  target_root="$(dirname "$target_dir")"

  mkdir -p "${target_root}"

  if [[ -d "${target_dir}" ]]; then
    if [[ "${FORCE}" == "1" ]]; then
      rm -rf "${target_dir}"
      mkdir -p "${target_dir}"
    else
      echo "Target already exists: ${target_dir}"
      echo "Update in place (use FORCE=1 for clean reinstall)."
    fi
  else
    mkdir -p "${target_dir}"
  fi

  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete \
      --exclude ".git" \
      --exclude ".DS_Store" \
      --exclude "node_modules" \
      "${SRC_DIR}/" "${target_dir}/"
  else
    cp -R "${SRC_DIR}/." "${target_dir}/"
    rm -rf "${target_dir}/.git" "${target_dir}/node_modules" || true
  fi

  chmod +x "${target_dir}/scripts/reroll_buddy.py" || true
  chmod +x "${target_dir}/install.sh" || true
  return 0
}

echo "Installing skill: ${SKILL_NAME}"
echo "Source: ${SRC_DIR}"

OK_COUNT=0
for t in "${TARGETS[@]}"; do
  echo "Target: ${t}"
  if sync_to_target "${t}"; then
    OK_COUNT=$((OK_COUNT + 1))
  fi
done

if [[ "${OK_COUNT}" -eq 0 ]]; then
  echo "No targets updated."
  exit 1
fi

echo "Install complete (${OK_COUNT} target(s))."

mkdir -p "${BIN_DIR}"
cat > "${BIN_DIR}/buddy-reroll" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
python3 "$HOME/.claude/skills/buddy-reroll/scripts/reroll_buddy.py" "$@"
EOF
chmod +x "${BIN_DIR}/buddy-reroll"

echo "Try:"
echo "  python3 \"$HOME/.claude/skills/${SKILL_NAME}/scripts/reroll_buddy.py\" --random"
echo "  buddy-reroll --random"
