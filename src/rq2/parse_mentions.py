import pandas as pd

_df = pd.read_csv("data/rq2/github_queried_data_3.csv", low_memory=False)
df: pd.DataFrame = _df.query("only_codecov == True")

gdf = df.groupby("coverage_goes_down")
df = gdf.head(200)
gdf = df.groupby("coverage_goes_down")
mention_percentage = gdf["mentions"].value_counts() / 200 * 100
mention_percentage = mention_percentage.astype(str) + "%"
print(mention_percentage)


