#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export JUPYTER_CONFIG_DIR="$ROOT_DIR/.jupyter"
export JUPYTER_DATA_DIR="$ROOT_DIR/.jupyter-prefix/share/jupyter"
export IPYTHONDIR="$ROOT_DIR/.ipython"

exec jupyter lab
