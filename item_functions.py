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


def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y,):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target,
                        'message': Message(f'A lightning bolt strikes the {target.name} with a loud thunder! The damage is {damage}')})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None,
                        'message': Message('No enemy is in range')})

    return results


def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message(
            'You cannot target a tile outside of the spell range', libtcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message(
        f'The fireball, explodes, burning everything within {radius} tiles', libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append(
                {'message': Message(f'The {entity.name} gets burned for {damage} damage.', libtcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    return results
