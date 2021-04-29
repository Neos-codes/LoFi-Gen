import random

# The shortest note's duration
MINIMAL_DURATION = 0.3

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
        notes_total_duration = 0

        while notes_total_duration < duration:
            # creates random notes
            note_tone = random.choice(scale)
            note_duration = random.uniform(MINIMAL_DURATION, (duration - notes_total_duration))
            notes.append(Note(note_tone, note_duration))

            notes_total_duration += note_duration

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

        if duration_delta < 0:

            shorter_note_index = None
            for i in range(len(self.notes)):
                # check duration
                if (self.notes[i].duration - duration_delta) >= MINIMAL_DURATION:
                    shorter_note_index = i
                    break

            # if no adecuate note was found
            if shorter_note_index is None:
                self.notes.pop()

                # recursive call
                self.renew_integrity()

            else:
                self.notes[shorter_note_index].duration -= duration_delta

        elif duration_delta > 0:
            # select a random note
            longer_note_index = random.randint(0, len(self.notes) - 1)

            # longer its duration
            self.notes[longer_note_index].duration += duration_delta
