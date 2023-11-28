"""
Author: Tara Sassel
Date: 10/01/2023

In this script the basic infofor the stress controlled data is defined.
Making the process for future scripts easier
"""

import os
import pandas as pd 
from typing import Tuple, List

def get_info() -> List:
    """
    Function returns:
        cyclicturns
        friction coefficent
        colors
    """
    # Number of timestep until strain reversal
    # 0.1% strain, 0.5% strain, 1% strain
    # The same for 2, 4, 6 and 8m therefore x4
    cyclic_turns = [1113422, 5567104, 11134206]*4

    # Depth
    depth = [2, 2, 2, 4, 4, 4, 6, 6, 6, 8, 8, 8]

    # Get strainampl
    strainampl = [0.1, 0.5, 1]*4
   
    # Get fc 
    fc = [0.25, 0.25, 0.25]*4

    # Get colors
    c2 = ['lightgreen', 'forestgreen', 'darkgreen']
    c4 = ['lightsteelblue', 'royalblue', 'navy']
    c6 = ['mediumpurple', 'blueviolet','indigo']
    c8 = ['lightcoral', 'indianred','maroon']

    colors = c2 + c4 + c6 + c8

    return cyclic_turns, strainampl, colors, depth, fc  


def get_path_list(drive_letter: str) -> list:
    """
    Function creates list with all paths
    Input: letter of dirve for example 'F'
    """
    # Initial sample sizes
    path2_0p1 = rf'{drive_letter}:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_2m\Strain0p1'
    path2_0p5 = rf'{drive_letter}:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_2m\Strain0p5'
    path2_1p0 = rf'{drive_letter}:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_2m\Strain1'
    path4_0p1 = rf'{drive_letter}:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_4m\Strain0p1'
    path4_0p5 = rf'{drive_letter}:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_4m\Strain0p5'
    path4_1p0 = rf'{drive_letter}:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_4m\Strain1'
    path6_0p1 = rf'{drive_letter}:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_6m\Strain0p1'
    path6_0p5 = rf'{drive_letter}:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_6m\Strain0p5'
    path6_1p0 = rf'{drive_letter}:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_6m\Strain1'
    path8_0p1 = rf'{drive_letter}:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_8m\Strain0p1'
    path8_0p5 = rf'{drive_letter}:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_8m\Strain0p5'
    path8_1p0 = rf'{drive_letter}:\K0StrainControlledCyclic\Dry_K0_FC0p25to0p25_8m\Strain1'

    path_list = [
        path2_0p1,
        path2_0p5,
        path2_1p0,
        path4_0p1,
        path4_0p5,
        path4_1p0,
        path6_0p1,
        path6_0p5,
        path6_1p0,
        path8_0p1,
        path8_0p5,
        path8_1p0                    
        ]
    return path_list

def get_sample_dim(path_list: list) -> Tuple[list,list,list]:
    """
    Function collects sample initial dimension from dump files
    Input:  list with paths
    """
    # To store sample dimension
    sample_dimx = []
    sample_dimy = []
    sample_dimz = []
    for path in path_list:
        path_atom0 = path + r'\run1\atom\dump0.atom'
        with open(path_atom0, 'r') as fp:
            # lines to read
            line_numbers = [5,6,7]
            for i, line in enumerate(fp):
                # read line 5 to 7
                if i in line_numbers:
                    dimensions = line.split(" ")
                    # save sample x-dimension
                    if i == 5:
                        sample_dimx.append(float(dimensions[1]))
                    # save sample y-dimension
                    if i == 6:
                        sample_dimy.append(float(dimensions[1]))
                    # save sample z-dimension
                    if i ==7:
                        sample_dimz.append(float(dimensions[1]))
                elif i > 7:
                    # don't read after line 7 to save time
                    break
    return sample_dimx, sample_dimy, sample_dimz

def get_K0_info(drive_letter: str) -> pd.DataFrame:
    cyclic_turns, strainampl, colors, depth, fc = get_info()
    path_list = get_path_list(drive_letter)
    sample_dimx, sample_dimy, sample_dimz = get_sample_dim(path_list)
    K0Info = pd.DataFrame(data = {
        'path': path_list,
        'depth': depth,
        'strain_amplitude': strainampl,
        'friction_coefficient': fc,
        'cyclic_turns': cyclic_turns,
        'xdim': sample_dimx,
        'ydim': sample_dimy,
        'zdim': sample_dimz,
        'colors': colors
        }
    )
    return K0Info