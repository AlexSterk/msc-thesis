import pandas as pd

from _questions import QUALITATIVE

IN = "data/rq3/results/survey_with_codes.csv"
df = pd.read_csv(IN, header=[0,1,2])
QUALITATIVE = [c for c in QUALITATIVE if c[0] not in ["Q44"]]

df = df.droplevel(2,1).droplevel(1,1)
with pd.ExcelWriter(IN + ".xlsx") as writer:
    for q in QUALITATIVE:
        c = f"{q[0]} - Code"
        DF = pd.DataFrame()
        DF[q[1]] = df[q[0]]
        DF["All codes"] = df[c]
        coded = df[c].dropna().astype(str).str.split(" \+ ")
        DF["Code"] = coded
        explode = DF[[q[1], "All codes", "Code"]].dropna().explode("Code")
        codebook: pd.DataFrame = explode.reset_index().set_index(["Code", 'index']).sort_index(level=0)

        codebook.to_excel(writer, q[0])
