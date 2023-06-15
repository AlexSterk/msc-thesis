import pandas as pd


def merge(in1, in2, out, on="user"):
    df1 = pd.read_csv(in1, low_memory=False)
    df2 = pd.read_csv(in2, low_memory=False)

    df3 = df1.merge(df2, on=on)
    df3.to_csv(out, index=False)


def combine_users(In, out):
    df = pd.read_csv(In, low_memory=False)
    has_email = ~df["email"].isnull()
    is_user = df["type"] == "User"
    df = df[has_email & is_user]
    print(len(df["user"].unique()))

    def l(d):
        return pd.DataFrame([{
            "user": d.iloc[0]["user"],
            "commits": d["commits"].sum(),
            "last_commit": d["last_commit"].max(),
            "name": d.iloc[0]["name"],
            "email": d.iloc[0]["email"],
            "repos": d["repo"].count()
        }])

    df = df.groupby("user").apply(l)
    df.to_csv(out, index=False)


def filter(In):
    df = pd.read_csv(In, low_memory=False)
    print(len(df))

    recent = pd.to_datetime(df["last_commit"]) >= "2021-05-01"
    lots_of_commits = df["commits"] > 100
    repos = df["repos"] >= 3

    filtered = df[recent & lots_of_commits & repos]
    print(filtered)

    return filtered


def prepare_list(df: pd.DataFrame, out=None):
    l = pd.DataFrame()

    l["name"] = df.apply(lambda d: d["name"] if pd.notna(d["name"]) else d["user"], axis=1)
    l["email"] = df["email"]

    if out:
        l.to_csv(out, index=False)


def sample(In, out, n=2000):
    pd.read_csv(In, low_memory=False).sample(n).to_csv(out, index=False)


if __name__ == '__main__':
    # merge(
    #     "data/rq3/bq-results-20211119-115728-37xwbh2h4c5z.csv",
    #     "data/rq3/bq-results-20211119-115728-37xwbh2h4c5z-emails-5.csv",
    #     "data/rq3/bq-results-20211119-115728-37xwbh2h4c5z-merged.csv"
    # )

    # combine_users(
    #     "data/rq3/bq-results-20211119-115728-37xwbh2h4c5z-merged.csv",
    #     "data/rq3/bq-results-20211119-115728-37xwbh2h4c5z-combined.csv"
    # )

    # d = filter("data/rq3/bq-results-20211119-115728-37xwbh2h4c5z-combined.csv")
    # prepare_list(
    #     d,
    #     # "data/rq3/bq-results-20211119-115728-37xwbh2h4c5z-final.csv"
    # )

    # sample(
    #     "data/rq3/bq-results-20211119-115728-37xwbh2h4c5z-final.csv",
    #     "data/rq3/bq-results-20211119-115728-37xwbh2h4c5z-sample.csv",
    # )

    pass
