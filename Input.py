from pyboy import PyBoy
import numpy as np
from State import get_battle_state
from PIL import Image
from AccessMemory import get_active_pokemon_info, get_pokemon_info

def is_on_attack_menu(pyboy: PyBoy):
    state = get_battle_state(pyboy)
    screen = pyboy.screen.ndarray
    condition1 = np.array_equal(screen[116][75], [0, 0, 0, 255])
    condition2 = np.array_equal(screen[119][75], [255, 255, 255, 255])
    return condition1 and condition2 and state[0] != 0

def is_on_run_menu(pyboy: PyBoy):
    state = get_battle_state(pyboy)
    screen = pyboy.screen.ndarray
    condition1 = np.array_equal(screen[132][122], [0, 0, 0, 255])
    condition2 = np.array_equal(screen[128][122], [255, 255, 255, 255])
    return condition1 and condition2 and state[0] != 0

def is_on_pkm_menu(pyboy: PyBoy):
    state = get_battle_state(pyboy)
    screen = pyboy.screen.ndarray
    condition1 = np.array_equal(screen[116][122], [0, 0, 0, 255])
    condition2 = np.array_equal(screen[111][122], [255, 255, 255, 255])
    return condition1 and condition2 and state[0] != 0  

def is_on_item_menu(pyboy: PyBoy):
    state = get_battle_state(pyboy)
    screen = pyboy.screen.ndarray
    condition1 = np.array_equal(screen[132][74], [0, 0, 0, 255])
    condition2 = np.array_equal(screen[128][74], [255, 255, 255, 255])
    return condition1 and condition2 and state[0] != 0  


def is_battle_started(pyboy: PyBoy):
    screen = pyboy.screen.ndarray
    condition1 = np.array_equal(screen[49][48], [85, 85, 85, 255])
    condition2 = np.array_equal(screen[130][147], [0, 0, 0, 255])
    condition3 = np.array_equal(screen[128][147], [255, 255, 255, 255])
    return condition1 and condition2 and condition3

def is_all_range_same_color(pyboy: PyBoy, start=(0, 0), end=(144, 160)) -> bool:
    screen = pyboy.screen.ndarray
    for i in range(start[0], end[0]):
        for j in range(start[1], end[1]):
            if not np.array_equal(screen[i][j], screen[0][0]):
                return False
    return True
    
def check_list_conditions(conditions : list) -> bool:
    for condition in conditions:
        if not condition:
            return False
    return True

def is_waiting(pyboy: PyBoy):
    screen = pyboy.screen.ndarray
    conditions1 = [np.array_equal(screen[124][36], [255, 255, 255, 255]), np.array_equal(screen[124][68], [255, 255, 255, 255])] 
    conditions2 = [np.array_equal(screen[129][36], [255, 255, 255, 255]), np.array_equal(screen[129][68], [255, 255, 255, 255])]

    return (check_list_conditions(conditions1) or check_list_conditions(conditions2)) and not is_all_range_same_color(pyboy, (103, 6), (136, 152)) and is_on_pokemon(pyboy) == -1

def is_on_attack(pyboy: PyBoy) -> int:
    screen = pyboy.screen.ndarray
    conditions = [
        np.array_equal(screen[66][4], [0, 0, 0, 255]),
        np.array_equal(screen[66][3], [255, 255, 255, 255]),
        np.array_equal(screen[66][84], [0, 0, 0, 255]),
        np.array_equal(screen[66][83], [255, 255, 255, 255]),
        is_all_range_same_color(pyboy, (64, 5), (65, 82))

    ]

    if check_list_conditions(conditions):
        for i in range(4):
            condition1 = np.array_equal(screen[108 + 8*i][45], [0, 0, 0, 255])
            condition2 = np.array_equal(screen[107 + 8*i][45], [255, 255, 255, 255])

            if condition1 and condition2:
                return i

    return -1

def is_on_pokemon(pyboy: PyBoy) -> int:
    screen = pyboy.screen.ndarray

    conditions1 = [
        np.array_equal(screen[117][137], [0, 0, 0, 255]),
        np.array_equal(screen[118][138], [0, 0, 0, 255]),
        np.array_equal(screen[118][137], [0, 0, 0, 255]),
        np.array_equal(screen[117][138], [0, 0, 0, 255]),
        np.array_equal(screen[118][139], [255, 255, 255, 255]),
        np.array_equal(screen[116][137], [255, 255, 255, 255])
    ]

    conditions2 = [
        np.array_equal(screen[90][92], [0, 0, 0, 255]),
        np.array_equal(screen[90][91], [255, 255, 255, 255]),
        np.array_equal(screen[90][156], [0, 0, 0, 255]),
        np.array_equal(screen[90][157], [255, 255, 255, 255]),
        np.array_equal(screen[92][115], [0, 0, 0, 255])
    ]

    if check_list_conditions(conditions1) or check_list_conditions(conditions2):
        for i in range(6):
            if np.array_equal(screen[12 + i*16][1], [0, 0, 0, 255]):
                return i

        return 7
    
    return -1
        

