import libtcodpy as libtcod

from components.fighter import Fighter
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_states import GameStates
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all, RenderOrder


def main():
    # how to define a function in python

    screen_width = 80
    screen_height = 50
    # variables for screen size

    map_width = 80
    map_height = 45

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    # default algo used by libtcod
    fov_light_walls = True
    # tells us whether to light up walls we see
    fov_radius = 10
    # tells us how far our character can see
    max_monsters_per_room = 3

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }
    # dark wall/ground outside fov, light is what character can see

    fighter_component = Fighter(hp=30, defense=2, power=5)
    player = Entity(0, 0, '@', libtcod.white, 'Player',
                    blocks=True, render_order=RenderOrder.ACTOR,  fighter=fighter_component)
    entities = [player]

    libtcod.console_set_custom_font(
        'arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    # telling which font to use 'arial10x10' is the actual file we are importing, the other two are telling which type of file we are reading in this case a greyscale file with TCOD layout

    libtcod.console_init_root(screen_width, screen_height, 'X-ZOM', False)
    # creates the screen from width and height, with title and whether to go fullscreen or not

    con = libtcod.console_new(screen_width, screen_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size,
                      map_width, map_height, player, entities, max_monsters_per_room)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()
    # variable who hold our keyboard and mouse input

    game_state = GameStates.PLAYERS_TURN

    while not libtcod.console_is_window_closed():
        # game loop; won't end until we close the screen

        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        # will update key and mouse variables with the user inputs

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius,
                          fov_light_walls, fov_algorithm)
            # checks and recomputes the field of view

        render_all(con, entities, player, game_map, fov_map, fov_recompute,
                   screen_width, screen_height, colors)
        # draws entities on the entities list/array, takes the console, entities, screen size, and colors then calls draw_entity on them then "blits" (or draws) the changes on the screen

        fov_recompute = False

        libtcod.console_flush()
        # puts everything on the screen

        clear_all(con, entities)
        # clears the entities after drawing them to the screen so they don't leave a background

        action = handle_keys(key)

        move = action.get('move')
        # get() returns the value for the specified key if the key is in the dictionary
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        player_turn_results = []

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(
                    entities, destination_x, destination_y)

                if target:

                    if target.name == "NPC":
                        print('Hello Bob!')

                    else:
                        attack_results = player.fighter.attack(target)
                        player_turn_results.extend(attack_results)

                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')

            if message:
                print(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                print(message)

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(
                        player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            print(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            print(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN

        #key = libtcod.console_check_for_keypress()
        # if key.vk == libtcod.KEY_ESCAPE:
        #    return True
        # allows an exit by hitting an excape. if excape was hit, we return true and leave the loop


if __name__ == '__main__':
    main()
