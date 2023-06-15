import sys
from pathlib import Path

import pandas as pd


class Comment:
    def __init__(self, user_id, comment_id):
        self.user_id = user_id
        self.comment_id = comment_id

    def __hash__(self):
        return hash(self.comment_id)

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other):
        return isinstance(other, Comment) and self.comment_id == other.comment_id


def temp(x):
    return x.map(lambda _: set(x.sum()))


# Deal with file paths
IN = Path(sys.argv[1])
OUT = Path(sys.argv[2])
DUP_FILE = OUT.parent / "dup.csv"

# Read in data
df: pd.DataFrame = pd.read_json(IN, lines=True, orient="records")

# Create timestamps
df["created_at"] = pd.to_datetime(df["created_at"])
df["merged_at"] = pd.to_datetime(df["merged_at"])
df["headUpdateStamp"] = pd.to_datetime(df["headUpdateStamp"])
df["baseUpdateStamp"] = pd.to_datetime(df["baseUpdateStamp"])

# Merge issue and pr comments
df["comments"] = df["issueComments"] + df["prComments"]
df["comments"] = df["comments"].map(lambda l: [Comment(**c) for c in l])
df = df.drop(columns=["issueComments", "prComments"])

# Combine duplicate comment data
grouped = df.groupby(["project", "pull_id"])
comments_per_pr = grouped["comments"].transform(lambda s: [set(s.sum()) for _ in s])
df["comments"] = comments_per_pr

# Get reviewers from comments - authors
df["reviewers"] = df["comments"].map(lambda s: set([c.user_id for c in s])) - df["authors"].map(set)
df["comments"] = df["comments"].map(len)
df["reviewers"] = df["reviewers"].map(len)
df = df.drop(columns=["authors"])

# Remove duplicates part one
df = df.drop_duplicates().sort_values(["project", "pull_id", "created_at"])

# Get some insight on the duplicates present
dup_df = df[df.duplicated(["project", "pull_id"], False)]
diff: pd.DataFrame = dup_df.groupby(["project", "pull_id"]).diff().dropna(how="all")
non_zero = ~(diff == 0).all()
diff = diff[diff.columns[non_zero]]
diff.to_csv(DUP_FILE, index=False)

# Remove duplicates part two
df = df.drop_duplicates(["project", "pull_id"])
df = df.drop(columns=["headUpdateStamp", "baseUpdateStamp"])

# Write to CSV
df.to_csv(OUT, index=False)
