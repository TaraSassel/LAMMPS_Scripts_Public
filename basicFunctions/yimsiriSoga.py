"""
Autor: Tara Sassel
Date: 21/10/2022
"""
import numpy as np
from typing import Tuple
from sympy import symbols, Eq, solve

def get_a_yimsiri_soga(CNfabrictensor: np.array) -> Tuple[float, float, float, float]:
    """
    This function defines a as defined in Yimsiri and Soga (2010)
    DEM analysis of soil fabric effects on behaviour of sand
    """
    # Getting Eigenvalues from fabric tensor
    #EigenValues = np.linalg.eig(CNfabrictensor)
    #EigenValues = EigenValues[0] # Only want the eigenvalues and not the associated eigenvectors

    # Defining 3 equaltions defined in the paper
    a1 = symbols('a1')
    a2 = symbols('a2')
    a3 = symbols('a3')
    eq1 = Eq((3*a1-5)/(5*(a1-3))-CNfabrictensor[0,0])
    eq2 = Eq((3*a2-5)/(5*(a2-3))-CNfabrictensor[1,1])
    eq3 = Eq((-(5+a3))/(5*(a3-3))-CNfabrictensor[2,2])

    # Solving equations for a
    a_val1 = solve(eq1)[0]
    a_val2 = solve(eq2)[0]
    a_val3 = solve(eq3)[0]

    # Getting average value of a
    a = (a_val1 + a_val2 + a_val3)/3

    return a, a_val1, a_val2, a_val2
