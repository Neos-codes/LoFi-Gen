"""
"""
import random
import copy
import numpy as np
import utils # local module
from music_elements import Note, Bar, NOTE_DURATIONS, Mood # local module

def fitnessFunction(fitnessArray: np.array, generation_number):
    ''' rates the quality of the individuals '''

    amountInd = len(fitnessArray)

    for i in range(amountInd):
        file_name = f"{generation_number}-{i+1}.mid"
        utils.play_midi("product/" + file_name)

        print("Rating for", i+1 ,"(1-10): ", end='')

        # dev code
        random_value = random.randint(1, 10)
        fitnessArray[i] = random_value
        print(f"value assigned: {random_value}")

        # fitnessArray[i] = (input())


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
        split_point = random.randint(1, num_bars - 1)

        # creamos al nuevo ind
        new_ind = []
        for j in range(num_bars):
            if j < split_point:
                # usamos deepcopy para generar un nuevo elemento,
                # en vez de pushear la referencia al antiguo elemento
                new_ind.append(copy.deepcopy(parent1[j]))
            else:
                new_ind.append(copy.deepcopy(parent2[j]))

        # lo agregamos a la nueva population
        new_population.append(new_ind)

    return new_population

def mutationFunction(population: list, mutationRate: float, scale: list):
    ''' mutates notes from individuals '''

    for ind in population:
        for bar in ind:
            for note in bar.notes:
                value = random.uniform(0,1)

                if value < mutationRate:
                    note_index = bar.notes.index(note)
                    bar.notes[note_index].tone = random.choice(scale)
                    bar.notes[note_index].duration = random.choice(NOTE_DURATIONS)

            bar.renew_integrity(scale)

    return population

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


def makeScale():

    scale = []

    # Tonics in a dictionary first
    dictyNotes = {
        "C": 48,
        "C#": 49,
        "D": 50,
        "D#": 51,
        "E": 52,
        "F": 53,
        "F#": 54,
        "G": 55,
        "G#": 56,
        "A": 57,
        "A#": 58,
        "B": 59
    }
    #Scales and moods
    ##Las escalas NO repiren su ultima nota
    ##Todas DEBEN sumar 12
    majorScale = ("Major", [2, 2, 1, 2, 2, 2, 1])                      # Sweet, Love    "Ionic Scale"
    dorian = ("Dorian", [2, 1, 2, 2, 2, 1, 2])                         # melancolic, deep
    phrygian = ("Phrygian", [1, 2, 2, 2, 1, 2, 2])                     # depressed, mistery
    lydian = ("Lydian", [2, 2, 2, 1, 2, 2, 1])                         # floaty, otherworld, space
    mixolydian = ("Mixolydian", [2, 2, 1, 2, 2, 1, 2])                 # contemplative, sentimental
    aeolian = ("Aeolian", [2, 1, 2, 2, 1, 2, 2])                       # sad, emotional  MINOR SCALE
    locrian = ("Locrian", [1, 2, 2, 1, 2, 2, 2])                       # inquientante
    bluesScale = ("Blues", [3, 2, 1, 1, 3, 2])                         # emotional, regrets, soulful
    chromatic = ("Chromatic", [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1])    # abstract, free, anxiety
    wholeTone = ("Whole Tone", [2, 2, 2, 2, 2, 2])                     # dreamy, cosmic
    phrigianDominant = ("Phrygian Dominant", [1, 3, 1, 2, 1, 2 ,2])    # serious, severe
    pentatonicScale = ("Pentatonic", [2, 2, 3, 2, 3])                  # Joy 

    print("Please, enter the Tonic of your scale\n C C# D D# E F F# G G# A A# B")
    tonic = input()
    mood = Mood(tonic, dictyNotes[tonic])
    
    # Identificamos que escalas dan un mood en especifico
    print("Please, give us the number of your mood\n" + "1. Sad/Sentimental/Depressive\n2. Contemplative/Dreamy/Cosmic/Deep\n3. Emotional/Nostalgic\n4. Love\n5. Abstract/Free")
    mood_t = int(input())

    if mood_t == 1:
        mood.set_mood("Sad")
        mood.set_bpm(random.randint(65, 75))
        mood.append_scale(dorian)
        mood.append_scale(phrygian)
        mood.append_scale(aeolian)
        mood.append_scale(bluesScale)
    
    if mood_t == 2:
        mood.set_mood("Dreamy/Contemplative")
        mood.set_bpm(random.randint(85, 95))
        mood.append_scale(lydian)
        mood.append_scale(mixolydian)
        mood.append_scale(bluesScale)
        mood.append_scale(wholeTone)
    
    if mood_t == 3:
        mood.set_mood("Nostalgic")
        mood.set_bpm(random.randint(70, 85))
        mood.append_scale(dorian)
        mood.append_scale(mixolydian)
        mood.append_scale(aeolian)
        mood.append_scale(bluesScale)
        mood.append_scale(phrigianDominant)
    
    if mood_t == 4:
        mood.set_mood("Love")
        mood.set_bpm(random.randint(90, 100))
        mood.append_scale(majorScale)
        mood.append_scale(pentatonicScale)
    
    if mood_t == 5:
        mood.set_mood("Abstract/Free")
        mood.set_bpm(random.randint(66, 76))
        mood.append_scale(chromatic)
        mood.append_scale(lydian)

    mood.select_scale()

    return mood


