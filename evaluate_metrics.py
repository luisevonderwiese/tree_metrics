import os
import pandas as pd
from ete3 import Tree
import metrics
import matplotlib.pyplot as plt
dfs = {}
for type in ["lang", "bio"]:
    trees_dir = os.path.join("data", type, "trees", "rooted")
    tree_names = []
    for tree_name in os.listdir(trees_dir):
        tree_file_name = os.path.join(trees_dir, tree_name)
        if os.path.isfile(tree_file_name):
            tree_names.append(tree_name)
    df = pd.DataFrame(tree_names, columns=["tree_name"])

    for i, row in df.iterrows():
        tree =  Tree(os.path.join(trees_dir, row["tree_name"]))
        for metric_name in metrics.relative_metrics:
            df.at[i, metric_name] = metrics.relative(metric_name, tree)
    print(df)
    dfs[type] = df
    df.to_csv(os.path.join("data", type, "metrics.csv"))
