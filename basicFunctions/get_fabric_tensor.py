# Author: Tara Sassel
# Date: 20/10/22
"""
This script contains functions to calculate the fabric tensor
"""

import numpy as np
import pandas as pd

def get_fabric_tensor_cn(contact_data: pd.DataFrame) -> np.array:
    """
    Fabric tensor in the contact normal direction
        Input: pd.DataFrame of contact force dump file
        Output: fabric tensor in the contact normal direction as np.array
    """
    # Idenitify contacts with non-zero force
    contact_data_n0 = contact_data[contact_data[3]>0]
    contact_data_n0  = contact_data_n0.to_numpy().T

    # DETRMINING CONTACT FORCE ----------------------------------------------------
    # 1. Distance between centroids (branch vector)
    X1 = contact_data_n0[6,:]
    Y1 = contact_data_n0[7,:]
    Z1 = contact_data_n0[8,:]
    R1 = contact_data_n0[9,:]

    X2 = contact_data_n0[10,:]
    Y2 = contact_data_n0[11,:]
    Z2 = contact_data_n0[12,:]
    R2 = contact_data_n0[13,:]

    # determining branch vector
    BV = np.sqrt(((X1-X2)**2)+((Y1-Y2)**2)+((Z1-Z2)**2)) # disk disk brach vechtor

    # unit vectors describing contact normal orientation
    N_nx = (X1-X2)/BV
    N_ny = (Y1-Y2)/BV
    N_nz = (Z1-Z2)/BV

    # fabric tensor based on contact normal orientaions
    CNfabrictensor = np.zeros((3,3))

    CNfabrictensor[0,0] =   np.sum(N_nx*N_nx)
    CNfabrictensor[0,1] =   np.sum(N_nx*N_ny)
    CNfabrictensor[0,2] =   np.sum(N_nx*N_nz)

    CNfabrictensor[1,0] =   np.sum(N_ny*N_nx)
    CNfabrictensor[1,1] =   np.sum(N_ny*N_ny)
    CNfabrictensor[1,2] =   np.sum(N_ny*N_nz)

    CNfabrictensor[2,0] =   np.sum(N_nz*N_nx)
    CNfabrictensor[2,1] =   np.sum(N_nz*N_ny)
    CNfabrictensor[2,2] =   np.sum(N_nz*N_nz)

    CNfabrictensor[:,:] = np.nan_to_num(CNfabrictensor[:,:]/len(X1))

    return  CNfabrictensor


def get_fabric_tensor_f(contact_data: pd.DataFrame) -> np.array:
    """
    Fabric tensor for the resultant force orientation
        Input: pd.DataFrame of contact force dump file
        Output: fabric tensor in the resultant force orientation as np.array
    """
    # Idenitify contacts with non-zero force
    contact_data_n0 = contact_data[contact_data[3]>0]
    contact_data_n0  = contact_data_n0.to_numpy().T

    # DETRMINING CONTACT FORCE ----------------------------------------------------
    # 1. Distance between centroids (branch vector)
    X1 = contact_data_n0[6,:]
    Y1 = contact_data_n0[7,:]
    Z1 = contact_data_n0[8,:]
    R1 = contact_data_n0[9,:]

    X2 = contact_data_n0[10,:]
    Y2 = contact_data_n0[11,:]
    Z2 = contact_data_n0[12,:]
    R2 = contact_data_n0[13,:]

    NormalForce = np.zeros((3,len(X1)))
    NormalForce[0,:] = contact_data_n0[3,:]*(X1-X2) # x component of normal force
    NormalForce[1,:] = contact_data_n0[3,:]*(Y1-Y2) # y component of normal force
    NormalForce[2,:] = contact_data_n0[3,:]*(Z1-Z2) # z component of normal force

    ResultantForce = np.zeros((4,len(X1)))
    ResultantForce[0,:] = NormalForce[0,:] + contact_data_n0[0,:] # x component of resultant force, i.e. sum of normal shear force
    ResultantForce[1,:] = NormalForce[1,:] + contact_data_n0[1,:] # x component of resultant force, i.e. sum of normal shear force
    ResultantForce[2,:] = NormalForce[2,:] + contact_data_n0[2,:] # x component of resultant force, i.e. sum of normal shear force

    ResultantForce[3,:] = np.sqrt(ResultantForce[0,:]*ResultantForce[0,:]+ResultantForce[1,:]*ResultantForce[1,:]+ResultantForce[2,:]*ResultantForce[2,:])

    # Unit vectors describing resultant force orientations
    F_nx = ResultantForce[0,:]/ResultantForce[3,:]
    F_ny = ResultantForce[1,:]/ResultantForce[3,:]
    F_nz = ResultantForce[2,:]/ResultantForce[3,:]

    # fabric tensor
    Ffabrictensor = np.zeros((3,3))

    Ffabrictensor[0,0] =  np.sum(F_nx*F_nx)
    Ffabrictensor[0,1] =  np.sum(F_nx*F_ny)
    Ffabrictensor[0,2] =  np.sum(F_nx*F_nz)

    Ffabrictensor[1,0] =  np.sum(F_ny*F_nx)
    Ffabrictensor[1,1] =  np.sum(F_ny*F_ny)
    Ffabrictensor[1,2] =  np.sum(F_ny*F_nz)

    Ffabrictensor[2,0] =  np.sum(F_nz*F_nx)
    Ffabrictensor[2,1] =  np.sum(F_nz*F_ny)
    Ffabrictensor[2,2] =  np.sum(F_nz*F_nz)

    Ffabrictensor[:,:] = np.nan_to_num(Ffabrictensor[:,:]/len(X1))

    return Ffabrictensor
