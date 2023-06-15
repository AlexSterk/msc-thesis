import glob
from pathlib import Path

import pandas as pd
import progress.bar

IN = Path("results/data")
OUT = Path("results/data.csv")
DATA_FILE = OUT.parent / "_dataframe"

COLUMNS = ["repo", "pull_id", "created_at", "merged_at", "intra_branch"]
COVERAGE_DATA = list("cfnhmp")


def read_json():
    print("Processing JSON files into single DataFrame")
    files = glob.glob(str(IN / "*.json"))
    df = pd.DataFrame()
    for f in progress.bar.Bar('Processing', suffix="[%(index)d / %(max)d] - %(eta)ds").iter(files):
        f_df = pd.read_json(f, orient="records", lines=True)
        df = df.append(f_df, ignore_index=True)
    df.to_pickle(str(DATA_FILE))
    return df


if __name__ == '__main__':
    df = read_json() if not DATA_FILE.is_file() else pd.read_pickle(DATA_FILE)
    print(df)

#
# files = glob.glob(s)
# # for f in progress.bar.Bar('Processing', suffix="[%(index)d / %(max)d] - %(eta)ds").iter(files):
# #     time.sleep(1)
# # exit(0)
#
# for f in progress.bar.Bar('Processing', suffix="[%(index)d / %(max)d] - %(eta)ds").iter(files):
#     e_df = pd.DataFrame()
#     f_df = pd.read_json(f, orient="records", lines=True)
#
#     df = df.append(f_df, ignore_index=True)
#     continue
#
#     e_df[COLUMNS] = f_df[COLUMNS]
#
#     coverage_before = f_df["coverge_base"].combine_first(f_df["coverage_compared_to"]).dropna()
#     coverage_before = coverage_before.map(json.loads)
#     coverage_before = coverage_before.apply(pd.Series)[COVERAGE_DATA]
#     coverage_before = coverage_before.rename(columns={
#         "c": "coverage",
#         "f": "files",
#         "n": "lines",
#         "h": "hits",
#         "m": "misses",
#         "p": "partials"
#     })
#     coverage_before["coverage"] = coverage_before["coverage"].astype(float)
#     e_df = e_df.join(coverage_before.add_prefix("coverage_before_"), how="inner")
#
#     coverage_after = f_df["coverage_head"].dropna()
#     coverage_after = coverage_after.map(json.loads)
#     coverage_after = coverage_after.apply(pd.Series)[COVERAGE_DATA]
#     coverage_after = coverage_after.rename(columns={
#         "c": "coverage",
#         "f": "files",
#         "n": "lines",
#         "h": "hits",
#         "m": "misses",
#         "p": "partials"
#     })
#     coverage_after["coverage"] = coverage_after["coverage"].astype(float)
#     e_df = e_df.join(coverage_after.add_prefix("coverage_after_"), how="inner")
#
#     coverage_diff: pd.DataFrame = coverage_after - coverage_before
#     e_df = e_df.join(coverage_diff.add_prefix("coverage_diff_"), how="inner")
#
#     patch_coverage = f_df["coverage_diff"].dropna()
#     patch_coverage = patch_coverage.map(json.loads)
#     patch_coverage = patch_coverage.apply(pd.Series)
#     patch_coverage: pd.DataFrame = patch_coverage.drop(columns=patch_coverage.columns[6:])
#     patch_coverage.columns = ['files', 'lines', 'hits', 'misses', 'partials', 'coverage']
#     e_df = e_df.join(patch_coverage.add_prefix("patch_coverage_"), how="inner")
#
#     e_df["time_to_merge"] = (e_df["merged_at"] - e_df["created_at"]) / pd.Timedelta(hours=1)
#     e_df["commits_in_project"] = f_df["commit_authors_in_project"].map(len)
#     e_df["contributors_in_project"] = f_df["commit_authors_in_project"].map(set).map(len)
#     e_df["commits_in_pr"] = f_df["commit_authors_in_pr"].map(len)
#     e_df["authors_in_pr"] = f_df["commit_authors_in_pr"].map(set).map(len)
#     e_df["number_of_comments"] = f_df["issue_comments_authors"].map(len) + f_df["pr_review_comment_authors"].map(len)
#     e_df["number_of_reviewers"] = ((f_df["issue_comments_authors"] + f_df["pr_review_comment_authors"]).map(set) - f_df["commit_authors_in_pr"].map(set)).map(len)
#
#     # print(e_df.groupby(["repo", "pull_id"]).filter(lambda x: len(x) > 1).sort_values(by=["repo", "pull_id"]))
#     # print(e_df.head().to_string())
#     df = df.append(f_df, ignore_index=True)
#
# df.to_csv('results/test.csv', index=False)
# print(df)