def is_gain_lvl(pyboy: PyBoy):
    screen = pyboy.screen.ndarray
    condition1 = np.array_equal(screen[90][76], [0, 0, 0, 255])
    condition2 = np.array_equal(screen[90][75], [255, 255, 255, 255])

    return condition1 and condition2

def get_pp(pyboy: PyBoy, index : int):
    pokemon_info = get_active_pokemon_info(pyboy)

    return pokemon_info["pp_moves"][index]

def get_pokemon_hp(pyboy: PyBoy, index : int):
    pokemon_info = get_pokemon_info(pyboy, index)

    return pokemon_info["current_hp"]

def is_pokemon_main(pyboy: PyBoy, index : int):
    pokemon_info = get_pokemon_info(pyboy, index)
    active_pokemon_info = get_active_pokemon_info(pyboy)

    return pokemon_info["id"] == active_pokemon_info["id"]

def switch(pyboy: PyBoy, index : int):
    hasnt_switched = True

    while get_pokemon_hp(pyboy, index) == 0 or is_pokemon_main(pyboy, index):
        index = (index + 1) % 6

    while hasnt_switched:
        
        for _ in range(4):
            pyboy.tick()

        if is_on_pkm_menu(pyboy):
            pyboy.button('a')
            continue
        elif is_on_attack(pyboy) != -1:
            pyboy.button('b')
            continue
        elif is_on_run_menu(pyboy):
            pyboy.button('up')
            continue
        elif is_on_attack_menu(pyboy):
            pyboy.button('right')
            continue
        elif is_on_item_menu(pyboy):
            pyboy.button('up')
            continue

        switch = is_on_pokemon(pyboy)
             
        if switch == index:
            pyboy.button('a')
        elif switch < index and switch >= 0:
            pyboy.button('down')
        elif switch > index and switch >= 0:
            pyboy.button('up')

        

        if is_waiting(pyboy):
            hasnt_switched = False

    screen = pyboy.screen.ndarray

    while is_waiting(pyboy) or is_all_range_same_color(pyboy, (103, 6), (136, 152)):        
        for _ in range(4):
            pyboy.tick()
        if np.array_equal(screen[130][147], [0, 0, 0, 255]) or is_gain_lvl(pyboy):
            pyboy.button('a')
    


def attack(pyboy: PyBoy, index : int):
    hasnt_attacked = True
    last_index = -1
    last_down = False
    should_attack = False

    if get_pp(pyboy, 0) != 0 or get_pp(pyboy, 1) != 0 or get_pp(pyboy, 2) != 0 or get_pp(pyboy, 3) != 0:
        while get_pp(pyboy, index) == 0:
            index = (index + 1) % 4

    while hasnt_attacked:
        for _ in range(4):
            pyboy.tick()
        attack = is_on_attack(pyboy)
        
        if is_on_attack_menu(pyboy):
            pyboy.button('a')
            continue
        elif is_on_run_menu(pyboy):
            pyboy.button('up')
            continue
        elif is_on_pkm_menu(pyboy):
            pyboy.button('left')
            continue
        elif is_on_item_menu(pyboy):
            pyboy.button('up')
            continue
        
        if last_index <= attack and last_down:
            should_attack = True

        last_down = False
        last_index = attack
        
        if attack == index or should_attack:
            pyboy.button('a')
        elif attack < index and attack >= 0:
            pyboy.button('down')
            last_down = True
        elif attack > index and attack >= 0:
            pyboy.button('up')

        

        if is_waiting(pyboy):
            hasnt_attacked = False

    screen = pyboy.screen.ndarray

    while is_waiting(pyboy) :        
        for _ in range(4):
            pyboy.tick()
        if np.array_equal(screen[130][147], [0, 0, 0, 255]) or is_gain_lvl(pyboy):
            pyboy.button('a')

def save_screenshot(pyboy : PyBoy, filename="screenshot.png"):
    screen_image = pyboy.screen.ndarray
    screen_image = Image.fromarray(screen_image)
    screen_image.save(filename)
    print(f"Screenshot saved to {filename}")
        