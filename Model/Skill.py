class Skill:
    def __init__(self, name, damage, mp_cost):
        self.name = name
        self.damage = damage
        self.mp_cost = mp_cost

    def info(self):
        return {
            "name": self.name,
            "damage": self.damage,
            "mp_cost": self.mp_cost
        }