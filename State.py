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
            active_pokemon["id"],
            TYPES_NAME_TO_ID[active_pokemon_stats["type1"]],
            TYPES_NAME_TO_ID[active_pokemon_stats["type2"]],
            active_pokemon["current_hp"],
            active_pokemon["max_hp"],
            active_pokemon["level"],
            active_pokemon["status"],

            # Player's Pokemon moves
            *[
                item
                for i in range(4)
                for item in (
                    active_pokemon["moves"][i]["id"],
                    moves_effectiveness[i],
                    moves_info[i]["effect"],
                    moves_info[i]["power"],
                    moves_info[i]["type"],
                    moves_info[i]["accuracy"],
                    moves_info[i]["pp"],
                    active_pokemon["pp_moves"][i]
                )
            ],


            #Party
            *[
                item
                for i in range(5)
                for item in (
                    pokemon_party[i]["id"],
                    pokemon_party[i]["type1"],
                    pokemon_party[i]["type2"],
                    pokemon_party[i]["current_hp"],
                    pokemon_party[i]["max_hp"],
                    pokemon_party[i]["level"],
                    pokemon_party[i]["status"]
                )
            ],

            # Enemy's Pokemon
            enemy_pokemon["id"],
            TYPES_NAME_TO_ID[enemy_pokemon_stats["type1"]],
            TYPES_NAME_TO_ID[enemy_pokemon_stats["type2"]],
            enemy_pokemon["current_hp"],
            enemy_pokemon["max_hp"]
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