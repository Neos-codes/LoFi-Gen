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

PRODUCT_DIR = "product/"

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

        print(f"MIXER: playing {midi_file}")
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            clock.tick(30) # check if playback has finished

    except KeyboardInterrupt:
        # if user hits Ctrl/C then
        pygame.mixer.music.stop()
        print('')


def toMidi(individual: list, generation, indId, numBars: int, chords_seq: list, bpm: int, tonic: int, onlyChords = False):
    ''' Generates a midi file '''

    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 1    # In beats, default value
    tempo    = bpm  # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    # Track 0 para notas, track 1 para los acordes
    MyMIDI = MIDIFile(numTracks = 2)

    # One track, defaults to format 1 (tempo track automatically created)
    MyMIDI.addTempo(track, time, tempo)

    filename = f"{generation}-{indId}.mid"

    # A midi las notas en el track 0
    if not onlyChords:
        for bar in individual:
            for note in bar.notes:
                if note.tone != 0:
                    MyMIDI.addNote(track, channel, note.tone, time, note.duration, volume)
                    time = time + note.duration # This implies notes will be played 1 by 1

                else: # silence
                    time = time + note.duration
    
    
    # A midi los acordes en el track 1
    time = 0
    nChords = len(chords_seq)
    for i in range(numBars):
        chord_duration = None
        for j in range(len(chords_seq[i % nChords])):
            if j == 0:
                chord_duration = chords_seq[i % nChords][0]
            else:
                MyMIDI.addNote(1, channel, chords_seq[i % nChords][j], time, chord_duration, 80)
        time += chord_duration
        

    with open(PRODUCT_DIR + filename, "wb") as output_file:
        MyMIDI.writeFile(output_file)


def shuffled(not_shuffled):
    ''' returns a shuffled list'''

    new_list = not_shuffled.copy()
    random.shuffle(new_list)

    return new_list
