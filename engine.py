import libtcodpy as libtcod

from components.fighter import Fighter
from components.inventory import Inventory
from death_functions import kill_monster, kill_player
from entity import Entity, get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import MessageLog, Message
from game_states import GameStates
from input_handlers import handle_keys
from map_objects.game_map import GameMap
from render_functions import clear_all, render_all, RenderOrder


def main():
    # how to define a function in python

    screen_width = 80
    screen_height = 50
    # variables for screen size

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 80
    map_height = 43

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
    max_items_per_room = 2

    colors = {
        'dark_wall': libtcod.Color(0, 0, 100),
        'dark_ground': libtcod.Color(50, 50, 150),
        'light_wall': libtcod.Color(130, 110, 50),
        'light_ground': libtcod.Color(200, 180, 50)
    }
    # dark wall/ground outside fov, light is what character can see

    fighter_component = Fighter(hp=30, defense=2, power=5)
    # player stats
    inventory_component = Inventory(26)
    # how many items can be held

    player = Entity(0, 0, '@', libtcod.white, 'Player',
                    blocks=True, render_order=RenderOrder.ACTOR,  fighter=fighter_component, inventory=inventory_component)
    entities = [player]

    libtcod.console_set_custom_font(
        'arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    # telling which font to use 'arial10x10' is the actual file we are importing, the other two are telling which type of file we are reading in this case a greyscale file with TCOD layout

    libtcod.console_init_root(screen_width, screen_height, 'X-ZOM', False)
    # creates the screen from width and height, with title and whether to go fullscreen or not

    con = libtcod.console_new(screen_width, screen_height)
    panel = libtcod.console_new(screen_width, panel_height)

    game_map = GameMap(map_width, map_height)
    game_map.make_map(max_rooms, room_min_size, room_max_size,
                      map_width, map_height, player, entities, max_monsters_per_room, max_items_per_room)

    fov_recompute = True

    fov_map = initialize_fov(game_map)

    message_log = MessageLog(message_x, message_width, message_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()
    # variable who hold our keyboard and mouse input

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state
    # for use after closing a menu and not losing a turn

    while not libtcod.console_is_window_closed():
        # game loop; won't end until we close the screen

        libtcod.sys_check_for_event(
            libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)
        # will update key and mouse variables with the user inputs

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, fov_radius,
                          fov_light_walls, fov_algorithm)
            # checks and recomputes the field of view

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   screen_width, screen_height, bar_width, panel_height, panel_y,  mouse, colors, game_state)
        # draws entities on the entities list/array, takes the console, entities, screen size, and colors then calls draw_entity on them then "blits" (or draws) the changes on the screen

        fov_recompute = False

        libtcod.console_flush()
        # puts everything on the screen

        clear_all(con, entities)
        # clears the entities after drawing them to the screen so they don't leave a background

        action = handle_keys(key, game_state)

        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        exit = action.get('exit')
        # get() returns the value for the specified key if the key is in the dictionary
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
                        message_log.add_message(
                            Message('hi bob', libtcod.yellow))

                    else:
                        attack_results = player.fighter.attack(target)
                        player_turn_results.extend(attack_results)

                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(
                    Message('There is nothing here to pick up.', libtcod.white))

        if show_inventory:
            # need the if here to check otherwise you can get stuck in the inventory screen
            if game_state != GameStates.SHOW_INVENTORY:
                previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.inventory.items):
            item = player.inventory.items[inventory_index]

            if game_state == GameStates.SHOW_INVENTORY:
                player_turn_results.extend(player.inventory.use(item))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        # refactor here to include a sure you want to quit?

        if exit:
            # w/ esc we exit to game from menu or quit from main game
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
                game_state = previous_game_state
            else:
                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            #print('player turn result', player_turn_result)
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

        if game_state == GameStates.ENEMY_TURN:
            for entity in entities:
                if entity.ai:
                    enemy_turn_results = entity.ai.take_turn(
                        player, fov_map, game_map, entities)

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            else:
                                message = kill_monster(dead_entity)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break

            else:
                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()
