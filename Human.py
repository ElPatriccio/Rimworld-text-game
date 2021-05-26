from TextGenerator import TextGenerator
from Health import Health
from Weapon import Weapon
from os import system
import random
import time

class Human():
    def __init__(self, name, gender, age, skill) -> None:
        self.name = name
        self.name_suffix = ""
        self.gender = gender
        self.age = age
        self.skill = skill
        self.health = Health(self)
        self.weapon = Weapon("No weapon", 0, 0)
    
    def reset_name_suffix(self):
        self.name_suffix = ""

    def has_weapon(self):
        return False if not(self.weapon.status) else True

    def shoot(self, target):
        TextGenerator().clear_terminal()
        accuracy =  self.weapon.calc_accuracy(self.skill) / target.health.protection
        print(self.name + " is shooting " + target.name + "!\n")
        time.sleep(2.5)

        hits = 0
        for i in range(0, self.weapon.shots): 
            chance = random.randint(0, 100)
            if chance <= accuracy:
                print("Hit!")
                hits += 1
                time.sleep(0.5)
            else:
                print("Miss!")
                time.sleep(0.5)

        print(str(accuracy)+"% Chance!")
        return target.health.take_damage(self.weapon.damage * hits)

class Colonist(Human):
    def __init__(self, name, gender, age, skill) -> None:
        super().__init__(name, gender, age, skill)
        self.type = "colonist"
    
    def equip_weapon(self, weapon):
        if self.has_weapon():
            x = self.weapon
        else:
            x = None
        
        self.weapon = weapon
        return [x, weapon]

class Enemy(Human):
    def __init__(self, name, gender, age, skill) -> None:
        super().__init__(name, gender, age, skill)
        self.type = "enemy"