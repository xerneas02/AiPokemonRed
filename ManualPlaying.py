import pyboy.api
import pyboy.utils
from pynput import keyboard
from GameFrame import *

from tensorflow.keras.optimizers import Adam
from pyboy import PyBoy
import time
from Constante import *
from AccessMemory import *
import threading

# PyBoy ROM and settings
ROM_PAH = "Rom/Pokemon Red.gb"
SHOW_DISPLAY = True  # Set to True for real-time display

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
    'space': 'a',
    'shift': 'b',
    'a': 'start',
    'e': 'select',
    'r': 'save'  # "R" key for saving the game state
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
    with open("State/starting_house/starting_state.state", "rb") as state:
        pyboy.load_state(state)
    total_frames = 0
    done = False
    while not done:
        time.sleep(0.006)
        # Check which keys are pressed and send the corresponding action to the game
        for action in keys_pressed.copy():
            if action == 'save':  # Check if the save state button was pressed
                save_game_state(pyboy, "State/starting_house/save_state.state")
            else:
                pyboy.button(action)

        # Advance the game by one tick
        pyboy.tick()

        # Display player position
        display_position(pyboy)

        total_frames += 1


# Start the manual control mode
play_manually()

listener.stop()  # Stop the keyboard listener when done
