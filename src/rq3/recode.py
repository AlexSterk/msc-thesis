import pandas as pd

RECODE = {
    "Q35": [
        125,
    ]
}

IN = "data/rq3/results/survey_with_codes.csv"
_df = pd.read_csv(IN)

for q,arr in RECODE.items():
    q_df: pd.DataFrame = _df.iloc[[i + 2 for i in arr]]
    for index, res in q_df.iterrows():
        cur = res[f"{q} - Code"]
        print(f"Q: {q}, index: {index}, cur: {cur}")
        n = input("> ")
        if n:
            _df.at[index, f"{q} - Code"] = n
            _df.to_csv(IN, index=False)

