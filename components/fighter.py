import tcod as tcod

from game_messages import Message
from utility.utility_func import is_critical


class Fighter:
    def __init__(self, hp, defense, power, crit_chance=0, xp=0, owner=None):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp
        self.crit_chance = crit_chance
        self.owner = owner

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defense(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defense_bonus
        else:
            bonus = 0

        return self.base_defense + bonus

    def take_damage(self, amount):
        results = []

        self.hp -= amount

        if self.hp <= 0:
            self.hp = 0

        if self.hp == 0:
            results.append({'dead': self.owner, 'xp': self.xp})

        return results

    def heal(self, amount):
        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def gain_attack(self, amount):
        self.base_power += amount

    def attack(self, target, alt_attack=None):
        results = []
        is_crit = is_critical(self.crit_chance)

        damage = self.power - target.fighter.defense

        if is_crit:
            damage = int(damage * 1.5)

        if alt_attack:
            damage = alt_attack - target.fighter.defense

        if damage > 0 and not is_crit:
            results.append({'message': Message('{0} attacks {1} for {2} hit points.'.format(
                self.owner.name.capitalize(), target.name, str(damage)), tcod.white)})
            results.extend(target.fighter.take_damage(damage))
        elif damage > 0:
            results.append({'message': Message(
                f'{self.owner.name.capitalize()} attacks {target.name} with at Critical Hit!!! It does {str(damage)}!')})
        else:
            results.append({'message': Message('{0} attacks {1} but does no damage.'.format(
                self.owner.name.capitalize(), target.name), tcod.white)})

        return results

    # def __repr__(self):
        # return f'Fighter: hp = {self.hp}, defense = {self.defense}, power = {self.power}, xp = {self.xp}'
