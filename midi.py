# Code to convert a midi (.mdi) file into our note system.
# We first convert each track into an array of 

import mido

def midi2text(ifile,ofile):
    i = mido.MidiFile(ifile)
    o = open(ofile,'w')
    for track in i.tracks:
        o.write("\n===== Track =====\n")
        for msg in track:
            o.write(str(msg)+"\n")
    o.close()

midi2text("Fugue22.mid", "Fugue22.txt")
