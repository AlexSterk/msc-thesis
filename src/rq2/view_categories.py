import pandas as pd

IN = "results/rq2/comments_5.csv"

_df = pd.read_csv(IN, low_memory=False)

_df["coverage_goes_up"] = ~_df["coverage_goes_down"]
df = _df[["S1", "S2", "S3", "S4", "coverage_goes_up"]].sort_values("S4").groupby("coverage_goes_up").head(200).copy()
# df["closed"] = df["state"] == "closed"
# df["merged"] = df["state"] == "merged"
# df["open"] = df["state"] == "open"
gdf = df.groupby(["coverage_goes_up"])
print(gdf.sum().transpose().to_string())

print(_df[~_df["coverage_goes_up"] & _df["S3"]][["state", "url"]])




# df = _df.sort_values("S4").groupby("coverage_goes_down").head(200)
#
# tab = pd.crosstab(df["coverage_goes_down"], [df["S1"], df["S2"], df["S3"], df["S4"]], margins=True)
# print(tab.to_string())
