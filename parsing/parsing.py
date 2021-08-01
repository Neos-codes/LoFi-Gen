from MIDI import MIDIFile
from sys import argv

def parse(file):
	print("Parsing...")
	c=MIDIFile(file)
	c.parse()
	print(str(c))
	for idx, track in enumerate(c):
		print("index: ", idx, "|","track:",str(track))
		print(type(track))
		track.parse()
		print(f'Track {idx}:')
		print(str(track))

def main():
	#f = open("29-15.mid", "r")
	print(argv[1])
	print(type(argv[1])) 
	parse(argv[1])

if __name__ == "__main__":
	# execute only if run as a script
	main()

