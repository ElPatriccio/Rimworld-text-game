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
                print(TextGenerator().view_people_stats(self.colonists)) 
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
                print(TextGenerator().view_people_stats(self.enemies))
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

        if battle_status == 1: # All colonists dead or downed
            print("You loose!")

        elif battle_status == 2: # All enemies dead or downed
            print("You win!")

        elif battle_status == 3: # Enemies fled
            print("Enemies are fleeing!")
        
        time.sleep(3)               
                    
    def advance_battle_loop(self, colonist):
        if not colonist:
            for e in self.enemies:
                e.cooldown = False

        for c in self.colonists:
            c.health.reset_protection()
            TextGenerator().clear_terminal()
            if colonist == c or not colonist:
                if c.health.status == "Alive":
                    action = input(TextGenerator().get_battle_action_menue(c.name))

                    if action == "vs":
                        TextGenerator().clear_terminal()
                        print(TextGenerator().view_people_stats(self.colonists, c))
                        if input(TextGenerator().get_press_enter(text= c.name)):
                            TextGenerator().clear_terminal()
                            if self.give_weapon_to_colonist(c) == False:
                                self.advance_battle_loop(c)
                        else:
                            self.advance_battle_loop(c)
                    
                    elif action == "ew":
                        TextGenerator().clear_terminal()
                        if self.give_weapon_to_colonist(c) == False:
                            self.advance_battle_loop(c)

                    elif action == "se":
                        TextGenerator().clear_terminal()
                        if self.shoot_enemy(c) == False:
                            self.advance_battle_loop(c)

                    elif action == "hbc":
                        TextGenerator().clear_terminal()
                        print(c.health.get_cover(c.name, c.type))
                        time.sleep(2.5)
                    
                    elif action == "rc":
                        if self.rescue_colonist(c) == False:
                            self.advance_battle_loop(c) 

                    else:
                        self.advance_battle_loop(c)

                elif c.health.status == "Recovering" and not c.cooldown:
                    c.health.heal(10)
                    time.sleep(3.5)
                    if c.health.status == "Alive":
                        self.advance_battle_loop(c)
        
        for c in self.colonists:
            c.cooldown = False

        alive_enemies = self.get_alive_enemies()
        if alive_enemies == -1:
            return 2

        chance = random.randint(0, 100)
        if chance >= ((alive_enemies / Consts.all_enemies) * 100 + 10) and alive_enemies >= 1:
            return 3   

        if not colonist:
            for e in self.enemies:
                e.health.reset_protection()
                action = random.randint(0, 3)
                TextGenerator().clear_terminal()

                if e.health.status == "Alive": 
                    if action == 3:
                        if self.get_downed_enemies() > 0:
                            target = self.get_random_downed_enemy()
                            print(TextGenerator().get_rescue_msg(e, target))
                            target.cooldown = True
                            time.sleep(3)
                            target.health.recover()
                        else:
                            self.shoot_colonist(e)

                    if action < 2:
                        self.shoot_colonist(e)

                    elif action == 2:
                        print(e.health.get_cover(e.name, e.type))
                        time.sleep(2.5)
                
                elif e.health.status == "Recovering":
                    if not e.cooldown:
                        e.health.heal(10)
                        time.sleep(3.5) 
        
        alive_colonists = self.get_alive_colonists()
        if alive_colonists == 0:
            return 1
        return 0 
        

    def find_colonist(self, colonist):
        for c in self.colonists:
            if c.name.lower() == colonist.lower():
                return c
        return None 

    def get_alive_colonists(self):
        num = 0
        for c in self.colonists:
            if c.health.status == "Alive" or c.health.status == "Recovering":
                num +=1
        return num
    
    def get_downed_colonists(self):
        num = 0
        for c in self.colonists:
            if c.health.status == "Downed":
                num += 1
        return num
    
    def rescue_colonist(self, c, target=None):
        if self.get_downed_colonists() == 0:
            TextGenerator().perform_error_message("There is no one to rescue!")
            return False

        while not target:
            TextGenerator().clear_terminal()
            print(TextGenerator().header("Downed Colonists"))
            print(TextGenerator().view_downed_colonists(self.colonists))
            
            if target := input(TextGenerator().get_press_enter(text= "Name")):
                TextGenerator().clear_terminal()
                if (target := self.find_colonist(target)) == None:
                    TextGenerator().perform_error_message("Colonist was not found! Try again!")
            else:   
                return False
        print(TextGenerator().get_rescue_msg(c, target))
        target.cooldown = True
        time.sleep(3)
        target.health.recover()

    def give_weapon_to_colonist(self, colonist = None, weapon = None):
        while not weapon:
            TextGenerator().clear_terminal()
            print(TextGenerator().header("Which weapon do you want to equip?"))
            print(TextGenerator().view_equipable_weapons(self.weapons, is_menue = True))
            if not(weapon := input(TextGenerator().get_press_enter(text="Weapon"))):
                return False
            else:
                if not (weapon := self.find_weapon(weapon)):
                    TextGenerator().perform_error_message("Weapon not found! Try again!")
            
        while not colonist:
            TextGenerator().clear_terminal()
            print(TextGenerator().header("Whom do you want to give the weapon?"))
            print(TextGenerator().view_people_stats(self.colonists, is_menue = True))
            if not (colonist := input(TextGenerator().get_press_enter(text="Name"))):
                return False
            else:
                if not (colonist := self.find_colonist(colonist)):
                    TextGenerator().perform_error_message("Colonist not found! Try again!")

        if weapon and colonist:
            x = colonist.equip_weapon(weapon)
            if x[0]:
                self.weapons.append(x[0])
            self.weapons.remove(x[1])
            TextGenerator().clear_terminal()
            print(TextGenerator().weapon_equipped(colonist.name, colonist.type, weapon.name, weapon.rarity))
            time.sleep(3)

        else:
            TextGenerator().perform_error_message("Colonist or Weapon not found! Try again")
            self.give_weapon_to_colonist(colonist, weapon)

    def find_weapon(self, weapon):
        for w in self.weapons:
            if not w.short_name:
                short = ""
            else:
                short = w.short_name.lower()

            if w.name.lower() == weapon.lower() or short == weapon.lower():
                return w
        return None
    
    def find_enemy(self, enemy):
        for e in self.enemies:
            if e.name.lower() == enemy.lower():
                return e
        return None 
    
    def shoot_enemy(self, c):
        TextGenerator().clear_terminal()
        print(TextGenerator().header("Who do you want to shoot?"))
        print(TextGenerator().view_people_stats(self.enemies, is_menue= True)) 

        if target := input(TextGenerator().get_press_enter(text="Name")):
            if not (target := self.find_enemy(target)):
                TextGenerator().perform_error_message("Person you want to shoot does not exist! Try again!")
                self.shoot_enemy(c)
            else:
                print(c.shoot(target))
                time.sleep(3)
        else:
            self.advance_battle_loop(c)

    def get_alive_enemies(self):
        num = 0
        for e in self.enemies:
            if e.health.status == "Alive" or e.health.status == "Recovering":
                num+=1
        if num == 0:
            return -1
        return num

    def get_downed_enemies(self):
        num = 0
        for e in self.enemies:
            if e.health.status == "Downed":
                num += 1
        return num
    
    def get_random_downed_enemy(self):
        enemies_downed = []
        for e in self.enemies:
            if e.health.status == "Downed":
                enemies_downed.append(e)
        index = random.randint(0, len(enemies_downed) - 1)
        return enemies_downed[index]

    def shoot_colonist(self, e):
        target = self.colonists[random.randint(0, len(self.colonists) - 1)]
        print(e.shoot(target))
        time.sleep(3)

if __name__ == "__main__":
    object_spawner = ObjectSpawner()
    world = RimWorld(object_spawner.colonists, object_spawner.silver, object_spawner.weapons, object_spawner.enemies)