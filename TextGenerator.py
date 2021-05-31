from os import system
class TextGenerator():

    def clear_terminal(self):
        system("cls")
    
    def get_press_enter(self):
        return "\nPress " + TFormats.bold + "\"enter\"" + TFormats.end + " to continue:  "
    
    def get_attack_enemies(self):
        return "\nAttack enemies? (" + TFormats.green + "y" + TFormats.end + "|" + TFormats.red + "n" + TFormats.end + ") "
    
    def get_start_message(self, colonists, weapons, silver, enemies):
        return(self.header("You started a new world!\n") + "\nYou own " + str(colonists) + TFormats.green + " colonists" + TFormats.end + ", " + str(weapons) + " weapons and " + str(silver) + " silver. " +  str(enemies) + TFormats.red + " enemies" + TFormats.end + " are roaming in your area.")

    def get_action_menue(self):
        return self.header("What do you want to do?") + "\n\n-View colonist stats: (vcs)\n-View equipable weapons: (vew)\n-Equip weapon: (ew)\n-View enemy stats: (ves)\n-Engage battle: (eb)\n\nAction:  "

    def get_battle_action_menue(self, name):
        return self.header("What shall " + name + " do?") + "\n\n-View " + name + " stats (vs)\n-Equip weapon (ew)\n-Shoot enemy (se)\n-Hide behind cover (hbc)\n-Rescue colonist (rc)\n\nAction:  "

    def view_people_stats(self, type, people, name = None, is_menue = False):
        text = ""
        if type == "colonist":
            if not(is_menue):
                text = self.header("Your Colony!\n")

        elif type == "enemy":
            if not(is_menue):
                text = self.header("Enemies in your area:\n")

        for human in people:
            if human == name or not(name):
                text += (self.format_stats_of_human(human.name, human.gender, human.age, human.skill, human.weapon.name, TFormats.rarities[human.weapon.rarity], human.health.points, human.health.status, human.health.color, human.type, human.name_suffix))
        return text

    def format_stats_of_human(self, name, gender, age, skill, weapon_name, weapon_color, hp, health_status, health_color, type, name_suffix):
        desc_color = ""
        if type == "colonist":
            name_color = TFormats.cyan

        else:
            name_color = TFormats.magenta
        
        if health_status == "Dead":
            desc_color = TFormats.grey

        return "\n" + name_color + "--" + name + TFormats.end + name_suffix + name_color + "--" + TFormats.end + desc_color + "\nGender: " + self.attribute(gender) + desc_color +"\nAge: " + self.attribute(str(age)) + desc_color + "\nShooting skill: " + self.attribute(str(skill)) + desc_color + "\nEquipped Weapon: " + self.attribute(weapon_color + weapon_name) + desc_color + "\nHealth: " + health_color + self.attribute(str(hp)) + health_color + self.attribute("%") + TFormats.end + self.attribute(", ") + health_color + self.attribute(health_status) + "\n"


    def view_health_of_human(self, name, health_color, status, hp):
        return "\n" + name + " is " + health_color + status + TFormats.end + " and has " + health_color + str(hp) + "%" + TFormats.end + " health left"

    def view_equipable_weapons(self, weapons, is_menue = False):
        if not(is_menue):
            text = self.header("--Your weapon stockpile--\n")
        
        else:
            text = ""

        for weapon in weapons:
            text += self.format_stats_of_weapon(weapon.name, weapon.short_name, weapon.damage, weapon.bonus_damage, weapon.shots, weapon.rarity, is_menue)
        
        return text
    
    def format_stats_of_weapon(self, name, short_name, damage, bonus_damage, shots, rarity, is_menue):
        short = ""
        if short_name and is_menue:
            short = " (" + short_name + ")"

        bonus_damage = self.color_rarity(" (+" + str(bonus_damage) + ")", rarity) if bonus_damage else ""

        return ("\n" + self.color_rarity("--" + name  + "--", rarity) + TFormats.end + short + "\nDamage: " + str(damage) + bonus_damage +"\nShots per round: " + str(shots) + "\nRarity: " + self.color_rarity(rarity, rarity) +"\n")

    def weapon_equipped(self, name, weapon, rarity):
        return name + " equipped a " + self.color_rarity(rarity, rarity) + " " + weapon +"!"

    def get_cover_name_suffix(self):
        return TFormats.yellow + " (" + TFormats.bold + "HIDING! 2x" + TFormats.end + TFormats.yellow +  " less hit chance)" + TFormats.end

    def header(self, text):
        return TFormats.bold + TFormats.cyan + text + TFormats.end
    
    def attribute(self, text):
        return TFormats.italic + text + TFormats.end

    def color_rarity(self, text, rarity):
        return TFormats.rarities[rarity] + text + TFormats.end

    def error(self, text):
        return TFormats.red + TFormats.bold + "ERROR: " + TFormats.end + text

class TFormats():
    end = "\033[0m"
    bold = "\033[1m"
    italic = "\033[3m"
    underline = "\033[4m"
    green ="\033[32m"
    yellow = "\033[33m"
    red = "\033[31m"
    blue = "\033[34m"
    cyan = "\033[36m"
    magenta = "\033[35m"
    purple = "\033[38;5;93m"
    grey = "\033[38;5;240m"
    orange = "\033[38;5;214m"
    brown = "\033[38;5;130m"
    silver = "\033[38;5;7m"

    rarities = {
        "common" : "",
        "uncommon" : "\033[32m",
        "rare" : "\033[38;5;27m",
        "epic" : "\033[38;5;93m",
        "legendary" : "\033[1m\033[38;5;208m",
    }