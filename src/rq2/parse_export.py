import json
from glob import glob
from pathlib import Path
from sys import argv

import pandas as pd

IN = Path(argv[1])
# TEMP_FILE = IN.parent / "df.temp.pickle"
OUT = Path(argv[2]) if len(argv) >= 3 else None
csv_files = glob(str(IN / "*.csv"))


def transform_totals(totals, diff=False):
    try:
        totals = json.loads(totals)
    except TypeError:
        return pd.Series()
    coverage = float(totals['c'])
    d = totals["diff"]
    patch = float(d[5]) if diff and d and d[5] is not None else None
    s = [coverage]
    if patch:
        s.append(patch)
    index = ["coverage"]
    if patch:
        index.append("patch_coverage")
    return pd.Series(s, index)


def transform_df(df: pd.DataFrame):
    print("\tParsing JSON")
    print("\t\tCurrent")
    cur = df["current_totals"].map(json.loads, 'ignore')
    print("\t\tBase")
    base = df["base_totals"].map(json.loads, 'ignore')
    print("\t\tHead")
    head = df["head_totals"].map(json.loads, 'ignore')
    print("\t\tDiff")
    diff = df["patch_coverage"].map(json.loads, 'ignore')
    print("\tCalculating coverage")
    print("\t\tCurrent")
    cur_cov = cur.map(lambda d: d["c"], "ignore").astype(float)
    print("\t\tBase")
    base_cov = base.map(lambda d: d["c"], "ignore").astype(float)
    print("\t\tHead")
    head_cov = head.map(lambda d: d["c"], "ignore").astype(float)
    print("\t\tCurrent Patch")
    cur_patch = cur.map(lambda d: d["diff"], "ignore").map(lambda a: a[5], "ignore").astype(float)
    print("\t\tHead Patch")
    head_patch = diff.map(lambda a: a[5], "ignore").astype(float)
    print("Updating Dataframe")
    df = df.drop(columns=["current_totals", "base_totals", "head_totals", "patch_coverage"])
    df = df.assign(cur_cov=cur_cov, base_cov=base_cov, head_cov=head_cov, cur_patch=cur_patch, head_patch=head_patch)
    return df


def main():
    print("Reading data")
    df: pd.DataFrame = pd.concat(map(pd.read_csv, csv_files))
    # df = pd.read_pickle(TEMP_FILE)
    print("Transforming data")
    df = transform_df(df)
    print(df)
    if OUT:
        print("Writing data")
        df.to_csv(OUT, index=False)
    print("Done")


main()
