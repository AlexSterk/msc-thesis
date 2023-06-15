import numpy as np
import pandas as pd
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from _questions import QUALITATIVE

IN = "data/rq3/survey_results/Questionnaire_December 15, 2021_13.36.csv"
OUT = "data/rq3/results/survey_with_codes.csv"
QUALITATIVE = [c for c in QUALITATIVE if c[0] not in ["Q44"]]

_df = pd.read_csv(OUT, header=[0,1,2])
df = _df.droplevel(2, axis=1)
df = df.droplevel(1, axis=1)
df = df[df["Finished"]]

for q in QUALITATIVE:
    c = f"{q[0]} - Code"
    if c not in _df.columns:
        _df[c] = None

_df.to_csv(OUT, index=False)

for q in QUALITATIVE:
    responses = df[q[0]]
    responses = responses[~responses.isna()]
    code_label = f"{q[0]} - Code"
    uncoded = responses[_df[code_label].isnull().squeeze()]
    coded = _df[~_df[code_label].isnull().squeeze()]
    _codes = coded[code_label].squeeze(1).astype(str).str.split(" \+ ", expand=True).values.ravel()
    _codes = np.unique(_codes[_codes != None]).tolist()
    completer = WordCompleter(_codes)
    n = 0
    for index, res in uncoded.iteritems():
        n += 1
        print("\033c")
        print(pd.DataFrame([q[1], res, f"{n}/{len(uncoded)}"], index=['Question', 'Response', 'Progress']).to_string())
        codes = []
        while code := prompt("Code > ", completer=completer, complete_while_typing=True):
            if code not in _codes:
                _codes.append(code)
            if code not in codes:
                codes.append(code)
        _df.at[index, code_label] = " + ".join(codes)
        _df.to_csv(OUT, index=False)


