# src/config.py
import os
from pathlib import Path

# Project root directory
ROOT_DIR = Path(__file__).parent.parent

# Data directories
DATA_DIR = os.path.join(ROOT_DIR, "data")
BRONZE_DIR = os.path.join(DATA_DIR, "bronze")
SILVER_DIR = os.path.join(DATA_DIR, "silver")
GOLD_DIR = os.path.join(DATA_DIR, "gold")

# Create directories if they don't exist
for directory in [BRONZE_DIR, SILVER_DIR, GOLD_DIR]:
    os.makedirs(directory, exist_ok=True)
