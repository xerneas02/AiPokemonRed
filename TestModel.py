from stable_baselines3 import PPO
from Env.PokemonRedEnv import PokemonRedEnv

def play():
    # Create the environment
    env = PokemonRedEnv("Rom/Pokemon Red.gb", show_display=True)

    # Load the trained model
    model = PPO.load("Model/ppo_pokemon_red", env=env)

    # Reset the environment
    obs = env.reset()

    # Play the game
    done = False
    while True:
        # Predict the next action
        action, _states = model.predict(obs, deterministic=True)
        #print(action)
        # Take the action in the environment
        obs, reward, done, info = env.step(action)

        print("Reward:", reward)
        if done:
            obs = env.reset()

    # Close the environment
    env.close()

if __name__ == "__main__":
    play()