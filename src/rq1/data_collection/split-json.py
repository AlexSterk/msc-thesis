import os
import sys
from pathlib import Path

DIR = Path(sys.argv[1])
OUT = DIR.parent / (DIR.name + "_slim")

OUT.mkdir(parents=True, exist_ok=True)

count = 0


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


for file in os.listdir(DIR):
    p = DIR / file
    with open(p, 'r') as f:
        lines = f.readlines()
    for chunk in chunks(lines, 1000):
        OUTFILE = OUT / (str(count) + ".json")
        count += 1
        with open(OUTFILE, 'w') as f:
            f.writelines(chunk)



