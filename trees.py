# conda activate domusic
# python3 trees.py

from notebase import *

import h2o 
from h2o.automl import H2OAutoML

# http://localhost:54321/
# autoML applied to the numeric dataset:

h2o.init()

# from h2o.automl import H2OAutoML
# train = h2o.import_file("note_sequences_numeric.csv")
# y = "label"
# x = list(train.columns)
# x.remove(y)
# aml = H2OAutoML(max_runtime_secs = 30)
# aml.train(x = x, y = y, training_frame = train)
# aml.leaderboard
# test =  h2o.import_file("note_sequences_numeric_test.csv")
# predictions=aml.predict(test)

# from h2o.estimators import H2OGradientBoostingEstimator
# #from h2o.tree import H2OTree

# notes = h2o.import_file("note_sequences_numeric.csv")
# gbm = H2OGradientBoostingEstimator(ntrees=1)
# gbm.train(x=["note_t-2", "note_t-1"], y="label", training_frame=notes)
# tree = H2OTree(model = gbm, tree_number = 0)

# airlines = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/airlines/AirlinesTrain.csv")
# gbm = H2OGradientBoostingEstimator(ntrees=1)
# #gbm.train(x=["Origin", "Dest"], y="IsDepDelayed", training_frame=airlines)
# gbm.train(x=["UniqueCarrier", "Origin"], y="Dest", training_frame=airlines)
# gbm.train(x=["N_3", "N_2", "N_3"], y="NextNote", training_frame=songs)
# #tree = H2OTree(model = gbm, tree_number = 0 , tree_class = "NO")
# sfo_tree = H2OTree(model = gbm, tree_number = 0 , tree_class = "SFO")

# traverse_tree(tree.root_node, {"Origin": "ATL", "Dest": "ORD"})
# traverse_tree(tree.root_node, {"Origin": "PHL", "UniqueCarrier": "UA"})
# traverse_tree(H2OTree(model = gbm, tree_number = 0 , tree_class = "SFO").root_node,{"Origin": "SJC", "UniqueCarrier": "UA"})

# ================== Create Tailing Datasets  ================== 

def generate_dataset(directory, output_file, n=2):
    # Put notes in csv files into a list 
    all_notes = []
    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        notes = load_cds_csv_notes(filepath)
        all_notes.extend(notes)

    # Make list into a dataset 
    dataset = []
    for i in range(n, len(all_notes)):
        features = all_notes[i-n:i]
        label = all_notes[i]
        dataset.append(features + [label])
    
    # Make dataset into csv file
    
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        header = [f'note_t-{i}' for i in range(n, 0, -1)] + ['label']
        writer.writerow(header)
        # Write data
        writer.writerows(dataset)

generate_dataset("CSD/english/csv", "note_sequences.csv",2)

def generate_numeric_dataset(directory, output_file, n=2):
    # Put notes in csv files into a list 
    all_notes = []
    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        notes = load_cds_csv_numbers(filepath)
        all_notes.extend(notes)

    # Make list into a dataset 
    dataset = []
    for i in range(n, len(all_notes)):
        features = all_notes[i-n:i]
        label = all_notes[i]
        dataset.append(features + [label])
    
    # Make dataset into csv file
    
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        # Write header
        header = [f'note_t-{i}' for i in range(n, 0, -1)] + ['label']
        writer.writerow(header)
        # Write data
        writer.writerows(dataset)

generate_numeric_dataset("CSD/english/csv", "note_sequences_numeric.csv",2)

# ================== Tree Utils ================== 

def tree_paths(node):
    if isinstance(node, h2o.tree.tree.H2OLeafNode):
        return [node, node.prediction]
    else:
        return [node, node.split_feature, [node.left_levels, tree_paths(node.left_child)], [node.right_levels, tree_paths(node.right_child)]]

def traverse_tree(node, indict):
    if isinstance(node, h2o.tree.H2OLeafNode):
        return node.prediction
    else:
        val = indict[node.split_feature]
        if val in node.right_levels:
            return traverse_tree(node.right_child, indict)
        else:
            return traverse_tree(node.left_child, indict)

# ================== Tree Training ================== 

train = h2o.import_file("note_sequences_numeric.csv")
y = "label"
x = list(train.columns)
x.remove(y)
aml = H2OAutoML(max_runtime_secs = 30)
aml.train(x = x, y = y, training_frame = train)
aml.leaderboard
test =  h2o.import_file("note_sequences_numeric_test.csv")
predictions=aml.predict(test)

print(str(predictions))

# def generate_notes_tree(num_notes,speed,temp, start_note="0"):
#     global aml

#     while(start_note == "0"):
#         start_note = numpy.random.choice(flattened_note_names)
#     generated_sequence = [start_note]
#     current_note = start_note
#     for i in range(num_notes):
#         if current_note == "0":
#             break
        
#         input_dict = {}
#         for i in range(len(generated_sequence)):
#             if i >= len(x):
#                 break
#             input_dict[f'note_t-{i+1}'] = note_to_index[generated_sequence[i]]

#         next_index = #Unsure how to find the next index? 
#         next_note = get_note_name(next_index + BASE)

#         if next_note == "0":
#                 break

#         generated_sequence.append(next_note)
#         current_note = next_note

#     print(generated_sequence)
#     play_tune(generated_sequence, speed)

# def run_jig(num_notes, speed, temp, data="kids",start_note="0"):
#     #Do we even need a jig function if all of the training is done in the generate function? 
#     generate_notes_tree(num_notes,speed,temp,start_note=start_note)






