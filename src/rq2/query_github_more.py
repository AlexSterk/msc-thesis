import os
import re
from math import inf
from shutil import copy
from time import time, sleep
from typing import Union

import pandas as pd
from dotenv import load_dotenv
from github import Github
from github.CommitComment import CommitComment
from github.GithubException import GithubException
from github.IssueComment import IssueComment
from github.PullRequest import PullRequest
from github.PullRequestComment import PullRequestComment
from urllib3.exceptions import ReadTimeoutError

load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
IN = "results/rq2/comments_5.csv"
OUT = "results/rq2/comments_5.csv"
KEYWORDS = ["coverage", "codecov", "test", "suggest", "improve", "write"]
RETRY = 3


def checkpoint(df: pd.DataFrame):
    if OUT:
        df.to_csv(OUT, index=False)


def check_remaining(github, df, remaining_limit):
    if remaining_limit <= 10:
        checkpoint(df)
        sleep_until = github.rate_limiting_resettime + 120
        print()
        while time() < sleep_until:
            print(f"\rRate limit almost reached ({remaining_limit}), sleeping for {sleep_until - time()} seconds",
                  end="")
            sleep(1)
        print()


def get_comments(pull: PullRequest):
    def by_codecov(comment: Union[IssueComment, PullRequestComment, CommitComment]):
        u = comment.user
        if u is None or u.login is None:
            return False
        return "codecov" in u.login.lower()

    review_comments = [c.body for c in pull.get_comments() if not by_codecov(c)]
    issue_comments = [c.body for c in pull.get_issue_comments() if not by_codecov(c)]

    return review_comments + issue_comments


def main():
    if IN == OUT:
        copy(IN, IN + ".bak")
    g = Github(TOKEN, per_page=100)
    df = pd.read_csv(IN)

    for kw in KEYWORDS:
        for p in ["commits", "comments", "body"]:
            c = f"mentions_{kw}_{p}"
            if c not in df.columns:
                df[c] = None
            df[c] = df[c].astype(str).replace('nan', '')

    if "second_query" not in df.columns:
        df["second_query"] = False
    checkpoint(df)
    _df = df[df["second_query"] == False]
    n = 1
    max_n = len(_df)
    for i, data in _df.iterrows():
        remaining_limit, _ = g.rate_limiting
        check_remaining(g, df, remaining_limit)

        print(f"\rCurrently running for index {i}: {n}/{max_n}. Remaining limit: {remaining_limit}", end="")
        n += 1

        for x in range(RETRY):
            try:
                repo = g.get_repo(data["username"] + "/" + data["name"])
                pull = repo.get_pull(data["pullid"])

                body = pull.body
                comments = get_comments(pull)
                commit_msgs = [c.commit.message for c in pull.get_commits()]

                for kw in KEYWORDS:
                    r = rf"\w*{kw}\w*"
                    body_match = re.search(r, body, re.IGNORECASE) if body else None
                    comment_matches = [re.search(r, comment, re.IGNORECASE) for comment in comments]
                    commit_matches = [re.search(r, commit, re.IGNORECASE) for commit in commit_msgs]

                    if body_match:
                        df.at[i, f"mentions_{kw}_body"] = body_match.group()
                    comment_match = min(comment_matches + [None], key=lambda m: len(m.group()) if m else inf)
                    if comment_match:
                        df.at[i, f"mentions_{kw}_comments"] = comment_match.group()
                    commit_match = min(commit_matches + [None], key=lambda m: len(m.group()) if m else inf)
                    if commit_match:
                        df.at[i, f"mentions_{kw}_commits"] = commit_match.group()
            except (ReadTimeoutError, GithubException):
                print(f"\nError in try {x + 1}/{RETRY}")
                df.at[i, "second_query"] = "ERROR"
                continue
            df.at[i, "second_query"] = True
            break
        checkpoint(df)


main()
