from ete3 import Tree
import math
import numpy as np
from collections import Counter

absolute_metrics =[
    "average_leaf_depth",
    "variance_of_leaves_depths",
    "sackin_index",
    "total_path_length",
    "total_internal_path_length",
    "average_vertex_depth",
    "B_1_index",
    "B_2_index",
    "height",
    "maximum_width",
    "maxdiff_widths",
    "modified_maxdiff_widths",
    "max_width_over_max_depth",
    "s_roof_shape",
    "cherry_index",
    "modified_cherry_index",
    "d_index",
    "cophenetic_index",
    "diameter",
    "area_per_pair_index",
    "root_imbalance",
    "I_root",
    "colless_index",
    "corrected_colless_index",
    "quadratic_colless_index",
    "I_2_index",
    "stairs1",
    "stairs2",
    "rogers_j_index",
    "symmetry_nodes_index",
    "mean_I",
    "total_I",
    "mean_I_prime",
    "total_I_prime",
    "mean_I_w",
    "total_I_w",
    "rooted_quartet_index",
    "colijn_plazotta_rank",
    "furnas_rank",
    "treeness",
    "stemminess"]

R_metrics = [
        "area_per_pair_index",
        "average_leaf_depth",
        "average_vertex_depth",
        "B_1_index",
        "B_2_index",
        "cherry_index",
        "colless_index",
        "corrected_colless_index",
        "quadratic_colless_index",
       # "colijn_plazotta_rank",
        "I_2_index",
        "furnas_rank",
        "mean_I",
        "total_I",
        "mean_I_prime",
        "total_I_prime",
        "mean_I_w",
        "total_I_w",
        "maxdiff_widths",
        "modified_maxdiff_widths",
        "height",
        "max_width",
        "modified_cherry_index",
        "max_width_over_max_depth",
        "rogers_j_index",
        "rooted_quartet_index",
        "sackin_index",
        "s_roof_shape",
        "stairs1",
        "stairs2",
        "symmetry_nodes_index",
        "cophenetic_index",
        "total_internal_path_length",
        "total_path_length",
        "variance_of_leaves_depths",
        "d_index"]


balance_metrics =[
    "B_1_index",
    "B_2_index",
    "maximum_width",
    "maxdiff_widths",
    "modified_maxdiff_widths",
    "max_width_over_max_depth",
    "cherry_index",
    "rooted_quartet_index",
    "furnas_rank"]


imbalance_metrics =[
    "average_leaf_depth",
    "variance_of_leaves_depths",
    "sackin_index",
    "total_path_length",
    "total_internal_path_length",
    "average_vertex_depth",
    "height",
    "s_roof_shape",
    "modified_cherry_index",
    "cophenetic_index",
    "root_imbalance",
    "I_root",
    "colless_index",
    "corrected_colless_index",
    "quadratic_colless_index",
    "I_2_index",
    "stairs1",
    "stairs2",
    "rogers_j_index",
    "symmetry_nodes_index",
    "mean_I",
    "total_I",
    "mean_I_prime",
    "total_I_prime",
    "mean_I_w",
    "total_I_w",
    "colijn_plazotta_rank"]


relative_metrics = [
    "average_leaf_depth",
    "variance_of_leaves_depths",
    "sackin_index",
    "total_path_length",
    "total_internal_path_length",
    "average_vertex_depth",
    "B_2_index",
    "height",
    "s_roof_shape",
    "cherry_index",
    "modified_cherry_index",
    "cophenetic_index",
    "root_imbalance",
    "I_root",
    "colless_index",
    "quadratic_colless_index",
    "stairs1",
    "rogers_j_index",
    "symmetry_nodes_index",
    "furnas_rank",
    "treeness",
    "stemminess"]
#============ GENERAL ============

def precompute(tree):
    precompute_clade_sizes(tree)
    precompute_depths(tree)
    

def width(tree, i):
    leaf_depths(tree).count(i)

def leaf_depths(tree):
    try:
        return [l.depth for l in tree.iter_leaves()]
    except:
        raise Exception("Run precompute_depths(tree) first")


