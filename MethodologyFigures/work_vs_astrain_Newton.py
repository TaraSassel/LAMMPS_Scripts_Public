"""
Author: Tara Sassel
Date: 24/01/2023

Figure for qp vs axial strain to compare newton on to newton off
"""
# Imports
import os 
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

from basicFunctions.get_qp import get_qp

# Fonts
TF = 20     # Title Font Size
LGF = 12    # Legend Font Size
LBF = 16    # Label Font Size
TS = 14     # Tick Size
lw1 = 2     # Line width 


# Paths 
path_TX_FC0p1_NOn = r'D:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\TXShear100kPa_fromFC0p1to0p1\merged_data'
path_TX_FC0p1_NOff = r'D:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\NewtonOff\TXShear100kPa_fromFC0p1to0p1\merged_data'

path_TX_FC0p25_NOn = r'D:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\TXShear100kPa_fromFC0p1to0p25\merged_data'
path_TX_FC0p25_NOff = r'D:\PhD_Data_Back_Up\LAMMPS\Random_Packing\TX Shear\NewtonOff\TXShear100kPa_fromFC0p1to0p25\merged_data'

paths = [path_TX_FC0p1_NOn, path_TX_FC0p1_NOff, path_TX_FC0p25_NOn, path_TX_FC0p25_NOff]
label_list = [
    'Newton On with $\mu = 0.1$', 
    'Newton Off with $\mu = 0.1$', 
    'Newton On with $\mu = 0.25$', 
    'Newton Off with $\mu = 0.25$'
    ]
color_list = ['indianred','maroon','lightgreen','forestgreen']
ls_list = ['-','--','-','--']
lw_list = [4,2,4,2]

plt.figure(figsize = (10,5))
for i, path in enumerate(paths):
    print(path)
    os.chdir(path)

    print("Processing Stress Data")
    stress_data = pd.read_csv("stress_data.csv")
    q, p = get_qp(stress_data)

    step_s = stress_data.step_s.to_numpy().T
    time_step = 5.23762e-09
    timeinterval = (step_s[2]-step_s[1])

    # strain
    length_x = stress_data.length_x.to_numpy().T
    length_y = stress_data.length_y.to_numpy().T
    length_z = stress_data.length_z.to_numpy().T
    xstrain = (length_x[0] - length_x)/length_x[0]
    ystrain = (length_y[0] - length_y)/length_y[0]
    zstrain = (length_z[0] - length_z)/length_z[0] 
    xstrain = xstrain*100 # to percentage
    ystrain = ystrain*100 # to percentage
    zstrain = zstrain*100 # to percentage

    # Calculate delta length 
    print("Loop1")
    k = 0
    delta_xx = np.zeros(len(length_x))
    delta_yy = np.zeros(len(length_x))
    delta_zz = np.zeros(len(length_x))
    while k < len(length_x)-1:
        delta_xx[k] =  length_x[k] - length_x[k+1]
        delta_yy[k] =  length_y[k] - length_y[k+1]
        delta_zz[k] =  length_z[k] - length_z[k+1]
        k += 1

    delta_xstrain =delta_xx/length_x    # Not in percentage
    delta_ystrain =delta_yy/length_y    # Not in percentage
    delta_zstrain =delta_zz/length_z    # Not in percentage

    delta_xsrate = delta_xstrain*time_step*timeinterval
    delta_ysrate = delta_ystrain*time_step*timeinterval
    delta_zsrate = delta_zstrain*time_step*timeinterval

    xsrate = np.zeros(len(length_x))
    ysrate = np.zeros(len(length_x))
    zsrate = np.zeros(len(length_x))
    xsrate[0] = delta_xsrate[0]
    ysrate[0] = delta_ysrate[0]
    zsrate[0] = delta_zsrate[0]

    print("Loop2")
    j = 1
    while j < len(length_x)-1:
        xsrate[j] = xsrate[j-1] + delta_xsrate[j]
        ysrate[j] = xsrate[j-1] + delta_ysrate[j]
        zsrate[j] = zsrate[j-1] + delta_zsrate[j]
        j += 1

    qstrain = (2/3)*(zsrate-0.5*(xsrate+ysrate))
    vstrain = (xsrate + ysrate + zsrate)

    print("Processing Energy Data")
    # Energy Data 
    energy_data = pd.read_csv("energy_data.csv")
    
    # Calculation for Boundary Work ------------------------------------------------
    # Convert DataFrame to numpy 
    E_f = energy_data.friE.to_numpy().T    # Frictional Energy
    E_sn = energy_data.normE.to_numpy().T   # Total ormal strain energy
    E_st = energy_data.shearE.to_numpy().T  # Total tangental strain energy
    E_kt = energy_data.tkE.to_numpy().T     # Transitional kinetric energy
    E_kr = energy_data.rkE.to_numpy().T     # Rotational kinetic energy
    E_vol = energy_data.volE.to_numpy().T   # Volumetric Energ
    E_dist = energy_data.distE.to_numpy().T # Distortional energy 

    # Initial Energy Values
    E_sn0 = E_sn[0]         # Initial total normal strain eregry
    E_st0 = E_st[0]         # Initial total tangental strain energy
    E_kt0 = E_kt[0]         # Initial transitional kinetric energy
    E_kr0 = E_kr[0]         # Initial rotational kinetic energy

    # Work 
    W1 = energy_data.boundE.to_numpy().T    # Total boundary work

    W2 = E_vol + E_dist                     # As sum of vol and dist Work
    
    Wv = p*vstrain                          # Calculated from strain 
    Wd = (q*qstrain)
    W3 = Wv + Wd

    # Error in Energy Balance

    dE1 = E_sn0 + E_st0 + E_kt0 + E_kr0 + W1 - E_f - E_sn - E_st - E_kt - E_kr    
    dE2 = E_sn0 + E_st0 + E_kt0 + E_kr0 + W2 - E_f - E_sn - E_st - E_kt - E_kr    
    #dE3 = E_sn0 + E_st0 + E_kt0 + E_kr0 + W3 - E_f - E_sn - E_st - E_kt - E_kr    
    
    W1_error = 100*dE1/W1
    W2_error = 100*dE2/W2

    a1 = len(zstrain)
    a2 = len(W1_error)
    if a1 < a2:
        a = a1
    else:
        a = a2
    # Figure
    plt.plot(zstrain[0:a], W1[0:a], marker = '', markevery= 1000, label = "W1", c = color_list[i], ls = ls_list[i], lw = lw_list[i])
    plt.plot(zstrain[0:a], W2[0:a], marker = 'x', markevery= 1000, label = "W2", c = color_list[i], ls = ls_list[i], lw = lw_list[i])

# Annoate
plt.legend(loc = 'lower right', fontsize = LGF)
plt.xlabel('Axial strain ($\epsilon_{zz}$) [%]', fontsize = LBF)
plt.ylabel('Error in energy balance[%]', fontsize = LBF)
plt.xlim(0,5)
plt.ylim(0,)

ax = plt.gca()

# Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

# make arrows
ax.plot((1), (0), ls="", marker=">", ms=10, color="k",
        transform=ax.get_yaxis_transform(), clip_on=False)
ax.plot((0), (1), ls="", marker="^", ms=10, color="k",
        transform=ax.get_xaxis_transform(), clip_on=False)

plt.tick_params(axis='both', which='major', labelsize=TS)
plt.show()