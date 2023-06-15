import pandas as pd

df = pd.read_csv("data/rq3/survey_results/Questionnaire_December 15, 2021_13.36.csv", header=[0, 1, 2])
df = df.droplevel(2, axis=1)
df.columns.to_frame()
df = df.droplevel(1, axis=1)
df = df[df["Finished"]]

QUALITATIVE = ["Q17", "Q20", "Q27", "Q29", "Q31", "Q35", "Q42", "Q43", "Q44"]
df = df[QUALITATIVE]
ten_percent = df.head(len(df) // 10)
ten_percent.to_clipboard()
