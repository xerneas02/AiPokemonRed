import neat
import numpy as np
from pyboy import PyBoy
from AccessMemory import *
from Constante import *

class PokemonRedBattleEnv:
    def __init__(self, rom_path, state_path, show_display=False):
        # Initialize PyBoy
        window_type = "SDL2" if show_display else "null"
        self.pyboy = PyBoy(rom_path, window_type=window_type)
        if show_display:
            self.pyboy.set_emulation_speed(0)
        else:
            self.pyboy.set_emulation_speed(1_000_000)

        # Load the state
        with open(state_path, "rb") as game_state:
            self.pyboy.load_state(game_state)

    

    def reset(self):
        # Reset the state of the environment to an initial state
        with open(self.state_path, "rb") as game_state:
            self.pyboy.load_state(game_state)

        self.state = np.zeros((12,), dtype=np.uint8)  # Example initial state
        return self.state

    def step(self, action):
        # Execute one time step within the environment
        self.state = np.random.randint(0, 256, (12,), dtype=np.uint8)
        reward = np.random.rand()
        done = np.random.choice([True, False])
        return self.state, reward, done, {}

    def fitness(self, genome, config):
        # Implement the fitness function for neat-python
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        observation = self.reset()
        fitness = 0.0
        done = False
        while not done:
            action = net.activate(observation)
            action = max(action, key=abs)
            observation, reward, done, _ = self.step(int(action))
            fitness += reward
        return fitness