def clade_size(v):
    try:
        return v.clade_size
    except:
        raise Exception("Run precompute_clade_sizes(tree) first")


def precompute_clade_sizes(tree):
    for node in tree.traverse("postorder"):
        if node.is_leaf():
            node.add_feature("clade_size", 1)
            continue
        c = node.children
        assert(len(c) == 2)
        node.add_feature("clade_size", c[0].clade_size + c[1].clade_size)


def precompute_depths(tree):
    tree.add_feature("depth", 0)
    depths_recursive(tree)

def depths_recursive(tree):
    c = tree.children
    assert(len(c) == 2)
    d = tree.depth + 1
    for child in c:
        child.add_feature("depth", d)
        if not child.is_leaf():
            depths_recursive(child)

def widths(tree):
    return Counter([v.depth for v in tree.traverse("postorder")])


def connecting_path_length(tree, v1, v2):
    ancestor = tree.get_common_ancestor(v1, v2)
    return v1.depth + v2.depth - 2 * ancestor.depth

def inner_nodes(tree):
    inner_nodes = []
    for v in tree.traverse("postorder"):
        if not v.is_leaf():
            inner_nodes.append(v)
    return inner_nodes


def balance_index(tree, v):
    if v.is_leaf():
        return 0
    else:
        c = v.children
        assert(len(c) == 2)
        return abs(clade_size(c[0]) - clade_size(c[1]))

def prob_recursive(tree):
    c = tree.children
    assert(len(c) == 2)
    p = tree.prob/2
    for child in c:
        child.add_feature("prob", p)
        if not child.is_leaf():
            prob_recursive(child)


def we(x):
    lookup = [0, 1, 1, 1, 2, 3, 6, 11, 23, 46, 98, 207, 451, \
            983, 2179, 4850, 10905, 24631, 56011, 127912, \
            293547, 676157, 1563372, 3626149, 8436379, \
            19680277, 46026618, 107890609, 253450711, \
            596572387, 1406818759, 3323236238, 7862958391, \
            18632325319, 44214569100]
    if x >= len(lookup):
        raise Exception("WE Number not provided for " + str(x))
    return lookup[x]

def furnas_ranks(tree):
    for node in tree.traverse("postorder"):
        if node.is_leaf():
            node.add_feature("furnas", 1)
            continue
        c = node.children
        if c[0].clade_size <= c[1].clade_size:
            f_l = c[0].furnas
            alpha = c[0].clade_size
            f_r = c[1].furnas
            beta = c[1].clade_size
        else:
            f_l = c[1].furnas
            alpha = c[1].clade_size
            f_r = c[0].furnas
            beta = c[0].clade_size
        s = 0
        for i in range(1, alpha):
            try:
                s += we(i) * we(node.clade_size - i)
            except:
                node.add_feature("furnas", float("nan"))
                continue
        try:
            s += (f_l - 1) * we(beta) + f_r
        except:
            node.add_feature("furnas", float("nan"))
            continue
        if alpha == beta:
            s -= (f_l * f_l - f_l) / 2
        node.add_feature("furnas", s)


def isomorphic(v1, v2):
    if v1.is_leaf():
        return v2.is_leaf()
    if v2.is_leaf():
        return False
    c1 = v1.children
    c2 = v2.children
    return (isomorphic(c1[0], c2[0]) and isomorphic(c1[1], c2[1])) or (isomorphic(c1[0], c2[1]) and isomorphic(c1[1], c2[0]))



def I(v):
    assert(not v.is_leaf())
    c = v.children
    assert(len(c) == 2)
    n_v1 = max(clade_size(c[0]), clade_size(c[1]))
    n_v = clade_size(v)
    half = math.ceil(n_v / 2.0)
    if (n_v - 1 - half) == 0:
        return 0
    return (n_v1 - half) / (n_v - 1 - half)

def I_prime(v):
    I_value = I(v)
    n_v = clade_size(v)
    if n_v > 0 and n_v % 2 == 0:
        I_value *= (n_v - 1) / n_v
    return I_value


