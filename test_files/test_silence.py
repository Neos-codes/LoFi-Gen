# Standar import to generation package
import sys
import os
sys.path.append(os.path.abspath('../generation'))

from utils import toMidi
from music_elements import Bar

SCALE = [48, 50, 52, 55, 57, 60, 62, 64, 67, 69, 72]

# crear un ind
ind = []
for _ in range(4):
    ind.append(Bar.from_scale(SCALE, 4, 4))

for bar in ind:
    print(bar)