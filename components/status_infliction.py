class Status_Infliction:
    def __init__(self, name, damage=None, duration=None):
        self.name = name
        self.damage = damage
        self.duration = duration

    def __repr__(self):
        return f'Status name :{self.name}, damage: {self.damage}, duration: {self.duration}'
