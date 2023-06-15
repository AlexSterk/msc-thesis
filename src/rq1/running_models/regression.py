import pandas as pd
import statsmodels.api as sm
from pandas import DataFrame

# Read in data

df: DataFrame = pd.read_csv('data/marquee_open_source_full_no_dupl.csv')
print(len(df))
# Remove faulty rows
df = df.dropna()
print(len(df))

# df = df[(df.project == 'nodejs/node')]
df = df.drop(labels=['pull_id', 'project'], axis=1)
# df[df.columns] = RobustScaler().fit_transform(df)

# Set up dependent and indep. vars
# df = get_dummies(df, prefix='project', columns=['project'])
# df = df[df['project'] == 'GoogleChrome/lighthouse']
# x = df.drop(labels=['timeToMergeInHours', 'sizeOfProjectInBytes', 'project'], axis=1)
x = df.drop(labels=['timeToMergeInHours'], axis=1)
y = df['timeToMergeInHours']

# Add variable for intercept
x = sm.add_constant(x)

# Create and fit model, get results
model = sm.OLS(y.astype(float), x.astype(float), hasconst=True)
results = model.fit()
print(results.summary())
