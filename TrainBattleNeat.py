import neat
import os
import pickle
from Env.PokemonRedBattleEnv import PokemonRedBattleEnv
from Callbacks import BestGenomeSaver
from multiprocessing import Pool, cpu_count, Manager

def eval_genome(genome_config_tuple):
    genome, config, rom_path, state_path, progress_counter = genome_config_tuple
    env = PokemonRedBattleEnv(rom_path, state_path, show_display=False, progress_counter=progress_counter)
    genome.fitness = env.fitness(genome, config)
    if genome.fitness is None:
        genome.fitness = 0.0
    
    progress_counter.value += 1
    print(f"Genome {genome.key} fitness: {genome.fitness}")
    return genome

def eval_genomes(genomes, config, rom_path, state_path, progress_counter):
    genome_config_tuples = [(genome, config, rom_path, state_path, progress_counter) for genome_id, genome in genomes]
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(eval_genome, genome_config_tuples)
    for genome, result in zip(genomes, results):
        #print(f"Genome {genome[1].fitness} result: {result.fitness}")
        genome[1].fitness = result.fitness
        print(f"Genome {genome[1].key} fitness: {genome[1].fitness}")
    
def eval_genomes_sequential(genomes, config, rom_path, state_path, progress_counter):
    for genome_id, genome in genomes:
        eval_genome((genome, config, rom_path, state_path, progress_counter))


def run_neat(config_file):
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    rom_path = "Rom/Pokemon Red.gb"
    state_path = "State/battle/"

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Add the custom reporter to save the best genome
    best_genome_saver = BestGenomeSaver(save_path='./best_genomes')
    p.add_reporter(best_genome_saver)

    manager = Manager()
    progress_counter = manager.Value('i', 0)

    def eval_genomes_with_progress(genomes, config):
        progress_counter.value = 0
        eval_genomes(genomes, config, rom_path, state_path, progress_counter)
        print(f"Evaluated {progress_counter.value} genomes")

    winner = p.run(eval_genomes_with_progress, n=50)
    if winner is not None:
        print(f'\nBest genome:\n{winner}')
    else:
        print('No winner found.')

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), 'config-feedforward')
    run_neat(config_path)