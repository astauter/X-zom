from map_objects.tile import Tile

class GameMap:
    # passes in the width and height and initializes a 2d array of Tiles set to non-blocking
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

    def initialize_tiles(self):
        tiles = [[Tile(False) for y in range(self.height)] for x in range(self.width)]

        tiles[30][22].blocked = True
        tiles[30][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True
        tiles[31][22].blocked = True
        tiles[31][22].block_sight = True

        #presetting tiles for demonstration
        return tiles

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False
