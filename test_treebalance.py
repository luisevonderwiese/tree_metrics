from ete3 import Tree
import os
import math
import unittest
import pandas as pd

from treebalance import TreeBalance
import indexlists

class TestMetrics(unittest.TestCase):
    ref_dir = "results/treebalance/metrics/evonaps_dna"
    tree_dir = "data/evonaps_dna/trees/rooted"
    expected = {}
    for tree_name in os.listdir(tree_dir):
        try:
            df = pd.read_csv(os.path.join(ref_dir, tree_name + ".csv"))
        except FileNotFoundError:
            continue
        results = {}
        for i, row in df.iterrows():
            results[row["names"]] = float(row["results"])
        expected[tree_name] = results

    def test(self):
        test_trees = {}
        for test_tree_name in os.listdir(self.tree_dir):
            if not test_tree_name in self.expected:
                continue
            tree = Tree(os.path.join(self.tree_dir, test_tree_name))
            tb_b = TreeBalance(tree, "BINARY")
            tb_a = TreeBalance(tree, "ARBITRARY")
            for index_name in indexlists.treebalance_indices:
                print(index_name)
                try:
                    self.assertAlmostEqual(tb_b.absolute(index_name), self.expected[test_tree_name][index_name])
                except ValueError as e:
                    print(e)
                    self.assertAlmostEqual(tb_a.absolute(index_name), self.expected[test_tree_name][index_name])


if __name__ == '__main__':
    unittest.main()
