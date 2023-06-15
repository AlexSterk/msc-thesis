from pathlib import Path
from sys import argv

import pandas as pd

IN = Path(argv[1])
QUERY = argv[2] if len(argv) >= 3 else None
OPTIONS = argv[3:] if len(argv) >= 4 else []
OPTIONS = [s.split("=") for s in OPTIONS]
OPTIONS = {a[0]: a[1] for a in OPTIONS if len(a) == 2}

N = int(OPTIONS["n"]) if "n" in OPTIONS else None
C = OPTIONS["c"].split(",") if "c" in OPTIONS else None

df = pd.read_csv(IN)
f_df = df.query(QUERY).copy() if QUERY else df.copy()

f_df["url"] = "https://github.com/" + f_df["username"] + "/" + f_df["name"] + "/pull/" + f_df["pullid"].astype(str)

print(len(f_df))
columns = C if C else [c for c in f_df.columns if c != "raw_data"]
head = f_df[columns].head(N if N else 10)
print(head.to_string())