def I_weight(v):
    n_v = clade_size(v)
    if n_v % 2 == 1:
        return 1
    if n_v == 0:
        return 0
    I_v = I(v)
    if I_v == 0:
        return (2 * (n_v - 1)) / n_v
    else:
        return (n_v - 1) / n_v

def I_weight_sum(tree):
    weights = []
    for node in tree.traverse("postorder"):
        if clade_size(node) >= 4:
            weights.append(I_weight(node))
    return sum(weights) / len(weights)

def I_w(v, sw):
    return (I_weight(v) * I(v)) / sw


def I_values(tree, mode, sw = 0):
    assert(mode in ["I", "I_prime", "I_w"])
    values = []
    for node in tree.traverse("postorder"):
        if clade_size(node) >= 4:
            if mode == "I":
                values.append(I(node))
            elif mode == "I_prime":
                values.append(I_prime(node))
            elif mode == "I_w":
                values.append(I_w(node, sw))
    return values


def is_bifurcating(tree):
    c = tree.children
    if len(c) == 2:
        return is_bifurcating(c[0]) and is_bifurcating(c[1])
    if len(c) == 0:
        return True
    return False



#============ ABSOLUTE METRICS ============

def absolute(metric_name, tree):
    if not metric_name in absolute_metrics:
        print(metric_name, " is not an implemented absolute metric!")
        return
    match metric_name:
        case "average_leaf_depth":
            depths = leaf_depths(tree)
            return sum(depths) / len(depths)

        case "variance_of_leaves_depths":
            return np.var(leaf_depths(tree))

        case "sackin_index":
            return sum(leaf_depths(tree))

        case "total_path_length":
            return sum([node.depth for node in tree.traverse("postorder")])

        case "total_internal_path_length":
            s = 0
            for node in tree.iter_descendants("postorder"):
                if not node.is_leaf():
                    s += node.depth
            return s

        case "average_vertex_depth":
            depths = [node.depth for node in tree.traverse("postorder")]
            return sum(depths) / len(depths)

        case "B_1_index":
            s = 0
            tree
            for node in tree.iter_descendants("postorder"):
                if node.is_leaf():
                    node.add_feature("height", 0)
                    continue
                c = node.children
                assert(len(c) == 2)
                h = 1 + max(c[0].height, c[1].height)
                node.add_feature("height", h)
                s += 1/ h
            return s

        case "B_2_index":
            s = 0
            tree.add_feature("prob", 1)
            prob_recursive(tree)
            for leaf in tree.iter_leaves():
                p_leaf = leaf.prob
                s += p_leaf * math.log2(p_leaf)
            return - s

        case "height":
            return max(leaf_depths(tree)) 

        case "maximum_width":
            return max(widths(tree).values())

        case "maxdiff_widths":
            w = widths(tree)
            res = 0
            for i in range(len(w) - 1):
                diff = abs(w[i + 1] - w[i])
                res = max(res, diff)
            return res

        case "modified_maxdiff_widths":
            w = widths(tree)
            res = 0
            for i in range(len(w) - 1):
                diff = w[i + 1] - w[i]
                res = max(res, diff)
            return res

        case "max_width_over_max_depth":
            return absolute("maximum_width", tree) / absolute("height", tree)

        case "s_roof_shape":
            s = 0
            for node in tree.traverse("postorder"):
                if not node.is_leaf():
                    s += math.log2(clade_size(node) - 1)
            return s

        case "cherry_index":
            cnt = 0
            for node in tree.traverse("postorder"):
                if node.is_leaf():
                    continue
                c = node.children
                if c[0].is_leaf() and c[1].is_leaf():
                    cnt += 1
            return cnt

        case "modified_cherry_index":
            return clade_size(tree) - 2 * absolute("cherry_index", tree) 

        case "d_index":
            n = clade_size(tree)
            f_n = Counter([clade_size(node) for node in tree.traverse()])
            s = 0
            for z in range(2, n):
                p_n = (n / (n - 1)) * (2 / (z * (z + 1)))
                s += z * abs(f_n[z] - p_n)
            s += n * abs(f_n[n] - (1 / (n - 1)))
            return s


        case "cophenetic_index":
            s = 0
            for node in tree.iter_descendants("postorder"):
                if not node.is_leaf():
                    s += math.comb(clade_size(node), 2)
            return s

        case "diameter":
            leaves = [l for l in tree.iter_leaves()]
            m = 0
            for i, node1 in enumerate(leaves):
                for j in range(i):
                    node2 = leaves[j]
                    m = max(m, connecting_path_length(tree, node1, node2))
            return m

        
        case "area_per_pair_index":
            n = clade_size(tree)
            s = absolute("sackin_index", tree)
            c = absolute("cophenetic_index", tree)
            return  2 / n * s - 4 / (n * (n - 1)) * c

        case "root_imbalance":
            c = tree.children
            return max(clade_size(c[0]), clade_size(c[1])) / clade_size(tree)

        case "I_root":
            return I(tree)

        case "colless_index":
            s = 0
            for node in tree.traverse("postorder"):
                if not node.is_leaf():
                    s += balance_index(tree, node)
            return s

        case "corrected_colless_index":
            n = len(tree)
            return (2 * absolute("colless_index", tree)) / ((n-1) * (n-2))

        case "quadratic_colless_index":
            s = 0
            for node in tree.traverse("postorder"):
                if not node.is_leaf():
                    b = balance_index(tree, node)
                    s += b * b
            return s

        case "I_2_index":
            n = clade_size(tree)
            s = 0
            for node in tree.traverse("postorder"):
                n_v = clade_size(node)
                if n_v > 2:
                    b = balance_index(tree, node)
                    s += b / (n_v - 2)
            return s / (n - 2)

        case "stairs1":
            return absolute("rogers_j_index", tree) /  (clade_size(tree)- 1)       

        case "stairs2":
            s = 0
            for node in tree.traverse("postorder"):
                if node.is_leaf():
                    continue
                c = node.children
                n0 = clade_size(c[0])
                n1 = clade_size(c[1])
                s += min(n0, n1) / max(n0, n1)
            return s / (clade_size(tree) - 1)

        case "rogers_j_index":
            s = 0
            for node in tree.traverse("postorder"):
                if not node.is_leaf():
                    if balance_index(tree, node) != 0:
                        s += 1
            return s

        case "symmetry_nodes_index":
            cnt = 0
            for node in tree.traverse("postorder"):
                if not node.is_leaf():
                    c = node.children
                    if not isomorphic(c[0], c[1]):
                        cnt += 1
            return cnt

        case "mean_I":
            values = I_values(tree, "I")
            return sum(values) / len(values)

        case "total_I":
            return sum(I_values(tree, "I"))

        case "mean_I_prime":
            values = I_values(tree, "I_prime")
            return sum(values) / len(values)

        case "total_I_prime":
            return sum(I_values(tree, "I_prime"))

        case "mean_I_w":
            sw = I_weight_sum(tree)
            values = I_values(tree, "I_w", sw)
            return sum(values) / len(values)

        case "total_I_w":
            sw = I_weight_sum(tree)
            return sum(I_values(tree, "I_w", sw))

        case "rooted_quartet_index":
            s = 0
            for node in tree.traverse("postorder"):
                if node.is_leaf():
                    continue
                c = node.children
                assert(len(c) == 2)
                s += math.comb(clade_size(c[0]), 2) * math.comb(clade_size(c[1]), 2)
            return s * 3

        case "colijn_plazotta_rank":
            if clade_size(tree) == 1:
                return 1
            c = tree.children
            assert(len(c) == 2)
            cp1 = absolute("colijn_plazotta_rank", c[0])
            cp2 = absolute("colijn_plazotta_rank", c[1])
            if cp1 >= cp2:
                return 0.5 * cp1 * (cp1 - 1) + cp2 + 1
            else:
                return 0.5 * cp2 * (cp2 - 1) + cp1 + 1

        case "furnas_rank":
            furnas_ranks(tree)
            return tree.furnas

        case "treeness":
            all_brlens = 0
            internal_brlens = 0
            for node in tree.traverse("postorder"):
                brlen = node.dist
                all_brlens += brlen
                if not node.is_leaf():
                    internal_brlens += brlen
            return internal_brlens / all_brlens

        case "stemminess":
            values = []
            for node in tree.iter_descendants("postorder"):
                d = node.dist
                if node.is_leaf():
                    node.add_features(sum_below=d)
                else:
                    c = node.children
                    s = d + c[0].sum_below + c[1].sum_below
                    values.append(d / s)
                    node.add_features(sum_below=s)
            return sum(values) / len(values)






