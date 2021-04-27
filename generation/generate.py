"""
"""
import random
import numpy as np
import utils # local module
from note import Note # local module

def fitnessFunction(fitnessArray: np.array, generationNumber):

    amountInd = len(fitnessArray)
    for i in range(amountInd):
        file_name = f"{generationNumber}-{i}.mid"
        utils.play_midi("/product" + file_name)

        print("Rating for", i ,"(1-10): ", end='')
        fitnessArray[i] = (input())

    #mostramos los individuos
    """for i in range(amountInd):
        print(fitnessArray[i])"""
    return fitnessArray

def selectionFunction(amountInd: int, populationFitness: np.array):
    ''' selects individuals to generate the next population,
        this is done using propabilities and roulette wheel selection
        # https://www.youtube.com/watch?v=-B15r-8WX48 (roulette wheel selection)
                                                                                '''

    totalFitness = np.sum(populationFitness)
    relativeFitness = np.zeros(amountInd)
    for i in range(amountInd):
        relativeFitness[i] = populationFitness[i] / totalFitness

    cumulativeProbabilityArray = np.zeros(amountInd)
    currentSum = 0
    for i in range(amountInd):
        cumulativeProbabilityArray[i] = relativeFitness[i] + currentSum
        currentSum = cumulativeProbabilityArray[i]

    # print("Cumulative probability vector")
    # for i in range(amountInd):
    #     print(cumulativeProbabilityArray[i], " ", end='')
    # print("\n")

    #ahora que tenemos la probabilidad cumulativa
    #debemos retornar el vector que indica los pares que
    #debemos cruzar entre si para obtener los hijos

    def getParent(value: int, probArray: np.array):
    # REVISAR !!!
    # La defini aqui, porque solo se usa en esta misma funcion
        for i in range(len(probArray)):
            if (value <= probArray[i]):
                #print("found at",i, "| value is", value)
                return i

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

def geneticIteration(population: list, mutationRate: float, scale: list, generationNumber: int):
    ''' generates a new population '''

    numInd = len(population)
    # numDNA = int(np.shape(population)[1])

    i = 1
    for ind in population:
        print(f"Individual #{i}: {ind}")
        print('')
        i = i + 1

    #####rateamos la poblacion
    individualRating = np.zeros(numInd)
    populationFitness = fitnessFunction(individualRating, generationNumber)

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

def generateInitialPop(scale: list, bar_number: int, start_note: int):
    ''' generates the intial population '''

    #startNote unused por ahora
    #scale es la escala de notas que usaremos
    #barNumber es la cantidad de compases

    initial_pop = []

    # inicialmente cada compas tiene 4 notas
    for _ in range(bar_number * 4):
        #agregamos a la poblacion inicial notas al azar de la escala
        initial_pop.append(Note(random.choice(scale), 1))

    return initial_pop

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

    # esto sera una lista de listas
    population = []

    # Generamos la poblacion inicial
    for i in range(numIndividuals):
        auxlist = generateInitialPop(notesTest, numBars, 0)
        population.append(auxlist)

    for i in range(numIndividuals):
        utils.toMidi(baseNote, notesTest, numBars, population[i], generationNumber, i)

    # while 1:
    #     population = geneticIteration(population, mutationRate, notesTest, generationNumber)
    #     generationNumber = generationNumber + 1

    #     for i in range(numIndividuals):
    #         utils.toMidi(baseNote, notesTest, numBars, population[i], generationNumber, i)

    #     print("Continue? (1/0)")
    #     run = int(input())
    #     if run == 0:
    #         break

if __name__ == "__main__":
    main()





"""
if (pauses):
            if (90 < random.randint(1,100)):
                print ("pause for ", time)
                time = time + duration
                continue"""

########## DEPRECATED CODE BELOW

# def generateNotes(scale: list, startNote: int):
#     #*scale = lista de la escala
#     #startNote = nota startNote de donde empezamos
#     #DESC: Genera las notas posibles que podra usar
#     #el algoritmo
#     print("generating notes...")
#     offset = 8 - len(scale)
#     print("offset:", offset)

#     startNote = startNote - 12
#     currentNote = startNote
#     listNotes = [currentNote]

#     scaleLength = len(scale*2)
#     for i in range(scaleLength):
#         currentNote = currentNote + scale[i%len(scale)]
#         listNotes.append(currentNote)
#     print(scaleLength, "notes were generated")

#     if (scaleLength < 16):
#         print("need", 16 - scaleLength,"more")
#     else:
#         print("need", 16 - scaleLength,"less")



#     return listNotes
# #generateNotesEnd