import os
import re
from math import inf
from pathlib import Path
from sys import argv
from time import time, sleep
from typing import Union

import pandas as pd
from dotenv import load_dotenv
from github import Github
from github.Commit import Commit
from github.GithubException import UnknownObjectException, GithubException
from github.IssueComment import IssueComment
from github.PullRequest import PullRequest
from github.PullRequestComment import PullRequestComment
from urllib3.exceptions import ReadTimeoutError

from src.util import find

# SETUP
load_dotenv()
TOKEN = os.getenv("GITHUB_TOKEN")
IN = Path(argv[1])
OUT = Path(argv[2]) if len(argv) >= 3 else None
SAMPLES = 200
GROUP = "coverage_goes_down"
KEYWORDS = ["coverage", "codecov", "test", "suggest", "improve", "write"]
RETRY = 3


def get_repo_pull(github: Github, data: pd.Series):
    try:
        repo = github.get_repo(f"{data['username']}/{data['name']}", lazy=True)
        pull = repo.get_pull(data["pullid"])
        return repo, pull
    except UnknownObjectException:
        return None, None


def get_commit(pull: PullRequest, sha: str):
    if pull is None:
        return None
    commits = [c for c in pull.get_commits() if c.sha == sha]
    return commits[0] if len(commits) > 0 else None


def get_failures(commit: Commit):
    statuses = list(commit.get_statuses())
    failures = [s for s in statuses if s.state in ['failure', 'error']]
    codecov_failures = [s for s in failures if s.context.startswith('codecov/')]
    return len(codecov_failures) > 0, 0 < len(codecov_failures) == len(failures)


def get_comments(pull: PullRequest):
    def by_codecov(comment: Union[IssueComment, PullRequestComment]):
        u = comment.user
        if u is None or u.login is None:
            return False
        return "codecov" in u.login.lower()

    review_comments = [c.body for c in pull.get_comments() if not by_codecov(c)]
    issue_comments = [c.body for c in pull.get_issue_comments() if not by_codecov(c)]
    return review_comments + issue_comments


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


def main():
    g = Github(TOKEN, per_page=100)
    df = pd.read_csv(IN)
    samples = {k: SAMPLES for k in df[GROUP].unique()}
    for col in ["commit_exists", "codecov_fail", "only_codecov", "mentions"]:
        if col not in df.columns:
            df[col] = None

    # Find first place where to start
    i_df = df[df["commit_exists"].isnull()]
    start = i_df.index[0]
    print(f"Starting from index {start}")

    for index_label, row_series in i_df.iterrows():
        remaining_limit, _ = g.rate_limiting
        check_remaining(g, df, remaining_limit)

        print(f"\rCurrently running for index {index_label}. Remaining limit: {remaining_limit}", end="")
        # Check PR/commit exists
        pull = commit = None
        error = False
        for n in range(RETRY):
            try:
                repo, pull = get_repo_pull(g, row_series)
                commit = get_commit(pull, row_series["commitid"])
            except (ReadTimeoutError, GithubException):
                print(f"\nError in try {n + 1}/{RETRY}")
                error = True
                continue
            error = False
            break
        if pull is None or commit is None or error:
            df.at[index_label, "commit_exists"] = False if not error else "ERROR"
            if index_label % 10 == 0:
                checkpoint(df)
            continue
        df.at[index_label, "commit_exists"] = True

        error = False
        comments = []
        only_codecov = False
        for n in range(RETRY):
            try:
                # Check commit statuses for Codecov failure
                codecov_failure, only_codecov = get_failures(commit)
                df.at[index_label, "codecov_fail"] = codecov_failure
                df.at[index_label, "only_codecov"] = only_codecov

                # Check comments for Codecov mention
                comments = get_comments(pull)
            except (ReadTimeoutError, GithubException):
                print(f"\nError in try {n + 1}/{RETRY}")
                error = True
                continue
            error = False
            break
        if error:
            df.at[index_label, "commit_exists"] = "ERROR"
            if index_label % 10 == 0:
                checkpoint(df)
            continue
        priority_match = (inf, None)
        for comment in comments:
            rs = [rf"\w*{kw}\w*" for kw in KEYWORDS]
            matches = [re.search(r, comment, re.IGNORECASE) for r in rs]
            found_match = find(lambda t: t[1] is not None, enumerate(matches))
            if found_match and found_match[0] < priority_match[0]:
                priority_match = found_match
                if priority_match[0] == 0:
                    break
        if priority_match[1]:
            df.at[index_label, "mentions"] = priority_match[1].group()

        # Intermediate save
        if index_label % 10 == 0:
            checkpoint(df)

        # Break loop when enough samples are found
        if only_codecov:
            checkpoint(df)
            samples[row_series[GROUP]] -= 1
            ltf = samples[row_series[GROUP]]
            print(f"\n[{row_series[GROUP]}] {ltf} samples left to find.")
            if all([v <= 0 for v in samples.values()]):
                break

    checkpoint(df)
    print("\nDone!")


main()