def relative(metric_name, tree):
    if not metric_name in relative_metrics:
        print(metric_name, " is not an implemented relative metric!")
        return
    v = absolute(metric_name, tree)
    n = clade_size(tree)
    min_v = minimum(metric_name, n)
    max_v = maximum(metric_name, n)
    if max_v == min_v:
        return float('nan')
    if max_v - v < -0.00001:
        print("Value above max for", metric_name)
        print("max_v:", str(max_v))
        print("v:", str(v))
        assert(False)
    if v - min_v < -0.00001:
        print("Value below min for", metric_name)
        print("min_v:", str(min_v))
        print("v:", str(v))
        assert(False)
    return (v - min_v) / (max_v - min_v)


def relative_normalized(metric_name, tree):
    rel = relative(metric_name, tree)
    if rel != rel:
        return rel
    if metric_name in balance_metrics:
        return 1 - rel
    return rel


def maximum(metric_name, n):
    match metric_name:
        case "average_leaf_depth":
            m = n-1
            return m - (((m - 1) * m) / (2 * n))

        case "variance_of_leaves_depths":
            return ((n - 1) * (n - 2) * (n*n + 3*n -6)) / (12 * n * n) #no tight minimum for binary trees

        case "sackin_index":
            m = n - 1
            return (n * m) - (((m - 1) * m) / 2)

        case "total_path_length":
            return (n * n) - n

        case "total_internal_path_length":
            return ((n - 1) * (n - 2)) / 2

        case "average_vertex_depth":
            return ((n * n) - n) / (2 * n - 1)

        case "B_1_index":
            return float('nan')

        case "B_2_index":
            x  = math.floor(math.log2(n))
            pow_x = math.pow(2, x)
            return x + ((n - pow_x) / pow_x)

        case "height":
            return n - 1

        case "maximum_width":
            return float('nan')

        case "maxdiff_widths":
            return float('nan')
        
        case "modified_maxdiff_widths":
            return float('nan')

        case "max_width_over_max_depth":
            return float('nan')

        case "s_roof_shape":
            return math.log2(math.factorial(n - 1)) #no tight minimum for binary trees

        case "cherry_index":
            return math.floor(n / 2)

        case "modified_cherry_index":
            return n - 2

        case "d_index":
            return float("nan")

        case "cophenetic_index":
            return math.comb(n, 3)

        case "diameter":
            return float('nan')
            #return n #problem with min

        case "area_per_pair_index":
            return float('nan')

        case "root_imbalance":
            return (n - 1) / n

        case "I_root":
            return 1

        case "colless_index":
            return ((n - 1) * (n - 2)) / 2

        case "corrected_colless_index":
            return float('nan')
            #return 1 #use colleess instead

        case "quadratic_colless_index":
            return math.comb(n, 3) + math.comb(n - 1, 3)

        case "I_2_index":
            return float('nan')
            #return 1 problem with minimum
        
        case "stairs1":
            return max(0, n - 2) / (n - 1)
        
        case "stairs2":
            return float('nan')
            #return sum([1 / i for i in range(1, n)]) / (n - 1) (holds for caterpillar but is not the maximum)

        case "rogers_j_index":
            return max(0, n - 2)

        case "symmetry_nodes_index":
            return n - 2

        case "mean_I":
            return float('nan')

        case "total_I":
            return float('nan')

        case "mean_I_prime":
            return float('nan')

        case "total_I_prime":
            return float('nan')

        case "mean_I_w":
            return float('nan')

        case "total_I_w":
            return float('nan')

        case "rooted_quartet_index":
            return float("nan")

        case "colijn_plazotta_rank":
            return float('nan')

        case "furnas_rank":
            try:
                return we(n)
            except:
                return float("nan")

        case "treeness":
            return 1 #pseudo bound

        case "stemminess":
            return 1 #pseudo bound



