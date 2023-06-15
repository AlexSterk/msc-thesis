raise Exception("This should never run again")

IN = "data/rq2/github_queried_data_3.csv"
IN2 = "data/rq2/github_queried_data_3_with_comments.csv"
OUT = "data/rq2/github_queried_data_3_with_comments.csv"

df: pd.DataFrame = pd.read_csv(IN, low_memory=False)
df2: pd.DataFrame = pd.read_csv(IN2, low_memory=False)
# df["url"] = "https://github.com/" + df["username"] + "/" + df["name"] + "/pull/" + df["pullid"].astype(str)
# f_df = df.query("only_codecov == True")
# f_df = f_df.groupby("coverage_goes_down").head(200)

x_df = df.merge(df2, how="left")
x_df = x_df.drop(columns=["url"])
x_df.to_csv(OUT, index=False)


# f_df = f_df[~f_df["mentions"].isnull()]
# max_i = len(f_df)
# print(max_i)
# n = 0
# for i, d in f_df.iterrows():
#     print(df.at[i, "commitid"] == df2.at[n, "commitid"])
#     n += 1
