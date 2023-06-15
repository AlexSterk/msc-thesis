import pandas as pd

DF1 = "data/rq3/results/survey_with_codes.csv"
DF2 = "data/rq3/survey_results/Questionnaire_March+7,+2022_16.56.csv"

df1 = pd.read_csv(DF1)
df2 = pd.read_csv(DF2)

# merged = df2.merge(df1, how="outer", on="ResponseId", suffixes=[None, None])
merged = df2.combine_first(df1).reindex(columns=df1.columns)
print(df1)
print(df2)
print(merged)

merged.to_csv(DF1, index=False)
