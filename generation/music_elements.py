import random
from utils import shuffled # local module

# standar durations of notes
NOTE_DURATIONS = [0.5, 1, 2]

# The shortest note's duration
MINIMAL_DURATION = 0.5

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

        return f"[{self.pulses}/{self.duration}, {notes_str}]"

    # this works as an alternative constructor
    @classmethod
    def from_scale(cls, scale: list, duration: int, pulses: int):
        ''' creates random notes from the scale '''

        notes = []
        remaining_time = duration

        while remaining_time >= MINIMAL_DURATION:
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

    def renew_integrity(self, scale: list):
        ''' checks the duration of the bar and adds or remove notes if the duration do not match '''

        # calculate total duration
        total_duration = 0
        for note in self.notes:
            total_duration += note.duration

        duration_delta = self.duration - total_duration

        while duration_delta != 0:
            for note in shuffled(self.notes):
                if duration_delta < 0: # we try to reduce bar's duration

                    # By removing notes
                    self.notes.remove(note)

                    duration_delta += note.duration

                else: # we try to increse bar's duration

                    # By adding notes
                    new_duration = None
                    for duration in NOTE_DURATIONS:
                        if duration == duration_delta:
                            new_duration = duration_delta
                            break

                    if not new_duration:
                        new_duration = random.choice(NOTE_DURATIONS)

                    new_tone = random.choice(scale) # this could be better, using a relative tone

                    new_note = Note(new_tone, new_duration)
                    self.notes.append(new_note)

                    duration_delta -= new_duration


class Mood():
   #""" Un mood con escalas """

    steps = None     # Lista con la distancia entre las notas de la escala
    scale_ =  []     # Notas de las 2 octavas de la escala
    tonic = "empty"  # String con la tonica de la escala
    tonic_midi = 0   # Midi de la tonica de la escala
    chords = []      # Todos los acordes básicos
    seq_chords = []  # Secuencia de acordes
    seq_size = None  # Num acordes en la secuencia de acordes
    numBars = None   # Cantidad de compases de los individuos


    # Constructor, se setea aqui la tonica y el valor midi de la tonica
    def __init__(self, tonic: str, tonic_midi: int):
        self.tonic = tonic
        self.tonic_midi = tonic_midi
        self.scale_.append(tonic_midi)
        print("Tonic in midi: " + str(self.tonic_midi))
        

    # Aqui se setea el mood de la pista
    def set_mood(self, mood_: str):
        self.mood = mood_

    # Aqui se setea el bpm según el mood
    def set_bpm(self, bpm_: int):
        self.bpm = bpm_

    # Aqui se guardan las escalas para escoger una y crear las notas
    def append_scale(self, scale: tuple):
        self.steps = scale
        self.make_scale()

    def make_scale(self):
        # Tomar la nota base de la escala (Tonica)
        actual_note = self.tonic_midi
        # Se guarda el largo de la escala
        scale_len = len(self.steps[1])
        # Se crean 2 octavas de la escala
        for midi_note in range(scale_len * 2):
            aux_note = actual_note + self.steps[1][midi_note % len(self.steps[1])]
            self.scale_.append(aux_note)
            #print("Midi note: " + str(aux_note))
            actual_note = aux_note
        # Se printea la escala
        #for x in self.scale_:
        #    print(x)

    def make_chords(self, numBars: int,  falling: bool):
        """ Generates a sequence of chords """
        
        actual_note = self.tonic_midi
        scale = [actual_note]

        sequence_size = None
        self.numBars = numBars

        """
        # De 3 a 4 compases tendrá la secuencia de acordes
        self.seq_size = random.randint(3, 4)
        if self.seq_size > numBars:
            self.seq_size = numBars
        """


        # Crear la escala
        for i in range(6):
            actual_note = actual_note + self.steps[1][i % len(self.steps[1])]
            scale.append(actual_note)
        
        
        # ----- Crear acordes
        # Triadas
        actual_note = self.tonic_midi
        len_steps = len(self.steps[1])    # Largo de arreglo de steps de la escala
        for i in range(7):
            chord = []
            chord.append(actual_note)
            acum = 0
            for j in range(5):
                acum += self.steps[1][((i + j) % len_steps)]
                if j == 1:
                    chord.append(actual_note + acum)
                if j == 3:
                    chord.append(actual_note + acum)
                    continue
            self.chords.append(chord)
            actual_note += self.steps[1][i]
        
        print("Chords")
        print(self.chords)

        # Escoger los acordes de la secuencia
        self.select_chords(falling)

    def select_chords(self, falling: bool):

        # Escoger acordes para la secuencia
        # De momento es muy dummy
        self.seq_chords.clear()      # Limpiar lista si ya tiene acordes

        # Secuencia Descendiente
        if falling:
            deegres = [[5, 4, 3], [0, 5, 3, 4], [0, 0, 3, 5], [5, 3, 0, 4], [0, 6, 5, 6], [3, 0, 4, 5]]

            rand_ = random.randint(0, 3)

            for i in range(len(deegres[rand_])):
                self.seq_chords.append([4] + self.chords[deegres[rand_][i]])


        # Secuencia random
        else:
            for i in range(self.seq_size):
                self.seq_chords.append([4] + random.choice(self.chords))   # [4] es la duración del acorde (1 compás)



