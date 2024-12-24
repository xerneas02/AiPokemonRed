# Pokémon Red AI Project

## Overview

This project aims to develop an AI capable of playing Pokémon Red using reinforcement learning. The objective is to train the AI to navigate through the game, complete various tasks, and ultimately see how far it can progress.

## Project Structure

- **Env/**: Contains the custom environment for the Pokémon Red game.
  - `PokemonRedEnv.py`: Defines the custom Gym environment for Pokémon Red.
- **State/**: Contains various saved states of the game for training and testing.
- **Rom/**: Contains the ROM file for Pokémon Red.
- **Callbacks/**: Contains custom callback implementations.
  - `PositionLoggingCallback.py`: Logs the positions of the player during training.
- **Logs/**: Directory for storing logs and TensorBoard data.
- **Model/**: Directory for saving trained models.
- **GameFrame.py**: Preprocesses game frames for input into the neural network.
- **Constante.py**: Defines constants used throughout the project.
- **MemoryAdresse.py**: Contains memory addresses for accessing game data.
- **AccessMemory.py**: Functions for accessing and manipulating game memory.
- **ManualPlaying.py**: Script for manually playing the game using keyboard inputs.
- **TestModel.py**: Script for testing the trained model.
- **TrainModel.py**: Script for training the model.
- **requirement.txt**: List of required Python packages.

## Installation

1. **Clone the repository**:
```bash
git clone <repository_url>
cd <repository_directory>
```

2. **Install the required packages**:
```bash
pip install -r requirement.txt
```

3. **Download the Pokémon Red ROM** and place it in the `Rom/` directory.

## Usage

### Training the Model

To train the model, run the `TrainModel.py` script:

```bash
python TrainModel.py
```

This script will create a vectorized environment, define callbacks for logging and checkpointing, and train the PPO model using the custom Pokémon Red environment.

### Testing the Model

To test the trained model, run the `TestModel.py` script:

```bash
python TestModel.py
```

This script will load the trained model and run it in the environment, displaying the actions taken and rewards received.

### Manual Playing

To manually play the game using keyboard inputs, run the `ManualPlaying.py` script:

```bash
python ManualPlaying.py
```

This script allows you to control the game using predefined key mappings.

### Viewing Logs

To view the training logs using TensorBoard, run the following command:

```bash
tensorboard --logdir=Logs/PPO_PokemonRed
```

Then, open your web browser and navigate to `http://localhost:6006`.

## Key Mappings for Manual Playing

- `z`: Move up
- `q`: Move left
- `s`: Move down
- `d`: Move right
- `space`: Press 'A' button
- `shift`: Press 'B' button
- `a`: Press 'Start' button
- `e`: Press 'Select' button
- `r`: Save the game state

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.