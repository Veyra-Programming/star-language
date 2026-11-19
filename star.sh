#!/usr/bin/env sh
export PYTHONUTF8=1
export PYTHONIOENCODING=utf-8
DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -f "$DIR/star.py" ]; then
    TARGET_PY="$DIR/star.py"
elif [ -f "$DIR/../star.py" ]; then
    TARGET_PY="$DIR/../star.py"
else
    TARGET_PY="$DIR/star.py"
fi

if command -v python3 >/dev/null 2>&1; then
    exec python3 "$TARGET_PY" "$@"
elif command -v python >/dev/null 2>&1; then
    exec python "$TARGET_PY" "$@"
else
    echo "[ERROR] python3 was not found in PATH." >&2
    exit 1
fi
