class Status_Infliction:
    def __init__(self, name, damage=None, duration=None, chance=None):
        self.name = name
        self.damage = damage
        self.duration = duration
        self.chance = chance

    def __repr__(self):
        return f'Status name :{self.name}, damage: {self.damage}, duration: {self.duration}, chance: {self.chance}'
