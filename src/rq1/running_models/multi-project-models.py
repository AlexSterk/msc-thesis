import sys
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from pandas import DataFrame
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import cross_validate
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import RobustScaler

np.set_printoptions(suppress=True)
pd.options.display.float_format = '{:.3f}'.format
SAVE = True
SCALE = False


# Run cross validation for a dataframe
def test_model(dataframe: DataFrame):
    # Split up data in x and y
    x, y = get_x_y(dataframe)

    # Add scaling if necessary
    clf = make_pipeline(RobustScaler(), LinearRegression()) if SCALE else LinearRegression()
    # Run cross validation and convert result to dataframe
    scores = cross_validate(clf, x, y, cv=10)
    scores = DataFrame(scores)
    # Return the score
    return scores['test_score'].mean(), scores['test_score'].std()


# Split up dataframe in x and y dataframes
def get_x_y(dataframe):
    x: DataFrame = dataframe.drop(labels=['timeToMergeInHours'], axis=1)
    y: DataFrame = dataframe['timeToMergeInHours'].to_frame()
    return x, y


# Create model using statsmodel API
def run_statsmodel(df, results):
    # Split dataframe in x and y
    x, y = get_x_y(df)
    # Add constant
    x = sm.add_constant(x)
    # Train OLS model
    m = sm.OLS(y.astype(float), x.astype(float), hasconst=True)
    r = m.fit()
    # Get the model score
    results["R-squared"] = r.rsquared
    results["R-squared-adj."] = r.rsquared_adj
    results["F-statistic"] = r.fvalue
    results["Prob (F-statistic)"] = r.f_pvalue
    results["AIC"] = r.aic
    results["BIC"] = r.bic
    results["Log-likelihood"] = r.llf
    results["Condition-number"] = r.condition_number

    # Add coeffs. and p values to results
    for k in r.params.index:
        results[f"{k}_coeff"] = r.params[k]
        results[f"{k}_std_err"] = r.bse[k]
        results[f"{k}_pvalue"] = r.pvalues[k]


# Get all stats for a project
def get_stats(project, results):
    # Run cross_validation
    # results[f"mean"], results[f"std"] = test_model(project)
    scalers = {}
    # Create a copy for scaling
    scaled_project = project.copy()
    if SCALE:
        # scale each column and keep the scaler so we can inverse it later
        for c in scaled_project.columns:
            if c == 'timeToMergeInHours':
                continue
            scalers[c] = s = RobustScaler()
            scaled_project[c] = s.fit_transform(scaled_project[c].to_frame())
    # Get statsmodel coeffs. and p values
    run_statsmodel(scaled_project, results)


def get_header(project):
    header = {"name": name, "size": len(project)}
    for f in ["created_at", "merged_at"]:
        x_at = project[f]
        x_at = pd.to_datetime(x_at)
        at_max = x_at.max()
        at_min = x_at.min()
        timespan = at_max - at_min
        timespan = timespan.days
        header[f"first_entry_{f}"] = at_min
        header[f"last_entry_{f}"] = at_max
        header[f"timespan_{f}"] = timespan
    return header


# Main entry point
if __name__ == '__main__':
    IN = Path("data/rq1/marquee_open_source_full_3_no_dupl_first.csv")
    if not IN.is_file():
        sys.exit("File not found, exiting...")
    OUT = Path("data/post/recreate_results_rq1_part1.csv")
    # Read in data
    df = pd.read_csv(IN)
    print(len(df))
    # Remove faulty rows
    df = df.dropna()

    print(len(df))
    res = []
    projects = df.groupby('project')
    print(len(projects))

    # Loop over projects
    for project in projects.groups:
        name = project
        project: DataFrame = projects.get_group(project)
        # Need at least 20 rows for cross validation
        if len(project) < 20:
            continue
        _results = get_header(project)
        project = project.drop(labels=['project', 'pull_id', 'created_at', 'merged_at'], axis=1)

        # Get stats for model WITH booleans
        results = _results.copy()
        # results["features"] = "all"
        get_stats(project, results)
        res.append(results)

        continue

        # And now for without booleans
        noBooleans = project.drop(labels=['coverageGoesUp', 'coverageDoesntChange'], axis=1)
        results = _results.copy()
        results["features"] = "no_booleans"
        get_stats(noBooleans, results)
        res.append(results)

        # More advanced feature selection
        results = _results.copy()
        results["features"] = "feature_selection"
        # Remove features with a covariance of 0
        threshold = VarianceThreshold(threshold=0)
        threshold.fit(project)
        adv: DataFrame = project.loc[:, threshold.get_support()]

        # Remove correlated features
        correlated_features = set()
        correlation_matrix = adv.drop(labels=['timeToMergeInHours'], axis=1).corr()
        for i in range(len(correlation_matrix.columns)):
            for j in range(i):
                if abs(correlation_matrix.iloc[i, j]) > 0.9:
                    colname = correlation_matrix.columns[i]
                    correlated_features.add(colname)
        adv = adv.drop(labels=correlated_features, axis=1)

        # print(adv.columns)
        get_stats(adv, results)
        res.append(results)

    # Aggregate results in a dataframe
    results = DataFrame(data=res)
    # Sort by R^2
    sorted_results = results.sort_values(by=['R-squared'], ascending=False)
    print(sorted_results.to_string())
    # Save to a file
    if OUT is not None:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        sorted_results.to_csv(OUT, index=False)
