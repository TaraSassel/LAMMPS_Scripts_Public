"""
Author: Tara Sassel
Date: 14/01/2023

This code is to create a plot that shows an example of earth pressures,
as predicted by design codes
"""

# ========================================================================
# IMPORTS
import numpy as np 
import matplotlib.pyplot as plt 

# ========================================================================
# Define Plot Fontsizes
LGF = 10   # Legend Font Size
LBF = 12    # Label Font Size
TS = 10     # Tick Size
lw1 = 1
# ========================================================================
depth = np.arange(0,5.01,0.1) # Up to a depth of 5m
phi = 30 * np.pi / 180
sh1 = 0.05
sh2 = 0.02
sh3 = 0.03

# ========================================================================
# CALCULATIONS
sigma_v = 20.5*depth

# Earth pressure at rest
K0 = 1 - np.sin(phi)
sigma_0 = sigma_v * K0

# Active earth pressure
Ka = (1 - np.sin(phi))/(1 + np.sin(phi))
sigma_a = sigma_v * Ka

# Passive earth pressure 
Kp = (1 + np.sin(phi))/(1 - np.sin(phi))
sigma_p = sigma_v * Kp

# German code
alpha = 0.02
Kph = -2/3 * phi

vz1 = (5 - depth)*np.tan(np.arctan(sh1/5))
Kph_mob1 = K0 + (Kp - K0) * ((vz1/depth)/(alpha + (vz1/depth)))
sigma_g1 = sigma_v * Kph_mob1

vz2 = (5 - depth)*np.tan(np.arctan(sh2/5))
Kph_mob2 = K0 + (Kp - K0) * ((vz2/depth)/(alpha + (vz2/depth)))
sigma_g2 = sigma_v * Kph_mob2

vz3 = (5 - depth)*np.tan(np.arctan(sh3/5))
Kph_mob3 = K0 + (Kp - K0) * ((vz3/depth)/(alpha + (vz3/depth)))
sigma_g3 = sigma_v * Kph_mob3

# BA42
d2 = sh3 # displacemnet for second figure
Kstar = ((d2/(sh3*5))**0.4)*Kp;
sigma_BA42 = sigma_v * Kstar

for i in np.arange(26,len(depth)):
    if sigma_BA42[i]> sigma_0[i]:
        sigma_BA42[i] = sigma_BA42[25]
    if sigma_BA42[i]< sigma_0[i]:
        sigma_BA42[i] = sigma_0[i]

# PD 6494
# C is 20 for foundations on flexible (unconfined) soils with E ? 100 MPa;
# C is 66 for foundations on rock or soils with E ? 1 000 MPa;
# C may be found by linear interpolation for values of E between 100 MPa and 1 000 MPa;

def get_PD6694(sh,C,depth) -> np.array:
    """
    Function to calculate sigma h using PD6694
    """
    K_PD6694= K0 + (C*sh/5)**0.6*Kp

    sigma_PD6694 = np.zeros((len(depth),))

    for i in range(0,26):
        sigma_PD6694[i] = K_PD6694 * sigma_v[i]

    var1 = (sigma_PD6694[25]-sigma_0[-1])/25
    a1 = 1

    for i in range(26,len(depth)):
        sigma_PD6694[i] = sigma_PD6694[25]-a1*var1
        a1 += 1
    
    return sigma_PD6694

# Case 1  C = 20
C1 = 20
sigma_PD6694_1 = get_PD6694(sh3,C1,depth)

# Case 2 C - xx
C2 = 66
sigma_PD6694_2 = get_PD6694(sh3,C2,depth)

# ========================================================================
# FIGURE  1
plt.plot(sigma_0,depth, c = 'black', lw = 2, ls = '--', label = 'Earth pressure at rest')
plt.plot(sigma_a,depth, c = 'black', lw = 2, ls = ':', label = 'Active earth pressure')
plt.plot(sigma_p,depth, c = 'black', lw = 2, ls = '-', label = 'Passive earth pressure')
plt.plot(sigma_g1,depth, c = 'forestgreen', lw = 2, ls = '-', label = 'German design code with $s_h$ = 0.05')
plt.plot(sigma_g2,depth, c = 'navy', lw = 2, ls = '-', label = 'German design code with $s_h$  = 0.02')

plt.xlim(0,)
plt.ylim(0,5)
plt.xlabel("$\sigma_h$ [kPa]", fontsize = LBF)
plt.ylabel("Depth [m]", fontsize = LBF)
plt.legend(loc = 'upper right', fontsize = LGF)

ax = plt.gca()
ax.invert_yaxis()
ax.tick_params(which='major', labelsize=TS)

# ========================================================================
# FIGURE  2 Comparson of diffren design codes
plt.figure(2)
plt.plot(sigma_0,depth, c = 'black', lw = 2, ls = '--', label = 'Earth pressure at rest')
plt.plot(sigma_a,depth, c = 'black', lw = 2, ls = ':', label = 'Active earth pressure')
plt.plot(sigma_p,depth, c = 'black', lw = 2, ls = '-', label = 'Passive earth pressure')
plt.plot(sigma_BA42,depth, c = 'red', lw = 2, ls = '-', label = 'BA42')
plt.plot(sigma_g3,depth, c = 'forestgreen', lw = 2, ls = '-', label = 'German design code')
plt.plot(sigma_PD6694_1,depth, c = 'orange', lw = 2, ls = '-', label = 'PD 6694 C = 20')
plt.plot(sigma_PD6694_2,depth, c = 'orange', lw = 2, ls = ':', label = 'PD 6694 C = 66')
ax = plt.gca()
ax.fill_betweenx(depth, sigma_PD6694_1, sigma_PD6694_2, color = 'orange', alpha = 0.2)

print(sigma_PD6694_1[24:27])
print(sigma_PD6694_2[24:27])

plt.xlim(0,)
plt.ylim(0,5)
plt.xlabel("$\sigma_h$ [kPa]", fontsize = LBF)
plt.ylabel("Depth [m]", fontsize = LBF)
plt.legend(loc = 'upper right', fontsize = LGF)

ax.invert_yaxis()
ax.tick_params(which='major', labelsize=TS)

plt.grid()
plt.show()

