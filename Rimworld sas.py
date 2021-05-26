from Weapon import Weapon
import random
from consts import Consts, ObjectSpawner
import time
from math import floor
from TextGenerator import TextGenerator

battle_not_over = True

text_generator = TextGenerator()

class RimWorld():
    __game_cases = {
        "vcs" : 0,
        "vew" : 1,
        "ew" : 2,
        "ves": 3,
        "eb" : 4,
    }

    __battle_cases = {
        "vs" : 0,
        "ew" : 1,
        "se" : 2,
        "hbc" : 3,
        "rc" : 4,
    }

    def __init__(self, colonists, silver, weapons, enemies) -> None:
        self.colonists = colonists
        self.silver = silver
        self.weapons = weapons
        self.enemies = enemies

        for e in self.enemies:
            e.weapon = ObjectSpawner().generate_weapons(1)[0]

        text_generator.clear_terminal()
        print(text_generator.get_start_message(len(self.colonists), len(self.weapons), self.silver, len(self.enemies)))
        time.sleep(4)
        self.advance_game()

    def advance_game(self):
        text_generator.clear_terminal()
        action = input(text_generator.get_action_menue())

        if self.__game_cases.get(action, None) != None:
            action = self.__game_cases[action]
            if action == 0:
                text_generator.clear_terminal()
                print(text_generator.view_people_stats("colonist", self.colonists))
                input(text_generator.get_press_enter())
            
            elif action == 1:
                text_generator.clear_terminal()
                print(text_generator.view_equipable_weapons(self.weapons))
                input(text_generator.get_press_enter())

            elif action == 2:
                text_generator.clear_terminal()
                self.give_weapon_to_colonist()

            elif action == 3:
                text_generator.clear_terminal()
                print(text_generator.view_people_stats("enemy", self.enemies))
                input(text_generator.get_press_enter())

            elif action == 4:
                term = input(text_generator.get_attack_enemies())
                if  term == "y":
                    self.advance_battle()
                else:
                    self.advance_game()

        self.advance_game()
    
    def advance_battle(self, colonist = None):
        battle_status = 0
        while battle_status < 1:            
            battle_status = self.advance_battle_loop(colonist)
            
        text_generator.clear_terminal()

        for c in self.colonists:
            c.health.reset_protection()

        for e in self.enemies:
            e.health.reset_protection()

        if battle_status == 1: # All colonists dead
            print("You loose!")

        elif battle_status == 2: # All enemies dead
            print("You win!")

        elif battle_status == 3: # Enemies fled
            print("Enemies are fleeing!")
        
        time.sleep(3)               
                    
    def advance_battle_loop(self, colonist):
        for c in self.colonists:
            c.health.reset_protection()
            text_generator.clear_terminal()
            if colonist == c or not colonist:
                if c.health.status == "Alive":
                    action = input(text_generator.get_battle_action_menue(c.name))
                    
                    if self.__battle_cases.get(action, None) != None:
                        action = self.__battle_cases[action]
                        if action == 0:
                            text_generator.clear_terminal()
                            print(text_generator.view_people_stats("colonist", self.colonists, c))
                            input(text_generator.get_press_enter())
                            self.advance_battle_loop(c)
                            
                        
                        elif action == 1:
                            text_generator.clear_terminal()
                            self.give_weapon_to_colonist(c)

                        elif action == 2:
                            text_generator.clear_terminal()
                            print(text_generator.header("Who do you want to shoot?"))
                            print(text_generator.view_people_stats("enemy", self.enemies, is_menue= True)) 
                            target = self.find_enemy(input("Name: "))

                            if target == None:
                                print(text_generator.error("Person you want to shoot does not exist! Try again!"))
                                time.sleep(2)
                                self.advance_battle_loop(c)
                            print(c.shoot(target))
                            time.sleep(3)

                        elif action == 3:
                            text_generator.clear_terminal()
                            print(c.health.get_cover(c.name))
                            time.sleep(2.5)
                    else:
                        self.advance_battle_loop(c)

        alive_enemies = self.get_alive_enemies()
        if alive_enemies == -1:
            return 2

        chance = random.randint(0, 100)
        if chance >= ((alive_enemies / Consts.enemyMoral) * 100) and alive_enemies >= 1:
            return 3   

        if not colonist:
            for e in self.enemies:
                e.health.reset_protection()
                action = random.randint(0, 2)
                text_generator.clear_terminal()
                if e.health.status == "Alive": 
                    if action < 2:
                        target = self.colonists[random.randint(0, len(self.colonists) - 1)]
                        print(e.shoot(target))
                        time.sleep(3)

                    elif action == 2:
                        print(e.health.get_cover(e.name))
                        time.sleep(2.5)
        
        alive_colonists = self.get_alive_colonists()
        if alive_colonists == 0:
            return 1
        return 0 
        

    def find_colonist(self, colonist):
        for c in self.colonists:
            if c.name == colonist:
                return c
        return None 

    def get_alive_colonists(self):
        num = 0
        for c in self.colonists:
            if c.health.status == "Alive":
                num +=1
        return num
    
    def find_weapon(self, weapon):
        for w in self.weapons:
            if w.name == weapon or w.short_name == weapon:
                return w
        return None
    
    def give_weapon_to_colonist(self, colonist = None):
        print(text_generator.header("Which weapon do you want to equip?"))
        print(text_generator.view_equipable_weapons(self.weapons, is_menue = True))
        weapon = self.find_weapon(input("Weapon: "))
        text_generator.clear_terminal()

        if not colonist:
            print(text_generator.header("Whom do you want to give the weapon?"))
            print(text_generator.view_people_stats("colonist", self.colonists, is_menue = True))
            colonist = self.find_colonist(input("Name: "))
            text_generator.clear_terminal()

        if weapon and colonist:
            x = colonist.equip_weapon(weapon)
            if x[0]:
                self.weapons.append(x[0])
            self.weapons.remove(x[1])
            print(text_generator.weapon_equipped(colonist.name, weapon.name, weapon.rarity))
            time.sleep(3)

        else:
            print(text_generator.error("Colonist or Weapon was not found! Try again!"))
            time.sleep(2.5)
            text_generator.clear_terminal()
            self.give_weapon_to_colonist(colonist)
    
    def find_enemy(self, enemy):
        for e in self.enemies:
            if e.name == enemy:
                return e
        return None 
    
    def get_alive_enemies(self):
        num = 0
        for e in self.enemies:
            if e.health.status == "Alive":
                num+=1
        if num == 0:
            return -1
        return num

if __name__ == "__main__":
    world = RimWorld(Consts.colonists, Consts.silver, Consts.weapons, Consts.enemies)