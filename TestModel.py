import os
import glob
import neat
import pickle
from graphviz import Digraph
from Env.PokemonRedBattleEnv import PokemonRedBattleEnv

def get_most_recent_model(model_dir):
    list_of_files = glob.glob(os.path.join(model_dir, '*.pkl'))  # Adjust the extension if needed
    if not list_of_files:
        raise FileNotFoundError("No model files found in the directory.")
    latest_file = max(list_of_files, key=os.path.getctime)
    return latest_file

def load_best_genome(file_path):
    with open(file_path, 'rb') as f:
        best_genome = pickle.load(f)
    return best_genome

def visualize_network(genome, config):
    node_names = {0: 'Output'}
    for i in range(1, 13):  # Assuming 12 inputs
        node_names[-i] = f'Input {i}'

    dot = Digraph(format='png')
    for node in genome.nodes:
        if node in node_names:
            dot.node(str(node), node_names[node])
        else:
            dot.node(str(node), str(node))

    for cg in genome.connections.values():
        if cg.enabled:
            dot.edge(str(cg.key[0]), str(cg.key[1]))

    dot.render('network', view=True)

def test_best_genome(best_genome_file, config_file, rom_path, state_path):
    # Load the best genome
    best_genome = load_best_genome(best_genome_file)

    # Load the NEAT configuration
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Visualize the neural network
    visualize_network(best_genome, config)

    # Create the environment
    env = PokemonRedBattleEnv(rom_path, state_path, show_display=True)

    # Create the neural network from the best genome
    net = neat.nn.FeedForwardNetwork.create(best_genome, config)

    # Run the best genome in the environment
    observation = env.reset()
    done = False
    total_reward = 0.0
    while not done:
        action = net.activate(observation)
        action = max(action, key=abs)
        observation, reward, done, _ = env.step(int(action))
        total_reward += reward
        print(f"Action: {action}, Reward: {reward}, Total Reward: {total_reward}")

    print(f"Total Reward for Best Genome: {total_reward}")

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), 'config-feedforward')
    best_genome_file = get_most_recent_model('./best_genomes')  # Change this to the path of your best genome file
    rom_path = "Rom/Pokemon Red.gb"
    state_path = "State/battle/"
    test_best_genome(best_genome_file, config_path, rom_path, state_path)