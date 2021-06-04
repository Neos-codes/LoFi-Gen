'''
    Testing if mutationFunction is working correctly
                                                    '''

import sys
import os
sys.path.append(os.path.abspath('../generation'))

from music_elements import Bar, NOTE_DURATIONS
import random
import copy

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

            bar.renew_integrity()

    return population



MUTATION_RATE = 0.5
SCALE = [48, 50, 52, 55, 57, 60, 62, 64, 67, 69, 72]

# crear population
population_before = []
for _ in range(4): # cuatro individuos
    ind = []
    for _ in range(4): # cuatro bars
        ind.append(Bar.from_scale(SCALE, 4, 4))

    population_before.append(ind)

# for ind in population_before:
#     for bar in ind:
#         print(bar)

population_clone = copy.deepcopy(population_before)

population_after = mutationFunction(population_clone, MUTATION_RATE, SCALE)

print("#################################### (BEFORE MUTATION)")

for ind in population_before:
    for bar in ind:
        print(bar)

print("#################################### (AFTER MUTATION)")

for ind in population_after:
    for bar in ind:
        print(bar)


## == CHECK OF SUCCESS == ##
count = 0
for ind in range(4):
    for bar in range(4):
        try:
            for index in range(100):
                if population_after[ind][bar].notes[index].tone != population_before[ind][bar].notes[index].tone:
                    print("hay mutacion")
                    count += 1
                if population_after[ind][bar].notes[index].duration != population_before[ind][bar].notes[index].duration:
                    print("hay mutacion")
                    count += 1

        except IndexError:
            pass

print(f"Hay un total de {count} mutaciones")
