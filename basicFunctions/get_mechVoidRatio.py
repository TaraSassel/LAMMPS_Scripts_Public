"""
Author: Tara Sassel
Date: 16/11/2022
In this script a function to calculate the mechanical void ratio is included.
"""
import os
import pandas as pd
import numpy as np

def get_mechVoidRatio(path: str, dump_file_number: int) -> float:
    """
    This function calculates the mechanical voids ratio.
    The mechanical void ratio does not include particles with 1 or 2 contacts.
    The path to the specific run should be provided not the dump files.
    This is because both the atom and contact dump file is required.
    """
    # ==========================================================================
    # LOADING DATA
    # Loading Atom data
    os.chdir(path + r'\atom')
    with open(f"dump{dump_file_number}.atom", 'r') as fp:
        header_line = fp.readlines()[8]
        header_line = header_line.replace("ITEM: ATOMS ", "")
        header_line = header_line.split()

        atom_data = pd.read_csv(
            f"dump{dump_file_number}.atom",
            skiprows = 9,
            header = None,
            names = header_line,
            delimiter = ' ',
            index_col=False)

    # Box dimensions
    with open(f"dump{dump_file_number}.atom", 'r') as fp:
        x_dim = np.array(fp.readlines()[5].split(" "))[1].astype(float)
    with open(f"dump{dump_file_number}.atom", 'r') as fp:
        y_dim = np.array(fp.readlines()[6].split(" "))[1].astype(float)
    with open(f"dump{dump_file_number}.atom", 'r') as fp:
        z_dim = np.array(fp.readlines()[7].split(" "))[1].astype(float)

    V_box = x_dim*y_dim*z_dim

    # Loading Connectivity data
    os.chdir(path + r'\connectivity')
    with open(f"dump{dump_file_number}.connectivity", 'r') as fp:
        header_line = fp.readlines()[8]
        header_line = header_line.replace("ITEM: ATOMS ", "")
        header_line = header_line.split()

        connectivity_data= pd.read_csv(
            f"dump{dump_file_number}.connectivity",
            skiprows = 9,
            header = None,
            names = header_line,
            delimiter = ' ',
            index_col=False)

    joined_data = pd.merge(atom_data, connectivity_data, on = 'id')

    # ==========================================================================
    # PROCESSING DATA
    # Renaming column with coordination number
    # The only column name with a c_ will be the coordination number
    col_names = list(joined_data.columns)
    coordination_name = [name for name in col_names if (name[0:1] in "c_")]
    joined_data = joined_data.rename(columns = {coordination_name[0]: "coord"})

    # For the mechanical void ratio we only take the particles with coord > 1
    mech_data = joined_data[joined_data["coord"]>1]

    if "radius" in col_names:
        radius = joined_data["radius"].to_numpy().T
        V_spheres =  np.sum((4/3)*np.pi*radius**3)
        e_mech = (V_box-V_spheres)/V_spheres

    elif "diameter" in col_names:
        diameter = joined_data["diameter"].to_numpy().T
        V_spheres = np.sum((1/6)*np.pi*diameter**3)
        e_mech = (V_box-V_spheres)/V_spheres

    else:
        print("ERROR: No column with radius or diameter")
        return np.NAN

    return e_mech
