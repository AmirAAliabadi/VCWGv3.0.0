import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Load the Excel file and choose the sheet to read
file_path = r"C:\Users\Moji\Dropbox\PHD\Codes\Smart VCWG\VCWGv3.0.0-main\Codes\Results\2024-11-19_14-26_T1H1New_15\output_2024-11-19_14-26_T1H1New_T1H1New.xlsx"
###########################################################################################################
###########################################################################################################
######################################July#####################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################
# # # ##############################################################################################################################Jul
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Load the Excel file and choose the sheet to read
file_path = r"C:\Users\Moji\Dropbox\PHD\Codes\Smart VCWG\VCWGv3.0.0-main\Codes\Results\2024-11-19_14-26_T1H1New_15\output_2024-11-19_14-26_T1H1New_T1H1New.xlsx"
sheet_name = 'Jul'  # Replace with your specific sheet name
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Create a figure and two subplots, vertically aligned
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True, gridspec_kw={'height_ratios': [1, 1]})

# --------------------------------
# First Plot: July Temperature Profile
# --------------------------------
# Define the x-axis column and the columns you want to plot
x_column = 'Hour [hr]'
columns_to_plot_1 = [
    'Indoor Temperature [K]',
    'Outdoor Temperature [K]',
    'Heating HH Setpoint [K]',
    'Heating H Setpoint [K]',
    'Heating L Setpoint [K]',
    'Heating LL Setpoint [K]',
    'Cooling HH Setpoint [K]',
    'Cooling H Setpoint [K]',
    'Cooling L Setpoint [K]',
    'Cooling LL Setpoint [K]'
]

# Define custom labels for the first two plotted lines
custom_labels_1 = [
    'Indoor Temp [°C]',
    'Outdoor Temp [°C]'
]

# Plot each column on ax1 with custom labels
colors = ['purple', 'darkgreen', 'red', 'red', 'red', 'red', 'blue', 'blue', 'blue', 'blue']
line_styles = ['-', '--', ':', ':', ':', ':', ':', ':', ':', ':']
line_widths = [2, 2, 1, 1, 1, 1, 1, 1, 1, 1]

for i, column in enumerate(columns_to_plot_1):
    if column in data.columns:
        # Use custom labels from the custom_labels list for the first two lines
        label = custom_labels_1[i] if i < 2 else None
        ax1.plot(data[x_column], data[column] - 273.15, color=colors[i],
                 label=label, linewidth=line_widths[i], linestyle=line_styles[i])

# Set labels and limits for the first plot
ax1.set_xlim(0, 400)
ax1.set_ylabel("Temperature [°C]", fontsize=15)
ax1.grid(alpha=0.3)

# Display the legend for the first two lines only
ax1.legend(fontsize=12)

# Add annotations
ax1.text(405, 29.8, 'HH', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='blue', edgecolor='black', boxstyle='round,pad=0.3'))
ax1.text(405, 26.9, 'H', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='blue', edgecolor='black', boxstyle='round,pad=0.3'))
ax1.text(405, 23.9, 'L', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='blue', edgecolor='black', boxstyle='round,pad=0.3'))
ax1.text(405, 20.9, 'LL', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='blue', edgecolor='black', boxstyle='round,pad=0.3'))

# Add rectangles and annotations
annotation_coords = [
    (90, 23, 'Indoor Temp. Converges to\nOutdoor and stops\nat L due to High Occupancy', (70, 17)),
    (113, 23, 'Indoor Temp. Converges to\nOutdoor and stops\nat L due to High Occupancy', (70, 17)),
    (124, 27, 'Indoor Temp. is Allowed to\nConverge to Outdoor Temp to HH\nDue to Low Occupancy', (15, 34.5))
]

