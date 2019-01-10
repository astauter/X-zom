class Entity:
    """
    A generic object to represent players, enemies, items, etc. Holds the coordinates, the character('@'), and color.
    """
    def __init__(self, x, y, char, color, name, blocks=False):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks = blocks

    def move(self, dx, dy):
        #move the entity by a given amount
        self.x += dx
        self.y += dy

def get_blocking_entities_at_location(entities, destination_x, destination_y):
    for entity in entities:
        if entity.blocks and entity.x == destination_x and entity.y == destination_y:
            return entity

    return None
    #Checks if the entity is "blocking" and if it occupies the x and y location, if so, we return it
