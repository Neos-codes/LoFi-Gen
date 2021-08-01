import pretty_midi
midi_data = pretty_midi.PrettyMIDI('1.mid')
print("duration:",midi_data.get_end_time())
print("tempo changes:",midi_data.get_tempo_changes())
print("tempo:",midi_data.estimate_tempo())
#print(f'{"note":>15} {"start":>15} {"end":>15}{"duration":>15}')
print("beats:" ,midi_data.get_beats())
print("downbeats:",midi_data.get_downbeats())
print("quarter duration:", midi_data.estimate_tempo()/60)
#print(midi_data.initial_tempo)
print(f'{"note":>15} {"start":>15} {"duration":>15}')
for instrument in midi_data.instruments:
    print("instrument:", instrument.program);
    for note in instrument.notes:
        #print(f'{note.pitch:15} {note.start:15} {note.end:15} {note.get_duration():15}')
        print(f'{note.pitch:15} {note.start:15} {note.duration:15}')
        print(midi_data.time_to_tick(note.duration))