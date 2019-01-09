import libtcodpy as libtcod

def render_all(con, entities, game_map, fov_map, fov_recompute, screen_width, screen_height, colors):
    # Draws each tile on the game map, & checks if it blocks sight or not,if yes it draws a wall, if not it draws a floor
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                #if tile falls in fov_map, draw with light colors, if not draw with dark
                if visible:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)

                else:
                    if wall:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

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


