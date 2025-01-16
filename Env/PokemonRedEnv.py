import gym
from gym import spaces
import numpy as np
from pyboy import PyBoy
from AccessMemory import get_pos, get_pokemon_party_levels, set_pos  # Importe tes fonctions existantes4
from GameFrame import preprocess_frame
import os
import random

def get_random_state(directory = "State/starting_house"):    
    # Obtenir une liste de tous les fichiers dans le dossier
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    
    if not files:
        raise ValueError(f"Aucun fichier trouvé dans le dossier : {directory}")
    
    # Choisir un fichier au hasard
    random_file = random.choice(files)
    
    # Retourner le chemin complet vers le fichier
    return os.path.join(directory, random_file)


class PokemonRedEnv(gym.Env):
    def __init__(self, rom_path, show_display=False):
        super(PokemonRedEnv, self).__init__()

        # Initialize PyBoy
        window_type = "SDL2" if show_display else "null"
        self.pyboy = PyBoy(rom_path, window_type=window_type)
        if show_display:
            self.pyboy.set_emulation_speed(0)
        else:
            self.pyboy.set_emulation_speed(1_000_000)
        
        # Définir l'espace d'action (bouger dans 4 directions et 2 actions : "a" et "b")
        self.action_space = spaces.Discrete(6)
        
        # Définir l'espace d'observation, ici une image en niveaux de gris de taille (84, 84)
        self.observation_space = spaces.Box(low=0, high=255, shape=(84, 84, 1))
        self.observation_space.dtype = np.uint8
        self.steps = 0

        self.visited_positions = set()

        self.goals = {
            38: [(7, 1, 38)],
            37: [(2, 8, 37)]
        }
        self.coefficients = {
            38: 0.1,
            37: 1.0
        }
        self.current_goal_index = {map_id: 0 for map_id in self.goals}
        
        # Track the last action
        self.last_action = None
        self.repeat_action_count = 0

        # Track the last position and steps without discovering new positions
        self.last_position = None
        self.steps_without_new_position = 0
        self.max_steps_without_new_position = 100

        

    def reset(self):
        # Charger l'état de jeu de départ
        with open(get_random_state(), "rb") as state:
            self.pyboy.load_state(state)
        
        # Récupérer l'observation initiale
        observation = self._get_observation()
        self.steps = 0

        self.visited_positions.clear()

        # Reset action tracking
        self.last_action = None
        self.repeat_action_count = 0

        # Reset position tracking
        self.last_position = None
        self.steps_without_new_position = 0

        
        self.current_goal_index = {map_id: 0 for map_id in self.goals}

        x, y ,map_id = get_pos(self.pyboy)

        return observation
    
    def get_pos(self):
        return get_pos(self.pyboy)

    def step(self, action):
        # Convertir l'action en une action de bouton sur PyBoy
        self._apply_action(action)

        # Avancer d'un tick dans PyBoy
        self.pyboy.tick()

        # Obtenir l'observation suivante
        observation = self._get_observation()
        
        self.steps += 1

        # Vérifier si l'agent a découvert une nouvelle position
        x, y, map_id = get_pos(self.pyboy)
        current_position = (x, y, map_id)
        if current_position not in self.visited_positions:
            #self.visited_positions.add(current_position)
            self.steps_without_new_position = 0
        else:
            self.steps_without_new_position += 1

        # Calculer la récompense
        reward = self._calculate_reward(action)

        # Vérifier si l'épisode est terminé
        done = self._is_done()

        # Appliquer une pénalité si l'agent ne découvre pas de nouvelles positions pendant trop longtemps
        #if self.steps_without_new_position >= self.max_steps_without_new_position:
        #    reward -= 100  # Pénalité pour ne pas découvrir de nouvelles positions
        #    done = True


        return observation, reward, done, {}

    def _apply_action(self, action):
        actions = ["up", "down", "left", "right", "a", "b"]
        #print(actions[action])
        self.pyboy.button(actions[action])

    def _get_observation(self):
        # Prend un screenshot de l'écran actuel et le prétraite pour qu'il soit compatible avec ton CNN
        frame = self.pyboy.screen.ndarray
        return preprocess_frame(frame)
    

    ########################### Rewards ###########################
    def _calculate_exploration_reward(self, x, y, map_id):
        current_position = (x, y, map_id)
        if current_position not in self.visited_positions:
            self.visited_positions.add(current_position)
            return 1.0  # Maximum reward for discovering a new position
        return 0.0  # No reward for already visited positions

    def _calculate_goal_reward(self, x, y, map_id):
        if map_id in self.goals:
            goal_list = self.goals[map_id]
            goal_index = self.current_goal_index[map_id]
            if goal_index < len(goal_list):
                goal_x, goal_y, _ = goal_list[goal_index]
                distance_to_goal = abs(goal_x - x) + abs(goal_y - y)
                if (x, y) == (goal_x, goal_y):
                    self.current_goal_index[map_id] += 1  # Move to the next goal
                    return 1.0  # Maximum reward for reaching the goal
                return 1.0 / (distance_to_goal + 1)  # Reward inversely proportional to distance
            else:
                return -1.0  # Penalty for being on the map with no more goals
        return 0.0  # No reward if there are no goals for this map

    def _calculate_penalty_for_repeating_action(self, action):
        if action == self.last_action:
            self.repeat_action_count += 1
            return -0.1 * self.repeat_action_count  # Penalty increases with repetition
        else:
            self.repeat_action_count = 0
            self.last_action = action
            return 0.0  # No penalty for non-repeated actions

    def _calculate_reward(self, action):
        x, y, map_id = get_pos(self.pyboy)
        exploration_reward = self._calculate_exploration_reward(x, y, map_id)
        goal_reward = self._calculate_goal_reward(x, y, map_id)
        penalty_for_repeating_action = self._calculate_penalty_for_repeating_action(action)

        # Combine rewards with coefficients
        total_reward = (
            0.1  * exploration_reward +
            1.0  * goal_reward +
            0.0  * penalty_for_repeating_action +
            10.0 * (map_id == 0)  # Bonus for reaching the goal map
        )

        return total_reward

    def _is_done(self):
        # Logique pour vérifier la fin de l'épisode
        
        x, y, map_id = get_pos(self.pyboy)
        return self.steps >= 5000 # or map_id == 0

    def close(self):
        # Fermer PyBoy proprement
        self.pyboy.stop()
