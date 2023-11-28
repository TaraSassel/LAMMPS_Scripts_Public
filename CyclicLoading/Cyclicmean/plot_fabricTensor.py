"""
Author: Tara Sassel
Date: 30/11/2022
In this script the fabric tensor is plotted ffor seperated positions
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

# Definig Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 3     # Line Width

path = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data\SortedData\0_StartingPos\contact'
os.chdir(path)

fabric_tensor = pd.read_csv("fabric_tensor.csv")
print(fabric_tensor.head())

plt.figure(figsize = (7,7))

plt.plot(fabric_tensor.ft1, ls = ':', color = 'green', lw = lw1,label = '$\Phi_{1}$')
plt.plot(fabric_tensor.ft2, ls = ':', color = 'blue', lw = lw1,label = '$\Phi_{2}$')
plt.plot(fabric_tensor.ft3, ls = ':', color = 'red', lw = lw1,label = '$\Phi_{3}$')

plt.xlabel('Cycle Number', fontsize = LBF)
plt.ylabel('Princical Fabric', fontsize = LBF)
plt.legend(loc = 'upper right', fontsize = LGF)
plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
plt.gca().tick_params(which = 'major', labelsize = TS)
plt.xlim(0,50)
plt.grid()
plt.tight_layout()
plt.show()
