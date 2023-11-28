"""
Author: Tara Sassel
Date: 28/10/2022

Figure that explains CSL
"""
import os
import math
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import patches

def get_e_cs(p):
    """
    Critical State Equation
    """
    e_cs = Gamma - lambda1*math.log(p, np.e)
    return e_cs

# ==============================================================================
Gamma = 0.63
lambda1 = 0.000923

# Define CSL
p_values = np.arange(100,500,10)
e_cs = [get_e_cs(p) for p in p_values]
ln_p_cs = [math.log(p, np.e) for p in p_values]

# Point above CSL
p_250 = 250
e0_250 = 0.6252
e_cs_250 = get_e_cs(p_250)
ln_p_250 = math.log(p_250, np.e)

print(np.e**(-(e0_250-Gamma)/lambda1))

# Point below CSL
p_150 = 150
e0_150 = 0.6252
e_cs_150 = get_e_cs(p_150)
ln_p_150 = math.log(150, np.e)

# This is is 100 but I will label it as 1kPa
p_100 = 100
e_cs_100 = get_e_cs(p_100)
ln_p_100 = math.log(100, np.e)

# ==============================================================================
# Figure
plt.plot(1,1)
plt.plot(ln_p_cs, e_cs, color = 'black', lw = 2) # CSL
plt.plot(ln_p_250, e0_250, color = 'black', ls = '', marker = 'o') # Psi > 0
plt.vlines(ln_p_250, e_cs_250, e0_250, ls = ':', lw = 1, color = 'black')
plt.plot(ln_p_150, e0_150, color = 'black', ls = '', marker = 'o') # Psi > 0
plt.vlines(ln_p_150, e_cs_150, e0_150, ls = ':', lw = 1, color = 'black')

plt.vlines(ln_p_100, 0.624, e_cs_100, ls = ':', lw = 1, color = 'black')
plt.hlines(e_cs_100, 4.25, ln_p_100, ls = ':', lw = 1, color = 'black')
plt.hlines(get_e_cs(400), math.log(400, np.e), 5.7, ls = ':', lw = 1, color = 'black')
plt.hlines(e0_150,ln_p_150,ln_p_250, ls = ':', lw = 1, color = 'black')
# Angle
point1 = [math.log(360, np.e), get_e_cs(400)]
point2 = [math.log(360, np.e), get_e_cs(360)]

def arch_line(point1, point2):
    range1 = np.linspace(0,-0.01,50)
    range2 = np.linspace(-0.01,0,50)
    range = np.append(range1,range2)
    x = np.linspace(point1[0], point2[0], 100) + range
    y = np.linspace(point1[1], point2[1], 100)
    return (x,y)

x,y = arch_line(point1, point2)
plt.plot(x,y, color = 'black')

# Annotations
plt.text(4.21, e_cs_100, '$\Gamma$', va = 'center', ha = 'center', fontsize = 12)
plt.text(ln_p_100, 0.6239, '1kPa', va = 'center', ha = 'center', fontsize = 12)
plt.text(6,0.62450, "CSL", fontsize = 12)
plt.text(ln_p_250+0.1, e_cs_250 + (e0_250-e_cs_250)/2, "$\psi > 0$", color = 'black', fontsize = 12)
plt.text(ln_p_150-0.25, e0_150 + (e_cs_150-e0_150)/2, "$\psi < 0$", color = 'black', fontsize = 12)
plt.text(5.8, 0.62455, "$\lambda$", fontsize = 12, va = 'center', ha = 'center')

# Label Axis
plt.xlabel("$ln(p')$", fontsize = 14)
plt.ylabel("Void Ratio $(e)$", fontsize = 14)
plt.xlim(4.25,6.5)
plt.ylim(0.624,0.62625)

plt.gca().get_xaxis().set_ticks([])
plt.gca().get_yaxis().set_ticks([])

# Hide the right and top spines
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['top'].set_visible(False)
plt.tight_layout()
os.chdir(r'C:\Users\shrab\Google Drive\PhD\PhDFigures')
plt.savefig('CSL_StateParameter.png')
plt.savefig('CSL_StateParameter.eps', format='eps')
plt.show()
