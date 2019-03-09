import tcod as tcod

from game_messages import Message


class Status:
    def __init__(self, is_poisoned=False, is_bleeding=False, poison_damage=False, bleeding_duration=0, bleeding_damage=False, paralyzed_duration=0, is_paralyzed=False):
        self.is_poisoned = is_poisoned
        self.poison_damage = poison_damage
        self.is_bleeding = is_bleeding
        self.bleeding_damage = bleeding_damage
        self.bleeding_duration = bleeding_duration
        self.is_paralyzed = is_paralyzed
        self.paralyzed_duration = paralyzed_duration

    def set_status(self, status_infliction):

        if status_infliction.name == 'poisoning':
            self.is_poisoned = True
            self.poison_damage = status_infliction.damage
        if status_infliction.name == 'paralysing':
            self.is_paralyzed = True
            self.paralyzed_duration = status_infliction.duration
        if status_infliction.name == 'bleeding':
            self.is_bleeding = True
            self.bleeding_duration = status_infliction.duration
            self.bleeding_damage = status_infliction.bleeding_damage

    def process_poison(self, owner):
        results = []

        results.append({'message': Message(
            f'{owner.name.capitalize()} takes {self.poison_damage} points of poison damage', tcod.green)})
        results.extend(owner.fighter.take_damage(self.poison_damage))

        return results

    def process_bleeding(self, owner):
        results = []
        if self.bleeding_duration >= 1:
            self.bleeding_duration -= 1
            results.append({'message': Message(
                f'{owner.name.capitalize()} takes {self.bleeding_damage} points of bleeding damage', tcod.red)})

            results.extend(owner.fighter.take_damage(self.bleeding_damage))

        else:
            self.is_bleeding = False
            self.bleeding_damage = 0

            results.append({'message': Message(
                f'{owner.name.capitalize()}\'s wound closes up', tcod.white)})

        return results

    def process_paralysis(self, owner):
        if self.paralyzed_duration >= 1:
            self.paralyzed_duration -= 1

            return {'message': Message(f'{owner.name.capitalize()} is paralyzed! They can\'t move!', tcod.yellow)}

        else:
            self.is_paralyzed = False

            return {'message': Message(f'{owner.name.capitalize()}\'s paralysis wears off', tcod.white)}

    def __repr__(self):
        return f'Status: is poisoned:{self.is_poisoned}, poison damage:{self.poison_damage}'
