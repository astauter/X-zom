from equipment_slots import EquipmentSlots
from utility.equipment_utility_func import stat_bonus


class Equipment:
    print("ENUM", EquipmentSlots.MAIN_HAND.value)

    def __init__(self, main_hand=None, off_hand=None, helmet=None, armor=None, ring=None, amulet=None):
        setattr(self, EquipmentSlots.MAIN_HAND.value, main_hand)
        setattr(self, EquipmentSlots.OFF_HAND.value, off_hand)
        setattr(self, EquipmentSlots.HELMET.value, helmet)
        setattr(self, EquipmentSlots.ARMOR.value, armor)
        setattr(self, EquipmentSlots.RING.value, ring)
        setattr(self, EquipmentSlots.AMULET.value, amulet)
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

        slot = equippable_entity.equippable.slot.value
        equipment = equippable_entity.equippable
        currentlyequipped = getattr(self, slot)

        already_equipped = currentlyequipped == equippable_entity
        if already_equipped:
            setattr(self, slot, None)
            self.equipped.remove(equipment)
            results.append({'dequipped': equippable_entity})
        else:
            if currentlyequipped:
                self.toggle_equip(currentlyequipped)

            setattr(self, slot, equippable_entity)
            self.equipped.append(equipment)
            results.append({'equipped': equippable_entity})

        return results
