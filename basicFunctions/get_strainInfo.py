"""
Author: Tara Sassel
Date: 13/12/2022

In this script the basic info of the strain controlled data is defined.
Which makes it easier to collect this info for further simulations
"""
import os
import pandas as pd
from typing import Tuple, List

def get_cyclic_info() -> List:
    # Number of timestep until strain reversal
    # 0.1% strain, 0.5% strain, 1% strain
    cyclic_turns100 = [1114194, 5570965, 11141932]
    cyclic_turns200 = [1113966, 5569822, 11139642]
    cyclic_turns300 = [1113698, 5568485, 11136970, 1113698, 5568485, 11136970, 1113698, 5568485, 11136970]

    cyclic_turns = cyclic_turns100 + cyclic_turns200 + cyclic_turns300

    # Get isostress
    isostress100 = [100, 100, 100]
    isostress200 = [200, 200, 200]
    isostress300 = [300, 300, 300, 300, 300, 300, 300, 300, 300]   

    isostress = isostress100 + isostress200 + isostress300

    # Get strainampl
    strainampl100 = [0.1, 0.5, 1]
    strainampl200 = [0.1, 0.5, 1]
    strainampl300 = [0.1, 0.5, 1, 0.1, 0.5, 1, 0.1, 0.5, 1]

    strainampl = strainampl100 + strainampl200 + strainampl300

    # Get fc
    fc100 = [0.25, 0.25, 0.25]
    fc200 = [0.25, 0.25, 0.25]
    fc300 = [0.25, 0.25, 0.25, 0.15, 0.15, 0.15, 0.1, 0.1, 0.1]
    fc = fc100 + fc200 + fc300

    # Get colors
    c100 = ['lightgreen', 'forestgreen', 'darkgreen']
    c200 = ['lightsteelblue', 'royalblue', 'navy']
    c300 = ['lightcoral', 'indianred','maroon', 'lightcoral', 'indianred','maroon', 'lightcoral', 'indianred','maroon']
    
    c = c100 + c200 + c300

    # color screme 2
    c100_2 = ['forestgreen']*3
    c200_2 = ['royalblue']*3
    c300_2 = ['indianred']*9
    c2 = c100_2 + c200_2 + c300_2

    return cyclic_turns, isostress, strainampl, fc, c, c2



def get_path_list(drive_letter: str) -> list:
    """
    Function creates list with all paths
    Input: letter of dirve for example 'F'
    """
    # Initial sample sizes
    path100_0p1 = rf'{drive_letter}:\StrainControlledCyclic\100kPa\Strain0p1'
    path100_0p5 = rf'{drive_letter}:\StrainControlledCyclic\100kPa\Strain0p5'
    path100_1p0 = rf'{drive_letter}:\StrainControlledCyclic\100kPa\Strain1'
    path200_0p1 = rf'{drive_letter}:\StrainControlledCyclic\200kPa\Strain0p1'
    path200_0p5 = rf'{drive_letter}:\StrainControlledCyclic\200kPa\Strain0p5'
    path200_1p0 = rf'{drive_letter}:\StrainControlledCyclic\200kPa\Strain1'
    path300_0p1 = rf'{drive_letter}:\StrainControlledCyclic\300kPa\Strain0p1'
    path300_0p5 = rf'{drive_letter}:\StrainControlledCyclic\300kPa\Strain0p5'
    path300_1p0 = rf'{drive_letter}:\StrainControlledCyclic\300kPa\Strain1'
    path300_0p1_fc0p15 = rf'{drive_letter}:\StrainControlledCyclic\300kPa_FC0p15\Strain0p1'
    path300_0p5_fc0p15 = rf'{drive_letter}:\StrainControlledCyclic\300kPa_FC0p15\Strain0p5'
    path300_1p0_fc0p15 = rf'{drive_letter}:\StrainControlledCyclic\300kPa_FC0p15\Strain1'
    path300_0p1_fc0p1 = rf'{drive_letter}:\StrainControlledCyclic\300kPa_FC0p1\Strain0p1'
    path300_0p5_fc0p1 = rf'{drive_letter}:\StrainControlledCyclic\300kPa_FC0p1\Strain0p5'
    path300_1p0_fc0p1 = rf'{drive_letter}:\StrainControlledCyclic\300kPa_FC0p1\Strain1'

    path_list = [
        path100_0p1,
        path100_0p5,
        path100_1p0,
        path200_0p1,
        path200_0p5,
        path200_1p0,
        path300_0p1,
        path300_0p5,
        path300_1p0,
        path300_0p1_fc0p15,
        path300_0p5_fc0p15,
        path300_1p0_fc0p15,
        path300_0p1_fc0p1,
        path300_0p5_fc0p1,
        path300_1p0_fc0p1
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

def get_strain_info(drive_letter: str) -> pd.DataFrame:
    cyclic_turns, isostress, strainampl, fc, c, c2 = get_cyclic_info()
    path_list = get_path_list(drive_letter)
    sample_dimx, sample_dimy, sample_dimz = get_sample_dim(path_list)

    strainInfo = pd.DataFrame(data = {
        'path': path_list,
        'iso_stress': isostress,
        'strain_amplitude': strainampl,
        'friction_coefficient': fc, 
        'cyclic_turns': cyclic_turns,
        'xdim': sample_dimx,
        'ydim': sample_dimy,
        'zdim': sample_dimz,
        'colors': c,
        'colors2': c2
        }
    )
    return strainInfo