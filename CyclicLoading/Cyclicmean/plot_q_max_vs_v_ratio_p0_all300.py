"""
Author: Tara Sassel
Date: 23/11/2022
This script gerenerates a figure of q_max vs void ratio
q_max was established from monotonic shearing
"""

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

# Define Plot Fontsizes
TF = 24     # Text font
LGF = 7   # Legend Font Size
LBF = 12    # Label Font Size
TS = 10     # Tick Size
lw1 = 2     # Line Width

color_list = ["forestgreen", "cornflowerblue", 'black']

e_max_300_90_p0 = [0.6612, 0.6498, 0.6459, 0.6445, 0.6560, 0.6555, 0.6410, 0.6386, 0.6367, 0.6354, 0.6343]
q_max_300_90_p0 = [51.4, 23.4,50.5,63.8, 48.8, 54.4, 83.5, 88.9, 94.6, 98.9, 101.6]

e_max_300_90_p1 = [0.6569, 0.6474 , 0.6451, 0.6441, 0.6433, 0.6427, 0.6407, 0.6384, 0.6366, 0.6353, 0.6343]
q_max_300_90_p1 = [70.6, 77.2, 80.6, 81.8, 83.2, 84.8, 91.3, 94.7, 100.0, 103.1, 105.2]

e_iso = [0.6515, 0.6500, 0.6478, 0.6448, 0.6406, 0.6343, 0.6342, 0.6293, 0.6250]
q_iso = [84.6, 82.6, 92.7, 98.3, 111.7, 121.7, 128.4, 141.6, 168.0]

# Starting figure
plt.figure(figsize = (5,5))

plt.plot(e_max_300_90_p0 , q_max_300_90_p0, ls = '--', ms = 12, mfc = "white", mec = 'white', marker = 'o', color = color_list[0])
plt.plot(e_max_300_90_p1 , q_max_300_90_p1, ls = '--', ms = 12, mfc = "white", mec = 'white', marker = 'o', color = color_list[1])
plt.plot(e_iso, q_iso, ls = '--', color = color_list[2], marker = 's', ms = '5')

def plot_cycle_numbers(xs,ys,c1):
    """
    This function puts numbers as markers
    """
    cycle_number = [0, 1, 2, 3, 4, 5, 10, 20, 30, 40, 50]
    i = 0
    for x, y in zip(xs, ys):
        plt.text(x,y, str(cycle_number[i]) , ha = 'center', va = 'center', color = c1, fontsize = 8)
        i +=1

plot_cycle_numbers(e_max_300_90_p0,q_max_300_90_p0,color_list[0])
plot_cycle_numbers(e_max_300_90_p1,q_max_300_90_p1,color_list[1])

plt.xlabel("Void Ratio ($e$)", fontsize = LBF)
plt.ylabel("Maximum deviatoric stress ($q^{max}$) [kPa]", fontsize = LBF)

# Legend
custom_lines = [Line2D([0], [0], color=color_list[0], lw=1, ls = '--', marker = '$N$', ms = 5),
                Line2D([0], [0], color=color_list[1], lw=1, ls = '--', marker = '$N$', ms = 5),
                Line2D([0], [0], color=color_list[2], lw=1, ls = '--', marker = 's', ms = 5)]
ax = plt.gca()
ax.legend(custom_lines, ['Start of cycle', 'Neutral position when unloading', 'Isotropic sample'])

ax.tick_params(axis='both', which='major', labelsize=TS)
plt.grid()
plt.tight_layout()
plt.show()
