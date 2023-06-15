import pandas as pd

IN = "data/rq3/users_emails.csv"

df = pd.read_csv(IN)

print(df.count())
