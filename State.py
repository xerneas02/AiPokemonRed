from Constante import *
from AccessMemory import *
import numpy as np
import pyboy
from copy import deepcopy


def get_battle_state(pyboy : pyboy.PyBoy):
        active_pokemon = get_active_pokemon_info(pyboy)
        enemy_pokemon  = get_enemy_info(pyboy)

        pokemon_name = pokemon_id_to_name(active_pokemon["id"])
        active_pokemon_stats = POKEMON_BASE_STATS[pokemon_name]

        enemy_pokemon_name = pokemon_id_to_name(enemy_pokemon["id"])
        enemy_pokemon_stats = POKEMON_BASE_STATS[enemy_pokemon_name]

        moves_names = [MOVES_ID_TO_NAME[active_pokemon["moves"][i]["id"]] for i in range(4)]
        moves_info = deepcopy(active_pokemon["moves"])

        for i in range(len(moves_info)):
            if type(moves_info[i]["type"]) is not int:
                moves_info[i]["type"] = TYPES_NAME_TO_ID[moves_info[i]["type"]]
            if type(moves_info[i]["effect"]) is not int:
                moves_info[i]["effect"] = MOVE_EFFECT_TO_ID[moves_info[i]["effect"]]

        moves_effectiveness = [get_effectiveness(moves_info[i]["type"], enemy_pokemon_stats["type1"], enemy_pokemon_stats["type2"]) for i in range(4)]
        
        pokemon_party = []
        main_pokemon_found = False
        for i in range(6):
            poke_info = get_pokemon_info(pyboy, i)

            pokemon_name = pokemon_id_to_name(poke_info["id"])
            pokemon_stats = POKEMON_BASE_STATS[pokemon_name]

            if poke_info["id"] != active_pokemon["id"] or main_pokemon_found:
                   poke_info["type1"] = TYPES_NAME_TO_ID[pokemon_stats["type1"]]
                   poke_info["type2"] = TYPES_NAME_TO_ID[pokemon_stats["type2"]]

                   pokemon_party.append(poke_info)
            else:
                   main_pokemon_found = True


        state = np.array([
            # Player's Pokemon
            active_pokemon["id"],                                           # 0
            TYPES_NAME_TO_ID[active_pokemon_stats["type1"]],                # 1
            TYPES_NAME_TO_ID[active_pokemon_stats["type2"]],                # 2
            active_pokemon["current_hp"],                                   # 3
            active_pokemon["max_hp"],                                       # 4            
            active_pokemon["level"],                                        # 5             
            active_pokemon["status"],                                       # 6                

            # Player's Pokemon moves
            *[
                item
                for i in range(4)
                for item in (
                    active_pokemon["moves"][i]["id"],                       # 7 - 15 - 23 - 31
                    moves_effectiveness[i],                                 # 8 - 16 - 24 - 32
                    moves_info[i]["effect"],                                # 9 - 17 - 25 - 33
                    moves_info[i]["power"],                                 # 10 - 18 - 26 - 34
                    moves_info[i]["type"],                                  # 11 - 19 - 27 - 35
                    moves_info[i]["accuracy"],                              # 12 - 20 - 28 - 36
                    moves_info[i]["pp"],                                    # 13 - 21 - 29 - 37
                    active_pokemon["pp_moves"][i]                           # 14 - 22 - 30 - 38
                )
            ],


            #Party
            *[
                item
                for i in range(5)
                for item in (
                    pokemon_party[i]["id"],                                 # 39 - 46 - 53 - 60 - 67
                    pokemon_party[i]["type1"],                              # 40 - 47 - 54 - 61 - 68
                    pokemon_party[i]["type2"],                              # 41 - 48 - 55 - 62 - 69
                    pokemon_party[i]["current_hp"],                         # 42 - 49 - 56 - 63 - 70
                    pokemon_party[i]["max_hp"],                             # 43 - 50 - 57 - 64 - 71     
                    pokemon_party[i]["level"],                              # 44 - 51 - 58 - 65 - 72
                    pokemon_party[i]["status"]                              # 45 - 52 - 59 - 66 - 73
                )
            ],

            # Enemy's Pokemon
            enemy_pokemon["id"],                                            # 74
            TYPES_NAME_TO_ID[enemy_pokemon_stats["type1"]],                 # 75    
            TYPES_NAME_TO_ID[enemy_pokemon_stats["type2"]],                 # 76
            enemy_pokemon["current_hp"],                                    # 77
            enemy_pokemon["max_hp"]                                         # 78
        ])

        return state


def print_state(state):
    index = 0

    def get_next():
        nonlocal index
        value = state[index]
        index += 1
        return value

    def get_next_n(n):
        return [get_next() for _ in range(n)]

    print("Player's Active Pokémon:")
    print(f"  ID: {POKEMON_ID_TO_NAME[get_next()]}")
    print(f"  Type 1: {TYPES_ID_TO_NAME[get_next()]}")
    print(f"  Type 2: {TYPES_ID_TO_NAME[get_next()]}")
    print(f"  Current HP: {get_next()}")
    print(f"  Max HP: {get_next()}")
    print(f"  Level: {get_next()}")
    print(f"  Status: {get_next()}")

    print("  Moves:")
    for i in range(4):
        print(f"    Move {i+1}:")
        print(f"      ID: {MOVES_ID_TO_NAME[get_next()]}")
        print(f"      Effectiveness: {get_next()}")
        print(f"      Effect: {get_next()}")
        print(f"      Power: {get_next()}")
        print(f"      Type: {TYPES_ID_TO_NAME[get_next()]}")
        print(f"      Accuracy: {get_next()}")
        print(f"      PP: {get_next()}")
        print(f"      Current PP: {get_next()}")

    print("Player's Pokémon Party:")
    for i in range(5):
        print(f"  Pokémon {i+1}:")
        print(f"    ID: {POKEMON_ID_TO_NAME[get_next()]}")
        print(f"    Type 1: {TYPES_ID_TO_NAME[get_next()]}")
        print(f"    Type 2: {TYPES_ID_TO_NAME[get_next()]}")
        print(f"    Current HP: {get_next()}")
        print(f"    Max HP: {get_next()}")
        print(f"    Level: {get_next()}")
        print(f"    Status: {get_next()}")

    print("Enemy's Pokémon:")
    print(f"  ID: {POKEMON_ID_TO_NAME[get_next()]}")
    print(f"  Type 1: {TYPES_ID_TO_NAME[get_next()]}")
    print(f"  Type 2: {TYPES_ID_TO_NAME[get_next()]}")
    print(f"  Current HP: {get_next()}")
    print(f"  Max HP: {get_next()}")