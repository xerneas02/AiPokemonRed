def parse_map_names(file_path):
    map_names = {}
    with open(file_path, 'r') as file:
        index = 0
        for line in file:
            if line.strip():  # Ignore empty lines
                parts = line.split('db')
                name = parts[1].replace('"', '').replace('@', '').strip()
                map_names[index] = name
                index += 1
    return map_names

# Usage
file_path = 'map.asm'
map_names = parse_map_names(file_path)
print(map_names)