import os
import glob
from stable_baselines3 import PPO
from Env.PokemonRedEnv import PokemonRedEnv

def get_most_recent_model(model_dir):
    list_of_files = glob.glob(os.path.join(model_dir, '*.zip'))  # Adjust the extension if needed
    if not list_of_files:
        raise FileNotFoundError("No model files found in the directory.")
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def play():
    # Create the environment
    env = PokemonRedEnv("Rom/Pokemon Red.gb", show_display=True)

    # Get the most recent model file
    model_file = get_most_recent_model("Model")

    print("Model file: ", model_file)

    # Load the trained model
    model = PPO.load(model_file, env=env)

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