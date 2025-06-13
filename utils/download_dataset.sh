#!/usr/bin/env bash
set -e

# Install kaggle CLI if missing
if ! command -v kaggle >/dev/null 2>&1; then
    pip install kaggle
fi

mkdir -p data/raw
# Download and unzip the dataset
kaggle datasets download aesthetic-face-rec-dataset --unzip -p data/raw

# Count images in data/raw
python - <<'PY'
import os
img_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
count = 0
for root, _, files in os.walk('data/raw'):
    for f in files:
        if os.path.splitext(f)[1].lower() in img_exts:
            count += 1
print(f"Downloaded {count} images.")
PY

