import os
import sys
sys.path.insert(0, os.getcwd())

from datasets import load_dataset
import pandas as pd

try:
    print("Loading open-llm-leaderboard/contents dataset...")
    # Load only the first few rows or streaming to check speed and columns
    dataset = load_dataset("open-llm-leaderboard/contents", split="train", streaming=True)
    # Take first row
    first_row = next(iter(dataset))
    print("\nColumns and sample row:")
    print(first_row.keys())
    for k, v in list(first_row.items())[:10]:
        print(f"{k}: {v}")
except Exception as e:
    print(f"Error: {e}")
