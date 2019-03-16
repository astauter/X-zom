import tcod as tcod

from game_messages import Message
from utility.attack_util_func import is_successful, damage_done
from components.status import Status


class Fighter():
    def __init__(self, hp, defense, power, crit_chance=0, xp=0, piercing_damage=None, status_infliction=None, owner=None):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defense = defense
        self.base_power = power
        self.xp = xp
        self.crit_chance = crit_chance
        self.owner = owner
        self.piercing_damage = piercing_damage
        self.status_infliction = status_infliction
        self.status = Status()

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

    def has_status_effects(self):
        if self.status.is_poisoned or self.status.is_paralyzed or self.status.is_bleeding:
            return True
        else:
            return False

    def process_statuses(self):
        results = []

        if self.status.is_poisoned:
            results.extend(self.status.process_poison(self.owner))
        if self.status.is_paralyzed:
            results.extend(self.status.process_paralysis(self.owner))
        if self.status.is_bleeding:
            results.extend(self.status.process_bleeding(self.owner))
        return results

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

    def cure_poison(self):
        self.status.is_poisoned = False
        self.status.poison_damage = 0

    def gain_attack(self, amount):
        self.base_power += amount

    def attack(self, target, alt_attack=None):
        results = []
        attack = self.power
        defense = target.fighter.defense
        is_crit = is_successful(self.crit_chance)
        damage = damage_done(attack, defense, is_crit, self.piercing_damage)

        if alt_attack:
            damage = damage_done(alt_attack, defense,
                                 is_crit, self.piercing_damage)

        if damage and is_crit:
            results.append({'message': Message(
                f'{self.owner.name.capitalize()} attacks {target.name} with a Critical Hit!!! It does {str(damage)} points of damage!', tcod.light_flame)})
            results.extend(target.fighter.take_damage(damage))

        elif damage and self.piercing_damage:
            results.append({'message': Message(
                f'{self.owner.name.capitalize()} pierces the{target.name}\'s armor! It does {str(damage)} points of damage!', tcod.white)})
            results.extend(target.fighter.take_damage(damage))

        elif damage:
            results.append({'message': Message(
                f'{self.owner.name.capitalize()} attacks {target.name} for {str(damage)} hit points.', tcod.white)})
            results.extend(target.fighter.take_damage(damage))

        else:
            results.append({'message': Message(
                f'{self.owner.name.capitalize()} attacks {target.name} but does no damage.', tcod.white)})

        if self.status_infliction:
            status_effect = self.status_infliction.name
            if status_effect == 'poisoning':
                results.append({'message': Message(
                    f'The {self.owner.name} attacks with a deadly poison', tcod.green)})
                target.fighter.status.set_status(
                    self.status_infliction)

            if status_effect == 'paralyzing':
                paralysis = is_successful(self.status_infliction.chance)
                if paralysis:
                    results.append({'message': Message(
                        f'The {self.owner.name} manages to paralyze {target.name}!', tcod.yellow)})
                    target.fighter.status.set_status(
                        self.status_infliction, target)

            if status_effect == 'bleeding' and not target.fighter.status.is_bleeding:
                results.append({'message': Message(
                    f'The {self.owner.name} slices into {target.name} deeply. They start to bleed heavily', tcod.red)})
                target.fighter.status.set_status(
                    self.status_infliction)

        return results

    def __repr__(self):
        return f'Fighter: hp = {self.hp}, defense = {self.defense}, power = {self.power}, xp = {self.xp}'
