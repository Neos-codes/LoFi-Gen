"""
"""
from midiutil import MIDIFile
import random

def generateNotes(scale, startNote):
	#*scale = lista de la escala
	#startNote = nota startNote de donde empezamos
	#DESC: Genera las notas posibles que podra usar
	#el algoritmo
	print("generating notes...")
	offset = 8 - len(scale)
	print("offset:", offset)

	startNote = startNote - 12
	currentNote = startNote
	listNotes = [currentNote]

	scaleLength = len(scale*2)
	for i in range(scaleLength):
		currentNote = currentNote + scale[i%len(scale)]
		listNotes.append(currentNote)
	print(scaleLength, "notes were generated")

	if (scaleLength < 16):
		print("need", 16 - scaleLength,"more")
	else:
		print("need", 16 - scaleLength,"less")



	return listNotes
#generateNotesEnd


def main():
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

	generatedNotes = [] 
	generatedNotes = generateNotes(majorScale, baseNote)


	
		
	print("Printing possible notes")
	for i in range(len(generatedNotes)):
		print(generatedNotes[i])

	
	"""
	gnLength = len(generatedNotes)
	for i in range(gnLength):
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
	

if __name__ == "__main__":
	main()
