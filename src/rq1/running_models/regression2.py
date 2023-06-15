import numpy as np
import pandas as pd
from sklearn import model_selection, linear_model

np.set_printoptions(suppress=True)

# Read in data
df = pd.read_csv('data/rq1_3_no_dupl.csv')
print(len(df))
# Remove faulty rows
df = df.dropna()
print(len(df))

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

classifier = linear_model.LinearRegression()

scores = model_selection.cross_val_score(classifier, x, y, cv=10, verbose=4)
print(f"{scores.mean()}, {scores.std()}")

classifier.fit(x, y)



