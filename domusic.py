# ToDo: Make this interpret chords, as:
#    play_tune(["C1",["C1","E1","G1"],"EF2",["C1","EF1","G1"],...],300)

# Adapted from: https://shallowsky.com/blog/programming/python-play-chords.html

import pygame, pygame.sndarray
pygame.mixer.init(channels=1)

def play_for(sample_wave, ms):
    """Play the given NumPy array, as a sound, for ms milliseconds."""
    sound = pygame.sndarray.make_sound(sample_wave)
    sound.play(-1)
    pygame.time.delay(ms)
    sound.stop()

import numpy
import scipy.signal

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

# Label the three octaves around middle C (C4). 

note_names = ["C3", ["CS3", "DF3"], "D3", ["DS3", "EF3"], "E3", "F3", ["FS3", "GF3"], "G3", ["GS3", "AF3"], "A3", ["AS3", "BF3"], "B3",
              "C4", ["CS4", "DF4"], "D4", ["DS4", "EF4"], "E4", "F4", ["FS4", "GF4"], "G4", ["GS4", "AF4"], "A4", ["AS4", "BF4"], "B4",
              "C5", ["CS5", "DF5"], "D5", ["DS5", "EF5"], "E5", "F5", ["FS5", "GF5"], "G5", ["GS5", "AF5"], "A5", ["AS5", "BF5"], "B5",
              "C6"]
global notes
note2freq = {}

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
print(note2freq)

# Simple version doesn't handle playing chords.
# ToDo: Make this interpret chords, as:
#    play_tune(["C4",["C4","E4","G4"],"EF3",["C5","EF5","G5"],...],300)

def play_tune(notes,ms=1000):
    global note2freq
    for note in notes:
        play_for(sine_wave(note2freq[note], 4096),ms)

#play_tune(["C4","C4","D4","C4","F4","E4","C4","C4","D4","C4","G4","F4"],300)

# Play a chord by note name
#play_for(sum([sine_wave(note2freq[note], 4096) for note in ["C4","E4","G4"]]), 1000) # C Major
#play_for(sum([sine_wave(note2freq[note], 4096) for note in ["C4","EF4","G4"]]), 1000) # C Minor

# Decoder for .csv files from: https://zenodo.org/records/4916302
# I think that C4 = 60 (Middle C), so C3 = 48
# According to: https://inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies

# Flatten the note_names list, using only the first entry of sublists
flattened_note_names = []
for note in note_names:
    if isinstance(note, list):
        flattened_note_names.append(note[0])
    else:
        flattened_note_names.append(note)

# Base value for the first note
BASE = 48

# Function to map number to note name
def get_note_name(number):
    index = number - BASE
    if 0 <= index < len(flattened_note_names):
        return flattened_note_names[index]
    else:
        return None

import csv

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
    return note_strings    

# Plays Joy to the World
play_tune(load_cds_csv("CSD/english/csv/en022a.csv"),200)

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