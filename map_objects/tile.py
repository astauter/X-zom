from utility.utility_func import distance_to


class Tile:
    """
    A tile on a map. might be blocked, and might block sight, they are seperate for edge cases, like windows or darkness
    """

    def __init__(self, x, y, blocked, block_sight=None):
        self.x = x
        self.y = y
        self.blocked = blocked
        if block_sight is None:
            block_sight = blocked
        self.block_sight = block_sight
        self.explored = False
        self.burned = False

    def distance_to(self, other):
        return distance_to(self.x, other.x, self.y, other.y)

    def __repr__(self):
        return f'Tile: x = {self.x}, y = {self.y}, blocked = {self.blocked}, block_sight = {self.block_sight}, burned = {self.burned} '
