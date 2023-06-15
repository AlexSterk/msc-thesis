import numpy as np
import pandas as pd
from sklearn import tree, model_selection

np.set_printoptions(suppress=True)

# Read in data
df = pd.read_csv('data/rq1_3_no_dupl.csv')
print(len(df))
# Remove faulty rows
df = df.dropna()
print(len(df))

x = df.drop(labels=['timeToMergeInHours', 'sizeOfProjectInBytes'], axis=1)
y = df['timeToMergeInHours']

classifier = tree.DecisionTreeRegressor()

scores = model_selection.cross_val_score(classifier, x, y, cv=10, verbose=4)
print(f"{scores.mean()}, {scores.std()}")

classifier.fit(x, y)



