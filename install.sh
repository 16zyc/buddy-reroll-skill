#!/usr/bin/env bash
set -euo pipefail

SKILL_NAME="buddy-reroll"
SRC_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_ROOT="${CODEX_HOME:-$HOME/.codex}/skills"
TARGET_DIR="${TARGET_ROOT}/${SKILL_NAME}"

echo "Installing skill: ${SKILL_NAME}"
echo "Source: ${SRC_DIR}"
echo "Target: ${TARGET_DIR}"

mkdir -p "${TARGET_ROOT}"

if [[ -d "${TARGET_DIR}" ]]; then
  if [[ "${FORCE:-0}" != "1" ]]; then
    echo "Target already exists: ${TARGET_DIR}"
    echo "Re-run with FORCE=1 to overwrite."
    exit 1
  fi
  rm -rf "${TARGET_DIR}"
fi

mkdir -p "${TARGET_DIR}"

if command -v rsync >/dev/null 2>&1; then
  rsync -a --delete \
    --exclude ".git" \
    --exclude ".DS_Store" \
    "${SRC_DIR}/" "${TARGET_DIR}/"
else
  cp -R "${SRC_DIR}/." "${TARGET_DIR}/"
  rm -rf "${TARGET_DIR}/.git" || true
fi

chmod +x "${TARGET_DIR}/scripts/reroll_buddy.py" || true

echo "Install complete."
echo "Try:"
echo "  python3 \"${TARGET_DIR}/scripts/reroll_buddy.py\" --seed user-2224"
