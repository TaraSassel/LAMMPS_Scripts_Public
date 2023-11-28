"""
Author: Tara Sassel
Date: 24/01/2023

Function to cacluclate qp
"""
import numpy as np 
import pandas as pd 

def get_qp(stress_data):
    """
    This function caclulates the deviatoric stress q
    and the mean effective stress p'

    Input:  stress_data -> pd.DataFrame
            must include stress_xx, stress_yy and stress_zz
    Output: q --> pd.DataFrame in Pa
            p --> pd.DataFrame in Pa
    """
    # convert to numpy 
    stress_xx = stress_data.stress_xx.to_numpy().T
    stress_yy = stress_data.stress_yy.to_numpy().T
    stress_zz = stress_data.stress_zz.to_numpy().T
    stress_xy = stress_data.stress_xy.to_numpy().T
    stress_yz = stress_data.stress_yz.to_numpy().T
    stress_xz = stress_data.stress_xz.to_numpy().T

    # Calculate q 
    #q = (stress_zz - stress_xx)
    q = np.sqrt(0.5*((stress_xx-stress_yy)**2+(stress_yy-stress_zz)**2+(stress_xx-stress_zz)**2+3*(stress_xy**2+stress_yz**2+stress_xz**2)))
    
    # Calculate p 
    p = (stress_xx + stress_yy + stress_zz)/3

    return q, p
