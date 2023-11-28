"""
This script contains function to load the data
Stress, Energy, Voids Ratio
"""
import os
import typing
import fnmatch
import pandas as pd

def get_stress_data(path: str) -> pd.DataFrame:
    """
    Imports stress data
        Input: path to stress data which is a string
        Output: pd Dataframe containg all stress data
    """

    os.chdir(path)

    # Names of Files
    for (dirpath, dirnames, filenames) in os.walk(path):
        for file in filenames:
            if file.endswith(".txt"):
                if fnmatch.fnmatch(file,"*stress*"):
                    stress_file = file
                    print(stress_file)

    stress_names = [
    'step_s',
    'stress_xx',
    'stress_yy',
    'stress_zz',
    'stress_xy',
    'stress_xz',
    'stress_yz',
    'length_x',
    'length_y',
    'length_z'
    ]

    stress_data = pd.read_csv(stress_file, index_col=None, delimiter = ' ', skiprows = 1, names = stress_names)
    return stress_data
