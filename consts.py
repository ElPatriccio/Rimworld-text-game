from Human import Colonist, Enemy
from Weapon import Weapon
from random import randint 


number_of_colonists = 1
number_of_weapons = 3
number_of_enemies = 3

class ObjectSpawner():
    def __init__(self, num_colonists = 3, num_weapons = 3, num_enemies = 2) -> None:
        self.number_colonists = num_colonists
        self.number_weapons = num_weapons
        self.number_enemies = num_enemies
    
        self.weapon_base = [
            ["Revolver", 1, 10, None],
            ["Bolt-Action-Rifle", 2, 8, "bar"],
            ["SMG", 3, 5, None],
        ]

        self.human_base = [
            ["Markus", "Male"],
            ["Anna", "Female"],
            ["Jens", "Female"],
            ["Noah", "Male"],
            ["Isaak", "Male"],
            ["Jakob", "Male"],
            ["Patrick", "deinemama"],
            ["Leo", "Male"],
        ]

    def rand(self, max):
        return randint(0, max - 1)

    def generate_people(self, type, max):
        people = []
        for i in range(0, max):
            age = randint(16, 80)
            skill = randint(0, 20)
            index = self.rand(len(self.human_base))

            if type == "colonist":
                people.append(Colonist(self.human_base[index][0], self.human_base[index][1], age, skill))

            elif type == "enemy":
                people.append(Enemy(self.human_base[index][0], self.human_base[index][1], age, skill))

        return people

    def generate_weapons(self, max):
        weapons = []
        for i in range (0, max):
            index = self.rand(len(self.weapon_base))
            weapons.append(Weapon(self.weapon_base[index][0], self.weapon_base[index][1], self.weapon_base[index][2], self.weapon_base[index][3]))
        return weapons

object_spawner = ObjectSpawner(number_of_colonists, number_of_weapons, number_of_enemies)
class Consts():
    colonists = object_spawner.generate_people("colonist", object_spawner.number_colonists)
    weapons = object_spawner.generate_weapons(object_spawner.number_weapons)
    enemies = object_spawner.generate_people("enemy", object_spawner.number_enemies)
    silver = 500
    enemyMoral = len(enemies)