for rect_x, rect_y, text, xy_text in annotation_coords:
    rect_width, rect_height = 15, 3 if 'Allowed' in text else 2  # Adjust height based on annotation type
    rectangle = Rectangle(
        (rect_x, rect_y), rect_width, rect_height,
        edgecolor='black', facecolor='lightgrey', linewidth=1
    )
    ax1.add_patch(rectangle)
    xy_left_edge = (rect_x, rect_y + rect_height / 2)
    ax1.annotate(
        text,
        xy=xy_left_edge,
        xytext=xy_text,
        arrowprops=dict(
            facecolor='red', arrowstyle='->', linewidth=1,
            connectionstyle="arc3,rad=0"
        ),
        bbox=dict(facecolor='lightgrey', alpha=0.3, edgecolor='none')
    )

# Add the vertical bracket using plt.text (| lines and top/bottom - lines)
x_pos = 420  # X position of the bracket
y_min = 19
y_max = 32
for y in range(y_min, y_max, 1):
    ax1.text(x_pos, y, '|', fontsize=20, ha='center', va='center')
ax1.text(x_pos - 2, y_max - 0.5, '-', fontsize=20, ha='center', va='center')
ax1.text(x_pos - 2, y_min - 0.5, '-', fontsize=20, ha='center', va='center')
ax1.text(x_pos + 10, (y_max + y_min) / 2, 'Refer to Figure 2', fontsize=10, ha='center', va='center', rotation=90)

# --------------------------------
# Second Plot: July Sensible Load
# --------------------------------
columns_to_plot_2 = [
    'Sensible Cooling Demand [W m^-2]',
    'Sensible Heating Demand [W m^-2]',
]

custom_labels_2 = [
    'Sensible Cooling Demand [W m⁻²]',
    'Sensible Heating Demand [W m⁻²]'
]

colors_2 = ['red', 'blue']
line_styles_2 = ['-', '--']

for i, column in enumerate(columns_to_plot_2):
    if column in data.columns:
        label = custom_labels_2[i] if i < 2 else None
        ax2.plot(data[x_column], data[column], color=colors_2[i], label=label,
                 linewidth=2, linestyle=line_styles_2[i])

# Set labels for the second plot
ax2.set_xlim(0, 400)
ax2.set_xlabel(x_column, fontsize=15)
ax2.set_ylabel("Load [W m⁻²]", fontsize=15)
ax2.grid(alpha=0.3)
ax2.legend(fontsize=12)

# Adding annotations 'a' and 'b' in the bottom right corner of each subplot
ax1.text(0.95, 0.05, '(a)', transform=ax1.transAxes, fontsize=16, fontweight='bold',
         va='bottom', ha='right', color='black')
ax2.text(0.95, 0.05, '(b)', transform=ax2.transAxes, fontsize=16, fontweight='bold',
         va='bottom', ha='right', color='black')

# Adjust the spacing between the two plots
plt.subplots_adjust(hspace=0.1)
fig.subplots_adjust(top=0.96, bottom=0.06, left=0.1, right=0.9, hspace=0.05)
ax1.set_title("July", fontsize=15)
# Show the final combined plot
plt.show()




###########################################################################################################
###########################################################################################################
######################################May#####################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# Load the Excel file and choose the sheet to read
file_path = r"C:\Users\Moji\Dropbox\PHD\Codes\Smart VCWG\VCWGv3.0.0-main\Codes\Results\2024-11-19_14-26_T1H1New_15\output_2024-11-19_14-26_T1H1New_T1H1New.xlsx"
sheet_name = 'May'  # Replace with your specific sheet name
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Create a figure and two subplots, vertically aligned
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True, gridspec_kw={'height_ratios': [1, 1]})

# --------------------------------
# First Plot: May Temperature Profile
# --------------------------------
# Define the x-axis column and the columns you want to plot
x_column = 'Hour [hr]'
columns_to_plot_1 = [
    'Indoor Temperature [K]',
    'Outdoor Temperature [K]',
    'Heating HH Setpoint [K]',
    'Heating H Setpoint [K]',
    'Heating L Setpoint [K]',
    'Heating LL Setpoint [K]',
    'Cooling HH Setpoint [K]',
    'Cooling H Setpoint [K]',
    'Cooling L Setpoint [K]',
    'Cooling LL Setpoint [K]'
]

# Define custom labels for the first two plotted lines
custom_labels_1 = [
    'Indoor Temp [°C]',
    'Outdoor Temp [°C]'
]

