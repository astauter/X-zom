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

    def make_map(self):
        #create two rooms to demonstrate
        room1 = Rect(20, 15, 10, 15)
        room2 = Rect(35, 15, 10, 15)

        self.create_room(room1)
        self.create_room(room2)

    def create_room(self, room):
        # got through the tiles in the created rectangle and make them passagble
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False
        #x1 +1 are used because we need to account for walls makes the rectangles 1 smaller then they seem, pythons range function does not include the end value in its range

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
