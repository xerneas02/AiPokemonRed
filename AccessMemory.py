from MemoryAdresse import *

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

def set_pos(pyboy, x, y, map_n):
    pyboy.memory[X_POS_ADDRESS] = x
    pyboy.memory[Y_POS_ADDRESS] = y
    pyboy.memory[MAP_N_ADDRESS] = map_n