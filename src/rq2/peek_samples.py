from pathlib import Path
from sys import argv

import pandas as pd

SAMPLES = 10

IN = Path(argv[1])
up = pd.read_csv(IN / "up.csv").head(SAMPLES)
down = pd.read_csv(IN / "down.csv").head(SAMPLES)

print("UP")
for url in "https://github.com/" + up["project"] + "/pull/" + up["pull_id"].astype(str):
    print(url)
print()
print("DOWN")
for url in "https://github.com/" + down["project"] + "/pull/" + down["pull_id"].astype(str):
    print(url)


