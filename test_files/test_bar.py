# Standar import to generation package
import sys
import os
sys.path.append(os.path.abspath('../generation'))

from music_elements import Bar
import utils

scale = [47, 48, 50, 52, 53, 55, 57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74]

ind = []
ind.append(Bar.from_scale(scale, 4, 4))
ind.append(Bar.from_scale(scale, 4, 4))
ind.append(Bar.from_scale(scale, 4, 4))
ind.append(Bar.from_scale(scale, 4, 4))

utils.toMidi(ind, 1 , 1)
