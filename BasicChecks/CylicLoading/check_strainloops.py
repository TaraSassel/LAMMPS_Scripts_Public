import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import seaborn as sns

from basicFunctions.get_strain import get_strain

path = r'F:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp20\merged_data'
os.chdir(path)

strain_amp = 1.0    # Strain Amplitude
N = 51             # Number of cycles

# Fontisze
LBF = 16    # Label Fontsize
TS = 12     # Ticksize
CBF = 14    # Colorbar Font

# if strain_amp == 0.1:
#     cylic_steps = 1113698*2 # 0.1
# if strain_amp == 0.5:
#     cylic_steps = 5568485*2 # 0.5
# if strain_amp == 1:
#     cylic_steps = 11136970*2 # 1

# Calculating cycle length
time_step = 5.242309e-09
period = 0.25
cylic_steps = int(period/(time_step))
cylic_steps = 11922227*4

# Load Data
stress_data = pd.read_csv('stress_data.csv')

# Adapt Data
stress_data['strain_z'] = get_strain(stress_data['length_z'])
stress_data['cycle_number'] = stress_data.step_s/cylic_steps
stress_data['cycle_number'] = stress_data['cycle_number'].round()

print(stress_data['cycle_number'])

# Figure
fig = plt.figure(figsize = (10,7))
color_list = cm.bone(np.linspace(0, 1, N))

cycle_number_list = list(stress_data['cycle_number'].unique())
for i, number in enumerate(cycle_number_list):
    if number < N:
        print(number)
        cycle_data = stress_data[stress_data['cycle_number'] == number]
        plt.plot(cycle_data['strain_z'],cycle_data['stress_zz']/1000, c = color_list[i])

#plt.axvline(strain_amp, ls = '--', color = 'indianred')

# Colorbar
sm = plt.cm.ScalarMappable(cmap=cm.bone, norm=plt.Normalize(vmin=0, vmax=N))
cb = plt.colorbar(sm)
cb.ax.tick_params(labelsize=TS)
cb.set_label('Cycle Number (N)', fontsize = CBF)

# Limit
#plt.ylim(100,600)

# Labels
plt.ylabel('Stress [kPa]', fontsize = LBF)
plt.xlabel('Strain [%]', fontsize = LBF)
plt.tick_params(axis='both', which='major', labelsize=TS)

plt.show()
