"""
"""
from midiutil import MIDIFile
import random

degrees  = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI note number
track    = 0
channel  = 0
time     = 0   # In beats
duration = 1   # In beats
tempo    = 120  # In BPM
volume   = 100 # 0-127, as per the MIDI standard

##Blues scale
##3 2 1 1 3 2 por semitonos
bluesScale = [60, 63, 65, 66, 67, 70, 72]
bluesScale2 = [3, 2, 1, 1, 3 ,2]

randDuration = [0.25, 0.5, 1, 2]

MyMIDI = MIDIFile(1) 
# One track, defaults to format 1 (tempo track automatically created)
MyMIDI.addTempo(track, time, tempo)

for i in range(16):
	pitch = degrees[random.randint(0,6)]
	duration = randDuration[random.randint(0,3)]
	MyMIDI.addNote(track, channel, pitch, time, duration, volume)
	print ("pitch: ", pitch)
	print ("time: ", time)
	time = time + 1

with open("output.mid", "wb") as output_file:
	MyMIDI.writeFile(output_file)