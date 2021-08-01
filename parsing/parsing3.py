#taken from https://github.com/HackerPoet/Composer/blob/master/midi.py
#not working yet

from mido import MidiFile, MidiTrack, Message
import numpy as np

num_notes = 96
samples_per_measure = 96

def midi_to_samples(fname):
	has_time_sig = False
	flag_warning = False
	mid = MidiFile(fname)
	print("dumb")
	ticks_per_beat = mid.ticks_per_beat
	ticks_per_measure = 4 * ticks_per_beat

	for i, track in enumerate(mid.tracks):
		for msg in track:
			if msg.type == 'time_signature':
				new_tpm = msg.numerator * ticks_per_beat * 4 / msg.denominator
				if has_time_sig and new_tpm != ticks_per_measure:
					flag_warning = True
				ticks_per_measure = new_tpm
				has_time_sig = True
	if flag_warning:
		print ("  ^^^^^^ WARNING ^^^^^^")
		print( "    " + fname)
		print( "    Detected multiple distinct time signatures.")
		print( "  ^^^^^^ WARNING ^^^^^^")
		return []
	
	all_notes = {}
	for i, track in enumerate(mid.tracks):
		abs_time = 0
		for msg in track:
			abs_time += msg.time
			if msg.type == 'note_on':
				if msg.velocity == 0:
					continue
				note = msg.note - (128 - num_notes)/2
				assert(note >= 0 and note < num_notes)
				if note not in all_notes:
					all_notes[note] = []
				else:
					single_note = all_notes[note][-1]
					if len(single_note) == 1:
						single_note.append(single_note[0] + 1)
				all_notes[note].append([abs_time * samples_per_measure / ticks_per_measure])
			elif msg.type == 'note_off':
				if len(all_notes[note][-1]) != 1:
					continue
				all_notes[note][-1].append(abs_time * samples_per_measure / ticks_per_measure)
	for note in all_notes:
		for start_end in all_notes[note]:
			if len(start_end) == 1:
				start_end.append(start_end[0] + 1)
	samples = []
	for note in all_notes:
		for start, end in all_notes[note]:
			sample_ix = start / samples_per_measure
			while len(samples) <= sample_ix:
				samples.append(np.zeros((samples_per_measure, num_notes), dtype=np.uint8))
			sample = samples[int(sample_ix)]
			start_ix = start - sample_ix * samples_per_measure
			if False:
				end_ix = min(end - sample_ix * samples_per_measure, samples_per_measure)
				while start_ix < end_ix:
					sample[start_ix, note] = 1
					start_ix += 1
			else:
				sample[start_ix, note] = 1
	return samples

midi_to_samples("29-15.mid")