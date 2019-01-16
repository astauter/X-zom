import libtcodpy as libtcod

from game_messages import Message


def heal(*args, **kwargs):
    # take the first arg which will be an entity and heal it by the key_word value amount
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message(
            'You are already at full health', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append(
            {'consumed': True, 'message': Message('Your wounds start to feel better!', libtcod.green)})

    return results


def gain_attack(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    entity.fighter.gain_attack(amount)
    results.append({'consumed': True, 'message': Message(
        'You feel the power coursing through your veins. You feel stronger!', libtcod.green)})

    return results
