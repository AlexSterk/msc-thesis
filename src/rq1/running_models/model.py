from functools import reduce

import numpy as np
import pandas as pd
from pandas.core.groupby import DataFrameGroupBy
from sklearn import model_selection, linear_model

_print = print


def set_print_level(level):
    global print
    tab = "\t"
    print = lambda x: _print(f'{tab * level}{x}')


np.set_printoptions(suppress=True)
PROJECTS = [
    'getsentry/sentry',
    'home-assistant/core',
    'sourcegraph/sourcegraph',
    'google/web-stories-wp',
    'webpack/webpack',
    'solana-labs/solana',
    'jina-ai/jina',
    'PyTorchLightning/pytorch-lightning',
    'pass-culture/pass-culture-pro',
    'm3db/m3',
    'Codecademy/client-modules',
    'GoogleChrome/lighthouse',
    'DataDog/integrations-core',
    'DataDog/datadog-agent',
    'home-assistant/supervisor'
]


def read_data(file):
    # Read in data
    df = pd.read_csv(file)
    print(len(df))
    # Remove faulty rows
    df = df.dropna()
    print(len(df))
    return df


def get_x_y(df):
    x = df.drop(labels=['timeToMergeInHours', 'sizeOfProjectInBytes', 'project'], axis=1)
    y = df['timeToMergeInHours']

    return x, y


def remove_correlated(X):
    cor = X.corr()
    correlated_features = set()
    for i in range(len(cor.columns)):
        for j in range(i):
            if abs(cor.iloc[i, j]) > 0.8:
                colname = cor.columns[i]
                correlated_features.add(colname)

    return X.drop(labels=correlated_features, axis=1)


def test_model(X, Y, regression, folds=10):
    print(f"Testing {type(regression).__name__}")
    scores = model_selection.cross_val_score(regression, X, Y, cv=folds)
    print("Done")
    print(f"{scores.mean()}, {scores.std()}")


if __name__ == '__main__':
    df = read_data('data/rq1_with_projects_no_dupl.csv')
    grouped: DataFrameGroupBy = df.groupby('project')
    group_sorted = grouped.size().sort_values(ascending=False)
    print(group_sorted.to_string())

    projects = [grouped.get_group(group) for group in PROJECTS]
    projects = reduce(lambda a, b: a.append(b), projects)

    x, y = get_x_y(projects)

    set_print_level(1)
    test_model(x, y, linear_model.LinearRegression())
    test_model(remove_correlated(x), y, linear_model.LinearRegression())
    set_print_level(0)
    # test_model(x, y, tree.DecisionTreeRegressor())
    # test_model(x, y, ensemble.RandomForestRegressor())
    # test_model(x, y, ensemble.AdaBoostRegressor())
    # test_model(x, y, ensemble.ExtraTreesRegressor())

    for group in PROJECTS:
        print(group)
        set_print_level(1)
        x, y = get_x_y(grouped.get_group(group))
        test_model(x, y, linear_model.LinearRegression())
        test_model(remove_correlated(x), y, linear_model.LinearRegression())
        set_print_level(0)
