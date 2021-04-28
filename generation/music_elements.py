import random

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
            # creates a notes
            note_tone = random.choice(scale)
            note_duration = random.uniform(0.5, (duration - notes_total_duration))
            notes.append(Note(note_tone, note_duration))

            notes_total_duration += note_duration

            # Note: this implementation may allow more than one note to be played at the same time

        return cls(notes, duration, pulses)

    def len(self):
        ''' amounts of notes in the bar '''

        return len(self.notes)
