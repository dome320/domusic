# conda activate domusic
# python3 markov.py

from notebase import *

# This is totally confusing. There are 37 notes (flattened, that is,
# picking just one of the pairs of synonymous flats and sharps), but
# there's also a "0" representing end-of-sequence, so there are 38
# rows and columns entries in the markov table. There could
# theoretically be 37 rows since "0" is never followed by anything,
# but it's confusing enough already. So, then there's the python
# complexity of being zero-origin. This is, like, Obiwan error world!

#for note in notes:
#    print(note+":"+str(markov_chain[note_to_index[note]]))
# (This will be redundant in the case that * was included in the input.)
#print("0"+":"+str(markov_chain[note_to_index["0"]]))

# If start_note = "0" (default), pick a random start note.

markov_table_size = n_notes+1
#print("markov_table_size: "+str(markov_table_size))
markov_chain = numpy.full((markov_table_size, markov_table_size), 1 / markov_table_size)

def train_markov_chain(notes):
    #print("Training on: " + str(notes))
    global markov_chain 
    for i in range(len(notes) - 1): 
        from_note = notes[i] 
        to_note = notes[i+1]
        from_index = note_to_index[from_note]
        to_index = note_to_index[to_note]
        markov_chain[from_index][to_index] += 1 / markov_table_size
    last_note = notes[-1]
    last_index = note_to_index[last_note]
    end_index = note_to_index["0"]
    markov_chain[last_index][end_index] += 1 / markov_table_size

# If, after training there are rows that are absolutely flat - that
# is, notes that never have a follow-on note, the algorithm will never
# walk away from them. In this case, we need to know, and so we make a
# table of the rows with this property so we can randomize away from
# them if we land one one. We call these tails.

global tails

def normalize(matrix):
    global flattened_note_names
    global tails
    tails = []
    # ??? Problem with 38
    for i in range(markov_table_size-1):
        total = numpy.round(numpy.sum(matrix[i]),decimals=3)
        matrix[i] /= total
        if total == 1.0:
            tail=flattened_note_names[i]
            tails.append(tail)

def generate_notes(num_notes,speed,temp,start_note="0"): 
    global tails
    global flattened_note_names
    minimum_allowed_notes = int(num_notes/2)
    if start_note == "0":
        start_note = 0 
        while start_note == 0:
            # WWW XXX Can choose "0" to start!
            start_note = numpy.random.choice(flattened_note_names)
    generated_sequence = [start_note]
    current_note = start_note
    for n in range(num_notes):
        # If there are no followers in the data, pick a random note.
        # FFF This isn't the best fix for this. Need to think on it.
        if current_note in tails:
            current_note = start_note = numpy.random.choice(flattened_note_names)
        current_index = note_to_index[current_note]
        probs = markov_chain[current_index]
        # Sort probabilities
        sorted_indices = list(reversed(numpy.argsort(probs)))
        # Select next state
        cumulative_probs = numpy.cumsum(probs[sorted_indices])
        mean_index = sorted_indices[0]
        new_index = int(numpy.random.normal(mean_index, temp))
        # Check bounds
        if new_index < 0:
            new_index = 0
        elif new_index > n_notes:
            new_index = n_notes
        next_note = flattened_note_names[new_index]
        # Don't allow to be too short
        if (next_note == "0"):
            if (n >= minimum_allowed_notes):
                break
        else:
            generated_sequence.append(next_note)
            current_note = next_note
    print(generated_sequence)
    play_tune(generated_sequence,speed)

def run_jig(num_notes, speed, temp, data="kids",start_note="0"):
    if data == "kids":
        all_notes = load_multiple_files_notes(directory="CSD/english/csv")
    else:
        if data == "all_scales":
            all_notes = load_scales(10)
        else:
            if data == "c_scales":
                all_notes = load_c_scales(10)
                start_note = "C4"
            else:
                exit(data+"????")
    train_markov_chain(all_notes)
    normalize(markov_chain)
    #print(markov_chain)
    generate_notes(num_notes,speed,temp,start_note=start_note)

#run_jig(50,200,0.0,data="c_scales")
#run_jig(50,200,0.25,data="kids")
run_jig(50,200,0.25,data="all_scales")
