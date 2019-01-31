import tcod as tcod
import math
from utility.utility_func import distance_to

from components.item import Item

from render_functions import RenderOrder


class Entity:
    """
    A generic object to represent players, enemies, items, etc. Holds the coordinates, the character('@'), and color.
    """

    def __init__(self, x, y, char, color, name, blocks=False, render_order=RenderOrder.CORPSE, fighter=None, ai=None, item=None, inventory=None, stairs=None, level=None, equipment=None, equippable=None):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks
        self.render_order = render_order
        self.fighter = fighter
        self.ai = ai
        self.item = item
        self.inventory = inventory
        self.stairs = stairs
        self.level = level
        self.equipment = equipment
        self.equippable = equippable

        if self.fighter:
            self.fighter.owner = self

        if self.ai:
            self.ai.owner = self

        if self.item:
            self.item.owner = self

        if self.inventory:
            self.inventory.owner = self

        if self.stairs:
            self.stairs.owner = self

        if self.level:
            self.level.owner = self

        if self.equipment:
            self.equipment.owner = self

        if self.equippable:
            self.equippable.owner = self

            if not self.item:
                item = Item()
                self.item = item
                self.item.owner = self

    def move(self, dx, dy):
        # move the entity by a given amount
        self.x += dx
        self.y += dy

    def move_towards(self, target_x, target_y, game_map, entities):
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx ** 2 + dy ** 2)

        dx = int(round(dx / distance))
        dy = int(round(dy / distance))

        if not (game_map.is_blocked(self.x + dx, self.y + dy) or
                get_blocking_entities_at_location(entities, self.x + dx, self.y + dy)):
            self.move(dx, dy)

    # pathfinding algo using A* method will need to look through later
    def move_astar(self, target, entities, game_map):
        # create a FOV map that has the dimensions of the map
        fov = tcod.map_new(game_map.width, game_map.height)

        # scan the current map each turn and set all the walls as unwalkable
        for y1 in range(game_map.height):
            for x1 in range(game_map.width):
                tcod.map_set_properties(
                    fov, x1, y1, not game_map.tiles[x1][y1].block_sight, not game_map.tiles[x1][y1].blocked)

        # Scan all the objects to see if there are objects that must be navigated around, check that the object is self or target(so that start and end points are free)
        # the ai class handles the situation if self is next to target and will not use A*
        for entity in entities:
            if entity.blocks and entity != self and entity != target:
                # set tile as a wall so it must be navigated around
                tcod.map_set_properties(
                    fov, entity.x, entity.y, True, False)

        # Allocate an A* path
        # 1.41 is the normal diagonal cost of moving, can be set to 0 if diagonal moves are prohibited
        my_path = tcod.path_new_using_map(fov, 1.41)

        # compute the path between selfs coordinates and the target's coordinates
        tcod.path_compute(my_path, self.x, self.y, target.x, target.y)

        # Check if the path exists and is shorter then 25 tiles
        # The path size matters if you want the monster to use alternative longer paths (for example through other rooms) if for example the player is in a corridor
        # It makes sense to keep path size relatively low to keep the monsters from running around the map if there's an alternative path really far away
        if not tcod.path_is_empty(my_path) and tcod.path_size(my_path) < 25:
            # find the next coordinates in the computed full path
            x, y = tcod.path_walk(my_path, True)
            if x or y:
                # set self's coordinates to the next path tile
                self.x = x
                self.y = y

        else:
            # Keep the old move function as a backup so that if there are no paths (for example another monster blocks a corridor)
            # it will still try to move towards the player (closer to the corridor opening)
            self.move_towards(target.x, target.y, game_map, entities)

            # delete path to free memory
        tcod.path_delete(my_path)

    def distance(self, x, y):
        return distance_to(x, self.x, y, self.y)

    def distance_to(self, other):
        return distance_to(other.x, self.x, other.y, self.y)

    def __repr__(self):
        return f'Entity: x = {self.x}, y = {self.y}, char = {self.char}, color = {self.color}, name = {self.name}, blocks = {self.blocks}, render_order = {self.render_order}, fighter = {self.fighter}. ai = {self.ai}. item = {self.item}, inventory = {self.inventory}'


def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
    # Checks if the entity is "blocking" and if it occupies the x and y location, if so, we return it
