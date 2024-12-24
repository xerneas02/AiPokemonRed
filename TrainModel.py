from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import CheckpointCallback
from stable_baselines3.common.vec_env import SubprocVecEnv
from Env.PokemonRedEnv import PokemonRedEnv
from Callbacks.PositionLoggingCallback import PositionLoggingCallback
    
def make_env(rank, rom_path, show_display=False, seed=0):
    def _init():
        env = PokemonRedEnv(rom_path, show_display=show_display)
        env.seed(seed + rank)
        return env
    return _init

def main():
    rom_path = "Rom/Pokemon Red.gb"
    num_cpu = 8  # Number of processes to use
    ep_length = 2048 * 10
    sess_path = "Logs/PPO_PokemonRed"

    # Create the vectorized environment
    env = PokemonRedEnv(rom_path, show_display=False)

    # Define the checkpoint callback
    checkpoint_callback = CheckpointCallback(save_freq=ep_length, save_path='./Model/',
                                             name_prefix='ppo_pokemon_red')
    # Define the position logging callback
    position_logging_callback = PositionLoggingCallback(log_dir='./Logs', save_freq=ep_length)

    # Create and train the model
    model = PPO('CnnPolicy', env, verbose=1, n_steps=ep_length // 8, batch_size=128, n_epochs=3, ent_coef=0.1, gamma=0.998, tensorboard_log=sess_path)
    model.learn(total_timesteps=(ep_length)*num_cpu*5000, callback=[checkpoint_callback, position_logging_callback])

    # Save the final model
    model.save("Model/ppo_pokemon_red")

if __name__ == "__main__":
    main()