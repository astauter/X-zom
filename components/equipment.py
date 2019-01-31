from equipment_slots import EquipmentSlots
from utility.equipment_utility_func import stat_bonus


class Equipment:
    def __init__(self, main_hand=None, off_hand=None, helmet=None, armor=None, ring=None, amulet=None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.helmet = helmet
        self.armor = armor
        self.ring = ring
        self.amulet = amulet
        self.equipped = []

    @property
    def max_hp_bonus(self):
        bonus = 0

        bonus += stat_bonus(bonus, self.equipped, "max_hp_bonus")

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        bonus += stat_bonus(bonus, self.equipped, "power_bonus")

        return bonus

    @property
    def defense_bonus(self):
        bonus = 0

        bonus += stat_bonus(bonus, self.equipped, "defense_bonus")

        return bonus

    def toggle_equip(self, equippable_entity):
        results = []

        equipment = equippable_entity.equippable
        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                self.equipped.remove(equipment)
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    self.toggle_equip(self.main_hand)

                self.main_hand = equippable_entity
                self.equipped.append(equipment)
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                self.equipped.remove(equipment)
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    self.toggle_equip(self.off_hand)

                self.off_hand = equippable_entity
                self.equipped.append(equipment)
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.RING:
            if self.ring == equippable_entity:
                self.ring = None
                self.equipped.remove(equipment)
                results.append({'dequipped': equippable_entity})
            else:
                if self.ring:
                    self.toggle_equip(self.ring)

                self.ring = equippable_entity
                self.equipped.append(equipment)
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.ARMOR:
            if self.armor == equippable_entity:
                self.armor = None
                self.equipped.remove(equipment)
                results.append({'dequipped': equippable_entity})
            else:
                if self.armor:
                    self.toggle_equip(self.armor)

                self.armor = equippable_entity
                self.equipped.append(equipment)
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.AMULET:
            if self.amulet == equippable_entity:
                self.amulet = None
                self.equipped.remove(equipment)
                results.append({'dequipped': equippable_entity})
            else:
                if self.amulet:
                    self.toggle_equip(self.amulet)

                self.amulet = equippable_entity
                self.equipped.append(equipment)
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.HELMET:
            if self.helmet == equippable_entity:
                self.helmet = None
                self.equipped.remove(equipment)
                results.append({'dequipped': equippable_entity})
            else:
                if self.helmet:
                    self.toggle_equip(self.helmet)

                self.helmet = equippable_entity
                self.equipped.append(equipment)
                results.append({'equipped': equippable_entity})

        return results
