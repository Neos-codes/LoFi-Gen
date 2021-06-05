# Standar import to generation package
import sys
import os
sys.path.append(os.path.abspath('../generation'))

from utils import toMidi
from music_elements import Bar

SCALE = [55, 57, 60, 0] # 0 means silence

# crear un ind
ind = []
for _ in range(4):
    ind.append(Bar.from_scale(SCALE, 4, 4))

for bar in ind:
    print(bar)

toMidi(ind, 'silence', 1, 60)
