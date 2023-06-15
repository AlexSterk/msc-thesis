import os
import sys
import traceback
from time import time, sleep

import pandas as pd
from dotenv import load_dotenv
from github import Github
from github.GithubException import UnknownObjectException

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")

def new():
    IN = "data/rq3/bq-results-20211119-115728-37xwbh2h4c5z.csv"
    df_in = pd.read_csv(IN)\
        .sort_values("last_commit", ascending=False)\
        .drop_duplicates(["user"])
    df_out = df_in[["user"]].copy()
    df_out["email"] = None
    df_out["name"] = None
    df_out["type"] = None
    return df_in, df_out

def cont():
    IN = "data/rq3/bq-results-20211119-115728-37xwbh2h4c5z-emails-4.csv"
    df_in = pd.read_csv(IN, low_memory=False)
    df_out = df_in
    return df_in, df_out


OUT = "data/rq3/bq-results-20211119-115728-37xwbh2h4c5z-emails-6.csv"
df_in, df_out = cont()

# df_in = df_in[df_in["type"].isnull()]
df_in = df_in[df_in["type"] == "Error"]

g = Github(TOKEN)
max_n = len(df_out)

for i, d in df_in.iterrows():
    remaining_limit, _ = g.rate_limiting
    if remaining_limit < 4:
        df_out.to_csv(OUT, index=False)
        sleep_until = g.rate_limiting_resettime + 120
        print()
        while time() < sleep_until:
            print(f"\rSleeping for {sleep_until - time()} seconds", end="")
            sleep(1)
        print()

    print(f"\r{i}/{max_n}, rate limit: {remaining_limit}", end="")
    try:
        u = g.get_user(d["user"])
        if u:
            df_out.at[i, "name"] = u.name
            df_out.at[i, "type"] = u.type
            if u.email:
                df_out.at[i, "email"] = u.email
    except UnknownObjectException:
        df_out.at[i, "type"] = "Not Found"
        df_out.to_csv(OUT, index=False)
    except Exception:
        df_out.at[i, "type"] = "Error"
        df_out.to_csv(OUT, index=False)
        sys.stderr.write(f"ERROR at {i}\n")
        traceback.print_exc()

    # if i % 1000 == 0:
    #     df_out.to_csv(OUT, index=False)
    df_out.to_csv(OUT, index=False)

df_out.to_csv(OUT, index=False)
