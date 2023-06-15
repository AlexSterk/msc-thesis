import pandas as pd

from _questions import QUALITATIVE

QUALITATIVE = [c for c in QUALITATIVE if c[0] not in ["Q44"]]

DATA = "data/rq3/results/survey_with_codes.csv"
GROUPS = "data/rq3/results/label_to_group.csv"

groups_df = pd.read_csv(GROUPS).set_index(["Question"])

_data_df = pd.read_csv(DATA, header=[0,1,2])
data_df = _data_df.droplevel(2,1).droplevel(1,1)

for q in QUALITATIVE:
    c = f"{q[0]} - Code"
    x = data_df[c]
    data_df[c] = x.str.split(" \+ ")
    x = data_df.explode(c)
    x = x.merge(groups_df.loc[q[0]], how="left", left_on=c, right_on="Code").set_index(x.index)
    x["Group"] = x["Group"].astype('Int64').map(str)

    x = x[~x["Code"].isna()]
    x = x.groupby(level=0)
    x = x["Group"].apply(list).apply(" + ".join)
    _data_df[f"{q[0]} - Groups"] = x

if __name__ == '__main__':
    _data_df.to_csv(DATA, index=False)
    pass
