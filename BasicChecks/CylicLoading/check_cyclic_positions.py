# Autor: Tara Sassel
# Date: 20/10/2022
# Script to check if positions of dump files are correct

# Import libraries
import numpy as np
import pandas as pd

# Calculating cycle length
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))
cyclic_int = np.round_(cycle_length/4, decimals = 0)

# Defining number of cycles
cycle_number = np.arange(0,100,1)

# Defining cyclic positions
pos0 = 4*cyclic_int*cycle_number
pos1 = cyclic_int + pos0
pos2 = cyclic_int*2 + pos0
pos3 = cyclic_int*3 + pos0

positions = pd.DataFrame(
    data ={
        'cycle_number': cycle_number,
        'starting_pos': pos0,
        'loaded_pos': pos1,
        'neutral_pos': pos2,
        'unloaded_pos': pos3
    })

with pd.option_context('display.float_format', '{:0.0f}'.format):
    print(positions.head(60))
