import gym
from gym import spaces
import numpy as np
from pyboy import PyBoy
from AccessMemory import get_pos, get_pokemon_party_levels  # Importe tes fonctions existantes4
from GameFrame import preprocess_frame

class PokemonRedEnv(gym.Env):
    def __init__(self, rom_path, show_display=False):
        super(PokemonRedEnv, self).__init__()

        # Initialize PyBoy
        self.pyboy = PyBoy(rom_path, window_type="null" if not show_display else "SDL2")
        if show_display:
            self.pyboy.set_emulation_speed(0)
        else:
            self.pyboy.set_emulation_speed(1_000_000)
        
        # Définir l'espace d'action (bouger dans 4 directions et 2 actions : "a" et "b")
        self.action_space = spaces.Discrete(6)  # 4 directions + "a" + "b"
        
        # Définir l'espace d'observation, ici une image en niveaux de gris de taille (84, 84)
        self.observation_space = spaces.Box(low=0, high=255, shape=(84, 84, 1))
        self.observation_space.dtype = np.uint8  # Définissez manuellement le dtype si nécessaire


    def reset(self):
        # Charger l'état de jeu de départ
        with open("State/starting_state.state", "rb") as state:
            self.pyboy.load_state(state)
        
        # Récupérer l'observation initiale
        observation = self._get_observation()
        return observation

    def step(self, action):
        # Convertir l'action en une action de bouton sur PyBoy
        self._apply_action(action)
        
        # Avancer d'un tick dans PyBoy
        self.pyboy.tick()
        
        # Obtenir l'observation suivante
        observation = self._get_observation()
        
        # Calculer la récompense
        reward = self._calculate_reward()
        
        # Vérifier si l'épisode est terminé
        done = self._is_done()
        
        return observation, reward, done, {}

    def _apply_action(self, action):
        actions = ["up", "down", "left", "right", "a", "b"]
        self.pyboy.button(actions[action])

    def _get_observation(self):
        # Prend un screenshot de l'écran actuel et le prétraite pour qu'il soit compatible avec ton CNN
        frame = self.pyboy.screen.ndarray
        return preprocess_frame(frame)

    def _calculate_reward(self):
        # Définir la logique de récompense, par exemple en fonction de la position ou du niveau des Pokémon
        party_levels = get_pokemon_party_levels(self.pyboy)
        reward = sum(party_levels)  # Par exemple, une récompense basée sur le niveau total des Pokémon
        return reward

    def _is_done(self):
        # Logique pour vérifier la fin de l'épisode
        # Par exemple, si le joueur est dans une certaine position ou après un certain nombre de frames
        x, y, map_id = get_pos(self.pyboy)
        return map_id == 1  # Ex: Fin de l'épisode si le joueur est arrivé dans une zone spécifique

    def close(self):
        # Fermer PyBoy proprement
        self.pyboy.stop()
