#!/usr/bin/env bash
# Mac/Linux setup: bash setup/setup.sh
cd "$(dirname "$0")/.."
PY=""
for c in python3 python; do
  if command -v $c >/dev/null && $c -c 'import sys; sys.exit(0 if sys.version_info>=(3,10) else 1)'; then PY=$c; break; fi
done
if [ -z "$PY" ]; then
  echo "Python 3.10+ not found. Mac: brew install python   Linux: sudo apt-get install -y python3 python3-pip python3-venv"; exit 1
fi
echo "Using $PY"
$PY engine/doctor.py --install
$PY engine/doctor.py
