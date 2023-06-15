import pandas as pd

# def Comment(comment_id, author_id):
#     return {
#         "comment_id": comment_id,
#         "author_id": author_id
#     }
from pandas import DataFrame

df: DataFrame

class Comment:
    def __init__(self, comment_id, author_id) -> None:
        super().__init__()
        self.author_id = author_id
        self.comment_id = comment_id

    def __str__(self) -> str:
        return str(self.__dict__)

    def __hash__(self):
        return hash(self.comment_id)

comments = [
    Comment(123, 11),
    Comment(124, 11),
    Comment(125, 11),
    Comment(126, 12),
    Comment(127, 13),
]

df = pd.DataFrame([
    {"comments": [comments[0], comments[1], comments[4]], "name": "abc"},
    {"comments": [comments[0], comments[2], comments[4]], "name": "abc"},
    {"comments": [], "name": "abd"},
])

def reduce_comments(x: DataFrame):
    return DataFrame([{
        "comment": set(x) if not x.isna().any() else set(),
        "t": 0
    }])


explode = df.explode("comments")
grouped = explode.groupby("name")
sets = grouped["comments"].apply(reduce_comments)
print(sets)
df = df.merge(sets, on="name").drop("comments", axis=1)
df["comment"] = df["comment"].transform(len)
df = df.drop_duplicates()

print(df)

