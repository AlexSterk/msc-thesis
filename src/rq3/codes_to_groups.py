import pandas as pd

from _questions import QUALITATIVE

IN = "data/rq3/results/survey_with_codes.csv"
OUT = "data/rq3/results/label_to_group.csv"
df = pd.read_csv(IN, header=[0,1,2])
QUALITATIVE = [c for c in QUALITATIVE if c[0] not in ["Q44"]]

df = df.droplevel(2,1).droplevel(1,1)

DF: pd.DataFrame = pd.DataFrame()

for q in QUALITATIVE:
    c = f"{q[0]} - Code"
    x = df[c]
    x = x.str.split(" \+ ").explode(c).dropna().unique()
    x = pd.Series(x).sort_values(ignore_index=True).to_frame()
    x["Code"] = q[0]
    # print(x)
    DF = pd.concat([DF, x])

DF = DF.set_index(["Code"])
DF["group"] = None
# print(DF)
DF.to_csv(OUT)
