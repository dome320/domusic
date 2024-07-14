# conda activate domusic

import numpy
import scipy.signal
import pygame, pygame.sndarray
import csv
import os
import mido

# ================== SETUP NOTES ==================

# Decoder for .csv files from: https://zenodo.org/records/4916302
# I think that C4 = 60 (Middle C), so C3 = 48
# According to: https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies

global note_names
global notes
global note2freq

note2freq = {}
note_names = ["C3", ["CS3", "DF3"], "D3", ["DS3", "EF3"], "E3", "F3", ["FS3", "GF3"], "G3", ["GS3", "AF3"], "A3", ["AS3", "BF3"], "B3",
              "C4", ["CS4", "DF4"], "D4", ["DS4", "EF4"], "E4", "F4", ["FS4", "GF4"], "G4", ["GS4", "AF4"], "A4", ["AS4", "BF4"], "B4",
              "C5", ["CS5", "DF5"], "D5", ["DS5", "EF5"], "E5", "F5", ["FS5", "GF5"], "G5", ["GS5", "AF5"], "A5", ["AS5", "BF5"], "B5",
              "C6"]
# Flatten the note_names list, using only the first entry of sublists
flattened_note_names = []
for note in note_names:
    if isinstance(note, list):
        flattened_note_names.append(note[0])
    else:
        flattened_note_names.append(note)
#print(len(flattened_note_names))

# Base value for the first note
BASE = 48

# Function to map number to note name
def get_note_name(number):
    index = number - BASE
    if 0 <= index < len(flattened_note_names):
        return flattened_note_names[index]
    else:
        return None

# Label the three octaves around middle C (C4). 

def setup_notes():
    global note2freq
    c0 = 130.81
    n = 0
    for note_name in note_names:
        f = c0*(2**(n/12))
        if (isinstance(note_name, str)):
            note2freq[note_name]=f
        else:
            note2freq[note_name[0]]=f
            note2freq[note_name[1]]=f
        n = n + 1
    
setup_notes()
#print(note2freq)

# ================== PLAYER ==================

# Adapted from: https://shallowsky.com/blog/programming/python-play-chords.html

pygame.mixer.init(channels=1)

def play_for(sample_wave, ms):
    """Play the given NumPy array, as a sound, for ms milliseconds."""
    sound = pygame.sndarray.make_sound(sample_wave)
    sound.play(-1)
    pygame.time.delay(ms)
    sound.stop()

sample_rate = 44100

def sine_wave(hz, peak, n_samples=sample_rate):
    """Compute N samples of a sine wave with given frequency and peak amplitude.
       Defaults to one second.
    """
    length = sample_rate / float(hz)
    omega = numpy.pi * 2 / length
    xvalues = numpy.arange(int(length)) * omega
    onecycle = peak * numpy.sin(xvalues)
    return numpy.resize(onecycle, (n_samples,)).astype(numpy.int16)

# Play A (440Hz) for 1 second as a sine wave:
#play_for(sine_wave(440, 4096), 1000)

# Chords
#play_for(sum([sine_wave(440, 4096), sine_wave(880, 4096)]), 1000)

# Simple version doesn't handle playing chords.
# ToDo: Make this interpret chords, as:
#    play_tune(["C4",["C4","E4","G4"],"EF3",["C5","EF5","G5"],...],300)

def play_tune(notes,ms=1000):
    global note2freq
    for note in notes:
        if isinstance(note, str): #Checks if the note is a single note
            play_for(sine_wave(note2freq[note], 4096),ms)
        elif isinstance(note, list): # Checks if the note is a chord
            play_for(sum([sine_wave(note2freq[note], 4096) for note in note]), ms)
        else:
            raise Exception(note)

#play_tune(["C4","C4","D4","C4","F4","E4","C4","C4","D4","C4","G4","F4"],300)
#play_tune(["C4", ["C4", "E4", "G4"], "D4"], 300)
# https://www.researchgate.net/figure/Bach-Fugue-No-22-in-B-minor-The-subject-is-stated-in-the-soprano-in-measures-55-57_fig5_277972990
# https://www.bachcentral.com/midiindexcomplete.html

