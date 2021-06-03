from consts import Consts
from TextGenerator import TextGenerator, TFormats

class Health():
    def __init__(self, parent) -> None:
        self.points = 100
        self.status = "Alive"
        self.color = TFormats.green
        self.protection = 1
        self.prot_status = "Unprotected"
        self.parent = parent
    
    def get_cover(self, name, type):
        self.protection = 2
        self.prot_status = "Behind cover"
        self.parent.name_suffix = TextGenerator().get_cover_name_suffix()
        return TextGenerator().get_cover_msg(self.parent.name, self.parent.type)

    def reset_protection(self):
        self.protection = 1
        self.prot_status = "Unprotected"
        self.parent.reset_name_suffix()

    def take_damage(self, damage):
        if self.status == "Dead":
            return (TextGenerator().perform_error_message(TextGenerator().color_type_human(self.parent.name, self.parent.type) + " is dead!"))
        
        self.points -= damage
        return self.update_health()
    
    def recover(self, remove = False):
        if remove:
            self.status = "Alive"
            self.color = TFormats.green
            print(TextGenerator().color_type_human(self.parent.name, self.parent.type) + " is fully recovered!")
        else:
            self.status = "Recovering"
            self.color = TFormats.cyan

    def heal(self, hp=10):
        self.points += hp
        if self.points >= 100:
            self.points = 100
            self.recover(remove = True)
        else:
            print(self.update_health(heal = True))
    
    def update_health(self, heal=False):
        if not heal:
            if self.points <= Consts.settings["health"]["downed-hp"]:
                self.status = "Downed"
                self.color = TFormats.orange
            
            if self.points <= 0:
                self.points = 0
                self.status ="Dead"
                self.color = TFormats.red
        
        return TextGenerator().view_health_of_human(TextGenerator().color_type_human(self.parent.name, self.parent.type), self.color, self.status, self.points)