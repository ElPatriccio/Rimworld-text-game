from Human import Colonist, Enemy
from Weapon import Weapon
from random import randint 

# SPAWN VALUES
number_colonists = 0
number_enemies = 0
number_weapons = 5

weapon_base = [
        ["Revolver", 1, 10, None],
        ["Bolt-Action-Rifle", 2, 8, "bar"],
        ["SMG", 3, 5, None],
    ]

def rand(max):
    return randint(0, max)

def generate_colonists():
    pass

def generate_ememies():
    pass

def generate_weapons():
    weapons = []
    for i in range (0, number_weapons):
        index = rand(len(weapon_base) - 1)
        weapons.append(Weapon(weapon_base[index][0], weapon_base[index][1], weapon_base[index][2], weapon_base[index][3]))
    return weapons


class Consts():
    colonists = [
        Colonist("Markus", "Male", 26, 20), 
        Colonist("Anna", "Female", 46, 9), 
        #Colonist("Fred", "Male", 77, 0)
        ]
    
    #weapons = generate_weapons()
    weapons = [
        Weapon("Revolver", 1, 10),
        Weapon("Bolt-Action-Rifle", 2, 8, "bar"),
        Weapon("SMG", 3, 5)
    ]
    enemies = [
        Enemy("Huso", "Male", 32, 10),
        Enemy("Kek", "Female", 19, 10)
    ]

    silver = 500

    enemyMoral = len(enemies)