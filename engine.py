import tcod as tcod

from death_functions import kill_monster, kill_player
from entity import get_blocking_entities_at_location
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message
from game_states import GameStates
from input_handlers import handle_keys, handle_mouse, handle_main_menu
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box
from render_functions import clear_all, render_all, RenderOrder


def play_game(player, entities, game_map, message_log, game_state, con, panel, constants):
    fov_recompute = True

    fov_map = initialize_fov(game_map)

    key = tcod.Key()
    mouse = tcod.Mouse()
    # variable who hold our keyboard and mouse input
    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state
    # for use after closing a menu and not losing a turn
    targeting_item = None

    while not tcod.console_is_window_closed():
        # game loop; won't end until we close the screen

        tcod.sys_check_for_event(
            tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)
        # will update key and mouse variables with the user inputs

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'],
                          constants['fov_light_walls'], constants['fov_algorithm'])
            # checks and recomputes the field of view

        render_all(con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['bar_width'], constants['panel_height'], constants['panel_y'],  mouse, constants['colors'], game_state)
        # draws entities on the entities list/array, takes the console, entities, screen size, and colors then calls draw_entity on them then "blits" (or draws) the changes on the screen

        fov_recompute = False

        tcod.console_flush()
        # puts everything on the screen

        clear_all(con, entities)
        # clears the entities after drawing them to the screen so they don't leave a background

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        take_stairs = action.get('take_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        wait = action.get('wait')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

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
                            Message('hi bob', tcod.yellow))

                    else:
                        attack_results = player.fighter.attack(target)
                        player_turn_results.extend(attack_results)

                else:
                    player.move(dx, dy)

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        elif wait:
            game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.item and entity.x == player.x and entity.y == player.y:
                    pickup_results = player.inventory.add_item(entity)
                    player_turn_results.extend(pickup_results)

                    break
            else:
                message_log.add_message(
                    Message('There is nothing here to pick up.', tcod.white))

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
                # (question)why not **kwargs here?
                player_turn_results.extend(player.inventory.use(
                    item, game_map, entities=entities, fov_map=fov_map))
            elif game_state == GameStates.DROP_INVENTORY:
                player_turn_results.extend(player.inventory.drop_item(item))

        if take_stairs and game_state == GameStates.PLAYERS_TURN:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    entities = game_map.next_floor(
                        player, message_log, constants)
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    tcod.console_clear(con)

                    break

            else:
                message_log.add_message(
                    Message('There are no stairs here.', tcod.yellow))

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 3
            elif level_up == 'def':
                player.fighter.base_defense += 1

            game_state = previous_game_state

        if show_character_screen:
            if game_state != GameStates.CHARACTER_SCREEN:
                previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click

                item_use_results = player.inventory.use(
                    targeting_item, game_map, entities=entities, fov_map=fov_map, target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)

            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})
                message_log.add_message(
                    Message('Targeting Cancelled', tcod.fuchsia))
        # refactor here to include a sure you want to quit?

        if exit:
            # w/ esc we exit to game from menu or quit from main game
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
                message_log.add_message(
                    Message('Targeting Cancelled', tcod.fuchsia))
            else:
                save_game(player, entities, game_map, message_log, game_state)
                return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            item_dropped = player_turn_result.get('item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            targeting_cancelled = player_turn_result.get(
                'targeting_cancelled')
            force_recompute = player_turn_result.get('force_recompute')
            xp = player_turn_result.get('xp')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                    # refactor add restart ability
                else:
                    message = kill_monster(dead_entity)

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if item_dropped:
                entities.append(item_dropped)
                game_state = GameStates.ENEMY_TURN

            if equip:
                equip_results = player.equipment.toggle_equip(equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        message_log.add_message(
                            Message(f'You equipped the {equipped.name}.'))

                    if dequipped:
                        message_log.add_message(
                            Message(f'You dequipped the {dequipped.name}'))

                game_state = GameStates.ENEMY_TURN

                if equipped:
                    message_log.add_message
            if targeting_cancelled:
                game_state = previous_game_state

            if force_recompute:
                fov_recompute = True

            if xp:
                leveled_up = player.level.add_xp(xp)
                message_log.add_message(
                    Message(f'You gain {xp} experience points'))

                if leveled_up:
                    message_log.add_message(Message(
                        f'You grow stronger. You are level {player.level.current_level}!', tcod.yellow))
                    previous_game_state = game_state
                    game_state = GameStates.LEVEL_UP

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


def main():
    constants = get_constants()

    tcod.console_set_custom_font(
        'arial10x10.png', tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
    # telling which font to use 'arial10x10' is the actual file we are importing, the other two are telling which type of file we are reading in this case a greyscale file with TCOD layout

    tcod.console_init_root(constants['screen_width'],
                           constants['screen_height'], 'X-ZOM', False)
    # creates the screen from width and height, with title and whether to go fullscreen or not

    con = tcod.console_new(
        constants['screen_width'], constants['screen_height'])
    panel = tcod.console_new(
        constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = tcod.image_load('menu_background1.png')

    key = tcod.Key()
    mouse = tcod.Mouse()

    while not tcod.console_is_window_closed():
        tcod.sys_check_for_event(
            tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(con, main_menu_background_image,
                      constants['screen_width'], constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'No save game to load', 50,
                            constants['screen_width'], constants['screen_height'])

            tcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state = get_game_variables(
                    constants)
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            tcod.console_clear(con)
            play_game(player, entities, game_map, message_log,
                      game_state, con, panel, constants)

            show_main_menu = True


if __name__ == '__main__':
    main()
