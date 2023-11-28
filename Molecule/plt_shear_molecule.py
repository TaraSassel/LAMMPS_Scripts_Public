# See othe script called plot_stress_strain_loops.py

import os
import pandas as pd 
import matplotlib.pyplot as plt 
from basicFunctions.get_strain import get_strain
from basicFunctions.get_qp import get_qp

LBF = 16
LGF = 16
TS = 12

apsect_ratios = [1,2,3,4]
colors = ['green','gold','darkorange','orangered']

plt.figure(figsize=(10,5))

for i, ar in enumerate(apsect_ratios):
    path = rf'E:\Molecules\ShearingMolecule\Shear_AR1p{ar}_FC0p25_ISO200\merged_data'
    os.chdir(path)

    stress_data = pd.read_csv('stress_data.csv')
    length_z = stress_data.length_z.to_numpy()
    q,p = get_qp(stress_data)
    epsz = get_strain(length_z)

    plt.plot(epsz, q/1000, label = rf'AR = 1.{ar}', lw = 2, c = colors[i])

plt.ylim(0,350)
plt.xlim(0,)
plt.xlabel(r'Axial strain ($\varepsilon_{zz}$) [%]', fontsize = LBF)
plt.ylabel(r'Deviatoric stress ($q$) [kPa]', fontsize = LBF)
plt.legend(loc = 'lower right')
plt.gca().tick_params(axis='both', which='major', labelsize=TS)
plt.grid(ls = '--', color = 'gray')
plt.show()