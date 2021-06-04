class Consts():
    ## SPAWN CONFIG ##

    # Name, shots per Round, base damage, short name, rarity
    weapon_base = [
        ["Revolver", 1, 10, None],
        ["Bolt-Action-Rifle", 2, 8, "bar"],
        ["SMG", 3, 5, None],
        ["Sniper-Rifle", 1, 20, "sr"],
        ["Chain-Shotgun", 3, 4, "cs"]
    ]

    #Name, gender
    human_names = [
        ["Markus", "Male"],
        ["Anna", "Female"],
        ["Jens", "Female"],
        ["Noah", "Male"],
        ["Isaak", "Male"],
        ["Jakob", "Male"],
        ["Patrick", "deinemama"],
        ["Leo", "Male"],
        ["Edi", "Male"],
        ["Rick", "Male"],
    ]

    ## SETTINGS ##
    
    number_of_colonists = 3
    number_of_weapons = 3
    number_of_enemies = all_enemies = 2
    silver = 500

    # if None is passed in, it will be generated randomly (Default = None)
    settings_colonist = {
        "age" : None,
        "skill": None,
    }

    settings_enemy = {
        "age" : None,
        "skill" : None,
    }

    settings_health = {
        "downed-hp" : 15
    }

    settings = {
        "colonist" : settings_colonist,
        "enemy" : settings_enemy,
        "health" : settings_health,
    }

    weapon_bonus_damage = {
        "common" : 0,
        "uncommon" : 5,
        "rare" : 10,
        "epic" : 15,
        "legendary" : 25,
    }

    