import numpy as np 
import matplotlib.pyplot as plt 
from matplotlib.ticker import (MultipleLocator)


color_list = ['orange', 'mediumpurple', 'cyan', 'orangered', 'indigo']
label_list = [
    "TXCC with $\sigma'_{zz}^{ampl}$ = 30kPa", 
    "TXCC with $\sigma'_{zz}^{ampl}$ = 60kPa",
    "TXCC with $\sigma'_{zz}^{ampl}$ = 90kPa",
    "TXCE with $\sigma'_{zz}^{ampl}$ = 30kPa",
    "TXCE with $\sigma'_{zz}^{ampl}$ = 60kPa"
]
      

plt.plot(10,7)
ax = plt.gca()
#ax.spines['left'].set_position('left')
ax.spines['bottom'].set_position('center')
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')



circle1 = plt.Circle((330, 0), radius=30, edgecolor = color_list[0], fill = False, label = label_list[0] )
circle2 = plt.Circle((360, 0), radius=60, edgecolor = color_list[1], fill = False, label = label_list[1] )
circle3 = plt.Circle((390, 0), radius=90, edgecolor = color_list[2], fill = False, label = label_list[2] )

circle1e = plt.Circle((270, 0), radius=30, edgecolor = color_list[3], fill = False, label = label_list[3] )
circle2e = plt.Circle((240, 0), radius=60, edgecolor = color_list[4], fill = False, label = label_list[4] )

ax.add_artist(circle1)
ax.add_artist(circle2)
ax.add_artist(circle3)

ax.add_artist(circle1e)
ax.add_artist(circle2e)

x = np.arange(0,600,1)
slope = np.tan(18*np.pi/180)
y = x*slope

plt.plot(x,y, lw = 1, ls = '-', color = 'black')

plt.xlim(0,600)
plt.ylim(-200,200)
ax.set_xticks(np.arange(100,700,100))
ax.xaxis.set_major_locator(MultipleLocator(100))
ax.set_xlabel(r'$\sigma$ [kPa]', fontsize=16, loc="right")
ax.set_ylabel(r'$\tau$ [kPa]', fontsize=16, rotation = 90)
ax.set_aspect( 1 )

plt.legend(loc = 'lower left', fontsize = 8)
plt.tight_layout()
plt.show()
