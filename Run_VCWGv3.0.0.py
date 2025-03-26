"""
Run VCWG for one month
Developed by Mojtaba Safdari and Amir A. Aliabadi
Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada
Last update: March 2025
Set the desired month by modifying the `month_number` variable below.
Example: `month_number = 1` runs the simulation for January.
"""

from VCWG_Smart import VCWG_Smart
from UpdateInitialParam import update_uwg_files
from datetime import datetime

'''
Modifying the 12 initialization files:
Any variable inside the .uwg file can be modified.

Instructions:
1. Uncomment the two lines of code below.
2. Replace the variable name "SmartHumidistat" with the desired variable
    (must match the variables inside the initialization files, e.g., initialize_Toronto_1.txt).
3. Change the variable value as needed (e.g., from "1" to "2").
4. Set a debug point at the `epwFileName` line and debug the code.
5. This will update all 12 initialization files accordingly.
6. Once modifications are confirmed, uncomment the two lines again to run the code.

file_names = [f'initialize_Toronto_{i}.uwg' for i in range(1, 13)]
update_uwg_files('resources/Parameters', file_names, 'SmartHumidistat', '1')
'''

# Define month names and their corresponding three-letter abbreviations
month_abbreviations = {
    1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"
}

# Automatically generate file names based on city and year
city = "Toronto"                                              # Define the city name
year = 2020                                                   # Define the year
month_number = 6                                              # Specify the month number (1-12)

Month_name = month_abbreviations[month_number]                # Get the three-letter abbreviation for the selected month
Months = [f"{Month_name}.txt"]                                # Create the list with the month filename

epwFileName = f'ERA5-{city}-{year}.epw'                       # EPW weather file
TopForcingFileName = None                                     # No top forcing file
VCWGParamFileName = f'initialize_{city}_{month_number}.uwg'   # Initialization file name
ViewFactorFileName = f'ViewFactor_{city}_MOST.txt'            # View factor file
case = city                                                   # Case name for output file naming

# Get current date and time for unique output naming
now = datetime.now()
date_str = now.strftime("%Y-%m-%d_%H-%M")

# Initialize the UWG object and run the simulation
VCWG = VCWG_Smart(epwFileName, TopForcingFileName, VCWGParamFileName,
                  ViewFactorFileName, case, Month_name, date_str)
VCWG.run()

