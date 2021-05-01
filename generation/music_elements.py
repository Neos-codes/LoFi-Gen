import random
from utils import shuffled # local module

# standar durations of notes
NOTE_DURATIONS = [0.25, 0.5, 1, 2]

# The shortest note's duration
MINIMAL_DURATION = 0.25

class Note():
    ''' Note in MIDI '''

    def __init__(self, tone=60, duration=1):
        self.tone = tone
        self.duration = duration

    def __str__(self):
        ''' Esto define como se printea esta clase '''
        return f"({self.tone}, {self.duration})"

class Bar():
    ''' En spanish, un compas '''

    def __init__(self, notes: list, duration: int, pulses: int):
        self.notes = notes
        self.duration = duration
        self.pulses = pulses

    def __str__(self):
        notes_str = ''
        for note in self.notes:
            notes_str = f"{notes_str} {note}"

        return f"({self.pulses}/{self.duration}, {notes_str})"

    # this works as an alternative constructor
    @classmethod
    def from_scale(cls, scale: list, duration: int, pulses: int):
        ''' creates random notes from the scale '''

        notes = []
        remaining_time = duration

        while remaining_time > MINIMAL_DURATION:
            # select a random tone from scale
            note_tone = random.choice(scale)

            # select a random duration less or equal to remaining_time
            while True:
                note_duration = random.choice(NOTE_DURATIONS)
                if note_duration <= remaining_time:
                    break

            notes.append(Note(note_tone, note_duration))

            remaining_time -= note_duration

            # Note: this implementation may allow more than one note to be played at the same time
            # Note2: Due to the way we are creating the midi file, the notes are played one by one
            # Note3: To add multiple notes at one time, Note class should have a time atributte.

        return cls(notes, duration, pulses)

    def len(self):
        ''' amounts of notes in the bar '''

        return len(self.notes)

    def renew_integrity(self):
        ''' check the notes of the bar and adjust them if the duration do not match '''

        # calculate total duration
        total_duration = 0
        for note in self.notes:
            total_duration += note.duration

        duration_delta = self.duration - total_duration

        while duration_delta < 0:
            for note in shuffled(self.notes):
                if note.duration is MINIMAL_DURATION:
                    self.notes.remove(note)
                    duration_delta += note.duration

                elif note.duration > MINIMAL_DURATION:
                    # We search a shorter duration
                    for duration in reversed(NOTE_DURATIONS):
                        difference = note.duration - duration

                        if difference > 0:
                            # get index of the note in original list
                            note_index = self.notes.index(note)
                            # modify original list
                            self.notes[note_index].duration = duration

                            duration_delta += difference
                            break

class Mood():
   #""" Un mood con escalas """

    scales = []
    scale_ = []
    tonic = "empty"
    tonic_midi = 0

    def __init__(self, tonic: str, tonic_midi: int):
        self.tonic = tonic
        self.tonic_midi = tonic_midi
        print("Tonic in midi: " + str(self.tonic_midi))

    def get_mood(self, mood_: str):
        self.mood = mood_


    def append_scale(self, scale: tuple):
        self.scales.append(scale)
    

    def scales_in_mood(self):
        for scales_ in self.scales:
            printf("Hi hi")     # Revisar esta wea
    

    def select_scale(self):
        actual_note = self.tonic_midi
        rand_scale = random.choice(self.scales)
        print("RandScale: " + rand_scale[0])
        print("Scale selected: " + rand_scale[0])
        scale_len = len(rand_scale[1])
        for midi_note in range(scale_len * 3):
            self.scale_.append(actual_note + rand_scale[1][midi_note%len(rand_scale[1])])
            print("Midi note: " + str(rand_scale[1][midi_note%len(rand_scale[1])]))
        return rand_scale


    def get_tonic(self, tonic: str, tonic_midi: int):
        self.tonic = tonic
        self.tonic_midi = tonic_midi
        print("Tonic: " + self.tonic + " in MIDI: " + str(self.tonic_midi))

    
