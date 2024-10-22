ImageSize = 84
Ncouleur = 4
action_space = ["up", "down", "left", "right", "a", "b"]

poke_id_to_name = {
    177: "Squirtle",
    255: "None",
    0: "None",
    165: "Rattata",
    36: "Pidgey",
    179: "Wartortle",
    150: "Pidgeotto",
    112: "Weedle",
    113: "Kakuna",
    114: "Beedrill",
    133: "Magikarp",
    169: "Geodude",
    107: "Zubat",
    109: "Paras",
    100: "Jigglypuff",
    84: "Pikachu",
    123: "Caterpie",
    124: "Metapod",
    4: "Clefairy",
    5: "Spearow",
    15: "Nidoran♀"
}
valid_list = [name for name in poke_id_to_name.values() if name != 'None']

place_label = {
    0:"PalletTown",
    1:"ViridianCity",
    12:"Road1",
    37:"HomeFloor",
    38:"StartingRoom",
    40:"Lab",
    42:"PokeMartViridianCity"
}

position_label = {
    (3, 6, 38):"StartingPos",
    (7, 1, 38):"ExitRoom",
    (2, 8, 37):"ExitHome",
    (3, 8, 37):"ExitHome",
    (10,3, 0 ):"EnterRoad1",
    (11,3, 0 ):"EnterRoad1",
    (7, 4, 40):"Squirtle",
    (10,0, 12):"ExitRoad1",
    (11,0, 12):"ExitRoad1",
    (29,20, 1):"MartEntrance"
}

