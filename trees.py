# conda activate domusic
# python3 trees.py

# Usually just need these functions, don't need to import them.
# from treeutils import * 

from notebase import *
import random 
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

# ================== Tree Training ================== 

train = h2o.import_file("note_sequences_numeric.csv")
y = "label"
x = list(train.columns)
x.remove(y)
aml = H2OAutoML(max_runtime_secs = 30)
aml.train(x = x, y = y, training_frame = train)
aml.leaderboard

#test =  h2o.import_file("note_sequences_numeric_test.csv")
#predictions=aml.predict(test)
#print(str(predictions))


def tRound(prediction, temp):
    if temp == 0.0:
        return round(prediction)

    else:
         adjustment = numpy.random.normal(scale=temp)
         new_prediction = prediction + adjustment
         return round(new_prediction)

def generate_notes_tree(num_notes,speed,temp,second_note="0", first_note="0"):
    global aml

    #Randomly Generate 2 Notes from 48 to 84 

    while(second_note == "0" or first_note == "0"):
        first_note = round(random.uniform(48, 84))
        second_note = round(random.uniform(48, 84))
    sequence = [first_note, second_note]
    
    print(f"Initial sequence: {sequence}")

    for i in range(num_notes):
        if(second_note == "0"):
            break
        input_frame = h2o.H2OFrame([[first_note, second_note]], column_names=["note_t-2", "note_t-1"])  
        #next_note = aml.predict(input_frame).as_data_frame().iloc[0, 0]
        next_note = tRound(aml.predict(input_frame)[0,0], temp)
        sequence.append(next_note)
        first_note = round(second_note)
        second_note = round(next_note)
    print(sequence)
    note_sequence = [get_note_name(i) for i in sequence]
    print(note_sequence)
    play_tune(note_sequence,speed) 

for i in range(8):
    print("-----------------",str(i/4.0),"-----------------")
    generate_notes_tree(30, 200, i/4.0)




