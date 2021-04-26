"""
"""
from midiutil import MIDIFile
import random
import numpy as np

def fitnessFunction(fitnessArray: np.array):

	amountInd = len(fitnessArray)
	for i in range(amountInd):
		print("Rating for", i ,"(1-10): ", end='')
		fitnessArray[i] = (input())

	#mostramos los individuos
	"""for i in range(amountInd):
		print(fitnessArray[i])"""
	return fitnessArray

def selectionFunction(population: np.array, fitnessArray: np.array):
	#https://www.youtube.com/watch?v=-B15r-8WX48
	amountInd = len(population)
	#usamos roulette wheel selection
	#for i in range(numIndiviuos)
	totalFitness = np.sum(fitnessArray)
	relativeFitness = np.zeros(amountInd)
	for i in range(amountInd):
		relativeFitness[i] = fitnessArray[i] / totalFitness
		#print(relativeFitness[i])

	cumulativeProbabilityArray = np.zeros(amountInd)
	currentSum = 0;
	for i in range(amountInd):
		cumulativeProbabilityArray[i] = relativeFitness[i] + currentSum
		currentSum = cumulativeProbabilityArray[i]

	"""print("Cumulative probability vector")
	for i in range(amountInd):
		print(cumulativeProbabilityArray[i], " ", end='')
	print("\n")"""

	#ahora que tenemos la probabilidad cumulativa
	#debemos retornar el vector que indica los pares que 
	#debemos cruzar entre si para obtener los hijos
	#-------
	#SELECCION
	#iremos tomando valores random entre 0-1 
	#para ir tomando pares segun la prob anterior
	#por ahora, se entregara un arreglo con tamano
	#2*numeroIndividuos
	selectedParents = np.zeros(amountInd*2)
	for i in range(amountInd*2):
		#generamos valor random entre 0-1
		value = random.uniform(0,1) 
		parent = getParent(value, cumulativeProbabilityArray)
		#print("parent is", parent)
		selectedParents[i] = parent

	return selectedParents

def getParent(value: int, probArray: np.array):
	#REVSIAR
	for i in range(len(probArray)):
		if (value <= probArray[i]):
			#print("found at",i, "| value is", value)
			return i

def crossoverFunction(parents: np.array, population: np.array):
	#print("Crossover function")
	#print(np.shape(population))
	numInd = int(np.shape(population)[0])
	numDNA = int(np.shape(population)[1])

	newPopulation = np.zeros((numInd, numDNA))
	for i in range(numInd):
		splitPoint = random.randint(0,numDNA)
		#print("split point", splitPoint)
		for j in range(numDNA):
			if (j < splitPoint):
				index = int(parents[i*2])
				#print(index)
				#print(type(index))
				newPopulation[i][j] = population[index][j]
			else:
				index = int(parents[i*2+1])
				#print(index)
				#print(type(index))
				newPopulation[i][j] = population[index][j]
	#print(numInd)


	return newPopulation

def mutationFunction(population: np.array, mutationRate: float, scale: list):
	numInd = int(np.shape(population)[0])
	numDNA = int(np.shape(population)[1])

	scaleLength = len(scale)
	for i in range(numInd):
		for j in range(numDNA):
			value = random.uniform(0,1) 
			if (value < mutationRate):
				population[i][j] = scale[random.randint(0,scaleLength-1)]

	return

def geneticIteration(population: np.array, mutationRate: float, scale: list, generationNumber: int):
	numInd = int(np.shape(population)[0])
	numDNA = int(np.shape(population)[1])

	for i in range(numInd):
		print("Individual", i)
		for j in range(4*4):
			print(population[i][j], " ", end='')
		print("\n ")

	#####rateamos la poblcaion
	individualRating = np.zeros(numInd)
	populationFitness = fitnessFunction(individualRating)

	#####seleccionamos individuos de poblacion inicial
	selectedIndividuals = selectionFunction(population, populationFitness)


	"""print("Selected parents")
	for i in range(len(selectedIndividuals)):
		print(selectedIndividuals[i], " ", end='')
	print("\n")
	"""

	#####Realizamos el crossover
	population = crossoverFunction(selectedIndividuals, population)
	"""print("Printing possible notes")
	for i in range(len(generatedNotes)):
		print(generatedNotes[i])"""

	"""for i in range(numIndividuals):
		print("Individual", i)
		for j in range(4*4):
			print(population[i][j], " ", end='')
		print("\n")"""

	mutationFunction(population, mutationRate, scale)

	print("Mutated population")
	for i in range(numInd):
		print("Individual", i)
		for j in range(4*4):
			print(population[i][j], " ", end='')
		print("\n ")
	return population

