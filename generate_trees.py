
from lingdata import database
import pandas as pd
import os
import shutil

def get_best_tree_path(prefix):
    return prefix + ".raxml.bestTree"

def get_prefix(results_dir, row, experiment, run):
    return os.path.join(results_dir, experiment, row["ds_id"], run)


def run_inference(msa_path, model, prefix, args = ""):
    if not os.path.isfile(msa_path):
        print("MSA " + msa_path + " does not exist")
        return
    prefix_dir = "/".join(prefix.split("/")[:-1])
    if not os.path.isdir(prefix_dir):
        os.makedirs(prefix_dir)
    #if not os.path.isfile(get_best_tree_path(prefix)):
    #    args = args + " --redo"
    command = raxmlng_path
    command += " --msa " + msa_path
    command += " --model " + model
    command += " --prefix " + prefix
    command += " --threads auto --seed 2 --redo"
    command += " " + args
    os.system(command)

def run_root_digger(msa_path, tree_path):
    command = rd_path
    command += " --msa " + msa_path
    command += " --tree " + tree_path
    command += "  --exhaustive --states 2 "
    os.system(command)
    suffixes = [".ckp" , "lwr.tree", ".rooted.tree"]



raxmlng_path = "./bin/raxml-ng"
rd_path = "./bin/rd"
config_path = "lingdata_config.json"
results_dir = "data/lang/results"
unrooted_trees_dir = "data/lang/trees/unrooted"
rooted_trees_dir = "data/lang/trees/rooted"
rd_dir = "data/lang/results/rd"

for my_dir in [unrooted_trees_dir, rooted_trees_dir]:
    if not os.path.isdir(my_dir):
        os.makedirs(my_dir)


database.read_config(config_path)
#database.download()
#database.compile()
df = database.data()
pd.set_option('display.max_rows', None)
print(df)

for (i, row) in df.iterrows():
    rooted_tree_path = os.path.join(rooted_trees_dir, row["ds_id"] + ".rooted.tree")
    if os.path.isfile(rooted_tree_path):
        continue
    prefix = get_prefix(results_dir, row, "raxmlng", "bin")
    run_inference(row["msa_paths"]["bin"], "BIN+G", prefix)
    best_tree_path = get_best_tree_path(prefix)
    unrooted_tree_path = os.path.join(unrooted_trees_dir, row["ds_id"] + ".unrooted.tree")
    shutil.copyfile(best_tree_path, unrooted_tree_path)
    run_root_digger(row["msa_paths"]["bin"], unrooted_tree_path)
    shutil.copyfile(unrooted_tree_path + ".rooted.tree", rooted_tree_path)
    suffixes = [".ckp" , ".lwr.tree", ".rooted.tree"]
    for suffix in suffixes:
        src = unrooted_tree_path + suffix
        dst_dir = os.path.join(rd_dir, row["ds_id"])
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)
        dst = os.path.join(dst_dir, "rd" + suffix)
        shutil.move(src, dst)

msa_dir = "data/bio/msa"
results_dir = "data/bio/results"
unrooted_trees_dir = "data/bio/trees/unrooted"
rooted_trees_dir = "data/bio/trees/rooted"
rd_dir = "data/bio/results/rd"

for my_dir in [unrooted_trees_dir, rooted_trees_dir]:
    if not os.path.isdir(my_dir):
        os.makedirs(my_dir)

for msa_name in os.listdir(msa_dir):
    msa_name_x = ".".join(msa_name.split(".")[:-1])
    rooted_tree_path = os.path.join(rooted_trees_dir, msa_name_x + ".rooted.tree")
    if os.path.isfile(rooted_tree_path):
        continue
    prefix = os.path.join(results_dir, "raxmlng", msa_name_x, "bin")
    run_inference(os.path.join(msa_dir, msa_name), "BIN+G", prefix)
    best_tree_path = get_best_tree_path(prefix)
    unrooted_tree_path = os.path.join(unrooted_trees_dir, msa_name_x + ".unrooted.tree")
    shutil.copyfile(best_tree_path, unrooted_tree_path)
    run_root_digger(os.path.join(msa_dir, msa_name), unrooted_tree_path)
    shutil.copyfile(unrooted_tree_path + ".rooted.tree", rooted_tree_path)
    suffixes = [".ckp" , ".lwr.tree", ".rooted.tree"]
    for suffix in suffixes:
        src = unrooted_tree_path + suffix
        dst_dir = os.path.join(rd_dir, msa_name_x)
        if not os.path.isdir(dst_dir):
            os.makedirs(dst_dir)
        dst = os.path.join(dst_dir, "rd" + suffix)
        shutil.move(src, dst)
