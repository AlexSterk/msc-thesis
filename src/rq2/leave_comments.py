from pathlib import Path
from sys import argv, stdin

import pandas as pd

SAMPLES = 20
PRINT = True

IN = Path(argv[1])
OUT = Path(argv[2]) if len(argv) > 2 else None


columns = ["coverage_goes_down", "state", "notification_type", "commitid", "url", "comment"]
def main():
    df: pd.DataFrame
    df = pd.read_csv(IN)

    if PRINT:
        print(df)
        exit()


    df.query("only_codecov == True", True)
    df = df.groupby("coverage_goes_down").head(SAMPLES).copy()
    df["url"] = "https://github.com/" + df["username"] + "/" + df["name"] + "/pull/" + df["pullid"].astype(str)
    df["comment"] = ""

    for i, s in df.iterrows():
        print(s[columns].to_frame().to_string())
        strip = stdin.readline().strip()
        if len(strip) > 0:
            df.at[i, "comment"] = strip

    if OUT:
        df[columns].to_csv(OUT, index=False)


def print(df: pd.DataFrame):
    if OUT:
        df["comment"] = df["comment"].map(str.strip)
        df[columns].to_csv(OUT, index=False)

main()
