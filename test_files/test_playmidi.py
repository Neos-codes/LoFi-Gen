# Standar import to generation package
import sys
import os
sys.path.append(os.path.abspath('../generation'))

import utils

product_dir = '../generation/product/'
file_name = '0-0.mid'

utils.play_midi(product_dir + file_name)
