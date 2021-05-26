from TextGenerator import TextGenerator, TFormats

text_generator = TextGenerator()

class Health():
    def __init__(self, parent) -> None:
        self.points = 100
        self.status = "Alive"
        self.color = TFormats.green
        self.protection = 1
        self.prot_status = "Unprotected"
        self.parent = parent
    
    def get_cover(self, name):
        self.protection = 2
        self.prot_status = "Behind cover"
        self.parent.name_suffix = text_generator.get_cover_name_suffix()
        return(name + " is hiding behind cover! (2x less hit chance)")

    def reset_protection(self):
        self.protection = 1
        self.prot_status = "Unprotected"
        self.parent.reset_name_suffix()

    def take_damage(self, damage):
        if self.status == "Dead":
            return (self.parent.name + " is dead!")
        
        self.points -= damage
        return self.update_health()
    
    def update_health(self):
        if self.points <= 15:
            self.status = "Downed"
            self.color = TFormats.orange
        
        if self.points <= 0:
            self.points = 0
            self.status ="Dead"
            self.color = TFormats.red
        
        return text_generator.view_health_of_human(self.parent.name, self.color, self.status, self.points)