import sys
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from pandas import Series, DataFrame

WRITE = True

def parse_metrics(df):
    metrics = []
    col: str
    for col in df.columns:
        if col.endswith("_coeff"):
            metrics.append(col.replace("_coeff", ""))
    return metrics


def get_metric_statistics(df: DataFrame, metrics):
    x_df = pd.DataFrame()

    for metric in metrics:
        coeffs = df[df[f"{metric}_pvalue"] < 0.05][f"{metric}_coeff"]
        coeffs = coeffs.to_frame()
        coeffs["metric"] = coeffs[f"{metric}_coeff"].map(lambda _: metric)
        coeffs["coeff"] = coeffs[f"{metric}_coeff"]
        coeffs = coeffs.drop(f"{metric}_coeff", axis=1)
        # print(coeffs)
        x_df = pd.concat([x_df, coeffs], axis=0)
        # print(x_df)

    desc: DataFrame = x_df.groupby("metric")["coeff"].describe()
    desc = desc.sort_values("count", ascending=False)
    return desc

    res = []
    for metric in metrics:
        data = {"metric": metric}
        if df[f"{metric}_pvalue"].count() == 0:
            continue

        c: Series
        c = (df[f"{metric}_pvalue"] < 0.05)
        data["significant"] = c.value_counts()[True] if True in c.value_counts() else 0

        significants = df[c]
        coeff_data = significants[f"{metric}_coeff"]
        data["min_coeff"] = coeff_data.min()
        data["max_coeff"] = coeff_data.max()
        data["mean_coeff"] = coeff_data.mean()
        data["std_coeff"] = coeff_data.std()

        data["feature_included"] = df[f"{metric}_pvalue"].count()

        res.append(data)
    res = pd.DataFrame(res).sort_values(by="significant", ascending=False)
    print(res)
    return res


def correlation(df: DataFrame, metrics):
    bools = [df[f"{metric}_pvalue"] < 0.05 for metric in metrics]
    new_df = pd.concat(bools, axis=1, keys=metrics)
    corr = new_df.corr()

    corr_pairs = corr.unstack().sort_values(ascending=False)
    pairs = corr_pairs

    for k1, metric1 in enumerate(metrics):
        for k2, metric2 in enumerate(metrics):
            if k2 >= k1:
                pairs = pairs.drop(index=(metric1, metric2))

    return corr, pairs


def plot_coeffs(df, metrics):
    for metric in metrics:
        f_df = df.query(f"{metric}_pvalue < 0.05")
        # remove outliers

        fig: Figure
        ax1: Axes
        ax2: Axes

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 5))
        # plt.gcf().subplots_adjust(bottom=0.5)
        fig.suptitle(f"{metric} N={len(f_df)}/{len(df)}")
        ax1.boxplot(f_df[f"{metric}_coeff"])
        ax2.scatter(f_df["name"], f_df[f"{metric}_coeff"])
        plt.xticks(rotation=45, ha='right')
        # plt.tick_params(axis="x", labelbottom=False)
        plt.tight_layout()
        if WRITE:
            fig.savefig(f'{FIG_DIR}/{metric}.png')
        plt.close()
        # plt.show()
    return


def plot_corr(corr):
    plt.figure(figsize=(4 * 6, 3 * 6))
    sns.heatmap(corr, xticklabels=True, yticklabels=True)
    if WRITE:
        plt.savefig(f'{FIG_DIR}/correlation.png')
    plt.close()
    # plt.show()


def get_project_stats(df, metrics):
    def temp(x):
        res = {
            metric: x[f"{metric}_pvalue"] < 0.05 for metric in metrics
        }
        res["name"] = x["name"]
        res["size"] = x["size"]
        res["significant"] = sum([ x[f"{metric}_pvalue"] < 0.05 for metric in metrics])
        res["significant coverage"] = sum([ x[f"{metric}_pvalue"] < 0.05 for metric in metrics if "coverage" in metric and not ("file" in metric or "line" in metric)])
        return res
    new_df: DataFrame = df.apply(temp, axis=1, result_type="expand")
    new_df = new_df[ ["name", "size", "significant"] + [col for col in new_df.columns if col not in ["name", "size", "significant"]] ]
    return new_df.sort_values("significant", ascending=False)

def project_analysis(df):
    orig_df = pd.read_csv(ORIG_DATA)
    projects = orig_df.groupby("project")
    multi_df = pd.DataFrame()
    for name in df["name"]:
        project: DataFrame = projects.get_group(name)
        desc = project.describe()
        index = pd.MultiIndex.from_product([[name], desc.index])
        desc = desc.set_index(index)
        multi_df = pd.concat([multi_df, desc], axis=0, join="outer")
    return multi_df

def write_data(df):
    orig_df = pd.read_csv(ORIG_DATA)
    orig_df = orig_df[orig_df["project"].isin(df["name"])]
    return orig_df

if __name__ == '__main__':
    IN = Path("data/post/recreate_results_rq1_part1.csv")
    OUT = Path("data/post/recreate_results_rq1_part2.xlsx")
    FIG_DIR = Path("data/post/figs/rq1")
    ORIG_DATA = Path("data/rq1/marquee_open_source_full_3_no_dupl_first.csv")

    if not IN.is_file():
        sys.exit("Input file not a file, exiting...")

    if not ORIG_DATA.is_file():
        sys.exit("Data file not a file, exiting...")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    FIG_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(IN)
    metrics = parse_metrics(df)
    writer = pd.ExcelWriter(OUT, engine='xlsxwriter') if WRITE else pd.ExcelWriter(tempfile.TemporaryFile(), engine='xlsxwriter')

    f_df: DataFrame = df.query(f"`R-squared` >= 0.7 & size >= 100").sort_values(by="R-squared", ascending=False)
    # print(f_df.to_string(), "\n")
    # print(len(f_df))
    f_df.to_excel(writer, "raw_data", index=False)

    res = get_metric_statistics(f_df, metrics)
    # print(res.to_string(), "\n")
    res.to_excel(writer, "coeff_analysis")

    corr, pairs = correlation(f_df, metrics)
    print(pairs[pairs.abs() > 0.7], "\n")
    corr.to_excel(writer, "significance_corr")

    plot_coeffs(f_df, metrics)
    plot_corr(corr)

    stats = get_project_stats(f_df, metrics)
    # print(stats)
    stats.to_excel(writer, "projects_analysis")

    multi = project_analysis(f_df)
    multi.to_excel(writer, "project_stats")

    data = write_data(df)
    data.to_excel(writer, "original_data")

    writer.save()
