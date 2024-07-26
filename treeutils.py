# ================== Tree Utils ================== 

# ================== Create Tailing Datasets  ================== 

# Nb. executes here are commented out -- only really need to do them
# once in the while (if ever more than once!)

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

#generate_dataset("CSD/english/csv", "note_sequences.csv",2)

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

#generate_numeric_dataset("CSD/english/csv", "note_sequences_numeric.csv",2)

# Tree walking.

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