# Plot each column on ax1 with custom labels
colors = ['purple', 'darkgreen', 'red', 'red', 'red', 'red', 'blue', 'blue', 'blue', 'blue']
line_styles = ['-', '--', ':', ':', ':', ':', ':', ':', ':', ':']
line_widths = [2, 2, 1, 1, 1, 1, 1, 1, 1, 1]

for i, column in enumerate(columns_to_plot_1):
    if column in data.columns:
        # Use custom labels from the custom_labels list for the first two lines
        label = custom_labels_1[i] if i < 2 else None
        ax1.plot(data[x_column], data[column] - 273.15, color=colors[i],
                 label=label, linewidth=line_widths[i], linestyle=line_styles[i])

# Set labels and limits for the first plot
ax1.set_xlim(400, 800)
ax1.set_ylabel("Temperature [°C]", fontsize=15)
ax1.grid(alpha=0.3)

# Display the legend for the first two lines only
ax1.legend(fontsize=12)

# Add annotations
ax1.text(805, 26.3, 'HH', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='red', edgecolor='black', boxstyle='round,pad=0.3'))
ax1.text(805, 23.5, 'H', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='red', edgecolor='black', boxstyle='round,pad=0.3'))
ax1.text(805, 20.5, 'L', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='red', edgecolor='black', boxstyle='round,pad=0.3'))
ax1.text(805, 17.5, 'LL', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='red', edgecolor='black', boxstyle='round,pad=0.3'))

# Cooling blue annotations
ax1.text(823, 29.8, 'HH', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='blue', edgecolor='black', boxstyle='round,pad=0.3'))
ax1.text(823, 26.3, 'H', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='blue', edgecolor='black', boxstyle='round,pad=0.3'))
ax1.text(823, 23.5, 'L', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='blue', edgecolor='black', boxstyle='round,pad=0.3'))
ax1.text(823, 20.5, 'LL', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='blue', edgecolor='black', boxstyle='round,pad=0.3'))

# Add rectangles and annotations
annotation_coords = [
    (437, 17, 'Neutral Mode', (503, 5)),
    (484, 17, 'Neutral Mode', (503, 5)),
    (700, 24.1, 'Indoor Temp.\nConverges to\nOutdoor Temp', (620, 33)),
    (713, 22, 'Indoor Temp.\nStops Converging\nto Outdoor and\nStops at L Setpoint\nDue to High Occupancy', (650, 8)),
    (735, 22.8, 'Indoor Temp.\nStops Converging\nto Outdoor and\nStops at L Setpoint\nDue to High Occupancy', (650, 8)),
    (749, 20, 'Indoor Temp.\nConverges to\nLL due to\nLow Occupancy', (720, 1))
]

for rect_x, rect_y, text, xy_text in annotation_coords:
    rect_width, rect_height = 15, 6 if 'Converges' in text else 2.5  # Adjust height based on annotation type
    rectangle = Rectangle(
        (rect_x, rect_y), rect_width, rect_height,
        edgecolor='black', facecolor='lightgrey', linewidth=1
    )
    ax1.add_patch(rectangle)
    xy_left_edge = (rect_x, rect_y + rect_height / 2)
    ax1.annotate(
        text,
        xy=xy_left_edge,
        xytext=xy_text,
        arrowprops=dict(
            facecolor='red', arrowstyle='->', linewidth=1,
            connectionstyle="arc3,rad=0"
        ),
        bbox=dict(facecolor='lightgrey', alpha=0.3, edgecolor='none')
    )

# --------------------------------
# Second Plot: May Sensible Load
# --------------------------------
columns_to_plot_2 = [
    'Sensible Cooling Demand [W m^-2]',
    'Sensible Heating Demand [W m^-2]',
]

custom_labels_2 = [
    'Sensible Cooling Demand [W m⁻²]',
    'Sensible Heating Demand [W m⁻²]'
]

colors_2 = ['red', 'blue']
line_styles_2 = ['-', '--']

