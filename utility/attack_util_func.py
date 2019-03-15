import math
from random import randint


def is_successful(chance):
    random_num = randint(1, 100)

    if random_num <= chance:
        return True

    return False


def damage_done(attack, defense, is_crit, piercing_damage):
    if is_crit:
        attack = attack * 1.5

    if piercing_damage:
        if defense + piercing_damage >= attack:
            return piercing_damage

    if attack > defense:
        return attack - defense

    return False
