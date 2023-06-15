from shutil import copy

import pandas as pd

F1 = "data/rq2/github_queried_data_3_with_comments_2.csv"
F2 = "results/rq2/comments.csv"
F3 = "results/rq2/comments_2.csv"
F4 = "results/rq2/comments_3.csv"
F5 = "results/rq2/comments_4.csv"


def pass_one(IN, OUT):
    if IN == OUT:
        copy(IN, IN + ".bak")
    _df = pd.read_csv(IN, low_memory=False)
    df = _df[~_df["comment"].isnull() & _df["only_codecov"] == True].copy()
    df["url"] = "https://github.com/" + df["username"] + "/" + df["name"] + "/pull/" + df["pullid"].astype(str)
    KWs = ["S1", "S2", "S3", "S4"]
    for kw in KWs:
        df[kw] = df["comment"].str.contains(kw)
    for kw in KWs:
        f = [x for x in KWs if x != kw]
        df[f"only_{kw}"] = df[kw] & ~(df[f[0]] | df[f[1]] | df[f[2]])
    df = df.sort_values(["coverage_goes_down"] + [f"only_{kw}" for kw in KWs] + KWs, ascending=False)
    df.to_csv(OUT, index=False)


def pass_two(IN, OUT):
    from selenium import webdriver
    if IN == OUT:
        copy(IN, IN + ".bak")
    _df = pd.read_csv(IN, low_memory=False)
    browser = webdriver.Chrome()
    if "verified" not in _df.columns:
        _df["verified"] = False
    # searches = ["S4", "S2", ["S3", "S1"], "S3", "S1"]
    # searches = ["S3"]
    searches = [True]
    for s in searches:
        df = _df[~((_df["only_S1"]) | (_df["only_S2"]) | (_df["only_S3"]) | (_df["only_S4"]))]
        _df.loc[df.index, "verified"] = False
        n = 1
        max_n = len(df)
        for i, d in df.iterrows():
            print(f"{n}/{max_n}")
            print(d[["commitid", "coverage_goes_down", "state", "notification_type", "mentions"]])
            print(d["comment"])
            browser.get(d["url"])
            comment = input("New comment? ").strip()
            if comment:
                _df.at[i, "comment"] = comment
            _df.at[i, "verified"] = True
            _df.to_csv(OUT, index=False)
            print()
            n += 1
        _df.to_csv(OUT, index=False)

    browser.close()


# pass_one(F1, F2)
pass_two(F5, F5)
pass_one(F5, F5)
