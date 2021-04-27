# Standar import to generation package
import sys
import os
sys.path.append(os.path.abspath('../generation'))

import utils

utils.play_midi('0-1.mid')
