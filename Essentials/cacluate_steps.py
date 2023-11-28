"""
Author: Tara Sassel
Data: 18/11/2022
This some basic script that calculates the steps
required for strain controlled cyclic loading.
Please, replace the values as required.
"""

Velocity = 0.001
TimeStep = 5.242*10**(-9)
SampleLength = 5.80918*10**(-3)
Strain = 1 # Percentage of strain

# Number of steps required to reach x% strain
Steps = (SampleLength*Strain)/(100*TimeStep*Velocity)
print(Steps)

cyclic_turns = 11081992 # Define number of steps for simulation
print(cyclic_turns/2) # Half cycle required for dump file

# Double checking if it really gives x% strain
strain = (TimeStep*Velocity*cyclic_turns)/(SampleLength)*100
print(strain)
