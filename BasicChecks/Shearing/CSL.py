"""
Author: Tara Sassel
Date: 01/11/2022
The critical state parameters are defined in accordance with Huang et al. (2014)
Three of my points at a friction coefficent of 0.25 are included at eps_zz = 35%.
"""
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 12    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width

# Table 1. Huang et al. (2014)
M_cs = 0.695
phi_cs = 18.2
lambda1 = 0.000923
Gamma = 0.632
p_a = 101.325

def get_e_cs(p: float) -> float:
    """
    Function that defines void ratio at critical state
    """
    e_cs = Gamma - lambda1*(p/p_a)**0.7
    return e_cs

p = np.arange(100,500,10)
e_cs = [get_e_cs(p_val) for p_val in p]

# Figure
plt.figure(figsize = (7,7))

plt.plot(
    p,
    e_cs,
    lw = lw1,
    ls = '--',
    color = 'black',
    label = r"$\Gamma - \lambda (\frac{p'}{p_a})^{0.7}$" + '\n' +
                "$\Gamma = 0.632$" + "\n" +
                "$\lambda = 0.000923$" + "\n" +
                "$p_a = 101.325kPa$")

plt.plot(100, 0.637, ls = '', marker = 's', color = 'green')
plt.plot(200, 0.635, ls = '', marker = 's', color = 'green')
plt.plot(300, 0.634, ls = '', marker = 's', color = 'green')

legend_elements = [Line2D([0], [0],
                    color='black',
                    ls = '--',
                    lw=lw1,
                    label="CSL (Huang et al., 2014)"),
                   Line2D([0], [0], marker='s', ls = '', color='green', label='$\mu = 0.25$')]

plt.legend(handles=legend_elements, loc='upper right', fontsize = LGF)
plt.xlabel(r"$(\frac{p'}{p_a})^{0.7}$", fontsize = LBF)
plt.ylabel('Void Ratio (e)', fontsize = LBF)
plt.gca().tick_params(which = 'major', labelsize = TS)
plt.grid()
plt.tight_layout()
plt.show()
