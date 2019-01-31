import tcod as tcod

from game_messages import Message


class Inventory:
    def __init__(self, capacity, owner=None):
        self.capacity = capacity
        self.owner = owner
        self.items = []

    def add_item(self, item):
        results = []

        if len(self.items) >= self.capacity:
            results.append({
                'item_added': None,
                'message': Message('You cannot carry anymore, your inventory is full', tcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You picked up a {0}.'.format(item.name), tcod.blue)
            })

            self.items.append(item)

        return results

    def use(self, item_entity, game_map=None, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message(
                    'The {0} cannot be used'.format(item_entity.name), tcod.yellow)})
        else:
            if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                results.append({'targeting': item_entity})
            else:
                kwargs = {**item_component.function_kwargs, **kwargs}

                item_use_results = item_component.use_function(
                    self.owner, game_map, **kwargs)

                for item_use_result in item_use_results:
                    if item_use_result.get('consumed'):
                        self.remove_item(item_entity)

                results.extend(item_use_results)

        return results

    def remove_item(self, item):
        self.items.remove(item)

    def drop_item(self, item):
        results = []

        if self.owner.equipment.main_hand == item:
            self.owner.equipment.toggle_equip(item)
        if self.owner.equipment.off_hand == item:
            self.owner.equipment.toggle_equip(item)
        if self.owner.equipment.helmet == item:
            self.owner.equipment.toggle_equip(item)
        if self.owner.equipment.armor == item:
            self.owner.equipment.toggle_equip(item)
        if self.owner.equipment.amulet == item:
            self.owner.equipment.toggle_equip(item)
        if self.owner.equipment.ring == item:
            self.owner.equipment.toggle_equip(item)

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message(
            'You dropped the {0}'.format(item.name), tcod.yellow)})

        return results

    def __repr__(self):
        return f'Inventory : capacity = {self.capacity}, items = {self.items}'
