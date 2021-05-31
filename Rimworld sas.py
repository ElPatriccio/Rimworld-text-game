import random
from consts import Consts
from ObjectSpawner import ObjectSpawner
import time
from TextGenerator import TextGenerator

battle_not_over = True

class RimWorld():
    # TODO __game_cases serves no use other than summarizing all possibilities to the devs -> Comment all ifs with its purpose 
    __game_cases = {
        "vcs" : 0,
        "vew" : 1,
        "ew" : 2,
        "ves": 3,
        "eb" : 4,
        "ied": 5,
    }
    # TODO __battle_cases serves no use other than summarizing all possibilities to the devs -> Comment all ifs with its purpose
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

        TextGenerator().clear_terminal()
        print(TextGenerator().get_start_message(len(self.colonists), len(self.weapons), self.silver, len(self.enemies)))
        time.sleep(4)
        self.advance_game()
    

    def advance_game(self, action = None):
        TextGenerator().clear_terminal()
        if not action:
            action = input(TextGenerator().get_action_menue())

        if self.__game_cases.get(action, None) != None:
            if action == "vcs":
                TextGenerator().clear_terminal()
                print(TextGenerator().view_people_stats("colonist", self.colonists)) 
                if c := input(TextGenerator().get_press_enter(text = "Name")): 
                    if not(c := self.find_colonist(c)):
                        TextGenerator().perform_error_message("Colonist was not found! Try again!")
                        self.advance_game(action = "vcs")
                    else:
                        self.give_weapon_to_colonist(colonist = c)
            
            elif action == "vew":
                TextGenerator().clear_terminal()
                print(TextGenerator().view_equipable_weapons(self.weapons))
                if w:= input(TextGenerator().get_press_enter(text = "Weapon")):
                    if not(w := self.find_weapon(w)):
                        TextGenerator().perform_error_message("Weapon was not found! Try again!")
                        self.advance_game(action = "vew")
                    else:
                        self.give_weapon_to_colonist(weapon= w)

            elif action == "ew":
                TextGenerator().clear_terminal()
                self.give_weapon_to_colonist()                    

            elif action == "ves":
                TextGenerator().clear_terminal()
                print(TextGenerator().view_people_stats("enemy", self.enemies))
                input(TextGenerator().get_press_enter())

            elif action == "eb":
                term = input(TextGenerator().get_attack_enemies())
                if  term == "y":
                    self.advance_battle()
                else:
                    self.advance_game()
            
            elif action == "ied":
                TextGenerator().clear_terminal()
                print(TextGenerator().header("Allah ist groß"))
                time.sleep(3)
                TextGenerator().clear_terminal()
                print("soos")
                time.sleep(0.5)
                TextGenerator().clear_terminal()

        self.advance_game()
    
    def advance_battle(self, colonist = None):
        battle_status = 0
        while battle_status < 1:            
            battle_status = self.advance_battle_loop(colonist)
            
        TextGenerator().clear_terminal()

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
            TextGenerator().clear_terminal()
            if colonist == c or not colonist:
                if c.health.status == "Alive":
                    action = input(TextGenerator().get_battle_action_menue(c.name))
                    
                    if self.__battle_cases.get(action, None) != None:
                        if action == "vs":
                            TextGenerator().clear_terminal()
                            print(TextGenerator().view_people_stats("colonist", self.colonists, c))
                            if input(TextGenerator().get_press_enter(text= c.name)):
                                TextGenerator().clear_terminal()
                                if error := self.give_weapon_to_colonist(c):
                                    self.advance_battle_loop(c)
                            else:
                                self.advance_battle_loop(c)
                            
                        
                        elif action == "ew":
                            TextGenerator().clear_terminal()
                            if error := self.give_weapon_to_colonist(c):
                                self.advance_battle_loop(c)

                        elif action == "se":
                            TextGenerator().clear_terminal()
                            print(TextGenerator().header("Who do you want to shoot?"))
                            print(TextGenerator().view_people_stats("enemy", self.enemies, is_menue= True)) 
                            target = self.find_enemy(input("Name: "))

                            if target == None:
                                TextGenerator().clear_terminal()
                                print(TextGenerator().error("Person you want to shoot does not exist! Try again!"))
                                time.sleep(2)
                                self.advance_battle_loop(c)
                            print(c.shoot(target))
                            time.sleep(3)

                        elif action == "hbc":
                            TextGenerator().clear_terminal()
                            print(c.health.get_cover(c.name))
                            time.sleep(2.5)
                    else:
                        self.advance_battle_loop(c)

        alive_enemies = self.get_alive_enemies()
        if alive_enemies == -1:
            return 2

        chance = random.randint(0, 100)
        if chance >= ((alive_enemies / Consts.all_enemies) * 100) and alive_enemies >= 1:
            return 3   

        if not colonist:
            for e in self.enemies:
                e.health.reset_protection()
                action = random.randint(0, 2)
                TextGenerator().clear_terminal()
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
    
    def give_weapon_to_colonist(self, colonist = None, weapon = None):
        while not weapon:
            TextGenerator().clear_terminal()
            print(TextGenerator().header("Which weapon do you want to equip?"))
            print(TextGenerator().view_equipable_weapons(self.weapons, is_menue = True))
            weapon = self.find_weapon(input("Weapon: "))
            if not weapon:
                TextGenerator().perform_error_message("Weapon not found! Try again!")
            
        while not colonist:
            TextGenerator().clear_terminal()
            print(TextGenerator().header("Whom do you want to give the weapon?"))
            print(TextGenerator().view_people_stats("colonist", self.colonists, is_menue = True))
            colonist = self.find_colonist(input("Name:  "))
            if not colonist:
                TextGenerator().perform_error_message("Colonist not found! Try again!")

        if weapon and colonist:
            x = colonist.equip_weapon(weapon)
            if x[0]:
                self.weapons.append(x[0])
            self.weapons.remove(x[1])
            TextGenerator().clear_terminal()
            print(TextGenerator().weapon_equipped(colonist.name, weapon.name, weapon.rarity))
            time.sleep(3)

        else:
            TextGenerator().perform_error_message("Colonist or Weapon not found! Try again")
            return True                         ## True means something went wrong

    def find_weapon(self, weapon):
        for w in self.weapons:
            if w.name == weapon or w.short_name == weapon:
                return w
        return None
    
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
    object_spawner = ObjectSpawner()
    world = RimWorld(object_spawner.colonists, object_spawner.silver, object_spawner.weapons, object_spawner.enemies)