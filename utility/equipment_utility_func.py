def stat_bonus(bonus, equipped, attribute):
    for equipment in equipped:
        boosted_stat = getattr(equipment, attribute)
        bonus += boosted_stat

    return bonus


def equip_handle(item, slot, equippible_entity, equipped):
    results = {}
    # if slot  === slot.slotName:
    # if slot.slotName == equippible_entity
    # slot.slotName == None
    #

    return results
