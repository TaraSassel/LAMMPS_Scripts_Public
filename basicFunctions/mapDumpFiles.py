"""
Get folder where dump files are located

"""

# Imports
import os
import re
import fnmatch
import pandas as pd
import numpy as np

from basicFunctions.get_combinedDump import get_combinedDump

# Create a map of dump files:
path = rf'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\run{r}'

def get_numbers_from_filename(filename):
    return re.search(r'\d+', filename).group(0)

for r in
