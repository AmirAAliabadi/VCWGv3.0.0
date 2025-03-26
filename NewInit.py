def read_uwg_file(file_path):
    parameters = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip() and not line.startswith("#"):
                parts = line.split(',')
                if len(parts) >= 3:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    comment = parts[2].strip() if len(parts) > 2 else ""
                    parameters.append((key, value, comment))
    return parameters

def write_uwg_file(file_path, parameters):
    with open(file_path, 'w') as file:
        file.write("# =================================================\n")
        file.write("# Sample VCWG simulation initialization parameters\n")
        file.write("# Mohsen Moradi and Amir A. Aliabadi\n")
        file.write("# Atmospheric Innovations Research (AIR) Laboratory, University of Guelph, Guelph, Canada\n")
        file.write("# Last update: May 2021\n")
        file.write("# =================================================\n\n")
        file.write("# =================================================\n")
        file.write("# SIMULATION CONTROL,\n")
        file.write("# =================================================\n")
        for key, value, comment in parameters:
            file.write(f"{key},{value},{comment}\n")
        file.write("\n# =================================================\n")
        file.write("# Control switches\n")
        file.write("# =================================================\n")

def update_parameter(parameters, key_to_update, new_value):
    for i, (key, value, comment) in enumerate(parameters):
        if key == key_to_update:
            parameters[i] = (key, new_value, comment)
            break
    return parameters

# Example usage
file_path = 'path/to/your/file.uwg'
parameters = read_uwg_file(file_path)
parameters = update_parameter(parameters, 'dtSim', '600')  # Change dtSim to 600
write_uwg_file(file_path, parameters)