# Code to convert a midi (.mdi) file into our note system.
# We first convert each track into an array of 

import mido

def midi2text(ifile,ofile):
    i = mido.MidiFile(ifile)
    o = open(ofile,'w')
    output = ''
    for track in i.tracks:
        print(track)
        for msg in track:
            #print(msg)
            if msg.type == 'note_on':
                output += str(msg.note) + ','
    o.write(output[:-1])
    o.close()

    
