"""
Run VCWG for 12 months using serial processing
Developed by Mojtaba Safdari and Amir A. Aliabadi
Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada
Last update: March 2025
More time-consuming compared to the parallel script.
Uses less CPU resources as it runs the simulations sequentially.
"""

from VCWG_Smart import VCWG_Smart
from datetime import datetime
from UpdateInitialParam import update_uwg_files

'''
Modifying the 12 initialization files:
Any variable inside the .uwg file can be modified.
Instructions:
1. Uncomment the two lines of code below.
2. Replace the variable name "SmartHumidistat" with the desired variable
    (must match the variables in the initialization files, e.g., initialize_Toronto_1.txt).
3. Change the variable value as needed (e.g., from "1" to "2").
4. Set a debug point at the `epwFileName` line and debug the code.
5. This will update all 12 initialization files accordingly.
6. Once modifications are confirmed, uncomment the two lines again to run the code.

file_names = [f'initialize_Toronto_{i}.uwg' for i in range(1, 13)]
update_uwg_files('resources/Parameters', file_names, 'SmartHumidistat', '1')
'''

# Define the city name and year (modify to change the city or year)
city = "Toronto"
year = 2020

# Automatically generate file names based on the city and year
epwFileName = f'ERA5-{city}-{year}.epw'                       # EPW weather file
TopForcingFileName = None                                     # No top forcing file
ViewFactorFileName = f'ViewFactor_{city}_MOST.txt'            # View factor file
case = city                                                   # Case name for output file naming
initialization_name = f'initialize_{city}'                    # Initialization file prefix

# List of month file names
Months = ['Jan.txt', 'Feb.txt', 'Mar.txt', 'Apr.txt', 'May.txt', 'Jun.txt',
          'Jul.txt', 'Aug.txt', 'Sep.txt', 'Oct.txt', 'Nov.txt', 'Dec.txt']

# Get current date and time for unique output naming
now = datetime.now()
date_str = now.strftime("%Y-%m-%d_%H-%M")

# Loop through all 12 months
for i in range(1, 13):
    Month_name = Months[i - 1].split('.')[0]                  # Extract month name
    VCWGParamFileName = f'{initialization_name}_{i}.uwg'      # Auto-generate file name

    # Run simulation
    VCWG = VCWG_Smart(epwFileName, TopForcingFileName, VCWGParamFileName,
                      ViewFactorFileName, case, Month_name, date_str)
    VCWG.run()

