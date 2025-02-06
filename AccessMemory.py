from MemoryAdresse import *
from Constante import *
import pyboy

# Function to get Pokémon levels in your party
def get_pokemon_party_levels(pyboy : pyboy.PyBoy):
    levels = []
    # Read levels from predefined memory addresses
    for level_address in LEVELS_ADDRESSES:
        level = pyboy.memory[level_address]  # Access memory directly
        levels.append(level)
    return levels

# Function to get the number of Pokémon in the party
def get_party_size(pyboy : pyboy.PyBoy):
    return pyboy.memory[PARTY_SIZE_ADDRESS]  # Access memory directly

# Function to get player position on the map
def get_player_position(pyboy : pyboy.PyBoy):
    x_pos = pyboy.memory[X_POS_ADDRESS]  # Access memory directly
    y_pos = pyboy.memory[Y_POS_ADDRESS]  # Access memory directly
    return (x_pos, y_pos)

# Function to get money (money is split across 3 bytes in memory)
def get_money(pyboy : pyboy.PyBoy):
    money_1 = pyboy.memory[MONEY_ADDRESS_1]  # Access memory directly
    money_2 = pyboy.memory[MONEY_ADDRESS_2]  # Access memory directly
    money_3 = pyboy.memory[MONEY_ADDRESS_3]  # Access memory directly
    money = (money_1 * 10000) + (money_2 * 100) + money_3
    return money

def get_number_of_turn(pyboy : pyboy.PyBoy):
    return pyboy.memory[NUMBER_OF_TURN]

def get_total_items(pyboy : pyboy.PyBoy):
    return pyboy.memory[TOTAL_ITEMS]

def set_text_speed_fast(pyboy : pyboy.PyBoy):
    current_options = pyboy.memory[OPTIONS_ADDRESS] 
    new_options = (current_options & MASK_HIGH_NYBBLE) | (TEXT_SPEED_FAST & 0x0F)
    pyboy.memory[OPTIONS_ADDRESS] = new_options

def set_battle_animation_off(pyboy: pyboy.PyBoy):
    """
    Disable battle animations by setting Bit 7 of OPTIONS_ADDRESS to 1.
    Set battle style to 'Set' by setting Bit 6 of OPTIONS_ADDRESS to 1.
    """
    current_options = pyboy.memory[OPTIONS_ADDRESS]
    
    # Set Bit 7 to 1 (Battle Animation Off)
    # Set Bit 6 to 1 (Battle Style Set)
    new_options = current_options | 0b11000000
    
    pyboy.memory[OPTIONS_ADDRESS] = new_options



# Function to check if the museum ticket event is active (flag-based event)
def has_museum_ticket(pyboy : pyboy.PyBoy):
    ticket_status = pyboy.memory[MUSEUM_TICKET_ADDRESS]  # Access memory directly
    return ticket_status == 1

def get_pos(pyboy : pyboy.PyBoy):
    x_pos = pyboy.memory[X_POS_ADDRESS]
    y_pos = pyboy.memory[Y_POS_ADDRESS]
    map_n = pyboy.memory[MAP_N_ADDRESS]
    
    return x_pos, y_pos, map_n

def get_enemy_pokemons(pyboy : pyboy.PyBoy):
    enemy_pokemons = []
    for i in range(6):
        enemy_pokemon_id = pyboy.memory[ENEMY_POKEMONS[i]]
        enemy_pokemon_hp = get_hp(ENEMY_POKEMONS[i] + 1, ENEMY_POKEMONS[i] + 2, pyboy)
        enemy_pokemons.append({"id" : enemy_pokemon_id, "current_hp" : enemy_pokemon_hp})
    return enemy_pokemons

def get_enemy_total_pokemon(pyboy : pyboy.PyBoy):
    return pyboy.memory[TOTAL_ENEMY_POKEMON]

def pokemon_id_to_name(pokemon_id):
    return POKEMON_ID_TO_NAME[pokemon_id]

def get_hp(adr_low, adr_high, pyboy : pyboy.PyBoy):
    hp_low = pyboy.memory[adr_low]
    hp_high = pyboy.memory[adr_high]
    
    hp = (hp_high << 8) | hp_low
    return hp

def get_enemy_hp(pyboy : pyboy.PyBoy):
    return get_hp(ENEMY_HP_ADDRESS_LOW, ENEMY_HP_ADDRESS_HIGH, pyboy)

