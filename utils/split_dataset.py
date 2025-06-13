#!/usr/bin/env python3
"""Split dataset images into train and validation folders."""

from pathlib import Path
import random
import shutil
import json

RAW_DIR = Path('data/raw')
TRAIN_DIR = Path('data/train')
VAL_DIR = Path('data/val')

random.seed(42)

# Collect all jpg and png images under data/raw
image_paths = [p for ext in ('*.jpg', '*.png') for p in RAW_DIR.rglob(ext)]

random.shuffle(image_paths)

split_idx = int(len(image_paths) * 0.8)
train_paths = image_paths[:split_idx]
val_paths = image_paths[split_idx:]

for path in train_paths:
    class_name = path.parent.name
    dest_dir = TRAIN_DIR / class_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), dest_dir / path.name)

for path in val_paths:
    class_name = path.parent.name
    dest_dir = VAL_DIR / class_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(path), dest_dir / path.name)

print(f"Moved {len(train_paths)} images to {TRAIN_DIR} and {len(val_paths)} to {VAL_DIR}.")

# Build class index mapping from folders in training directory
class_names = sorted({p.name for p in TRAIN_DIR.iterdir() if p.is_dir()})
class_index = {name: idx for idx, name in enumerate(class_names)}

# Save mapping to utils/class_index.json
index_file = Path('utils/class_index.json')
index_file.write_text(json.dumps(class_index, indent=2))
print(f"Saved class index mapping to {index_file}")
