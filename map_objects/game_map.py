import tcod as tcod
from random import randint

from components.ai import BasicMonster, RangedMonster, HunterMonster
from components.equipment import EquipmentSlots
from components.equippable import Equippable
from components.fighter import Fighter
from components.item import Item
from components.stairs import Stairs
from components.status_infliction import Status_Infliction

from entity import Entity

from game_messages import Message

from item_functions import heal, cure, gain_attack, cast_lightning, cast_fireball, cast_confuse

from map_objects.tile import Tile
from map_objects.rectangle import Rect
from render_functions import RenderOrder

from utility.utility_func import from_dungeon_level, random_choice_from_dict


class GameMap:
    # passes in the width and height and initializes a 2d array of Tiles set to non-blocking
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level

    def initialize_tiles(self):
        tiles = [[Tile(x, y, True) for y in range(self.height)]
                 for x in range(self.width)]
        # initialize all tiles to be blocked by default "dig" out as we go along

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities):
        rooms = []
        num_rooms = 0

        center_of_last_room_x = None
        center_of_last_room_y = None

        for r in range(max_rooms):
            # random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            # random position of room without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h - 1)

            new_room = Rect(x, y, w, h)

            # run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
                # so if the loop finds that the rooms find an intersect we break out
            else:
                # if the loop was allowed to finish without finding any intersections, i.e. the room is valid

                self.create_room(new_room)

                (new_x, new_y) = new_room.center()

                center_of_last_room_x = new_x
                center_of_last_room_y = new_y

                if num_rooms == 0:
                    # first room where player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    # all rooms after the first connect it to the previous room with a tunnel using the center coordinates of the previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    # flip a coin
                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities)

                # add the new room to our list/array
                rooms.append(new_room)
                num_rooms += 1

        stairs_component = Stairs(self.dungeon_level + 1)
        down_stairs = Entity(center_of_last_room_x,
                             center_of_last_room_y, '>', tcod.white, 'Stairs', render_order=RenderOrder.STAIRS, stairs=stairs_component)
        entities.append(down_stairs)

    def create_room(self, room):
        # go through the tiles in the created rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
        # x1 +1 are used because we need to account for walls makes the rectangles 1 smaller then they seem, pythons range function does not include the end value in its range

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities):
        max_monsters_per_room = from_dungeon_level(
            [[2, 1], [3, 4], [5, 6]], self.dungeon_level)
        max_items_per_room = from_dungeon_level(
            [[1, 1], [2, 4]], self.dungeon_level)
        number_of_monsters = randint(0, max_monsters_per_room)
        number_of_items = randint(0, max_items_per_room)

        monster_chances = {
            'orc': 80,
            'troll': from_dungeon_level([[15, 3], [30, 5], [60, 7]], self.dungeon_level),
            'archer': from_dungeon_level([[10, 1], [20, 3], [30, 5]], self.dungeon_level),
            'hunter': from_dungeon_level([[3, 3], [5, 4], [8, 5], [10, 7]], self.dungeon_level)
        }

        item_chances = {
            'healing_potion': 20,
            'antidote': 15,
            'attack_potion': 2,
            'lightning_scroll': from_dungeon_level([[25, 4]], self.dungeon_level),
            'fireball_scroll': from_dungeon_level([[25, 6]], self.dungeon_level),
            'confusion_scroll': from_dungeon_level([[10, 2]], self.dungeon_level),
            'sword': from_dungeon_level([[5, 4]], self.dungeon_level),
            'shield': from_dungeon_level([[15, 8]], self.dungeon_level),
            'ring_of_agility': from_dungeon_level([[10, 5]], self.dungeon_level),
            'amulet_of_health': from_dungeon_level([[5, 2]], self.dungeon_level),
            'chainmail': from_dungeon_level([[5, 2]], self.dungeon_level)
        }
        # npc_chances = {'NPC': 15}

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            # get random x and y

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                monster_choice = random_choice_from_dict(monster_chances)

                if monster_choice == 'orc':
                    status_component = Status_Infliction(
                        'paralyzing', duration=5, chance=0)
                    fighter_component = Fighter(
                        hp=20, defense=0, power=4, crit_chance=1, xp=40, status_infliction=status_component)
                    ai_component = BasicMonster()

                    monster = Entity(x, y, 'o', tcod.desaturated_green, 'Orc',
                                     blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                if monster_choice == 'troll':
                    fighter_component = Fighter(
                        hp=30, defense=2, power=8, crit_chance=4, xp=100)
                    ai_component = BasicMonster()

                    monster = Entity(
                        x, y, 'T', tcod.darker_green, 'Troll', blocks=True, render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                if monster_choice == 'archer':
                    fighter_component = Fighter(
                        hp=12, defense=0, power=3, crit_chance=2, piercing_damage=1, xp=50)
                    ai_component = RangedMonster(4)

                    monster = Entity(x, y, 'a', tcod.darker_green, 'Goblin Archer', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                if monster_choice == 'hunter':
                    fighter_component = Fighter(
                        hp=50, defense=2, power=10, crit_chance=5, piercing_damage=4, xp=250)
                    ai_component = HunterMonster(5, 6)

                    monster = Entity(x, y, 'H', tcod.dark_flame, 'Hunter', blocks=True,
                                     render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component)

                entities.append(monster)

                '''elif num > 50 and num < 80:
                    monster = Entity(
                        x, y, 'N', tcod.light_yellow, "NPC", blocks=True, render_order=RenderOrder.ACTOR)'''

        for i in range(number_of_items):
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                item_choice = random_choice_from_dict(item_chances)

                if item_choice == 'healing_potion':
                    item_component = Item(use_function=heal, amount=25)
                    item = Entity(x, y, '!', tcod.violet,
                                  'Healing Potion', render_order=RenderOrder.ITEM, item=item_component)
                if item_choice == 'antidote':
                    item_component = Item(use_function=cure)
                    item = Entity(x, y, '!', tcod.light_green, 'Antidote',
                                  render_order=RenderOrder.ITEM, item=item_component)
                if item_choice == 'confusion_scroll':
                    item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                        'Left-click an enemy to confuse it, or right-click to cancel.', tcod.light_blue))
                    item = Entity(x, y, '#', tcod.light_pink, 'Confusion Scroll',
                                  render_order=RenderOrder.ITEM, item=item_component)
                if item_choice == 'attack_potion':
                    item_component = Item(use_function=gain_attack, amount=1)
                    item = Entity(x, y, '!', tcod.red, 'Attack Potion',
                                  render_order=RenderOrder.ITEM, item=item_component)
                if item_choice == 'lightning_scroll':
                    item_component = Item(
                        use_function=cast_lightning, damage=40, maximum_range=5)
                    item = Entity(x, y, '#', tcod.yellow,
                                  'Lightning Scroll', render_order=RenderOrder.ITEM, item=item_component)
                if item_choice == 'fireball_scroll':
                    item_component = Item(
                        use_function=cast_fireball, targeting=True, targeting_message=Message('Left-click a target tile for the fireball, or right-click to cancel.', tcod.white), damage=25, radius=3)
                    item = Entity(x, y, '#', tcod.red, 'Fireball',
                                  render_order=RenderOrder.ITEM, item=item_component)
                if item_choice == 'sword':
                    equippable_component = Equippable(
                        EquipmentSlots.MAIN_HAND, power_bonus=3)
                    item = Entity(x, y, '/', tcod.sky, 'Sword',
                                  equippable=equippable_component)
                if item_choice == 'shield':
                    equippable_component = Equippable(
                        EquipmentSlots.OFF_HAND, defense_bonus=1)
                    item = Entity(x, y, '+', tcod.darker_orange,
                                  'shield', equippable=equippable_component)
                if item_choice == 'ring_of_agility':
                    equippable_component = Equippable(
                        EquipmentSlots.RING, defense_bonus=1)
                    item = Entity(
                        x, y, 'o', tcod.silver, 'Ring of Agility', equippable=equippable_component)
                if item_choice == 'amulet_of_health':
                    equippable_component = Equippable(
                        EquipmentSlots.AMULET, max_hp_bonus=30)
                    item = Entity(
                        x, y, 'v', tcod.gold,  "Amulet of Health", equippable=equippable_component)
                if item_choice == 'chainmail':
                    equippable_component = Equippable(
                        EquipmentSlots.ARMOR, defense_bonus=2)
                    item = Entity(x, y, 'A', tcod.light_gray,
                                  "chainmail", equippable=equippable_component)

                entities.append(item)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def get_tiles(self, x, y, radius):
        center_tile = self.tiles[x][y]
        affected_tiles = [center_tile]
        for tile_row in self.tiles:
            for tile in tile_row:
                if center_tile.distance_to(tile) < radius:
                    affected_tiles.append(tile)
        return affected_tiles

    def next_floor(self, player, message_log, constants):
        self.dungeon_level += 1
        entities = [player]

        self.tiles = self.initialize_tiles()
        self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'], constants['map_width'],
                      constants['map_height'], player, entities)

        player.fighter.heal(player.fighter.max_hp // 2)
        message_log.add_message(
            Message('You take a moment to rest, and recover your strength.', tcod.fuchsia))

        return entities

    def __repr__(self):
        return f'Game Map: Height = {self.height}, width = {self.width}, level = {self.dungeon_level}'
