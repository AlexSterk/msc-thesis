from pathlib import Path
from sys import argv

import pandas as pd

NOTIFICATION_TYPES = ["comment", "status_changes", "status_patch", "status_project", "checks_patch", "checks_changes",
                      "checks_project"]
# Read arguments
IN = Path(argv[1])
REPOS = Path(argv[2])
OUT = Path(argv[3]) if len(argv) >= 4 else None
OUT = None

# Parse inout files
df = pd.read_csv(IN)
repos = pd.read_csv(REPOS, header=None, names=["repo"], squeeze=True)

# Filter on repo
r: pd.Series = df["username"] + "/" + df["name"]
filtered = df[r.isin(repos)]

# Filter on notification type
filtered = filtered[filtered["notification_type"].isin(NOTIFICATION_TYPES)]

# Filter on coverage goes down in cur
cov_goes_down = (filtered["cur_cov"] - filtered["base_cov"]) < 0
incomplete_patch = filtered["cur_patch"] < 100
filtered = filtered[cov_goes_down | incomplete_patch]

# Group by coverage going up or down in head
filtered["coverage_goes_down"] = (filtered["head_cov"] - filtered["base_cov"]) < 0

# Remove duplicates
print(len(filtered))
filtered = filtered.sort_values("created_at", ascending=False)
filtered = filtered.drop_duplicates(["username", "name", "pullid"])
print(len(filtered))

# Shuffle rows so we can get a random sample later on
filtered = filtered.sample(frac=1)

# Output
if OUT:
    filtered.to_csv(OUT, index=False)
print(filtered)