for i, column in enumerate(columns_to_plot_2):
    if column in data.columns:
        label = custom_labels_2[i] if i < 2 else None
        ax2.plot(data[x_column], data[column], color=colors_2[i], label=label,
                 linewidth=2, linestyle=line_styles_2[i])

# Set labels for the second plot
ax2.set_xlim(400, 800)
ax2.set_xlabel(x_column, fontsize=15)
ax2.set_ylabel("Load [W m⁻²]", fontsize=15)
ax2.grid(alpha=0.3)
ax2.legend(fontsize=12)

# Add the vertical bracket using plt.text (| lines and top/bottom - lines)
x_pos = 840  # X position of the bracket
y_min = 17
y_max = 32
for y in range(y_min, y_max, 1):
    ax1.text(x_pos, y, '|', fontsize=20, ha='center', va='center')
ax1.text(x_pos - 2, y_max - 0.5, '-', fontsize=20, ha='center', va='center')
ax1.text(x_pos - 2, y_min - 0.5, '-', fontsize=20, ha='center', va='center')
ax1.text(x_pos + 5, (y_max + y_min) / 2, 'Refer to Figure 2', fontsize=10, ha='center', va='center', rotation=90)

# Add annotations to the second plot
annotation_coords_2 = [
    (439, -2, 'Neutral Mode', (447, 105)),
    (485, -2, 'Neutral Mode', (447, 105))
]

for rect_x, rect_y, text, xy_text in annotation_coords_2:
    rect_width, rect_height = 10, 6
    rectangle = Rectangle(
        (rect_x, rect_y), rect_width, rect_height,
        edgecolor='black', facecolor='lightgrey', linewidth=1
    )
    ax2.add_patch(rectangle)
    xy_left_edge = (rect_x, rect_y + rect_height / 2)
    ax2.annotate(
        text,
        xy=xy_left_edge,
        xytext=xy_text,
        arrowprops=dict(
            facecolor='red', arrowstyle='->', linewidth=1,
            connectionstyle="arc3,rad=0"
        ),
        bbox=dict(facecolor='lightgrey', alpha=0.3, edgecolor='none')
    )

# Adding annotations 'a' and 'b' in the bottom right corner of each subplot
ax1.text(0.95, 0.05, '(a)', transform=ax1.transAxes, fontsize=16, fontweight='bold',
         va='bottom', ha='right', color='black')
ax2.text(0.95, 0.05, '(b)', transform=ax2.transAxes, fontsize=16, fontweight='bold',
         va='bottom', ha='right', color='black')

# Adjust the spacing between the two plots
plt.subplots_adjust(hspace=0.1)
fig.subplots_adjust(top=0.93, bottom=0.06, left=0.1, right=0.9, hspace=0.05)
ax1.set_title("May", fontsize=15)
# Show the final combined plot
plt.show()



###########################################################################################################
###########################################################################################################
######################################Jan#####################################################################
###########################################################################################################
###########################################################################################################
###########################################################################################################


sheet_name = 'Jan'  # Replace with your specific sheet name
data = pd.read_excel(file_path, sheet_name=sheet_name)

# Create a figure and two subplots, vertically aligned
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10), sharex=True, gridspec_kw={'height_ratios': [1, 1]})

# --------------------------------
# First Plot: January Temperature Profile
# --------------------------------
# Define the x-axis column and the columns you want to plot
x_column = 'Hour [hr]'
columns_to_plot_1 = [
    'Indoor Temperature [K]',
    'Outdoor Temperature [K]',
    'Heating HH Setpoint [K]',
    'Heating H Setpoint [K]',
    'Heating L Setpoint [K]',
    'Heating LL Setpoint [K]'
]

# Define custom labels for each plotted line
custom_labels_1 = [
    'Indoor Temp [°C]',
    'Outdoor Temp [°C]'
]

# Plot each column on ax1 with custom labels
colors = ['purple', 'darkgreen', 'red', 'red', 'red', 'red']
line_styles = ['-', '--', ':', ':', ':', ':']
line_widths = [2, 2, 1, 1, 1, 1]

