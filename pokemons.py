import os

def parse_pokemon_names(file_path):
    pokemon_names = {}
    with open(file_path, 'r') as file:
        index = 1
        for line in file:
            if line.strip().startswith('db'):
                name = line.split('"')[1].replace('@', '').strip()
                pokemon_names[index] = name.lower()
                index += 1
    return pokemon_names

def parse_base_stats(directory):
    base_stats = {}
    for filename in os.listdir(directory):
        if filename.endswith('.asm'):
            pokemon_name = filename.replace('.asm', '')
            with open(os.path.join(directory, filename), 'r') as file:
                lines = file.readlines()
                stats = {
                    'hp': int(lines[2].split(',')[0][4:].strip()),
                    'atk': int(lines[2].split(',')[1].strip()),
                    'def': int(lines[2].split(',')[2].strip()),
                    'spd': int(lines[2].split(',')[3].strip()),
                    'spc': int(lines[2].split(',')[4].strip()),
                    'type1': lines[5].split(',')[0][4:].strip(),
                    'type2': lines[5].split(',')[1][:-7].strip()
                }
                base_stats[pokemon_name] = stats
    return base_stats

def print_data(dictionary): 
    for index, data in dictionary.items():
        print(f'"{index}": {data},')

# Usage
pokemon_file_path = 'pokemon.asm'
base_stats_directory = 'pokered-data/data/pokemon/base_stats'

pokemon_names = parse_pokemon_names(pokemon_file_path)
base_stats = parse_base_stats(base_stats_directory)

# Combine the data
pokemon_data = {}
for index, name in pokemon_names.items():
    if name in base_stats:
        pokemon_data[index] = {
            'name': name,
            'stats': base_stats[name]
        }
    else:
        print(name)

print_data(base_stats)