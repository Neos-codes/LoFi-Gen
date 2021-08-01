'''
    Raters for fitness function
                                '''

STANDAR_RELEVANCE = 0.5
TARGET_RATINGS = {
    'neighboring_pitch_range': 0.3,
    'direction_of_melody': 0.5,
    'stability_of_melody': 0.6,
    'pitch_range': 0.5,
    'continuos_silence': 0.5,
    'silences_density': 0.4,
    'syncopaty_in_melody': 0.5,
    'unique_note_pitches': 0.4,
    'equal_consecutive': 0.7,
    'unique_rhythm_values': 0.6
}

def neighboring_pitch_range(ind):
    '''
        Detects notes with a pitch value at least two octaves apart
        compared to the previous note

        Return
        ------
        rate: float (0 - 1)
    '''

    crazy_notes = 0
    total_notes = 0

    for bar in ind:
        for index in range(len(bar.notes)):
            total_notes += 1

            if index < len(bar.notes) - 1:
                diff = bar.notes[index].tone - bar.notes[index + 1].tone

                if abs(diff) >= 16:
                    crazy_notes += 1

            else:
                total_notes += 1 # adds final note
                break

    return crazy_notes/total_notes


def direction_of_melody(ind):
    '''
        Counts amount of time a tone is higher than the one before. (indicates the slope)

        Return
        ------
        rate: float (0 - 1)
    '''

    higher = 0
    total_notes = 0
    prev = None

    for bar in ind:
        for note in bar.notes:
            total_notes += 1

            if prev is None:
                prev = note
                continue

            if note.tone > prev.tone:
                higher += 1

            prev = note

    return higher/total_notes


def stability_of_melody(ind):
    '''
        Counts amount of times the melody pitch direction changes.

        Return
        ------
        rate: float (0 - 1)
    '''

    changes = 0
    prev = None
    total_notes = 0

    # calculate initial direction
    if (ind[0].notes[1].tone - ind[0].notes[0].tone) >= 0:
        direction = 'up'
    else:
        direction = 'down'

    for bar in ind:
        for note in bar.notes:
            total_notes += 1

            if prev is None:
                prev = note
                continue

            # get current direction
            if note.tone >= prev.tone:
                current_direction = 'up'
            else:
                current_direction = 'down'

            # compare directions
            if direction != current_direction:
                changes += 1
                direction = current_direction

            prev = note

    return changes/total_notes


def pitch_range(ind):
    '''
        Compares the highest and lowest pitch.

        Return
        ------
        rate: float (0 - 1)
    '''

    highest = 0
    lowest = 100

    for bar in ind:
        for note in bar.notes:
            if note.tone > highest:
                highest = note.tone
                continue

            if note.tone < lowest and note.tone != 0:
                lowest = note.tone

    return lowest/highest


def continuos_silence(ind):
    '''
        Identify long segments of silence.
            1. Find the longest bar
            2. Count total duration of silence in the longest bar.
            3. Compare duration of silence vs duration of the bar.
            4. Use equation:
                    rate = 1 - silence_duration/longest_bar_duration
    '''

    silence = None
    silence_duration = 0
    notes_duration = 0
    longest_silence = 0

    # Iniciar bandera con la primera nota del individuo
    # Si la primera nota es un silencio, silence = true, si no, silence = false
    if ind[0].notes[0].tone == 0:
        silence = True
    else:
        silence = False


    for bar in ind:
        for note in bar.notes:

            # Si estamos contando los "no silencio" y la nota actual es un silencio, comenzamos a contar silencios            
            if not silence and note.tone == 0:
                silence = True
            
            # Si estamos contando los "silencios" y la nota actual no es un silencio,
            # Obtenemos la relación de duracion silencios vs duracion total de la frase hasta este punto
            # No es una heuristica muy precisa, pero no hay formas de distinguir una frase al ser muy subjetivas
            elif silence and note.tone != 0:
                silence = False
                if silence_duration / (silence_duration + notes_duration) > longest_silence:
                    longest_silence = silence_duration / (silence_duration + notes_duration)
                    silence_duration = 0
                    notes_duration = 0


            if not silence:
                notes_duration += note.duration
            # Si es silencio, añadir duracion al acumulador de notas que SI son silencio
            else:
                silence_duration += note.duration
    
    #print("Relacion longest silence:", longest_silence, 1 - longest_silence)

    return 1 - longest_silence


def silences_density(ind):
    '''
        Compares the amount on silences vs amount of notes.
        --> This one is different from the paper!

        Return
        ------
        rate: float (0 - 1)
    '''

    silences = 0
    total_notes = 0

    for bar in ind:
        for note in bar.notes:
            total_notes += 1

            if note.tone == 0:
                silences +=1

    return silences/total_notes


def syncopaty_in_melody(ind):
    '''
        Counts amount of syncopations.
        syncopation => note duration is the same from note to note.

        Return
        ------
        rate: float (0 - 1)
    '''

    syncopations = 0
    prev = None
    sync_duration = None
    total_notes = 0

    for bar in ind:
        for note in bar.notes:
            total_notes += 1

            if prev is None:
                prev = note
                continue

            if sync_duration and (note.duration == sync_duration):
                syncopations += 1
                prev = note
                continue

            sync_duration = None

            if note.duration == prev.duration:
                syncopations += 2
                sync_duration = note.duration

            prev = note

    return syncopations/total_notes


def unique_note_pitches(ind):
    '''
        Count the unique tones and compares it with number of notes

        Return
        ------
        rate: float (0 - 1)
    '''

    pitches = []
    total_notes = 0

    for bar in ind:
        for note in bar.notes:
            total_notes += 1

            if note.tone not in pitches:
                pitches.append(note.tone)

    return len(pitches)/total_notes


def equal_consecutive(ind):
    '''
        Evaluates how many times two consecutive notes share the same pitch value.

        Return
        ------
        rate: float (0 - 1)
    '''

    pairs = 0
    prev = None
    total_notes = 0

    for bar in ind:
        for note in bar.notes:
            total_notes += 1

            if prev is None:
                prev = note
                continue

            if note.tone == prev.tone:
                pairs += 1

            prev = note

    return pairs/total_notes


def unique_rhythm_values(ind):
    '''
        Count the unique durations of notes and compares it with total number of notes

        Return
        ------
        rate: float (0 - 1)
    '''

    durations = []
    total_notes = 0

    for bar in ind:
        for note in bar.notes:
            total_notes += 1

            if note.duration not in durations:
                durations.append(note.duration)

    return len(durations)/total_notes



def rate(ind, target_ratings):
    '''
        Uses raters to rate the population.

        -->    MISSING: USE OF INFLUENCE FOR RATERS     <--
        -->    MISSING: REAL RATERS VALUES              <--

        Params
        ------
        ind : list
        target_ratigs : dict

        Return
        ------
        rate : float (0 - 1)

    '''

    RATERS = [
        neighboring_pitch_range,
        direction_of_melody,
        stability_of_melody,
        pitch_range,
        silences_density,
        syncopaty_in_melody,
        unique_note_pitches,
        equal_consecutive,
        unique_rhythm_values,
        continuos_silence
    ]

    parcial_rate = 0

    for rater in RATERS:
        Q = abs(target_ratings[rater.__name__] - rater(ind))
        parcial_rate += Q * STANDAR_RELEVANCE

    I = 0
    for _ in range(len(RATERS)):
        I += STANDAR_RELEVANCE

    return parcial_rate/I
