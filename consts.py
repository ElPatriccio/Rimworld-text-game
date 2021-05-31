class Consts():
    number_of_colonists = 1
    number_of_weapons = 3
    number_of_enemies = all_enemies = 2
    silver = 500

    weapon_base = [
        ["Revolver", 1, 10, None],
        ["Bolt-Action-Rifle", 2, 8, "bar"],
        ["SMG", 3, 5, None],
    ]

    human_base = [
        ["Markus", "Male"],
        ["Anna", "Female"],
        ["Jens", "Female"],
        ["Noah", "Male"],
        ["Isaak", "Male"],
        ["Jakob", "Male"],
        ["Patrick", "deinemama"],
        ["Leo", "Male"],
    ]

    weapon_bonus_damage = {
        "common" : 0,
        "uncommon" : 5,
        "rare" : 10,
        "epic" : 15,
        "legendary" : 25,
    }

    # if None is passed in, it will be generated randomly (Default = None)
    settings = {
        "colonist_age" : None,
        "colonist_skill": 20,
        "enemy_age" : None,
        "enemy_skill" : None,
    }