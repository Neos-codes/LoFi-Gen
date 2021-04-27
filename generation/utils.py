'''
    Utility objects
                        '''

import random
from midiutil import MIDIFile
import numpy as np
import os

# this blocks pygame self-advertise
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'

import pygame

def play_midi(midi_file):
    ''' plays a midi file '''

    # check if mixer is initialized
    if pygame.mixer.get_init() is None:
        print("Initializing mixer ...")

        # mixer config
        freq = 44100  # audio CD quality
        bitsize = -16   # unsigned 16 bit
        channels = 2  # 1 is mono, 2 is stereo
        buffer = 1024   # number of samples

        pygame.mixer.init(freq, bitsize, channels, buffer)

        # optional volume 0 to 1.0
        pygame.mixer.music.set_volume(0.8)

    # play midi
    try:
        clock = pygame.time.Clock()
        pygame.mixer.music.load(midi_file)

        print("MIXER: playing %s ", midi_file)
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            clock.tick(30) # check if playback has finished

    except KeyboardInterrupt:
        # if user hits Ctrl/C then exit
        pygame.mixer.music.fadeout(1000)
        pygame.mixer.music.stop()
        raise SystemExit from KeyboardInterrupt


def toMidi(baseNote: int, scale: list, barNumber: int, individual: np.array, generation: int, indId: int):
    ''' Generates a midi file '''

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

    filename = str(generation) + "-" + str(indId) + ".mid"
    print(filename)

    for i in range(indLen):
        #duration = randDuration[random.randint(0,3)]
        MyMIDI.addNote(track, channel, int(individual[i]), time, duration, volume)
        time = time + 1

    with open("product/" + filename, "wb") as output_file:
        MyMIDI.writeFile(output_file)
