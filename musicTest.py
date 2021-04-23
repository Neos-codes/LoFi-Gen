"""
"""
from midiutil import MIDIFile
import random

degrees  = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI note number
track    = 0
channel  = 0
time     = 0   # In beats
duration = 1   # In beats
tempo    = 100  # In BPM
volume   = 100 # 0-127, as per the MIDI standard

##Las escalas NO repiren su ultima nota
##Todas DEBEN sumar 12
majorScale = [2, 2, 1, 2, 2, 2, 1]
bluesScale = [3, 2, 1, 1, 3, 2]
minorScale = [2, 1, 2, 2, 1, 2, 2]
pentatonicScale = [2, 2, 3, 2, 3]

randDuration = [0.25, 0.5, 1, 2]

MyMIDI = MIDIFile(1) 
#One track, defaults to format 1 (tempo track automatically created)
MyMIDI.addTempo(track, time, tempo)



#Ahora calculamos las notas que puede tener el codigo
print("Enter base note: ")
baseNote = int(input())

#OPC

baseNote = baseNote - 12
currentNote = baseNote
possibleNotes = [currentNote]

scaleLength = len(majorScale*3)
for i in range(scaleLength):
	currentNote = currentNote + majorScale[i%len(majorScale)]
	possibleNotes.append(currentNote)
	

print("Printing possible notes")
for i in range(len(possibleNotes)):
	print(possibleNotes[i])

"""
for i in range(16):
	#cambiar rango a las notas de la scala
	noteInScale = degrees[random.randint(0,7)]
	duration = 1
	#duration = randDuration[random.randint(0,3)]
	MyMIDI.addNote(track, channel, baseNote + noteInScale, time, duration, volume)
	print ("pitch: ", noteInScale + baseNote)
	print ("time: ", time)
	time = time + 1

with open("output.mid", "wb") as output_file:
	MyMIDI.writeFile(output_file)

"""