# play_tune(
#     [
#         ["EF5","BF4","EF4", "GF3", "EF3"],
#         ["EF5","BF4","EF4", "EF3","F3"],
#         ["EF4","BF4","EF4", "GF3"],
#         ["EF4","BF4","F3","AF3"],
#         #
#         ["GF3","BF3"],
#         ["GF3","C3","DF5","F5"],
#         ["GF3","EF3","C5","EF5"],
#         ["GF3","EF3","BF4","DF5"]
#     ]) 

# Play a chord by note name
#play_for(sum([sine_wave(note2freq[note], 4096) for note in ["C4","E4","G4"]]), 1000) # C Major
#play_for(sum([sine_wave(note2freq[note], 4096) for note in ["C4","EF4","G4"]]), 1000) # C Minor

# Decoder for .csv files from: https://zenodo.org/records/4916302
# I think that C4 = 60 (Middle C), so C3 = 48
# According to: https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies


    
def load_cds_csv(filepath):
    note_strings = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 2:
                try:
                    number = int(row[2])
                    note_name = get_note_name(number)
                    if note_name:
                        note_strings.append(note_name)
                except ValueError:
                    # Handle the case where conversion to integer fails
                    continue
    note_strings.append("0") 
    return note_strings    

def load_cds_csv_numbers(filepath):
    note_strings = []
    with open(filepath, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) > 2:
                try:
                    number = int(row[2])
                    note_name = get_note_name(number)
                    if note_name:
                        note_strings.append(number)
                except ValueError:
                    # Handle the case where conversion to integer fails
                    continue
    return note_strings

def load_multiple_files(directory="CSD/english/csv"):
    all_notes = [] 
    for filename in os.listdir(directory):
        filepath = os.path.join(directory,filename)
        #print("loading from: "+filepath)
        notes = load_cds_csv(filepath)
        all_notes.extend(notes)
    return all_notes

# Plays Joy to the World
#print(load_cds_csv_numbers("CSD/english/csv/en022a.csv"))
#play_tune(load_cds_csv("CSD/english/csv/en022a.csv"),200)

# Something's wrong with the below. Need to debug at some point.  It
# came from the original web site (as at top) but seems to be broken.

def make_chord(hz, ratios):
    """Make a chord based on a list of frequency ratios."""
    sampling = 4096
    chord = waveform(hz, sampling)
    for r in ratios[1:]:
        chord = sum([chord, sine_wave(hz * r / ratios[0], sampling)])
    return chord

#play_for(make_chord(440,[1,2,3])

def major_triad(hz):
    return make_chord(hz, [4, 5, 6])

#play_for(major_triad(440), length)

def make_chord(hz, ratios, waveform=None):
    """Make a chord based on a list of frequency ratios
       using a given waveform (defaults to a sine wave).
    """
    sampling = 4096
    if not waveform:
        waveform = sine_wave
    chord = waveform(hz, sampling)
    for r in ratios[1:]:
        chord = sum([chord, waveform(hz * r / ratios[0], sampling)])
    return chord

def major_triad(hz, waveform=None):
    return make_chord(hz, [4, 5, 6], waveform)

#play_for(major_triad(440, square_wave), length)

# ================== MIDI UTILS ==================

# Code to convert a midi (.mdi) file into our note system.  This
# processes a single track, so you need to grab a track from the mid
# file. At the moment, just to make things simple, we convert the
# first track and drop the rest. (Actually, it's the second track
# since the first track is always metadata).

def midi1(ifile,track=1):
    i = mido.MidiFile(ifile)
    for msg in i.tracks[track]:
        print(str(msg.dict()))

#midi1("Fugue22.mid",1)

def midi2text(ifile,ofile):
    i = mido.MidiFile(ifile)
    o = open(ofile,'w')
    for track in i.tracks:
        o.write("\n===== Track =====\n")
        for msg in track:
            o.write(str(msg)+"\n")
    o.close()

#midi2text("Fugue22.mid", "Fugue22.txt")

#print(" --- Training ---")

flat_len = 1+len(flattened_note_names)
markov_chain = numpy.full((flat_len, flat_len), 1 / flat_len)
flattened_note_names.append("0") # Set the end token to be zero

# dictionary corresponding to each note and its index 
note_to_index = {note: idx for idx, note in enumerate(flattened_note_names)} 

