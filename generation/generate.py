"""
"""
import random
import numpy as np
import utils # local module
from music_elements import Note, Bar # local module

def fitnessFunction(fitnessArray: np.array, generation_number):

    amountInd = len(fitnessArray)

    i = 1
    for i in range(amountInd):
        file_name = f"{generation_number}-{i}.mid"
        utils.play_midi("product/" + file_name)

        print("Rating for", i ,"(1-10): ", end='')
        fitnessArray[i] = (input())

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

    selectedParents = []
    for i in range(amountInd*2):
        #generamos valor random entre 0-1
        value = random.uniform(0,1)
        parent = getParent(value, cumulativeProbabilityArray)
        #print("parent is", parent)
        selectedParents.append(int(parent))

    return selectedParents

def crossoverFunction(selected_index: list, population: list):
    ''' cross the selected individuals '''

    num_ind = len(population)
    num_bars = len(population[0])

    new_population = []

    # por cada nuevo individuo
    for i in range(num_ind):

        # obtenemos los padres
        parent1 = population[selected_index[i*2]]
        parent2 = population[selected_index[i*2 + 1]]

        # generamos un splitpoint
        split_point = random.randint(0, num_bars)
        print(f"split_point: {split_point}")

        # creamos al nuevo ind
        new_ind = []
        for j in range(num_bars):

            if j < split_point:
                new_ind.append(parent1[j])
            else:
                new_ind.append(parent2[j])

        # chequeamos la integridad del individuo
        for bar in new_ind:
            bar.renew_integrity()

        # lo agregamos a la nueva population
        new_population.append(new_ind)

    return new_population

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

def generateInitialPop(scale: list, num_bars: int, num_ind: int):
    ''' generates the intial population '''

    #startNote unused por ahora
    #scale es la escala de notas que usaremos
    #barNumber es la cantidad de compases
    # num_ind es la cantidad de individuos

    population = []
    for _ in range(num_ind):
        bars = []

        for _ in range(num_bars):
            foo = Bar.from_scale(scale, 4, 4)
            bars.append(foo)

        population.append(bars)

    return population

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
    scale = [47, 48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74]


    ### === INPUT === ###

    #Ahora calculamos las notas que puede tener el codigo
    # print("Enter base note: ")
    # baseNote = int(input())

    #print("Pauses? (1/0)")
    #pauses = int(input())

    # print("Enter tracks amount: ")
    # numIndividuals = int(input())
    numInd = 4

    # print("Enter bar amount: ")
    # numBars = int(input())
    numBars = 4

    # print("Enter mutation rate amount (0-1): ")
    # mutationRate = float(input())
    mutationRate = 0.2

    ### === INITIAL POPULATION === ###

    generation_number = 0

    # esto sera una lista de listas de Bars
    population = generateInitialPop(scale, numBars, numInd)

    # creamos los archivos midi
    for i in range(numInd):
        utils.toMidi(population[i], generation_number, i + 1)


    ### === GENETIC ITERATIONS === ###
    run = 1
    while run:

        # Show inds
        i = 1
        for ind in population:
            print(f"Individual #{i}: {ind}")
            print('')
            i = i + 1

        ##### rateamos la poblacion
        individual_rating = np.zeros(numInd)
        population_fitness = fitnessFunction(individual_rating, generation_number)

        ##### seleccionamos individuos de poblacion inicial
        selected_individuals = selectionFunction(numInd, population_fitness)

        #### Realizamos el crossover
        population = crossoverFunction(selected_individuals, population)

        # # ideal hacer que esta funcion retorne
        # mutationFunction(population, mutationRate, scale)

        generation_number = generation_number + 1

        # creamos los archivos midi
        for i in range(numInd):
            utils.toMidi(population[i], generation_number, i + 1)

        print("Continue? (1/0)")
        run = int(input())

main()


# """
# if (pauses):
#             if (90 < random.randint(1,100)):
#                 print ("pause for ", time)
#                 time = time + duration
#                 continue"""

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


# def geneticIteration(population: list, mutationRate: float, scale: list, generation_number: int):
#     ''' generates a new population '''

#     numInd = len(population)
#     # numDNA = int(np.shape(population)[1])

#     i = 1
#     for ind in population:
#         print(f"Individual #{i}: {ind}")
#         print('')
#         i = i + 1

#     #####rateamos la poblacion
#     individualRating = np.zeros(numInd)
#     populationFitness = fitnessFunction(individualRating, generation_number)

#     #####seleccionamos individuos de poblacion inicial
#     selectedIndividuals = selectionFunction(population, populationFitness)


#     """print("Selected parents")
#     for i in range(len(selectedIndividuals)):
#         print(selectedIndividuals[i], " ", end='')
#     print("\n")
#     """

#     #####Realizamos el crossover
#     population = crossoverFunction(selectedIndividuals, population)

#     """print("Printing possible notes")
#     for i in range(len(generatedNotes)):
#         print(generatedNotes[i])"""

#     """for i in range(numIndividuals):
#         print("Individual", i)
#         for j in range(4*4):
#             print(population[i][j], " ", end='')
#         print("\n")"""

#     mutationFunction(population, mutationRate, scale)

#     print("Mutated population")
#     for i in range(numInd):
#         print("Individual", i)
#         for j in range(4*4):
#             print(population[i][j], " ", end='')
#         print("\n ")
    # return population