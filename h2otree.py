import h2o

# http://localhost:54321/

h2o.init()
airlines = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/airlines/AirlinesTrain.csv")
gbm = H2OGradientBoostingEstimator(ntrees=1)
#gbm.train(x=["Origin", "Dest"], y="IsDepDelayed", training_frame=airlines)
gbm.train(x=["UniqueCarrier", "Origin"], y="Dest", training_frame=airlines)
gbm.train(x=["N_3", "N_2", "N_3"], y="NextNote", training_frame=songs)
#tree = H2OTree(model = gbm, tree_number = 0 , tree_class = "NO")
sfo_tree = H2OTree(model = gbm, tree_number = 0 , tree_class = "SFO")

def tree_paths(node):
    if isinstance(node, h2o.tree.tree.H2OLeafNode):
        return [node,node.prediction]
    else:
        return [node, node.split_feature, [node.left_levels, tree_paths(node.left_child)], [node.right_levels,tree_paths(node.right_child)]]
    
# tree_paths(tree.root_node)

def traverse_tree(node,indict):
    if isinstance(node, h2o.tree.tree.H2OLeafNode):
        return node.prediction
    else:
        val = indict[node.split_feature]
        if val in node.right_levels:
            return traverse_tree(node.right_child,indict)
        else:
            return traverse_tree(node.left_child,indict)

# traverse_tree(tree.root_node, {"Origin": "ATL", "Dest": "ORD"})
# traverse_tree(tree.root_node, {"Origin": "PHL", "UniqueCarrier": "UA"})

# traverse_tree(H2OTree(model = gbm, tree_number = 0 , tree_class = "SFO").root_node,{"Origin": "SJC", "UniqueCarrier": "UA"})

