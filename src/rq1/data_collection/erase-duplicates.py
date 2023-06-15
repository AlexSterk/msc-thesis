import sys
from pathlib import Path
from sys import argv

import pandas as pd
from pandas import DataFrame

FILE = Path(argv[1])

if not FILE.is_file():
    sys.exit("File not found, exiting...")

OUT = Path(argv[2]) if len(argv) >= 3 else None
DUP_FILE = Path(argv[3]) if len(argv) >= 4 else None

df = pd.read_csv(FILE)
print(len(df))
df = df.drop_duplicates()
print(len(df))

# TODO: Sort by some way to keep the latest version only, keep the latest entry

dropped = df.drop_duplicates(["project", "pull_id"])
print(len(dropped))

if OUT is not None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    dropped.to_csv(OUT, index=False)

if DUP_FILE is not None:
    DUP_FILE.parent.mkdir(parents=True, exist_ok=True)
    df["created_at"] = pd.to_datetime(df["created_at"])
    df["merged_at"] = pd.to_datetime(df["merged_at"])
    dup = df.duplicated(["project", "pull_id"], False)
    dup_df = df[dup].set_index(["project", "pull_id"]).sort_index()
    dup_df.to_csv(DUP_FILE)
    dropna: DataFrame
    dropna = dup_df.groupby(level=["project", "pull_id"]).diff().dropna(how="all")
    dropna = dropna[dropna.columns[dropna.nunique() > 1]]
    dropna.to_csv(DUP_FILE.parent / (DUP_FILE.name + "_diff.csv"))
