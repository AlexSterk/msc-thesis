import pandas as pd

# read xlsx file
df = pd.read_excel('data/rq1/Marquee Open Source.xlsx')
df = df[df["codecov_active"]]

all_projects = df.drop(["coveralls_updated", "coveralls_active", "coveralls"], axis=1)

df = pd.read_csv('results/rq1/data.csv', header=0)
# each line is a pull request belonging to a project
# we want to count the number of pull requests per project
df = df.groupby(['project']).size().reset_index(name='counts')
prs_per_project = df.rename(columns={"counts": "pull_requests"})

# add the number of pull requests to the dataframe all_projects
all_projects = pd.merge(all_projects, prs_per_project, how="left", left_on="concat", right_on="project")
# convert pull_requests to int
all_projects["pull_requests"] = all_projects["pull_requests"].fillna(0).astype(int)

df = pd.read_csv('results/rq1/models.csv', header=0)
# each line is a project
# We want to merge and keep the R-Squared column
df = df[["name", "R-squared"]]
all_projects = pd.merge(all_projects, df, how="left", left_on="project", right_on="name")

all_projects = all_projects.drop(["owner", "name_x", "name_y", "project"], axis=1)
# rename concat to project
all_projects = all_projects.rename(columns={"concat": "project"})
# make project the first column
all_projects = all_projects[["project"] + [col for col in all_projects.columns if col != "project"]]
# sort by name
all_projects = all_projects.sort_values(by=["project"])

# write to csv
all_projects.to_csv("results/rq1/nov2022/agg-list-of-projects.csv", index=False)