def main():
    #https://github.com/kiecodes/genetic-algorithms/blob/master/algorithms/genetic.py
    #https://github.com/kiecodes/generate-music/blob/main/algorithms/genetic.py
    """
    ##Las escalas NO repiren su ultima nota
    ##Todas DEBEN sumar 12
    majorScale = [2, 2, 1, 2, 2, 2, 1]   #Jonico   Sweet, Love
    dorian = [2, 1, 2, 2, 2, 1, 2]       # melancolic, deep
    phrygian = [1, 2, 2, 2, 1, 2, 2]     # depressed, mistery
    lydian = [2, 2, 2, 1, 2, 2, 1]       # floaty, otherworld, space
    mixolydian = [2, 2, 1, 2, 2, 1, 2]   # contemplative, sentimental
    aeolian = [2, 1, 2, 2, 1, 2, 2]      # sad, emotional  MINOR SCALE
    locrian = [1, 2, 2, 1, 2, 2, 2]      # inquientante
    bluesScale = [3, 2, 1, 1, 3, 2]      # emotional, regrets, soulful
    chromatic = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # abstract, free, anxiety
    wholeTone = [2, 2, 2, 2, 2, 2]       # dreamy, cosmic
    phrigianDominant = [1, 3, 1, 2, 1, 2 ,2]  # serious, severe
    pentatonicScale = [2, 2, 3, 2, 3]     # Joy
    """
    # randDuration = [0.5, 1, 1, 1, 1, 1, 1, 2, 2]

    # mood = makeScale()

    # scale = mood.scale_

    scale = [48, 50, 52, 55, 57, 60, 62, 64, 67, 69, 72]


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
    mutationRate = 0.5

    ### === INITIAL POPULATION === ###

    generation_number = 0

    # esto sera una lista de listas de Bars
    population = generateInitialPop(scale, numBars, numInd)

    # creamos los archivos midi
    for i in range(numInd):
        utils.toMidi(population[i], generation_number, i + 1, 70)#mood.bpm) comentado x mientras


    ### === GENETIC ITERATIONS === ###
    run = 1
    while run:
        # show inds
        i = 1
        for ind in population:
            ind_str = ''

            for bar in ind:
                ind_str = f"{ind_str} {bar}"

            print(f"Individual #{i}: {ind_str}")
            print('')
            i += 1

        ##### rateamos la poblacion
        individual_rating = np.zeros(numInd)
        population_fitness = fitnessFunction(individual_rating, generation_number)

        ##### seleccionamos individuos de poblacion inicial
        selected_individuals = selectionFunction(numInd, population_fitness)

        #### Realizamos el crossover
        population = crossoverFunction(selected_individuals, population)

        #### Realizamos la mutacion
        population = mutationFunction(population, mutationRate, scale)

        generation_number = generation_number + 1

        # creamos los archivos midi
        for i in range(numInd):
            utils.toMidi(population[i], generation_number, i + 1, 70)#mood.bpm)

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
