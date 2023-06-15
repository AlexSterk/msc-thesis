from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
from pandas import DataFrame

IN = Path("results/rq1/models.csv")
ORIG_DATA = Path("results/rq1/data.csv")


def parse_metrics(df):
    metrics = []
    col: str
    for col in df.columns:
        if col.endswith("_coeff"):
            metrics.append(col.replace("_coeff", ""))
    return metrics

def write_data(df):
    orig_df = pd.read_csv(ORIG_DATA)
    orig_df = orig_df[orig_df["project"].isin(df["name"])]
    return orig_df

def main():
    df = pd.read_csv(IN)
    f_df: DataFrame = df.query(f"`R-squared` >= 0.7 & size >= 100").sort_values(by="R-squared", ascending=False)
    data = write_data(f_df)
    print(data.columns)
    cov = data['patch_coverage_coverage']
    print(cov.describe())
    counts = cov.value_counts()
    print(counts)
    print(counts.sum(), len(cov))
    # sort data into three groups


    def label(x):
        x = cov[x]
        if x == 100:
            return "100%"
        elif x == 0:
            return "0%"
        else:
            return "Other"

    count = cov.groupby(label).count()
    print(count)
    count.plot(kind='bar')
    plt.show()



if __name__ == '__main__':
    main()
