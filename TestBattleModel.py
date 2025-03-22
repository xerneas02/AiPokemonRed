import pickle
import neat
import os
from Env.PokemonRedBattleEnv import PokemonRedBattleEnv
from Input import is_battle_won

# Charger le meilleur modèle depuis un simple fichier .pkl (pas un checkpoint compressé)

best_genome_path = './best_genomes/best_genome_gen_9.pkl'
config_path = os.path.join(os.path.dirname(__file__), 'config-feedforward')

# Charger la configuration NEAT
config = neat.Config(
    neat.DefaultGenome,
    neat.DefaultReproduction,
    neat.DefaultSpeciesSet,
    neat.DefaultStagnation,
    config_path
)

# Ouvrir directement le fichier en mode binaire et le charger avec pickle
with open(best_genome_path, 'rb') as f:
    best_genome = pickle.load(f)

# Initialiser l'environnement
rom_path = "Rom/pokered.gbc"
state_path = "State/battle/"
env = PokemonRedBattleEnv(rom_path, state_path, show_display=False)

# Créer le réseau de neurones
net = neat.nn.FeedForwardNetwork.create(best_genome, config)

# Variables pour les statistiques globales
nb_states = len(env.state_files)
nb_battles_per_state = 100
total_battles = nb_states * nb_battles_per_state
wins = 0
current_battle = 0

# Faire affronter chaque combat 10 fois, en traquant les victoires par state
for state_file in env.state_files:
    state_wins = 0
    for battle_num in range(nb_battles_per_state):
        current_battle += 1
        env.state_file = state_file
        print(f"Running battle {current_battle}/{total_battles} on state {state_file} - {battle_num+1}/{nb_battles_per_state}")
        
        # Reset l'environnement sur l'état en cours
        observation = env.reset()
        done = False

        # Boucle de jeu jusqu'à la fin du combat
        while not done:
            action = net.activate(observation)
            action = max(action, key=abs)
            observation, reward, done, _ = env.step(int(action))

        # Vérifier la victoire
        if is_battle_won(env.pyboy):
            wins += 1
            state_wins += 1
            print(f"Victory : {wins}/{current_battle}")
        else:
            print(f"Defeat  : {wins}/{current_battle}")

    # Calcul du pourcentage de victoire individuel pour ce state
    state_win_percentage = (state_wins / nb_battles_per_state) * 100
    print(f"\nRésultats pour l'état {state_file}: {state_wins}/10 victoires \
=> {state_win_percentage:.2f}% de victoires\n")

# Calculer le pourcentage de victoire global
win_percentage = (wins / total_battles) * 100
print(f"Le modèle a remporté {wins}/{total_battles} combats, soit {win_percentage:.2f}% de victoires au total.")
