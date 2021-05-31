from math import floor, ceil
from TextGenerator import TFormats
from random import randint
from consts import Consts

class Weapon():
    def __init__(self, name, shots, damage, short_name = None, rarity= None) -> None:
        self.name = name
        self.short_name = short_name

        if rarity == None and not(self.name == "No weapon"):
            self.rarity = self.get_random_rarity()

        elif self.name == "No weapon":
            self.rarity = "common"
        else:
            self.rarity = rarity

        self.shots = shots
        self.bonus_damage = ceil(Consts.weapon_bonus_damage[self.rarity] / self.shots) if self.shots else 0
        self.damage = damage + self.bonus_damage
        self.status = 1

        if self.name == "No weapon":
            self.name = TFormats.red + "No weapon" + TFormats.end
            self.status = 0
       
    def get_random_rarity(self):
        chance = randint(0, 100)
        if chance <= 50:
            rarity = "uncommon"
            chance = randint(0, 100)

            if chance <= 50:
                rarity = "rare"
                chance = randint(0, 100)

                if chance <= 50:
                    rarity = "epic"
                    chance = randint(0, 100)

                    if chance <= 50:
                        rarity = "legendary"
                        chance = randint(0, 100)

                        if chance <= 50:
                            rarity = "common"
        else:
            rarity = "common"
        return rarity

    def calc_accuracy(self, skill):
        return(floor(4.75 * skill + 2))