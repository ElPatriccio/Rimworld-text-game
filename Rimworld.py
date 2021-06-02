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
                    c = self.find_thing(c, "colonist") 
                    if not(c):
                        TextGenerator().perform_error_message("Colonist was not found! Try again!")
                        self.advance_game(action = "vcs")
                    elif c != -1:
                        self.give_weapon_to_colonist(colonist = c)
            
            elif action == "vew":
                TextGenerator().clear_terminal()
                print(TextGenerator().view_equipable_weapons(self.weapons))
                if w:= input(TextGenerator().get_press_enter(text = "Weapon")):
                    w = self.find_thing(w, "weapon")
                    if not(w):
                        TextGenerator().perform_error_message("Weapon was not found! Try again!")
                        self.advance_game(action = "vew")
                    elif w != -1:
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
                        if self.shoot(c) == False:
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

        if not (alive_enemies := self.get_alive_people("enemy")):
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
                        if self.get_downed_people("enemy") > 0:
                            self.rescue(e)
                        else:
                            self.shoot(e)

                    if action < 2:
                        self.shoot(e)

                    elif action == 2:
                        print(e.health.get_cover(e.name, e.type))
                        time.sleep(2.5)
                
                elif e.health.status == "Recovering":
                    if not e.cooldown:
                        e.health.heal(10)
                        time.sleep(3.5) 
         
        if self.get_alive_people("colonist") == 0:
            return 1
        return 0 

    def find_thing(self, name, type):
        things = []

        if type != "weapon":
            for h in self.colonists if type == "colonist" else self.enemies:
                if h.name.lower() == name.lower():
                    things.append(h)
        else:
            for w in self.weapons:
                if not w.short_name:
                    short = False
                else:
                    short = w.short_name.lower()

                if w.name.lower() == name.lower() or short == name.lower():
                    things.append(w)
        
        if len(things) == 0:
            return None

        if len(things) > 1:
            num = 0
            for thing in things:
                thing.index += " (" + str(num) + ") "
                num += 1

            TextGenerator().clear_terminal()
            print(TextGenerator().header("Which " + name + " do you mean?"))
            print(TextGenerator().view_people_stats(things, is_menue=True)) if type != "weapon" else print(TextGenerator().view_equipable_weapons(things, is_menue= True))

            for thing in things:
                thing.reset_index()

            if (index := input(TextGenerator().get_press_enter(text="index"))) != "":
                if index.isnumeric():
                    if (index := int(index)) < len(things):
                        return things[index]
                    else:
                        TextGenerator().perform_error_message("Index out of range! Try again!")
                        self.find_thing(name, type)
                else:
                    TextGenerator().perform_error_message("Your Index is not a number! Try again!")
                    self.find_thing(name, type)
            else:
                return -1


        return things[0]        

    def get_alive_people(self, type):
        num = 0
        for h in self.colonists if type == "colonist" else self.enemies:
            if h.health.status == "Alive" or h.health.status == "Recovering":
                num +=1
        return num
    
    def get_downed_people(self, type):
        num = 0
        for h in self.colonists if type == "colonist" else self.enemies:
            if h.health.status == "Downed":
                num += 1
        return num
    
    def shoot(self, h):
        if h.type == "colonist":
            TextGenerator().clear_terminal()
            print(TextGenerator().header("Who do you want to shoot?"))
            print(TextGenerator().view_people_stats(self.enemies, is_menue= True)) 

            if target := input(TextGenerator().get_press_enter(text="Name")):
                target = self.find_thing(target, "enemy")
                if not (target):
                    TextGenerator().perform_error_message("Person you want to shoot does not exist! Try again!")
                    self.shoot(h)
                elif target != -1:
                    print(h.shoot(target))
                    time.sleep(2.5)
                else:
                    self.advance_battle_loop(h)
            else:
                self.advance_battle_loop(h)
        else:
            target = self.colonists[random.randint(0, len(self.colonists) - 1)]
            print(h.shoot(target))
            time.sleep(2.5)
    
    def rescue(self, h, target=None):
        if h.type == "colonist":
            if self.get_downed_people("colonist") == 0:
                TextGenerator().perform_error_message("There is no one to rescue!")
                return False

            while not target:
                TextGenerator().clear_terminal()
                print(TextGenerator().header("Downed Colonists"))
                print(TextGenerator().view_downed_colonists(self.colonists))
                
                if target := input(TextGenerator().get_press_enter(text= "Name")):
                    target = self.find_thing(target, "colonist")
                    if not(target):
                        TextGenerator().perform_error_message("Colonist was not found! Try again!")
                    elif target == -1:
                        self.advance_battle_loop(h)
                else:   
                    return False
        else:
            target = self.get_random_downed_enemy()            

        print(TextGenerator().get_rescue_msg(h, target))
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
                weapon = self.find_thing(weapon, "weapon")
                if not (weapon):
                    TextGenerator().perform_error_message("Weapon not found! Try again!")
                elif weapon == -1:
                    return False
            
        while not colonist:
            TextGenerator().clear_terminal()
            print(TextGenerator().header("Whom do you want to give the weapon?"))
            print(TextGenerator().view_people_stats(self.colonists, is_menue = True))
            if not (colonist := input(TextGenerator().get_press_enter(text="Name"))):
                return False
            else:
                colonist = self.find_thing(name = colonist, type ="colonist")
                if not (colonist):
                    TextGenerator().perform_error_message("Colonist not found! Try again!")
                    self.give_weapon_to_colonist(None, weapon)
                elif colonist == -1:
                    return False                    

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
    
    def get_random_downed_enemy(self):
        enemies_downed = []
        for e in self.enemies:
            if e.health.status == "Downed":
                enemies_downed.append(e)
        index = random.randint(0, len(enemies_downed) - 1)
        return enemies_downed[index]        

if __name__ == "__main__":
    object_spawner = ObjectSpawner()
    world = RimWorld(object_spawner.colonists, object_spawner.silver, object_spawner.weapons, object_spawner.enemies)