from stable_baselines3 import PPO
from Env.PokemonRedEnv import PokemonRedEnv

env = PokemonRedEnv("Rom/Pokemon Red.gb", show_display=False)

# Créer et entraîner le modèle
model = PPO("CnnPolicy", env, verbose=1)
model.learn(total_timesteps=100000)

# Sauvegarder le modèle
model.save("Model/ppo_pokemon_red")
