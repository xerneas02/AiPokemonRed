from MemoryAdresse import *
from Constante import *

# Function to get Pokémon levels in your party
def get_pokemon_party_levels(pyboy):
    levels = []
    # Read levels from predefined memory addresses
    for level_address in LEVELS_ADDRESSES:
        level = pyboy.memory[level_address]  # Access memory directly
        levels.append(level)
    return levels

# Function to get the number of Pokémon in the party
def get_party_size(pyboy):
    return pyboy.memory[PARTY_SIZE_ADDRESS]  # Access memory directly

# Function to get player position on the map
def get_player_position(pyboy):
    x_pos = pyboy.memory[X_POS_ADDRESS]  # Access memory directly
    y_pos = pyboy.memory[Y_POS_ADDRESS]  # Access memory directly
    return (x_pos, y_pos)

# Function to get money (money is split across 3 bytes in memory)
def get_money(pyboy):
    money_1 = pyboy.memory[MONEY_ADDRESS_1]  # Access memory directly
    money_2 = pyboy.memory[MONEY_ADDRESS_2]  # Access memory directly
    money_3 = pyboy.memory[MONEY_ADDRESS_3]  # Access memory directly
    money = (money_1 * 10000) + (money_2 * 100) + money_3
    return money

def get_total_items(pyboy):
    return pyboy.memory[TOTAL_ITEMS]

def set_text_speed_fast(pyboy):
    current_options = pyboy.memory[OPTIONS_ADDRESS]
    new_options = (current_options & MASK_HIGH_NYBBLE) | (TEXT_SPEED_FAST & 0x0F)
    pyboy.memory[OPTIONS_ADDRESS] = new_options


# Function to check if the museum ticket event is active (flag-based event)
def has_museum_ticket(pyboy):
    ticket_status = pyboy.memory[MUSEUM_TICKET_ADDRESS]  # Access memory directly
    return ticket_status == 1

def get_pos(pyboy):
    x_pos = pyboy.memory[X_POS_ADDRESS]
    y_pos = pyboy.memory[Y_POS_ADDRESS]
    map_n = pyboy.memory[MAP_N_ADDRESS]
    
    return x_pos, y_pos, map_n

def get_enemy_pokemons(pyboy):
    enemy_pokemons = []
    total_enemy_pokemon = pyboy.memory[TOTAL_ENEMY_POKEMON]
    for i in range(total_enemy_pokemon):
        enemy_pokemon_id = pyboy.memory[ENEMY_POKEMONS[i]]
        enemy_pokemons.append(enemy_pokemon_id)
    return enemy_pokemons

def get_enemy_total_pokemon(pyboy):
    return pyboy.memory[TOTAL_ENEMY_POKEMON]

def pokemon_id_to_name(pokemon_id):
    return poke_id_to_name[pokemon_id]

def get_hp(adr_low, adr_high, pyboy):
    hp_low = pyboy.memory(adr_low)
    hp_high = pyboy.memory(adr_high)
    
    hp = (hp_high << 8) | hp_low
    return hp

def get_enemy_hp(pyboy):
    return get_hp(ENEMY_HP_ADDRESS_LOW, ENEMY_HP_ADDRESS_HIGH, pyboy)

def get_enemy_max_hp(pyboy):
    return get_hp(ENEMY_MAX_HP_ADDRESS_LOW, ENEMY_MAX_HP_ADDRESS_HIGH, pyboy)

def get_enemy_level(pyboy):
    return pyboy.memory(ENEMY_LVL)

def get_pokemon_info(pyboy, pokemon_index):
    base_address = PLAYER_POKEMONS[pokemon_index]
    
    current_hp = get_hp(base_address + 1, base_address + 2, pyboy)
    max_hp = get_hp(base_address + 0x1A, base_address + 0x1B, pyboy)
    level = pyboy.memory[base_address + 3]
    status = pyboy.memory[base_address + 4]
    moves_list = [pyboy.memory[base_address + 0x0C + i] for i in range(4)]
    pp_moves_list = [pyboy.memory[base_address + 0x1D + i] for i in range(4)]
    
    moves_info = {f"move_{i+1}": moves[moves_list[i]] for i in range(4)}
    pp_moves_info = {f"pp_move_{i+1}": pp_moves_list[i] for i in range(4)}
    
    pokemon_info = {
        "current_hp": current_hp,
        "max_hp": max_hp,
        "level": level,
        "status": status,
        "moves": moves_info,
        "pp_moves": pp_moves_info
    }
    
    return pokemon_info
