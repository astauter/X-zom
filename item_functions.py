import tcod as tcod

from components.ai import ConfusedMonster

from game_messages import Message


def heal(*args, **kwargs):
    # take the first arg which will be an entity and heal it by the key_word value amount
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message(
            'You are already at full health', tcod.yellow)})
    else:
        if entity.fighter.status.is_bleeding:
            status = entity.fighter.status
            status.is_bleeding = False
            status.bleeding_damage = 0
            status.bleeding_duration = 0
        entity.fighter.heal(amount)
        results.append(
            {'consumed': True, 'message': Message('Your wounds start to heal!', tcod.green)})

    return results


def cure(*args, **kwargs):
    entity = args[0]

    results = []

    if entity.fighter.hp == entity.fighter.max_hp and entity.fighter.status.is_poisoned == False:
        results.append({'consumed': False, 'message': Message(
            'You do not need curing!', tcod.yellow)})
    elif entity.fighter.status.is_poisoned == False:
        entity.fighter.heal(8)
        results.append({'consumed': True, 'message': Message(
            'The antidote heals for a minor amount.', tcod.yellow)})
    else:
        entity.fighter.heal(8)
        entity.fighter.cure_poison()
        results.append({'consumed': True, 'message': Message(
            'You are no longer poisoned!')})

    return results


def gain_attack(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    entity.fighter.gain_attack(amount)
    results.append({'consumed': True, 'message': Message(
        'You feel the power coursing through your veins. You feel stronger!', tcod.green)})

    return results


def cast_lightning(caster, game_map, *args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and tcod.map_is_in_fov(fov_map, entity.x, entity.y,):
            distance = caster.distance_to(entity)

            if distance < closest_distance:
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target,
                        'message': Message(f'A lightning bolt strikes the {target.name} with a loud crash and scorches the ground! The damage is {damage}')})
        results.extend(target.fighter.take_damage(damage))
        burned_tile = game_map.tiles[target.x][target.y]
        burned_tile.burned = True
        results.append({'force_recompute': True})
    else:
        results.append({'consumed': False, 'target': None,
                        'message': Message('No enemy is in range')})

    return results


def cast_fireball(owner, game_map, *args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message(
            'You cannot target a tile outside of the spell range', tcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message(
        f'The fireball, explodes, burning everything within {radius} tiles', tcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
            results.append(
                {'message': Message(f'The {entity.name} gets burned for {damage} damage.', tcod.orange)})
            results.extend(entity.fighter.take_damage(damage))

    burned_tiles = game_map.get_tiles(target_x, target_y, radius)
    for tile in burned_tiles:
        tile.burned = True

    results.append({'force_recompute': True})
    return results


def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not tcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message(
            'You cannot target a tile outside of the field of view', tcod.white)})

        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message(
                f'The eyes of {entity.name} look at you in confusion', tcod.fuchsia)})

            break

    else:
        results.append({'consumed': False, 'message': Message(
            'There is no targetable enemy', tcod.yellow)})

    return results
