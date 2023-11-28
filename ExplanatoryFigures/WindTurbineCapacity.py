# Autor: Tara Sassel 
# Date: 06/05/2023

import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

LBF = 14
TS = 12
lw1 = 2
color_bar = 'lightsteelblue'
color_line = 'navy'

bars = [ 1.885, 3.472, 2.480, 2.976, 4.117, 5.456, 8.234, 8.581, 7.788, 7.937, 8.284, 8.333, 9.623, 
        10.81, 12.90, 14.93, 17.61, 19.69, 21.43, 21.43, 21.43, 21.43, 21.38, 21.38, 21.43, 21.43, 
        21.43, 21.33, 21.08, 20.14, 17.46, 15.38, 15.03
        ]

capacity = [17.86, 21.83, 24.80, 27.78, 30.75, 37.70, 45.63, 54.56, 60.52, 69.44, 76.39, 84.33, 94.25,
            106.2 ,116.1, 131.9, 148.8, 166.7, 189.5, 210.3, 232.1, 252.0, 270.8, 291.7, 311.5, 332.3, 
            353.2, 371.0, 390.9, 412.7, 427.6, 442.5, 450.4]

years = np.arange(2018, 2051, 1)


plt.figure(figsize = (10,5))

ax1 = plt.gca()
ax1.bar(years, bars, color = color_bar, ec = 'black')

ax2 = ax1.twinx() 
ax2.plot(years,capacity, color = color_line, lw = lw1)

ax1.set_ylabel(r'Installation rate [$\frac{GW}{year}$]', fontsize = LBF)
ax1.set_xlim(2017.25,2050.75)
ax1.set_ylim(0,25)

ax2.set_ylabel(r'Operational capacity [$GW$]', fontsize = LBF)
ax2.set_ylim(0,500)


legend_elements = [Patch(facecolor=color_bar, edgecolor='black',
                         label='Installed on sites'), 
                   Line2D([0], [0], color=color_line, lw=2, label='Operational capacity'),]

ax1.legend(handles=legend_elements, loc='upper left')

plt.gca().tick_params(axis='both', which='major', labelsize=TS)
plt.grid()
plt.show()