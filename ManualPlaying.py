import pyboy.api
import pyboy.utils
from pynput import keyboard
from GameFrame import *

from tensorflow.keras.optimizers import Adam
from pyboy import PyBoy
import time
from Constante import *
from AccessMemory import *
from State import get_battle_state, print_state
import threading
from PIL import Image
from Input import *
import random
import os

# PyBoy ROM and settings
ROM_PAH = "Rom/Pokemon Red.gb"
SHOW_DISPLAY = True  # Set to True for real-time display

nbBattle = 39
inBattle = False

# Start PyBoy emulator
pyboy = PyBoy(ROM_PAH, window_type="null" if not SHOW_DISPLAY else "SDL2")

if SHOW_DISPLAY:
    pyboy.set_emulation_speed(0)  # Real-time display
else:
    pyboy.set_emulation_speed(1_000_000)  # Fast mode without display

# Key mappings
key_mapping = {
    'z': 'up',
    'q': 'left',
    's': 'down',
    'd': 'right',
    'a': 'a',
    'shift': 'b',
    'f': 'start',
    'e': 'select',
    'r': 'save',  # "R" key for saving the game state
    'p': 'screen',
    't': 'attack',
    'm': 'walk_throught'
}

# Store the currently pressed keys
keys_pressed = set()

# Function to handle key press events
def on_press(key):
    try:
        if key.char in key_mapping:
            keys_pressed.add(key_mapping[key.char])
    except AttributeError:
        if key == keyboard.Key.shift:
            keys_pressed.add('b')
        elif key == keyboard.Key.space:
            keys_pressed.add('a')

# Function to handle key release events
def on_release(key):
    try:
        if key.char in key_mapping:
            keys_pressed.discard(key_mapping[key.char])
    except AttributeError:
        if key == keyboard.Key.shift:
            keys_pressed.discard('b')
        elif key == keyboard.Key.space:
            keys_pressed.discard('a')

def load_random_state(pyboy : PyBoy, folder_path):
    state_files = [f for f in os.listdir(folder_path) if f.endswith('.state')]
    
    random_state_file = random.choice(state_files)
    
    load_state(pyboy, os.path.join(folder_path, random_state_file))    

def load_state(pyboy : PyBoy, filename):
    with open(filename, "rb") as state:
        pyboy.load_state(state)

    set_battle_animation_off(pyboy)
    set_text_speed_fast(pyboy)

    #pyboy.gameshark("01FF56D3") # All badges
    #pyboy.gameshark.add("010138CD") # Walk through walls
    #pyboy.gameshark.add("01017CCF") # Master balls
    #pyboy.gameshark.add("01287CCF") # Rare candies
    #pyboy.gameshark.add("019947D3") # Infinite money
    pyboy.gameshark.clear_all()



    print(f"Loaded state: {filename}")


# Function to save a screenshot of the emulator screen
def save_screenshot(pyboy : PyBoy, filename="screenshot.png"):
    screen_image = pyboy.screen.ndarray
    screen_image = Image.fromarray(screen_image)
    screen_image.save(filename)
    print(f"Screenshot saved to {filename}")

# Start keyboard listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

# Function to display player's position
def display_position(pyboy):
    pos = get_pos(pyboy)  # Assuming get_pos() is defined elsewhere to get position
    print(f"Player Position: {pos}")

# Function to save the current game state
def save_game_state(pyboy, filename="save_state.state"):
    with open(filename, "wb") as f:
        pyboy.save_state(f)
    print(f"Game state saved to {filename}")

# Main game loop for manual control
def play_manually():
    global nbBattle, inBattle

    win = 0
    lose = 0
    folder_path = "State/battle/"

    load_random_state(pyboy, folder_path)
    #load_state(pyboy, "State/battle/ondine_43.state")#"save_state.state")

    

    total_frames = 0
    done = False
    battle_started = False
    cheat = True

    while not done:
        #time.sleep(0.003)
        if not inBattle and pyboy.memory[ENEMY_POKEMONS[0]] != 0:
            inBattle = True
            nbBattle += 1
            #save_game_state(pyboy, f"State/battle/{POKEMON_ID_TO_NAME[pyboy.memory[ENEMY_POKEMONS[0]]]}_{nbBattle}.state")
        
        if inBattle and pyboy.memory[ENEMY_POKEMONS[0]] == 0:
            inBattle = False
        
        # Check which keys are pressed and send the corresponding action to the game
        for action in keys_pressed.copy():
            if action == 'save':  # Check if the save state button was pressed
                save_game_state(pyboy, "save_state.state")
            elif action == 'screen':  # Check if the screenshot button was pressed
                save_screenshot(pyboy, "screenshot.png")
            elif action == 'attack':
                switch(pyboy, 0)
            elif action == 'walk_throught':
                if cheat:
                    pyboy.gameshark.remove("010138CD") # Walk through walls
                    print("Walk through walls disabled")
                else:
                    pyboy.gameshark.add("010138CD")
                    print("Walk through walls enabled")
                
                cheat = not cheat
            else:
                pyboy.button(action)

        # Advance the game by one tick
        pyboy.tick()
        
        if is_battle_started(pyboy):
            pyboy.button('a')

        if is_on_attack_menu(pyboy):
            battle_started = True
        

        if battle_started:
            play_random(pyboy)
            pass

        if is_battle_lost(pyboy) or is_battle_won(pyboy):
            win  += is_battle_won(pyboy)
            lose += is_battle_lost(pyboy)
            battle_started = False
            load_random_state(pyboy, folder_path)

            #print(f"Pourcentage de victoire: {win / (win + lose) * 100}%")
 
        # Display player position
        #state = get_battle_state(pyboy)
        
        
        total_frames += 1

def play_random(pyboy):
    play = random.randint(0, 6)

    if play != 0:
        if input_possible(pyboy)["attack"]:
            attack(pyboy, random.randint(0, 3))
        else:
            switch(pyboy, random.randint(0, 5))
    else:
        if input_possible(pyboy)["switch"]:
            switch(pyboy, random.randint(0, 5))
        else:
            attack(pyboy, random.randint(0, 3))




# Start the manual control mode
play_manually()

listener.stop()  # Stop the keyboard listener when done
