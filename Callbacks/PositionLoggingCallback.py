import os
from stable_baselines3.common.callbacks import BaseCallback

class PositionLoggingCallback(BaseCallback):
    def __init__(self, log_dir, save_freq, verbose=0):
        super(PositionLoggingCallback, self).__init__(verbose)
        self.log_dir = log_dir
        self.save_freq = save_freq
        self.positions = []

    def _on_step(self) -> bool:
        # Get the current position from the environment
        env = self.training_env.envs[0]  # Access the first environment
        x, y, map_id = env.get_pos()
        self.positions.append((x, y, map_id))

        # Save positions to log file at specified frequency
        if self.n_calls % self.save_freq == 0:
            self._save_positions()

        return True

    def _on_training_end(self) -> None:
        # Save positions at the end of training
        self._save_positions()

    def _save_positions(self):
        log_file = os.path.join(self.log_dir, 'positions.log')
        with open(log_file, 'a') as f:
            for pos in self.positions:
                f.write(f"{pos}\n")
        self.positions = []