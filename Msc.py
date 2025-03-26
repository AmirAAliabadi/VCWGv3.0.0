##there are some figures in this script that may have been commented the first one was setpointsetback and now the inputs

import numpy as np
import matplotlib.pyplot as plt
from skfuzzy import trimf

# Define the universe
# universe = np.arange(-1, 1, 0.01)
#
# # Define the membership functions
# NSSet = trimf(universe, [-1, -1, 0])
# ZSet = trimf(universe, [-0.25, 0, 0.25])
# PSSet = trimf(universe, [0, 1, 1])
#
# # Create the plot
# plt.figure(figsize=(8, 6))
# plt.plot(universe, NSSet, label='N', linewidth=2.5)
# plt.plot(universe, ZSet, label='Z', linewidth=2.5, linestyle='-.')
# plt.plot(universe, PSSet, label='P', linewidth=2.5, linestyle=':')
# plt.xlabel('w [-]', fontsize=14)
# plt.ylabel('Membership Grade of w', fontsize=14)
# plt.legend(loc='lower right', fontsize=14)
# plt.show()


# ########
#summer
# import numpy as np
# import matplotlib.pyplot as plt
# from skfuzzy import trapmf
#
# # Define the universe
# universe = np.arange(0, 24, 1)
#
# # Define the membership functions
# low = np.maximum(trapmf(universe, [0, 0, 7, 7]), trapmf(universe, [19, 19, 24, 24]))
# high = np.maximum(trapmf(universe, [7, 7, 11, 11]), trapmf(universe, [17, 17, 19, 19]))
# medium = trapmf(universe, [11, 11, 17, 17])
#
# # Create the plot
# plt.figure(figsize=(8, 6))
# plt.plot(universe, low, label='Low(Off-peak)', linewidth=3, linestyle='-.')
# plt.plot(universe, medium, label='High(On-peak)', linewidth=3)
# plt.plot(universe, high, label='Medium(Mid-peak)',  linewidth=3, linestyle=':')
# plt.xlabel('Time of Day [hr]', fontsize=14)
# plt.ylabel('Membership Grades of Electricity Price (Summer)', fontsize=14)
# plt.legend(loc='center left', fontsize=14)
# # plt.grid()
# plt.show()
######################################


#Price2
# import numpy
# import matplotlib.pyplot as plt
# from skfuzzy import trapmf
#
# # Define the universe
# universe = numpy.arange(0, 24, 1)
#
# # Define the membership functions for Winter TOU
# off_peak = numpy.maximum(trapmf(universe, [0, 0, 7, 7]), trapmf(universe, [19, 19, 24, 24]))
# mid_peak = trapmf(universe, [11, 11, 17, 17])
# on_peak = numpy.maximum(trapmf(universe, [7, 7, 11, 11]), trapmf(universe, [17, 17, 19, 19]))
#
# A=numpy.NaN
# print(A)
#
# # Create the plot
# plt.figure(figsize=(8, 6))
# plt.plot(universe, off_peak, label='Low(Off-peak)', linewidth=3, linestyle='-.')
# plt.plot(universe, on_peak, label='High(On-peak)', linewidth=3)
# plt.plot(universe, mid_peak, label='Medium(Mid-peak)', linewidth=3, linestyle=':')
# plt.xlabel('Time of Day [hr]', fontsize=14)
# plt.ylabel('Membership Grades of Electricity Price (Winter)', fontsize=14)
# plt.legend(loc='center left', fontsize=14)
# # plt.grid()
# plt.show()









##########
# import numpy as np
# import matplotlib.pyplot as plt
# from skfuzzy import trapmf, trimf
#
# # Define the universe
# universe = np.arange(0, 0.05, 0.001)
#
# # Define the membership functions
# low = trapmf(universe, [0, 0, 0.01, 0.02])
# medium = trimf(universe, [0.01, 0.02, 0.03])
# high = trapmf(universe, [0.02, 0.03, 0.05, 0.05])
#
# # Create the plot
# plt.figure(figsize=(8, 6))
# plt.plot(universe, low, label='Low', linewidth=2.5, linestyle='-.')
# plt.plot(universe, medium, label='Medium', linewidth=2.5, linestyle='-.')
# plt.plot(universe, high, label='High', linewidth=2.5)
# plt.xlabel('Occupancy [Person m⁻²]', fontsize=14)
# plt.ylabel('Membership Grades of Occupancy', fontsize=14)
# plt.xlim(0, 0.05)  # Limit x-axis to 0.05
# plt.legend(loc='center right', fontsize=14)
# plt.show()








##########################################################
#SetpointSetback
# import matplotlib.pyplot as plt
#
# # Set the y-values for the horizontal lines
# y_values = [1, 2, 3, 4]
#
# # Create a plot
# plt.figure()
#
# # Fill the background color for each specified range
# plt.fill_between(x=[0, 10], y1=0, y2=1, color='darkblue', alpha=0.7)
# plt.fill_between(x=[0, 10], y1=1, y2=2, color='deepskyblue', alpha=0.7)
# plt.fill_between(x=[0, 10], y1=2, y2=3, color='green', alpha=0.7)
# plt.fill_between(x=[0, 10], y1=3, y2=4, color='orange', alpha=0.7)
# plt.fill_between(x=[0, 10], y1=4, y2=5, color='darkred', alpha=0.7)
#
# # Plot horizontal lines
# for y in y_values:
#     plt.axhline(y=y, color='black', linestyle='-', linewidth=.5)
#
# # Add text labels
# plt.text(.2, 4, 'HighHigh (HH) Setback Criteria', color='white', fontsize=15, verticalalignment='center')
# plt.text(.2, 3, 'High (H) Setpoint Criteria', color='white', fontsize=15, verticalalignment='center')
# plt.text(.2, 2, 'Low (L) Setpoint Criteria', color='white', fontsize=15, verticalalignment='center')
# plt.text(.2, 1, 'LowLow (LL) Setback Criteria', color='white', fontsize=15, verticalalignment='center')
#
# # Add a vertical line with a multi-line label
# plt.axvline(x=10, color='black', linestyle='--', linewidth=2)
# plt.text(10.5, 2.5, 'Seasonal\nComfort\nZone', fontsize=15, color='black', verticalalignment='center', horizontalalignment='left')
# plt.text(10.5, 1.5, 'Setback\nZone', fontsize=15, color='black', verticalalignment='center', horizontalalignment='left')
# plt.text(10.5, 3.5, 'Setback\nZone', fontsize=15, color='black', verticalalignment='center', horizontalalignment='left')
# plt.text(10.5, 4.5, 'Unacceptable\nZone', fontsize=15, color='black', verticalalignment='center', horizontalalignment='left')
# plt.text(10.5, .5, 'Unacceptable\nZone', fontsize=15, color='black', verticalalignment='center', horizontalalignment='left')
# # Set the limits for x-axis
# plt.xlim(0, 15)
#
# # Set the limits for y-axis to cover all lines with some padding
# plt.ylim(0, 5)
#
# # Remove x and y ticks
# plt.xticks([])
# plt.yticks([])
#
# # Add labels and title
# plt.ylabel('Temperature/Humidity', fontsize=14)
#
# # Display the plot
# plt.show()
