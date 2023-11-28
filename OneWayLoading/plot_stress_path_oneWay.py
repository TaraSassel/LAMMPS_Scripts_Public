# Author: Tara Sassel 
# Date: 22/06/23

import os
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt 
from matplotlib.lines import Line2D

# Fonts 
lw1 = 2
LBF = 16
LGF = 16
TS = 12
TXS = 14

# Import Data 
path1 = r'E:\CyclicLoading\Cyclicmean_OneWay\TX330_FC0p25to0p25_amp30\merged_data'
os.chdir(path1)
stress_data1 = pd.read_csv("stress_data.csv")

path2 = r'E:\CyclicLoading\Cyclicmean_OneWay\TX270_FC0p25to0p25_amp30_rate1000\merged_data'
os.chdir(path2)
stress_data2 = pd.read_csv("stress_data.csv")

# Calculating cycle length 
step_interval = stress_data1.step_s[1]-stress_data1.step_s[0]
period = 0.25
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))
quarter_cycle_steps = int(cycle_length/(step_interval*4))
quarter_cycle_time = time_step/(cycle_length*4)

# Figure 
n1 = 0
n2 = 12
plt.figure(figsize = (12,7))
plt.plot(stress_data1.step_s[quarter_cycle_steps*n1:quarter_cycle_steps*n2]*time_step, 
         stress_data1.stress_xx[quarter_cycle_steps*n1:quarter_cycle_steps*n2]/1000, 
         color = 'black', 
         lw = lw1,
         label = r"$\sigma'_{xx}$",
         marker = 'x',
         markevery = quarter_cycle_steps,
         ms = 9)

plt.plot(stress_data1.step_s[quarter_cycle_steps*n1:quarter_cycle_steps*n2]*time_step, 
         stress_data1.stress_yy[quarter_cycle_steps*n1:quarter_cycle_steps*n2]/1000,
         color = 'navy',
         lw = lw1,
         label = r"$\sigma'_{yy}$")

plt.plot(stress_data1.step_s[quarter_cycle_steps*n1:quarter_cycle_steps*n2]*time_step, 
         stress_data1.stress_zz[quarter_cycle_steps*n1:quarter_cycle_steps*n2]/1000, 
         color = 'darkgreen',
         lw = lw1,
         label = r"$\sigma'_{zz}$")

#plt.plot(stress_data2.step_s[quarter_cycle_steps*n1:quarter_cycle_steps*n2]*time_step, 
#        stress_data2.stress_zz[quarter_cycle_steps*n1:quarter_cycle_steps*n2]/1000, 
#         color = 'darkgreen',
#         lw = lw1,
#         label = r"$\sigma'_{zz}$")

ax = plt.gca()
# H lines
ax.hlines(330,0,cycle_length*4*time_step, ls = '--', color = 'black')
ax.hlines(360,0,cycle_length*4*time_step, ls = '--', color = 'black')

# Position 0 
plt.plot(0, 330, marker = 'o', mec = 'black', color = 'orange')
plt.plot(0.25, 330, marker = 'o', mec = 'black', color = 'orange')
plt.plot(0.5, 330, marker = 'o', mec = 'black', color = 'orange')
# Position 1
plt.plot(0+0.25/4, 360, marker = 'o', mec = 'black', color = 'lightblue')
plt.plot(0.25+0.25/4, 360, marker = 'o', mec = 'black', color = 'lightblue')
# Position 2
plt.plot(0+0.25*2/4, 330, marker = 'o', mec = 'black', color = 'purple')
plt.plot(0.25+0.25*2/4, 330, marker = 'o', mec = 'black', color = 'purple')
# position 3
plt.plot(0+0.25*3/4, 300, marker = 'o', mec = 'black', color = 'lightgreen')
plt.plot(0.25+0.25*3/4, 300, marker = 'o', mec = 'black', color = 'lightgreen')

ax.annotate('', xy=(0.25/4, 360), xytext=(0.25/4, 330),
            arrowprops=dict(arrowstyle="->", facecolor='black', lw = 2))

ax.annotate('', xy=(0.25*3/4, 330), xytext=(0.25*3/4, 300),
            arrowprops=dict(arrowstyle="<-", facecolor='black', lw = 2))

ax.text(0.25/4, 345, r"$+\sigma_{zz}'^{ampl}$", fontsize = TXS, va = 'center')
ax.text(0.25*3/4, 315, r"$-\sigma_{zz}'^{ampl}$", fontsize = TXS, va = 'center')
ax.text(0.345, 332, r"mean stress in the z-direction ($\sigma_{zz}'^{av}$)", fontsize = TXS-2, va = 'bottom', bbox=dict(boxstyle='square, pad = 0.1', fc='white', ec='none'))
#ax.text(0.345, 362, r"maximum stress in the z-direction ($\sigma_{zz}'^{max}$)", fontsize = TXS-2, va = 'bottom', bbox=dict(boxstyle='square, pad = 0.1', fc='white', ec='none'))
ax.text(0.345, 298, r"initial mean effective stress ($p'_0$)", fontsize = TXS-2, va = 'top', bbox=dict(boxstyle='square, pad = 0.1', fc='white', ec='none'))

    
plt.xlabel("Time [s]", fontsize = LBF)
plt.ylabel("Stress [kPa]", fontsize = LBF)

x = np.arange(0,0.75,0.25/4)
ax.set_xticks(x)
ax.xaxis.set_major_formatter('{x:0.3f}')

ax.set_yticks(np.arange(180,420, 30))
ax.tick_params(axis='x', rotation=90)

plt.ylim(210,390)
plt.xlim(0,cycle_length*2*time_step)

# Legends 
l1 = plt.legend(loc = 'lower right', fontsize = LGF) 

custom_lines = [Line2D([0], [0], marker = 'o', mec = 'black', color = 'orange', ls = '', label = 'Position 1'),
                Line2D([0], [0], marker = 'o', mec = 'black', color = 'lightblue', ls = '', label = 'Position 2'),
                Line2D([0], [0], marker = 'o', mec = 'black', color = 'purple', ls = '', label = 'Position 3'),
                Line2D([0], [0], marker = 'o', mec = 'black', color = 'lightgreen', ls = '', label = 'Position 0')]
l2 = ax.legend(handles=custom_lines, loc='lower left', fontsize = LGF)
ax.add_artist(l1)

plt.grid( which='both')
plt.tick_params(axis='both', which='major', labelsize=TS)
plt.tight_layout()
plt.show()
