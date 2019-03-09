def stat_bonus(bonus, equipped, attribute):
    for equipment in equipped:
        boosted_stat = getattr(equipment, attribute)
        bonus += boosted_stat

    return bonus
