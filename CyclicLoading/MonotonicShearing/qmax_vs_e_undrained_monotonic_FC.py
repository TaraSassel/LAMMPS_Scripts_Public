"""
Author: Tara
Date: 02/11/2022

Script creates csv files with e0 and qmax
"""
# Import Libraries
import os
import numpy as np
import pandas as pd

# ==============================================================================
def get_qmax_e0(path):
    """
    This function returns qmax and e0 for undrained monotonic loading
    """
    os.chdir(path)
    stress_data = pd.read_csv('stress_data.csv')
    void_data = pd.read_csv('void_data.csv')

    # Convert to numpy
    np_stress_data = {}
    col_names = stress_data.columns

    for i, name in enumerate(col_names):
        np_stress_data[f"{name}"] = stress_data.iloc[:,i].to_numpy().T

    # Calculate q p
    q = (np_stress_data['stress_zz'] - np_stress_data['stress_xx'])
    p = (np_stress_data['stress_xx'] + np_stress_data['stress_yy'] \
    + np_stress_data['stress_zz'])/3

    qmax_val = np.max(q)
    e0_val = void_data.void_ratio[0]

    return qmax_val, e0_val

# ==============================================================================
ampl_list = [15,30,60,90]
friction_coeffcients = np.arange(10,21,1)
e0 = []
qmax = []

for FC in friction_coeffcients:

    path = rf'E:\Monotonic_Undrained\300kPa_FC\FC0p{FC}\merged_data'
    print(path)
    qmax_val, e0_val = get_qmax_e0(path)
    qmax.append(qmax_val)
    e0.append(e0_val)

fc = np.arange(0.10,0.21,0.01)
df = pd.DataFrame(data = {"friction_coefficient": fc, "void_ratio": e0, "qmax": qmax})

os.chdir(r"E:\Monotonic_Undrained")
df.to_csv(f"qmax_e_FC.csv",header = True, index = False)
