"""
Function
"""
import numpy as np

def get_strain(length: np.array) -> np.array:
    """
    Function that calculates change in strain in %
    """
    delta = np.zeros(len(length),)

    for i in range(len(length)):
        delta[i] =  length[i] - length[0]

    strain =delta*100/length[0]
    delta_strain = strain[0] - strain
    return delta_strain
