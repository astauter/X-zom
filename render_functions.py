import tcod as tcod

from enum import Enum

from menus import character_screen, inventory_menu, level_up_menu
from game_states import GameStates


class RenderOrder(Enum):
    # refactor auto() function
    STAIRS = 1
    CORPSE = 2
    ITEM = 3
    ACTOR = 4


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name for entity in entities if entity.x == x and entity.y ==
             y and tcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    tcod.console_set_default_background(panel, back_color)
    tcod.console_rect(panel, x, y, total_width, 1,
                      False, tcod.BKGND_SCREEN)

    tcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        tcod.console_rect(panel, x, y, bar_width, 1,
                          False, tcod.BKGND_SCREEN)

    tcod.console_set_default_foreground(panel, tcod.white)
    tcod.console_print_ex(panel, int(
        x + total_width / 2), y, tcod.BKGND_NONE, tcod.CENTER, '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height, bar_width, panel_height, panel_y, mouse, colors, game_state):
    # Draws each tile on the game map, & checks if it blocks sight or not,if yes it draws a wall, if not it draws a floor
    if fov_recompute:
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = tcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                burned = game_map.tiles[x][y].burned

                # if tile falls in fov_map, draw with light colors, if not draw with dark
                if visible:
                    if wall:
                        current_color = colors.get(
                            'charred_wall') if burned else colors.get('light_wall')
                        tcod.console_set_char_background(
                            con, x, y, current_color, tcod.BKGND_SET)
                    else:
                        current_color = colors.get(
                            'charred_ground') if burned else colors.get('light_ground')
                        tcod.console_set_char_background(
                            con, x, y, current_color, tcod.BKGND_SET)

                    game_map.tiles[x][y].explored = True

                elif game_map.tiles[x][y].explored:
                    if wall:
                        tcod.console_set_char_background(
                            con, x, y, colors.get('dark_wall'), tcod.BKGND_SET)
                    else:
                        tcod.console_set_char_background(
                            con, x, y, colors.get('dark_ground'), tcod.BKGND_SET)

    entities_in_render_order = sorted(
        entities, key=lambda x: x.render_order.value)

    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)

    tcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)
    # draws entities on the entities list/array, takes the console, entities, and screen size then calls draw_entity on them then "blits" (or draws) the changes on the screen

    tcod.console_set_default_background(panel, tcod.black)
    tcod.console_clear(panel)

    # Print game message, one line at at a time
    for y, message in enumerate(message_log.messages, 1):
        tcod.console_set_default_foreground(panel, message.color)
        tcod.console_print_ex(panel, message_log.x,
                              y, tcod.BKGND_NONE, tcod.LEFT, message.text)

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp,
               player.fighter.max_hp, tcod.light_red, tcod.darker_red)
    tcod.console_print_ex(panel, 1, 3, tcod.BKGND_NONE,
                          tcod.LEFT, f'Dungeon level: {game_map.dungeon_level}')

    tcod.console_set_default_foreground(panel, tcod.light_gray)
    tcod.console_print_ex(panel, 1, 0, tcod.BKGND_NONE,
                          tcod.LEFT, get_names_under_mouse(mouse, entities, fov_map))

    tcod.console_blit(panel, 0, 0, screen_width,
                      panel_height, 0, 0, panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        if game_state == GameStates.SHOW_INVENTORY:
            inventory_title = 'Press the key next to an item to use it, or Esc to cancel.\n'
        else:
            inventory_title = 'Press the key next to an item to drop it, or Esc to cancel.\n'

        inventory_menu(con, inventory_title, player,
                       50, screen_width, screen_height)

    elif game_state == GameStates.LEVEL_UP:
        level_up_menu(con, 'LEVEL UP! Choose a stat to raise:',
                      player, 40, screen_width, screen_height)
    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 15, screen_width, screen_height)


def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

    # clears the entities after drawing them to the screen


def draw_entity(con, entity, fov_map, game_map):
    if tcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        tcod.console_set_default_foreground(con, entity.color)
        tcod.console_put_char(
            con, entity.x, entity.y, entity.char, tcod.BKGND_NONE)

    # does the drawing, flexible to draw any entity passed to it


def clear_entity(con, entity):
    # erase the character that represents this object so when it moves there is no trail behind
    tcod.console_put_char(con, entity.x, entity.y, ' ', tcod.BKGND_NONE)
