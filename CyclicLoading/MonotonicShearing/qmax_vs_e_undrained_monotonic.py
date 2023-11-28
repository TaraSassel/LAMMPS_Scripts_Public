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
cycle_list = [1,2,3,4,5,10,20,30,40,50]
for ampl in ampl_list:
    path = r'E:\Monotonic_Undrained\Initial_300\merged_data'
    print(path)
    qmax_val, e0_val = get_qmax_e0(path)
    e0 = [e0_val]
    qmax = [qmax_val]

    for c in cycle_list:
        path = rf'E:\Monotonic_Undrained\300kPa_{ampl}\Cycle{c}\merged_data'
        print(path)
        qmax_val, e0_val = get_qmax_e0(path)
        qmax.append(qmax_val)
        e0.append(e0_val)

    cycle_numbers = [0,1,2,3,4,5,10,20,30,40,50]
    df = pd.DataFrame(data = {"cycle_number":cycle_numbers, "void_ratio": e0, "qmax": qmax})

    os.chdir(r"E:\Monotonic_Undrained")
    df.to_csv(f"qmax_e_{ampl}.csv",header = True, index = False)
