import libtcodpy as libtcod

def render_all(con, entities, screen_width, screen_height):
    for entity in entities:
        draw_entity(con, entity)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

#draws entities on the entities list/array, takes the console, entities, and screen size then calls draw_entity on them then "blits" (or draws) the changes on the screen

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

    #clears the entities after drawing them to the screen

def draw_entity(con, entity):
    libtcod.console_set_default_foreground(con, entity.color)
    libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

    #does the drawing, flexible to draw any entity passed to it


def clear_entity(con, entity):
    # erase the character that represents this object so when it moves there is no trail behind
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)


