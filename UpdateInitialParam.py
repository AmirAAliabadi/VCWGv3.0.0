import os

def update_uwg_files(directory, file_names, key_to_update, new_value):
    def read_uwg_file(file_path):
        with open(file_path, 'r') as file:
            lines = file.readlines()
        return lines

    def write_uwg_file(file_path, lines):
        with open(file_path, 'w') as file:
            file.writelines(lines)

    def update_parameter(lines, key_to_update, new_value):
        for i, line in enumerate(lines):
            if line.strip() and not line.startswith("#"):
                parts = line.strip().split(',')
                if len(parts) >= 2 and parts[0].strip() == key_to_update:
                    parts[1] = f" {new_value}"
                    lines[i] = ','.join(parts) + '\n'
                    break
        return lines

    for file_name in file_names:
        file_path = os.path.join(directory, file_name)
        lines = read_uwg_file(file_path)
        lines = update_parameter(lines, key_to_update, new_value)
        write_uwg_file(file_path, lines)