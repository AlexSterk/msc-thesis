from pathlib import Path
from sys import argv

import pandas as pd

SAMPLES = 400

# Read in full data
IN = Path(argv[1])
OUT = Path(argv[2]) if len(argv) >= 3 else None
df = pd.read_csv(IN)

# Keep only rows where coverage actually changes
df = df.query("diff_coverage_coverage != 0")

# Divide into classes
coverage_up = df["diff_coverage_coverage"] > 0
up: pd.DataFrame = df[coverage_up]
down: pd.DataFrame = df[~coverage_up]

# Sample from both
sample_up = up.sample(SAMPLES)
sample_down = down.sample(SAMPLES)

# Output to file
if OUT:
    OUT.mkdir(parents=True, exist_ok=True)
    sample_up.to_csv(OUT / "up.csv", index=False)
    sample_down.to_csv(OUT / "down.csv", index=False)
