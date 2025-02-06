import neat
import os
import pickle

class BestGenomeSaver(neat.reporting.BaseReporter):
    def __init__(self, save_path):
        self.save_path = save_path

    def post_evaluate(self, config, population, species, best_genome):
        # Save the best genome of the generation
        with open(os.path.join(self.save_path, f'best_genome_gen_{population.generation}.pkl'), 'wb') as f:
            pickle.dump(best_genome, f)
        print(f'Saved best genome of generation {population.generation}')