for i, column in enumerate(columns_to_plot_1):
    if column in data.columns:
        # Use custom labels from the custom_labels list for the first two lines
        label = custom_labels_1[i] if i < 2 else None
        ax1.plot(data[x_column], data[column] - 273.15, color=colors[i],
                 label=label, linewidth=line_widths[i], linestyle=line_styles[i])

# Set labels and limits for the first plot
ax1.set_xlim(0, 400)
ax1.set_ylabel("Temperature [°C]", fontsize=15)
ax1.grid(alpha=0.3)

# Display the legend for the first two lines only
ax1.legend(fontsize=12)

# Add annotations
ax1.annotate(
    'High Occupancy: Converging to Comfort Setpoints',
    xy=(2.6, 21), xytext=(35, 25),
    arrowprops=dict(facecolor='red', arrowstyle='->', linewidth=1),
    bbox=dict(facecolor='lightgrey', alpha=0.3, edgecolor='none')
)
ax1.annotate(
    'Low Occupancy: Building Tries to Save Energy by Converging to Setback',
    xy=(14, 18), xytext=(45, 13),
    arrowprops=dict(facecolor='red', arrowstyle='->', linewidth=1),
    bbox=dict(facecolor='lightgrey', alpha=0.3, edgecolor='none')
)

# Highlighted text annotations with bounding boxes heating
endxlim = 400
ax1.text(405, 26.3, 'HH', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='red', edgecolor='black', boxstyle='round,pad=0.3'))
ax1.text(405, 23.5, 'H', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='red', edgecolor='black', boxstyle='round,pad=0.3'))
ax1.text(405, 20.5, 'L', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='red', edgecolor='black', boxstyle='round,pad=0.3'))
ax1.text(405, 17.5, 'LL', fontsize=10, fontweight='bold', color='white',
         bbox=dict(facecolor='red', edgecolor='black', boxstyle='round,pad=0.3'))



# Add the vertical bracket using only plt.text (| lines and top/bottom - lines)
x_pos = endxlim + 25
y_min = 17
y_max = 30
for y in range(y_min, y_max, 1):
    ax1.text(x_pos, y, '|', fontsize=20, ha='center', va='center')
ax1.text(x_pos - 2, y_max, '-', fontsize=20, ha='center', va='center')
ax1.text(x_pos - 2, y_min - 1, '-', fontsize=20, ha='center', va='center')
ax1.text(x_pos + 8, (y_max + y_min) / 2, 'Refer to Figure 2', fontsize=10, ha='center', va='center', rotation=90)

# --------------------------------
# Second Plot: January Sensible Load
# --------------------------------
columns_to_plot_2 = [
    'Sensible Cooling Demand [W m^-2]',
    'Sensible Heating Demand [W m^-2]',
]

custom_labels_2 = [
    'Sensible Cooling Demand [W m⁻²]',
    'Sensible Heating Demand [W m⁻²]'
]

colors_2 = ['red', 'blue']
line_styles_2 = ['-', '--']

for i, column in enumerate(columns_to_plot_2):
    if column in data.columns:
        label = custom_labels_2[i] if i < 2 else None
        ax2.plot(data[x_column], data[column], color=colors_2[i], label=label,
                 linewidth=2, linestyle=line_styles_2[i])

# Set labels for the second plot
ax2.set_xlim(0, 400)
ax2.set_xlabel(x_column, fontsize=15)
ax2.set_ylabel("Load [W m⁻²]", fontsize=15)
ax2.grid(alpha=0.3)
ax2.legend(fontsize=12)

# Adding annotations 'a' and 'b' in the bottom right corner of each subplot
ax1.text(0.95, 0.05, '(a)', transform=ax1.transAxes, fontsize=16, fontweight='bold',
         va='bottom', ha='right', color='black')
ax2.text(0.95, 0.05, '(b)', transform=ax2.transAxes, fontsize=16, fontweight='bold',
         va='bottom', ha='right', color='black')

# Adjust the spacing between the two plots
plt.subplots_adjust(hspace=0.1)

fig.subplots_adjust(top=0.96, bottom=0.06, left=0.1, right=0.9, hspace=0.05)
ax1.set_title("January", fontsize=15)
# Show the final combined plot
plt.show()