def train_markov_chain(notes):
    #print("Training on: " + str(notes))
    global markov_chain 
    for i in range(len(notes) - 1): 
        from_note = notes[i] 
        to_note = notes[i+1]
        from_index = note_to_index[from_note]
        to_index = note_to_index[to_note]
        markov_chain[from_index][to_index] += 1 / flat_len
    last_note = notes[-1]
    last_index = note_to_index[last_note]
    end_index = note_to_index["0"]
    markov_chain[last_index][end_index] += 1 / flat_len

def load_scales(ncopies=1):
    notes = []
    for n in range(ncopies):
        notes.extend(["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]) # C major
        notes.extend(["D4", "E4", "FS4", "G4", "A4", "B4", "CS5", "D5"])  # D major
        notes.extend(["E4", "FS4", "GS4", "A4", "B4", "CS5", "DS5", "E5"])  # E major
        notes.extend(["F4", "G4", "A4", "AS4", "C5", "D5", "E5", "F5"])  # F major
        notes.extend(["G4", "A4", "B4", "C5", "D5", "E5", "FS5", "G5"]) # G major
        notes.extend(["A4", "B4", "CS5", "D5", "E5", "FS5", "GS5", "A5"]) # A major
        notes.extend(["B4", "CS5", "DS5", "E5", "FS5", "GS5", "AS5", "B5"])  # B major
    return(notes)

def load_c_scales(ncopies=1):
    notes = []
    for n in range(ncopies):
        notes.extend(["C4", "D4", "E4", "F4", "G4", "A4", "B4", "C5"]) # C major
    return(notes)

def normalize(matrix):
    for i in range(len(matrix)):
        total = numpy.sum(matrix[i])
        if total > 0:
            matrix[i] /= total

normalize(markov_chain)

#for note in notes:
    #print(note+":"+str(markov_chain[note_to_index[note]]))
# (This will be redundant in the case that * was included in the input.)
#print("0"+":"+str(markov_chain[note_to_index["0"]]))

#print(" --- Training done! ---")

#print(" --- Generating ---")

def generate_notes(num_notes,speed,temp,start_note="0"):
    if start_note == "0":
        start_note = 0 
        while start_note == 0:
            start_note = numpy.random.choice(flattened_note_names)
    generated_sequence = [start_note]
    current_note = start_note
    for _ in range(num_notes):
        #print("---------- Next note:")
        current_index = note_to_index[current_note]
        #print("current_index: "+str(current_index))
        probs = markov_chain[current_index]
        #print("probs: "+str(probs))
        #Sort probabilities
        sorted_indices = list(reversed(numpy.argsort(probs)))
        #print("sorted_indices: "+str(sorted_indices))
        # Select next state
        cumulative_probs = numpy.cumsum(probs[sorted_indices])
        #print("cumulative_probs: "+str(cumulative_probs))
        # ******* Since they are sorted you don't need this. The top will always be the first.
        #rand_num = numpy.random.rand()
        rand_num = 0
        #print("rand_num: "+str(rand_num))
        candidate_index = 0
        for i in range (len(cumulative_probs)):
            if rand_num <= cumulative_probs[i]:
                candidate_index = i
                break
        #print("candidate_index: "+str(candidate_index))
        # Add variability with temperature
        mean_index = sorted_indices[candidate_index]
        #print("mean_index: "+str(mean_index))
        #print("temp: " + str(temp))
        new_index = int(numpy.random.normal(mean_index, temp))
        #print("new_index (pre check): "+str(new_index))

        # Check bounds
        if new_index < 0:
            new_index = 0
        elif new_index >= len(flattened_note_names):
            new_index = len(flattened_note_names) - 1
        #print("new_index (after check): "+str(new_index))
        next_note = flattened_note_names[new_index]
        #print("next_note: "+str(next_note))
        if next_note == "0":
            break

        generated_sequence.append(next_note)
        current_note = next_note

    print(generated_sequence)
    play_tune(generated_sequence,speed)


#print(" --- Generating done! ---")

def run_jig(num_notes, speed, temp, data="kids",start_note="0"):
    if data == "kids":
        all_notes = load_multiple_files(directory="CSD/english/csv")
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

run_jig(100,200,0.01,data="c_scales")
