# Calculate required Dump file
import numpy as np

cyc_pos = 3 # 0 starting, 1 loaded, 2 neutural or 3 unloaded
cycle_n = [0,1,2,3,4,5,10,20,30,40,50] # reminder one more than acctual wanted number

time_step =  5.24231e-09 #5.242309e-09#3.187880e-09#5.242309e-09
period = 0.25
cycle_length = round(period/(time_step*4))
print(cycle_length)
cycle_length = 11922227
dump_array = []
for i in range(len(cycle_n)):
    wanted_dumps = cycle_length*cyc_pos + cycle_length*4*cycle_n[i]
    dump_array = np.append(dump_array, wanted_dumps)
print(np.uintc(dump_array))

print(11922227*4)
