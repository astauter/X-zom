import math
from random import randint


def is_critical(critical_chance):
    random_chance = randint(1, 100)

    if random_chance <= critical_chance:
        return True


def damage_done(attack, defense, is_crit, piercing_damage):
    if is_crit:
        attack = attack * 1.5

    if piercing_damage:
        if defense + piercing_damage >= attack:
            return piercing_damage

    if attack > defense:
        return attack - defense

    return False
