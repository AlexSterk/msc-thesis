import os
import sys
from pathlib import Path
from sys import argv
from time import time, sleep

import pandas as pd
from dotenv import load_dotenv
from github import Github

SAMPLES = 20
# GROUP = None
GROUP = "coverage_goes_down"


def check_commit_exists(index_label, row_series, df):
    sha = row_series["commitid"]

    try:
        repo = g.get_repo(f"{row_series['username']}/{row_series['name']}", lazy=True)
        pull = repo.get_pull(row_series["pullid"])
    except Exception as e:
        print(f"\nError found at index {index_label}: {row_series['username']}/{row_series['name']}/{row_series['pullid']}/{row_series['commitid']}")
        print(e, file=sys.stderr)
        df.at[index_label, "commit_exists"] = False
        return None, False

    commits = [c for c in pull.get_commits() if c.sha == sha]
    commit_exists = len(commits) > 0
    commit = commits[0] if commit_exists else None
    df.at[index_label, "commit_exists"] = commit_exists
    return commit, commit_exists


def check_codecov_failure(commit, index_label, df):
    statuses = list(commit.get_statuses())
    raw = [s.raw_data for s in statuses]

    df.at[index_label, "raw_data"] = raw

    failures = [s for s in statuses if s.state in ['failure', 'error']]
    codecov_failures = [s for s in failures if s.context.startswith('codecov/')]

    codecov_failure = len(codecov_failures) > 0
    only_codecov = codecov_failure and len(failures) == len(codecov_failures)
    df.at[index_label, "codecov_fail"] = codecov_failure
    df.at[index_label, "only_codecov"] = only_codecov
    return only_codecov


def checkpoint(df: pd.DataFrame):
    if OUT:
        df.to_csv(OUT, index=False)


load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
IN = Path(argv[1])
OUT = Path(argv[2]) if len(argv) >= 3 else None
g = Github(TOKEN, per_page=100)


def main():
    global SAMPLES
    df = pd.read_csv(IN)
    if GROUP:
        SAMPLES = {k: SAMPLES for k in df[GROUP].unique()}

    for col in ["commit_exists", "codecov_fail", "only_codecov", "raw_data"]:
        if col not in df.columns:
            df[col] = None

    i_df = df[df["commit_exists"].isnull()]
    start = i_df.index[0]
    print(f"Starting from index {start}")
    for index_label, row_series in i_df.iterrows():
        remaining_limit, _ = g.rate_limiting
        check_remaining(df, remaining_limit)

        print(f"\rCurrently running for index {index_label}. Remaining limit: {remaining_limit}", end="")
        commit, commit_exists = check_commit_exists(index_label, row_series, df)
        if not commit_exists:
            if index_label % 10 == 0:
                checkpoint(df)
            continue

        codecov_failure = check_codecov_failure(commit, index_label, df)
        if codecov_failure:
            checkpoint(df)
            if GROUP:
                _g = row_series[GROUP]
                SAMPLES[_g] -= 1
                print(f"\n[{_g}] {SAMPLES[_g]} samples left to find")
                if all([v <= 0 for v in SAMPLES.values()]):
                    print("Done!")
                    break
            else:
                SAMPLES -= 1
                print(f"\n{SAMPLES} samples left to find")
                if SAMPLES == 0:
                    print("Done!")
                    break

        if index_label % 10 == 0:
            checkpoint(df)

    print("Loop finished!")
    checkpoint(df)
    # print(df[df["Codecov failure"] == True].to_string())


def check_remaining(df, remaining_limit):
    if remaining_limit <= 10:
        checkpoint(df)
        sleep_until = g.rate_limiting_resettime + 120
        print()
        while time() < sleep_until:
            print(f"\rRate limit almost reached ({remaining_limit}), sleeping for {sleep_until - time()} seconds",
                  end="")
            sleep(1)
        print()


main()
print("DONE")
