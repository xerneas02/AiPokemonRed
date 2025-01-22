from pyboy import PyBoy
import numpy as np
from State import get_battle_state
from PIL import Image

def is_on_attack_menu(pyboy: PyBoy):
    state = get_battle_state(pyboy)
    screen = pyboy.screen.ndarray
    condition1 = np.array_equal(screen[116][75], [0, 0, 0, 255])
    condition2 = np.array_equal(screen[119][75], [255, 255, 255, 255])
    return condition1 and condition2 and state[0] != 0

def is_battle_started(pyboy: PyBoy):
    screen = pyboy.screen.ndarray
    condition1 = np.array_equal(screen[49][48], [85, 85, 85, 255])
    condition2 = np.array_equal(screen[130][147], [0, 0, 0, 255])
    condition3 = np.array_equal(screen[128][147], [255, 255, 255, 255])
    return condition1 and condition2 and condition3

def is_waiting(pyboy: PyBoy):
    screen = pyboy.screen.ndarray
    condition1 = np.array_equal(screen[124][36], [255, 255, 255, 255])
    condition2 = np.array_equal(screen[112][128], [255, 255, 255, 255])

    return condition1 and condition2

def is_on_attack(pyboy: PyBoy) -> int:
    screen = pyboy.screen.ndarray
    for i in range(4):
        condition1 = np.array_equal(screen[108 + 8*i][45], [0, 0, 0, 255])
        condition2 = np.array_equal(screen[107 + 8*i][45], [255, 255, 255, 255])

        if condition1 and condition2:
            return i

    return -1

def is_gain_lvl(pyboy: PyBoy):
    screen = pyboy.screen.ndarray
    condition1 = np.array_equal(screen[90][76], [0, 0, 0, 255])
    condition2 = np.array_equal(screen[90][75], [255, 255, 255, 255])

    return condition1 and condition2

def attack(pyboy: PyBoy, index : int):
    hasnt_attacked = True
    last_index = -1
    last_down = False
    should_attack = False

    while hasnt_attacked:
        for _ in range(4):
            pyboy.tick()
        attack = is_on_attack(pyboy)
        
        if is_on_attack_menu(pyboy):
            pyboy.button('a')
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
        