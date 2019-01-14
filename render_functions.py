import libtcodpy as libtcod

from enum import Enum

from menus import inventory_menu
from game_states import GameStates


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    ACTOR = 3


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities if entity.x == x and entity.y ==
             y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1,
                         False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1,
                             False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(
        x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state):
    # Draws each tile on the game map, & checks if it blocks sight or not,if yes it draws a wall, if not it draws a floor
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight

                # if tile falls in fov_map, draw with light colors, if not draw with dark
                if visible:
                    if wall:
                        libtcod.console_set_char_background(
                            con, x, y, colors.get('light_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(
                            con, x, y, colors.get('light_ground'), libtcod.BKGND_SET)

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        libtcod.console_set_char_background(
                            con, x, y, colors.get('dark_wall'), libtcod.BKGND_SET)
                    else:
                        libtcod.console_set_char_background(
                            con, x, y, colors.get('dark_ground'), libtcod.BKGND_SET)

    entities_in_render_order = sorted(
        entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    # draws entities on the entities list/array, takes the console, entities, and screen size then calls draw_entity on them then "blits" (or draws) the changes on the screen

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print game message, one line at at a time
    for y, message in enumerate(message_log.messages, 1):
        libtcod.console_set_default_foreground(panel, message.color)
        #print(y, message_log.x, libtcod.BKGND_NONE, )
        libtcod.console_print_ex(panel, message_log.x,
                                 y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp,
               player.fighter.max_hp, libtcod.light_red, libtcod.darker_red)

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE,
                             libtcod.LEFT, get_names_under_mouse(mouse, entities, fov_map))

    libtcod.console_blit(panel, 0, 0, screen_width,
                         panel_height, 0, 0, panel_y)

    if game_state == GameStates.SHOW_INVENTORY:
        inventory_menu(con, 'Press the key next to an item to use it, or Esc to cancel.\n',
                       player.inventory, 50, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

    # clears the entities after drawing them to the screen


def draw_entity(con, entity, fov_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(
            con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

    # does the drawing, flexible to draw any entity passed to it


def clear_entity(con, entity):
    # erase the character that represents this object so when it moves there is no trail behind
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)