def minimum(metric_name, n):
    match metric_name:
        case "average_leaf_depth":
            x = math.floor(math.log2(n / 2))
            return  x + 3 - (2 / n) * math.pow(2, x + 1)

        case "variance_of_leaves_depths":
            return 0 #bound only tight for general trees

        case "sackin_index":
            x = math.floor(math.log2(n / 2))
            return (x + 3) * n - math.pow(2, x + 2)

        case "total_path_length":
            l = math.floor(math.log2(n))
            return 2 * l * n - math.pow(2, l + 2) + 2 * n + 2

        case "total_internal_path_length":
            l = math.floor(math.log2(n))
            return l * n - math.pow(2, l + 1) + 2

        case "average_vertex_depth":
            l = math.floor(math.log2(n))
            return (2 * l * n - math.pow(2, l + 2) + 2 * n + 2) / (2 * n -1)

        case "B_1_index":
            return float('nan')

        case "B_2_index":
            return 2 - math.pow(2, 2 - n)

        case "height":
            return math.floor(math.log2(n)) + 1

        case "maximum_width":
            return float('nan')
            #return 2 #problem with maximum

        case "maxdiff_widths":
            return float('nan')
            #return 1 #problem with maximum

        case "modified_maxdiff_widths":
            return float('nan')
            #return 1 #problem with maximum

        case "max_width_over_max_depth":
            return float('nan')

        case "s_roof_shape":
            return math.log2(n - 1) #only tight for general trees

        case "cherry_index":
            return 1

        case "modified_cherry_index":
            return n % 2 

        case "d_index":
            return float("nan")

        case "cophenetic_index":
            factorial = 1
            a = 1
            s = 0
            for i in range(n):
                if i != 0:
                    factorial += i
                while factorial % (a * 2) == 0:
                    a *= 2
                s += a
            return 0

        case "diameter":
            return float('nan')
            #highest_1_bit = math.floor(math.log2(n))
            #lowest_1_bit = math.log2(n & -n) + 1
            #if highest_1_bit == lowest_1_bit or bin(n).count('1'):
            #    inbetween = 0
            #else:
            #    inbetween = minimum("diameter", n1)
            #return highest_1_bit + inbetween + lowest_1_bit

        case "area_per_pair_index":
            return float('nan')

        case "root_imbalance":
            return math.ceil(n / 2) / n

        case "I_root":
            return 0

        case "colless_index":
            sum_bound = math.ceil(math.log2(n))
            s = 0
            for j in range(1, sum_bound):
                x = math.pow(2, -j) * n
                triangle_wave = min(math.ceil(x) - x, x - math.floor(x))
                s += math.pow(2, j) * triangle_wave
            return s

        case "corrected_colless_index":
            return float('nan')
            #return (2 / ((n - 1) * (n - 2))) * minimum("colless_index", n) #noramlize colless instead

        case "quadratic_colless_index":
            sum_bound = math.ceil(math.log2(n))
            s = 0
            for j in range(1, sum_bound):
                x = math.pow(2, -j) * n
                triangle_wave = min(math.ceil(x) - x, x - math.floor(x))
                s += math.pow(2, j) * triangle_wave
            return s

        case "I_2_index":
            return float("nan")

        case "stairs1":
            return (bin(n).count("1") - 1) / (n - 1)

        case "stairs2":
            return float('nan')
            #return 0 #problem with maximum

        case "rogers_j_index":
            return bin(n).count("1") - 1

        case "symmetry_nodes_index":
            return  bin(n).count("1") - 1

        case "mean_I":
            return float('nan')

        case "total_I":
            return float('nan')

        case "mean_I_prime":
            return float('nan')

        case "total_I_prime":
            return float('nan')

        case "mean_I_w":
            return float('nan')

        case "total_I_w":
            return float('nan')

        case "rooted_quartet_index":
            return float("nan")
            #return 0

        case "colijn_plazotta_rank":
            return float('nan')

        case "furnas_rank":
            return 1

        case "treeness":
            return 0 #pseudo bound

        case "stemminess":
            return 0 #pseudo bound
