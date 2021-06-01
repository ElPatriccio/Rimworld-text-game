from random import randint
from Weapon import Weapon
from Human import Colonist, Enemy
from consts import Consts

class ObjectSpawner():
    def __init__(self) -> None:
        self.number_colonists = Consts.number_of_colonists
        self.number_weapons = Consts.number_of_weapons
        self.number_enemies = self.all_enemies = Consts.number_of_enemies
        self.human_names = Consts.human_names
        self.weapon_base = Consts.weapon_base

        self.colonists = self.generate_people("colonist", self.number_colonists)
        self.weapons = self.generate_weapons(self.number_weapons)
        self.enemies = self.generate_people("enemy", self.number_enemies)
        self.silver = Consts.silver

    def rand(self, max):
        return randint(0, max - 1)

    def generate_people(self, type, max):
        people = []
        for i in range(0, max):
            if (age := Consts.settings[type]["age"]) == None:
                age = randint(16, 80)
            if (skill := Consts.settings[type]["skill"]) == None:
                skill = randint(0, 20)
            index = self.rand(len(self.human_names))

            if type == "colonist":
                people.append(Colonist(self.human_names[index][0], self.human_names[index][1], age, skill))

            elif type == "enemy":
                people.append(Enemy(self.human_names[index][0], self.human_names[index][1], age, skill))
            
            age = Consts.settings[type]["age"]
            skill = Consts.settings[type]["skill"]

        return people

    def generate_weapons(self, max):
        weapons = []
        for i in range (0, max):
            index = self.rand(len(self.weapon_base))
            weapons.append(Weapon(self.weapon_base[index][0], self.weapon_base[index][1], self.weapon_base[index][2], self.weapon_base[index][3]))
        return weapons