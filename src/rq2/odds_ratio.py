import pandas as pd
from statsmodels.stats.contingency_tables import Table2x2

IN = "results/rq2/comments_5.csv"

_df: pd.DataFrame = pd.read_csv(IN, low_memory=False)
_df = _df.sort_values("S4").groupby("coverage_goes_down").head(200)


def mentions_coverage(s: str):
    if type(s) is not str:
        return False
    s = s.lower()
    return "codecov" in s or "coverage" in s


def mentions_tests(s: str):
    if type(s) is not str:
        return False
    s = s.lower()
    kws = ["test", "testing", "tested", "tests", "retest"]
    return any([kw == s for kw in kws])


_df["coverage_commits"] = (_df["mentions_coverage_commits"].apply(mentions_coverage)) | (
    _df["mentions_codecov_commits"].apply(mentions_coverage))
_df["coverage_comments"] = (_df["mentions_coverage_comments"].apply(mentions_coverage)) | (
    _df["mentions_codecov_comments"].apply(mentions_coverage))
_df["test_comments"] = _df["mentions_test_comments"].apply(mentions_tests)
_df["test_commits"] = _df["mentions_test_commits"].apply(mentions_tests)


def print_odds(_ct):
    ct = Table2x2(_ct)
    print(_ct)
    print("Odds ratio:", ct.oddsratio)
    print("P-value", ct.oddsratio_pvalue())
    print("Confidence interval", ct.oddsratio_confint())
    print()


_df["coverage_goes_up"] = ~_df["coverage_goes_down"]

for x in ["coverage", "test"]:
    for y in ["commits", "comments"]:
        print_odds(pd.crosstab(_df["coverage_goes_up"], _df[f"{x}_{y}"]))

print("Commits AND")
print_odds(pd.crosstab(_df["coverage_goes_up"], _df["coverage_commits"] & _df["test_commits"]))
print("Comments AND")
print_odds(pd.crosstab(_df["coverage_goes_up"], _df["coverage_comments"] & _df["test_comments"]))
print("Commits OR")
print_odds(pd.crosstab(_df["coverage_goes_up"], _df["coverage_commits"] | _df["test_commits"]))
print("Comments OR")
print_odds(pd.crosstab(_df["coverage_goes_up"], _df["coverage_comments"] | _df["test_comments"]))
