import matplotlib.pyplot as plt
import pandas as pd
import pingouin
import scipy.stats
from pandas import DataFrame


def read_data(file):
    # Read in data
    df = pd.read_csv(file)
    print(len(df))
    # Remove faulty rows
    df = df.dropna()
    print(len(df))
    return df


def compare_col(col, a, b):
    print(f"{col}: {a[col].mean()} {b[col].mean()}")
    fig, (ax1, ax2) = plt.subplots(ncols=2, sharey=True)
    # print(col)
    fig.suptitle(col)
    ax1.boxplot(a[col], showfliers=False)
    ax2.boxplot(b[col], showfliers=False)
    plt.savefig(f'figs/compares/no_outliers/{col}.png')
    fig.show()


if __name__ == '__main__':
    df: DataFrame = read_data('data/rq1_3_no_dupl.csv')

    UP: DataFrame = df[(df['coverageGoesUp'] == True)]
    print(len(UP))
    DOWN = df[(df['coverageGoesUp'] == False)]
    print(len(DOWN))

    columns = UP.columns
    columns = columns.drop(['timeToMergeInHours', 'coverageGoesUp'])

    # for col in columns:
    #     compare_col(col, UP, DOWN)
    # compare_col('timeToMergeInHours', UP, DOWN)

    print(scipy.stats.ranksums(UP['timeToMergeInHours'], DOWN['timeToMergeInHours']))
    print(pingouin.compute_effsize(UP['timeToMergeInHours'], DOWN['timeToMergeInHours']))
