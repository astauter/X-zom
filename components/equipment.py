from equipment_slots import EquipmentSlots
from utility_func import bonus_amount


class Equipment:
    def __init__(self, main_hand=None, off_hand=None, helmet=None, armor=None, ring=None, amulet=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.helmet = helmet
        self.armor = armor
        self.ring = ring
        self.amulet = amulet
        self.equipped = [self.main_hand, self.off_hand,
                         self.helmet, self.armor, self.ring, self.amulet]

    @property
    def max_hp_bonus(self):
        bonus = 0

        bonus += bonus_amount(bonus, self.equipped, "max_hp_bonus")

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        bonus += bonus_amount(bonus, self.equipped, "power_bonus")

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        bonus += bonus_amount(bonus, self.equipped, "defense_bonus")

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        return results
