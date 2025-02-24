
tree <- ape::read.tree("data/virus/trees/rooted/covid_edited.rooted.tree")
start.time <- Sys.time()
treebalance::areaPerPairI(tree)
treebalance::avgLeafDepI(tree)
treebalance::avgVertDep(tree)
treebalance::B1I(tree)
treebalance::B2I(tree)
treebalance::cherryI(tree)
treebalance::collessI(tree, method="original")
treebalance::collessI(tree, method="corrected")
treebalance::collessI(tree, method="quadratic")
# treebalance::colPlaLab(tree)
treebalance::ewCollessI(tree)
treebalance::furnasI(tree)
treebalance::IbasedI(tree, method="mean")
treebalance::IbasedI(tree, method="total")
treebalance::IbasedI(tree, method="mean", correction="prime")
treebalance::IbasedI(tree, method="total", correction="prime")
treebalance::IbasedI(tree, method="mean", correction="w")
treebalance::IbasedI(tree, method="total", correction="w")
treebalance::maxDelW(tree, method="original")
treebalance::maxDelW(tree, method="modified")
treebalance::maxDepth(tree)
treebalance::maxWidth(tree)
treebalance::mCherryI(tree)
treebalance::mWovermD(tree)
treebalance::rogersI(tree)
treebalance::rQuartetI(tree)
treebalance::sackinI(tree)
treebalance::sShapeI(tree)
treebalance::stairs1(tree)
treebalance::stairs2(tree)
treebalance::symNodesI(tree)
treebalance::totCophI(tree)
treebalance::totIntPathLen(tree)
treebalance::totPathLen(tree)
treebalance::varLeafDepI(tree)
treebalance::weighL1dist(tree)
end.time <- Sys.time()
time.taken <- end.time - start.time
time.taken
