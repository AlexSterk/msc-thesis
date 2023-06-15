from shutil import copy

import pandas as pd
from selenium import webdriver

# IN = "data/rq2/github_queried_data_3.csv"
# IN = "data/rq2/github_queried_data_3_with_comments.csv"
IN = "data/rq2/github_queried_data_3_with_comments_2.csv"
# OUT = "data/rq2/github_queried_data_3_with_comments.csv"
OUT = "data/rq2/github_queried_data_3_with_comments_2.csv"

# Backup input just in case
copy(IN, IN + ".bak")
# Load Data
df: pd.DataFrame = pd.read_csv(IN, low_memory=False)
if "comment" not in df.columns:
    df["comment"] = None


# Get rid of duplicates, but keep existing comments!
_dup = df.sort_values(["created_at"], ascending=False).duplicated(["username", "name", "pullid", "only_codecov", "comment"])
# Keep the ones we don't drop
_df = df[~_dup].query("only_codecov == True")
# This particular repo doesnt play nice so we should filter it out
_broken_repo = (_df["username"] == "apache") & (_df["name"] == "skywalking")
_df = _df[~_broken_repo]

# For counting purposes we only need 1 of each duplicate (we figure out the rest later)
_df = _df.drop_duplicates(subset=["username", "name", "pullid"])

# Get the first 200
groupby = _df.groupby("coverage_goes_down")
print(groupby.size())
_df: pd.DataFrame = groupby.head(200).copy()
_df["url"] = "https://github.com/" + _df["username"] + "/" + _df["name"] + "/pull/" + _df["pullid"].astype(str)

# Filter uncommented PRs
f_df = _df[_df["comment"].isnull()]
max_i = len(f_df)
print(max_i)
n = 1

# Set up Chrome
browser = webdriver.Chrome()
for i, d in f_df.iterrows():
    print(f"{n}/{max_i}")
    print(d[["commitid", "coverage_goes_down", "state", "notification_type", "mentions"]])
    browser.get(d["url"])
    comment = input("Comment? ").strip()
    if comment:
        df.at[i, "comment"] = comment
    df.to_csv(OUT, index=False)
    print()
    n += 1
df.to_csv(OUT, index=False)
browser.close()
