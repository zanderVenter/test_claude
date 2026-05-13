#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export R_LIBS_USER="$ROOT_DIR/.r-lib"
export JUPYTER_CONFIG_DIR="$ROOT_DIR/.jupyter"
export JUPYTER_DATA_DIR="$ROOT_DIR/.jupyter-prefix/share/jupyter"
export IPYTHONDIR="$ROOT_DIR/.ipython"

mkdir -p "$R_LIBS_USER" "$JUPYTER_CONFIG_DIR" "$JUPYTER_DATA_DIR" "$IPYTHONDIR"

Rscript -e "if (!requireNamespace('IRkernel', quietly = TRUE, lib.loc = Sys.getenv('R_LIBS_USER'))) install.packages('IRkernel', repos = 'https://cloud.r-project.org', lib = Sys.getenv('R_LIBS_USER'))"
Rscript -e "IRkernel::installspec(name = 'ir-local', displayname = 'R (local project)', user = FALSE, prefix = '$ROOT_DIR/.jupyter-prefix')"

echo "R kernel installed."
echo "Start Jupyter with: bash scripts/start_jupyter.sh"
