import random
import os
from pyboy import PyBoy
import numpy as np
import neat
from Input import input_possible, attack, switch, is_battle_lost, is_battle_won, is_on_attack_menu
from State import get_battle_state
from AccessMemory import set_battle_animation_off, set_text_speed_fast
from Constante import BATTLE_PER_GENOM, POPULATION_SIZE

def load_random_state(pyboy: PyBoy, folder_path='State/battle/'):
    state_files = [f for f in os.listdir(folder_path) if f.endswith('.state')]
    random_state_file = random.choice(state_files)
    load_state(pyboy, os.path.join(folder_path, random_state_file))
    return random_state_file

def load_state(pyboy: PyBoy, filename):
    with open(filename, "rb") as state:
        pyboy.load_state(state)

    set_battle_animation_off(pyboy)
    set_text_speed_fast(pyboy)

    pyboy.gameshark.clear_all()
    
    while(not is_on_attack_menu(pyboy)):
        for _ in range(4):
            pyboy.tick()
            
        pyboy.button('a')

def play_action(pyboy, action):
    possible_inputs = input_possible(pyboy)
    if 0 <= action <= 3:
        if possible_inputs["attack"]:
            attack(pyboy, action)
        else:
            switch(pyboy, random.randint(0, 5))
    elif 4 <= action <= 9:
        if possible_inputs["switch"]:
            switch(pyboy, action - 4)
        else:
            attack(pyboy, random.randint(0, 3))


class PokemonRedBattleEnv:
    def __init__(self, rom_path, state_path='State/battle/', show_display=False, progress_counter=None):
        # Initialize PyBoy
        window_type = "SDL2" if show_display else "null"
        self.pyboy = PyBoy(rom_path, window=window_type)
        
        if show_display:
            self.pyboy.set_emulation_speed(0)
        else:
            self.pyboy.set_emulation_speed(1_000_000)
            
        
        self.progress_counter = progress_counter
        self.state_path = state_path
        self.state = None
        self.reset()
        self.steps = 0
        self.nb_battles = 0
        self.state_file = ""

    def reset(self):
        self.state_file = load_random_state(self.pyboy, self.state_path)
        self.state = get_battle_state(self.pyboy)
        self.total_reward = 0.0
        self.steps = 0
        return self.state

    def step(self, action):
        # Execute one time step within the environment
        play_action(self.pyboy, action)
        self.state = get_battle_state(self.pyboy)
        
        if is_battle_won(self.pyboy):
            reward = 1.0
            done = True
        elif is_battle_lost(self.pyboy):
            reward = -1.0
            done = True
        elif self.steps >= 500:
            reward = -0.5
            done = True
            print(f"Time out - {self.state_file}")
        else:
            reward = 0.0
            done = False
        
        self.steps += 1

        return self.state, reward, done, {}

    def fitness(self, genome, config):
        # Implement the fitness function for neat-python
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        total_fitness = 0.0
        for battle_num in range(BATTLE_PER_GENOM):
            state_file = self.reset()
            print(f"Start - Genome {genome.key} - Battle {battle_num + 1}/{BATTLE_PER_GENOM} - Loaded state: {self.state_file}")
            observation = self.state
            fitness = 0.0
            done = False
            while not done:
                action = net.activate(observation)
                action = max(action, key=abs)
                observation, reward, done, _ = self.step(int(action))
                fitness += reward
            total_fitness += fitness
            print(f"End - Genome {genome.key} - Battle {battle_num + 1}/{BATTLE_PER_GENOM}")
        print(f"Genome {genome.key} fitness: {total_fitness / BATTLE_PER_GENOM}")
        return total_fitness / BATTLE_PER_GENOM