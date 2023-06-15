import pandas as pd

IN = "data/rq3/results/label_to_group.csv"
OUT = "data/rq3/results/groups.csv"

df = pd.read_csv(IN)
df = df.set_index(["Question", "Group"]).sort_index()
df["Codes"] = df.groupby(["Question", "Group"])["Code"].apply(" + ".join)
df = df.drop(columns="Code").reset_index().drop_duplicates()
df["Name"] = None
df["Summary"] = None
df["Extra comments"] = None
df["Group"] = df["Group"].astype('Int64')


# print(df)
df.to_csv(OUT, index=False)
