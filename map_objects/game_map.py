import libtcodpy as libtcod
from random import randint

from entity import Entity
from map_objects.tile import Tile
from map_objects.rectangle import Rect

class GameMap:
    # passes in the width and height and initializes a 2d array of Tiles set to non-blocking
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]
            #initialize all tiles to be blocked by default "dig" out as we go along

        #tiles[30][22].blocked = True
        #tiles[30][22].block_sight = True
        #tiles[31][22].blocked = True
        #tiles[31][22].block_sight = True
        #tiles[31][22].blocked = True
        #tiles[31][22].block_sight = True

        #presetting tiles for demonstration
        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, max_monsters_per_room):
        rooms = []
        num_rooms = 0

        for r in range(max_rooms):
            #random width and height
            w = randint(room_min_size, room_max_size)
            h = randint(room_min_size, room_max_size)

            # random position of room without going out of the boundaries of the map
            x = randint(0, map_width - w - 1)
            y = randint(0, map_height - h -1)

            new_room = Rect(x, y, w, h)

            #run through the other rooms and see if they intersect with this one
            for other_room in rooms:
                if new_room.intersect(other_room):
                    break
                #so if the loop finds that the rooms find an intersect we break out
            else:
                #if the loop was allowed to finish without finding any intersections, i.e. the room is valid

                self.create_room(new_room)
                (new_x, new_y) = new_room.center()

                if num_rooms == 0:
                    #first room where player starts at
                    player.x = new_x
                    player.y = new_y
                else:
                    #all rooms after the first connect it to the previous room with a tunnel using the center coordinates of the previous room
                    (prev_x, prev_y) = rooms[num_rooms - 1].center()

                    #flip a coin
                    if randint(0, 1) == 1:
                        self.create_h_tunnel(prev_x, new_x, prev_y)
                        self.create_v_tunnel(prev_y, new_y, new_x)
                    else:
                        self.create_v_tunnel(prev_y, new_y, prev_x)
                        self.create_h_tunnel(prev_x, new_x, new_y)

                self.place_entities(new_room, entities, max_monsters_per_room)

                #add the new room to our list/array
                rooms.append(new_room)
                num_rooms += 1


    def create_room(self, room):
        # got through the tiles in the created rectangle and make them passagble
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
        #x1 +1 are used because we need to account for walls makes the rectangles 1 smaller then they seem, pythons range function does not include the end value in its range

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def place_entities(self, room, entities, max_monsters_per_room):
        #get random # of monsters
        number_of_monsters = randint(0, max_monsters_per_room)

        for i in range(number_of_monsters):
            # Choose a random location in the room
            x = randint(room.x1 + 1, room.x2 - 1)
            y = randint(room.y1 + 1, room.y2 - 1)
            # get random x and y

            if not any([entity for entity in entities if entity.x == x and entity.y == y]):
                #if no monster is there we put a troll or an orc
                num = randint(0, 100)
                if num < 50:
                    monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True)
                elif num > 50 and num < 80:
                    monster = Entity(x, y, 'N', libtcod.light_yellow, "NPC", blocks=True)
                else:
                    monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True)

                entities.append(monster)

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
