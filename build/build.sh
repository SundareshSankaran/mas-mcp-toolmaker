#!/usr/bin/env bash

# Arguments


set -euo pipefail

python -m venv buildproj
. buildproj/bin/activate

pip install --upgrade uv

uv pip install -r requirements.txt --force-reinstall --upgrade

python -m ipykernel install --user --name=buildproj


# python scripts/



deactivate

# rm -rf buildproj