def get_enemy_max_hp(pyboy : pyboy.PyBoy):
    return get_hp(ENEMY_MAX_HP_ADDRESS_LOW, ENEMY_MAX_HP_ADDRESS_HIGH, pyboy)

def get_enemy_level(pyboy : pyboy.PyBoy):
    return pyboy.memory[ENEMY_LVL]

def get_enemy_info(pyboy : pyboy.PyBoy):
    enemy_pokemon_id = pyboy.memory[ENEMY_POKEMONS[0]]
    enemy_current_hp = get_enemy_hp(pyboy)
    enemy_max_hp = get_enemy_max_hp(pyboy)
    enemy_level = get_enemy_level(pyboy)
    
    enemy_info = {
        "id": enemy_pokemon_id,
        "current_hp": enemy_current_hp,
        "max_hp": enemy_max_hp,
        "level": enemy_level
    }
    
    return enemy_info

def get_pokemon_info(pyboy : pyboy.PyBoy, pokemon_index : int):
    base_address = PLAYER_POKEMONS[pokemon_index]
    
    current_hp = get_hp(base_address + 1, base_address + 2, pyboy)
    max_hp = get_hp(base_address + 0x22, base_address + 0x23, pyboy)
    level = pyboy.memory[base_address + 3]
    status = pyboy.memory[base_address + 4]
    moves_list = [pyboy.memory[base_address + 8 + i] for i in range(4)]
    pp_moves_list = [pyboy.memory[base_address + 0x1D + i] for i in range(4)]
    
    moves_names = [MOVES_ID_TO_NAME[moves_list[i]] for i in range(4)]
    moves_infos = [MOVE_STATS[moves_names[i]] for i in range(4)]
    pp_moves_info = [pp_moves_list[i] for i in range(4)]

    for i in range(len(moves_infos)):
        moves_infos[i]["id"] = moves_list[i]
    
    pokemon_info = {
        "id": pyboy.memory[base_address],
        "current_hp": current_hp,
        "max_hp": max_hp,
        "level": level,
        "status": status,
        "moves": moves_infos,
        "pp_moves": pp_moves_info
    }
    
    return pokemon_info

def get_active_pokemon_info(pyboy : pyboy.PyBoy):
    active_pokemon_id = pyboy.memory[ACTIVE_POKEMON_ID]
    active_pokemon_current_hp = get_hp(ACTIVE_POKEMON_CURRENT_HP[0], ACTIVE_POKEMON_CURRENT_HP[1], pyboy)
    active_pokemon_max_hp = get_hp(ACTIVE_POKEMON_MAX_HP[0], ACTIVE_POKEMON_MAX_HP[1], pyboy)
    active_pokemon_level = pyboy.memory[ACTIVE_POKEMON_LEVEL]
    active_pokemon_status = pyboy.memory[ACTIVE_POKEMON_STATUS]
    active_pokemon_moves_list = [pyboy.memory[ACTIVE_POKEMON_MOVES[i]] for i in range(4)]
    active_pokemon_pp_moves_list = [pyboy.memory[ACTIVE_POKEMON_PP_MOVES[i]] for i in range(4)]

    moves_names = [MOVES_ID_TO_NAME[active_pokemon_moves_list[i]] for i in range(4)]
    moves_infos = [MOVE_STATS[moves_names[i]] for i in range(4)]

    for i in range(len(moves_infos)):
        moves_infos[i]["id"] = active_pokemon_moves_list[i]

    pp_moves_info = [active_pokemon_pp_moves_list[i] for i in range(4)]

    active_pokemon_info = {
        "id": active_pokemon_id,
        "current_hp": active_pokemon_current_hp,
        "max_hp": active_pokemon_max_hp,
        "level": active_pokemon_level,
        "status": active_pokemon_status,
        "moves": moves_infos,
        "pp_moves": pp_moves_info
    }

    return active_pokemon_info


def get_effectiveness(move_type : str, target_type1 : str, target_type2 : str):
    effectiveness = 1.0

    if (move_type, target_type1) in TYPE_MATCHUP.keys():
            effectiveness *= TYPE_MATCHUP[(move_type, target_type1)]
    
    if target_type1 != target_type2:
        if (move_type, target_type2) in TYPE_MATCHUP.keys():
            effectiveness *= TYPE_MATCHUP[(move_type, target_type2)]

    return effectiveness