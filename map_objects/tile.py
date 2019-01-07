class Tile:
    """
    A tile on a map. might be blocked, and might block sight, they are seperate for edge cases, like windows or darkness
    """
    def __init__(self, blocked, block_sight=None):
        self.blocked = blocked

        # by default, if a tile is blocked, it also blocks sight
        if block_sight is None:
            #none is a bool value comperable to null assignments to None are illigal and raise a syntax error
            block_sight = blocked

        self.block_sight = block_sight

