import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from basicFunctions.get_strain import get_strain


# ==============================================================================
# Defining Path
drive = 'E'
path_300_15 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp15\merged_data'
path_300_20 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp20\merged_data'
path_300_30 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp30\merged_data'
path_300_60 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp60\merged_data'
path_300_90 = rf'{drive}:\CyclicLoading\Cyclicmean\TX300_FC0p25to0p25_amp90\merged_data'

path_list = [path_300_15, path_300_20, path_300_30, path_300_60, path_300_90]
color_list = ['#f0f9e8', '#bae4bc', '#7bccc4', '#43a2ca', '#0868ac']
# Defining Labels
label_list = [
    '15',
    '30',
    '30',
    '60',
    '90']
# ==============================================================================
# Define Plot Fontsizes
TF = 24     # Text font
LGF = 12   # Legend Font Size
LBF = 15    # Label Font Size
TS = 12     # Tick Size
lw1 = 2     # Line Width
# ==============================================================================
# Calculating cycle length
time_step = 5.242309e-09
period = 0.25
cycle_length = int(period/(time_step))

wanted_cycles = np.arange(0,51).astype(float)
wanted_stepsL = [cycle*cycle_length + cycle_length/4 for cycle in wanted_cycles]
wanted_stepsU = [cycle*cycle_length + 3*cycle_length/4 for cycle in wanted_cycles]
# ==============================================================================
for p, path in enumerate(path_list):
    os.chdir(path)
    strain_data = pd.read_csv('stress_data.csv')

    step_s = strain_data.step_s.to_numpy().T
    length_z = strain_data.length_z.to_numpy().T
    zstrain = get_strain(length_z)

    wanted_indexL = []
    for step in wanted_stepsL:
        wanted_indexL.append(np.argmax(step_s>=step))
    wanted_indexU = []
    for step in wanted_stepsU:
        wanted_indexU.append(np.argmax(step_s>=step))

    wanted_strainL = zstrain[wanted_indexL]
    wanted_stepsL = step_s[wanted_indexL]
    wanted_strainU = zstrain[wanted_indexU]
    wanted_stepsU = step_s[wanted_indexU]

    strain_amp = np.abs(wanted_strainL-wanted_strainU)
    plt.figure(1)
    plt.plot(
        wanted_cycles ,
        (strain_amp/100)*1000,
        marker = 'o',
        mec = 'k',
        color = color_list[p],
        label = label_list[p])

plt.legend(loc = 'upper right', title = "$\sigma'_1^{ampl} [kPa] =$", fontsize = LGF)
plt.xlabel('Cycle Number (N)', fontsize = LBF)
plt.ylabel('Strain amplitude ($\epsilon^{ampl}$) [$10^{-4}$]', fontsize = LBF)
plt.grid(ls = '--', lw = 1, color = 'gray')
plt.gca().tick_params(which = 'major', labelsize = TS)
plt.show()
