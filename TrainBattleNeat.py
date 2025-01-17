import neat
import os
import pickle
from Env.PokemonRedBattleEnv import PokemonRedBattleEnv

def eval_genomes(genomes, config, env):
    for genome_id, genome in genomes:
        genome.fitness = env.fitness(genome, config)

def run_neat(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    rom_path = "Rom/Pokemon Red.gb"
    state_path = "State/starting_house/rattata_fight_1.state"
    env = PokemonRedBattleEnv(rom_path, state_path, show_display=False)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(lambda genomes, config: eval_genomes(genomes, config, env), n=50)
    print('\nBest genome:\n{!s}'.format(winner))

    # Save the winner
    with open('best_genome.pkl', 'wb') as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), 'config-feedforward')
    run_neat(config_path)