def toMidi(baseNote: int, scale: list, barNumber: int, individual: np.array, generation: int, indId: int):
	track    = 0
	channel  = 0
	time     = 0   # In beats
	duration = 1   # In beats
	tempo    = 100  # In BPM
	volume   = 100 # 0-127, as per the MIDI standard	

	indLen = len(individual)

	MyMIDI = MIDIFile(1) 
	#One track, defaults to format 1 (tempo track automatically created)
	MyMIDI.addTempo(track, time, tempo)

	"""for i in range (len(individual)):
		print(individual[i], " ", end='')
	print("\n")"""

	filename = str(generation) + "-" + str(indId) + ".mid"
	print(filename)
	for i in range(indLen):
		#duration = randDuration[random.randint(0,3)]
		MyMIDI.addNote(track, channel, int(individual[i]), time, duration, volume)
		time = time + 1
		
	with open(filename, "wb") as output_file:
		MyMIDI.writeFile(output_file)

def generateInitialPop(scale: list, barNumber: int, startNote: int):
	#startNote unused por ahora
	#scale es la escala de notas que usaremos
	#barNumber es la cantidad de compases
	initialPop = []


	scaleLength = len(scale)

	#por ahora cada compas tiene 4 notas
	for i in range(barNumber*4):
		#agregamos a la posblacion inicial notas al azar de la escala
		initialPop.append((scale[random.randint(0,scaleLength-1)]))
		#print("Nota", i, "=", initialPop[i])
	return initialPop
#endfunction

def main():
	#https://github.com/kiecodes/genetic-algorithms/blob/master/algorithms/genetic.py
	#https://github.com/kiecodes/generate-music/blob/main/algorithms/genetic.py
	
	##Las escalas NO repiren su ultima nota
	##Todas DEBEN sumar 12
	majorScale = [2, 2, 1, 2, 2, 2, 1]
	bluesScale = [3, 2, 1, 1, 3, 2]
	minorScale = [2, 1, 2, 2, 1, 2, 2]
	pentatonicScale = [2, 2, 3, 2, 3]

	randDuration = [0.5, 1, 1, 1, 1, 1, 1, 2, 2]

	#pyo
	#EventScale
	notesTest = [47, 48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74]

	#reproducir midi dentro del programa



	#Ahora calculamos las notas que puede tener el codigo
	print("Enter base note: ")
	baseNote = int(input())
	#print("Pauses? (1/0)")
	#pauses = int(input())

	#numero de individuos que usaremos
	#inicializamos individualRating con el mismo tamano para ratear despues
	print("Enter tracks amount: ")
	numIndividuals = int(input())
	print("Enter bar amount: ")
	numBars = int(input())
	print("Enter mutation rate amount (0-1): ")
	mutationRate = float(input())
	#generatedNotes = [] 
	#generatedNotes = generateNotes(majorScale, baseNote)
	generationNumber = 0


	#numBars*4 porque por ahora se tienen 4 notas por compas
	population = np.zeros((numIndividuals,numBars*4))
	#print(type(population))

	#Generamos la poblacion inicial
	for i in range(numIndividuals):
		auxList = generateInitialPop(notesTest, numBars, 0)
		for j in range(numBars*4):
			population[i][j] = auxList[j]
		#endfor
	#endfor

	for i in range(numIndividuals):
		toMidi(baseNote, notesTest, numBars, population[i], generationNumber, i)

	#test = random.choices([0,1], k=50)
	#print(test)

	while(1):
		population = geneticIteration(population, mutationRate, notesTest, generationNumber)
		generationNumber = generationNumber + 1 
		for i in range(numIndividuals):
			toMidi(baseNote, notesTest, numBars, population[i], generationNumber, i)

		print("Continue? (1/0)")
		run = int(input())
		if (run == 0):
			break



	"""
	while(time < 32):
		pitch = degrees[random.randint(0,7)]
		#duration = 1
		duration = randDuration[random.randint(0,4)]
		
		MyMIDI.addNote(track, channel, pitch, time, duration, volume)
		print ("pitch: ", pitch, " | ", "time: ", time)
		time = time + duration


	with open("output.mid", "wb") as output_file:
		MyMIDI.writeFile(output_file)
	"""
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

"""
if (pauses):
			if (90 < random.randint(1,100)):
				print ("pause for ", time)
				time = time + duration
				continue"""




##########DEPRECATED CODE BELOW

def generateNotes(scale: list, startNote: int):
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