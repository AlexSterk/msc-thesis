import pandas as pd
import statsmodels.api as sm

df = pd.read_csv('data/rq1_3_no_dupl.csv')
cor = df.corr()

correlated_features = set()
for i in range(len(cor.columns)):
    for j in range(i):
        if abs(cor.iloc[i, j]) > 0.8:
            colname = cor.columns[i]
            correlated_features.add(colname)

# print(correlated_features)

x = df.drop(labels=correlated_features, axis=1)
x = x.drop(labels=['timeToMergeInHours', 'sizeOfProjectInBytes'], axis=1)
y = df['timeToMergeInHours']

x = sm.add_constant(x) 

print(sm.OLS(y.astype(float), x.astype(float), missing='drop', hasconst=True).fit().summary())
