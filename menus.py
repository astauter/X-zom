import tcod as tcod

from equipment_slots import EquipmentSlots

# return here to refactor


def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26:
        raise ValueError('Cannot have a menu with more than 26 options')

    # calculate total height for the header and one line per option
    header_height = tcod.console_get_height_rect(
        con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # create an off-screen console that represents the menu's window
    window = tcod.console_new(width, height)

    # print header with autowrap
    tcod.console_set_default_foreground(window, tcod.white)
    tcod.console_print_rect_ex(
        window, 0, 0, width, height, tcod.BKGND_NONE, tcod.LEFT, header)

    # refactor
    # print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ') ' + option_text
        tcod.console_print_ex(
            window, 0, y, tcod.BKGND_NONE, tcod.LEFT, text)
        y += 1
        letter_index += 1

    # blit contents of the "window" to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    tcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    # show a menu with each item of the inventory as an option
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        options = []

        for item in player.inventory.items:
            if player.equipment.main_hand == item:
                options.append(f'{item.name} (wielding)')
            elif player.equipment.off_hand == item:
                options.append(f'{item.name} (on off-hand)')
            elif player.equipment.amulet == item:
                options.append(f'{item.name} (wearing)')
            elif player.equipment.ring == item:
                options.append(f'{item.name} (wearing)')
            elif player.equipment.armor == item:
                options.append(f'{item.name} (wearing)')
            elif player.equipment.helmet == item:
                options.append(f'{item.name} (wearing)')
            else:
                options.append(item.name)

    menu(con, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, background_image, screen_width, screen_height):
    tcod.image_blit_2x(background_image, 0, 0, 0)

    tcod.console_set_default_foreground(0, tcod.light_yellow)
    tcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) -
                          4, tcod.BKGND_NONE, tcod.CENTER, 'DUNGEONS OF DESPAIR')
    tcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2),
                          tcod.BKGND_NONE, tcod.CENTER, 'By Alex Stauter and Willy Raedy')

    menu(con, '', ['Play a new game', 'Continue', 'Quit'],
         24, screen_width, screen_height)


def level_up_menu(con, header, player, menu_width, screen_width, screen_height):
    options = ['Constitution (+20 HP)',
               'Strength (+3 attack)', 'Agility (+1 defense)']

    menu(con, header, options, menu_width, screen_width, screen_height)


def message_box(con, header, width, screen_width, screen_height):
    menu(con, header, [], width, screen_width, screen_height)


def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = tcod.console_new(character_screen_width, character_screen_height)

    tcod.console_set_default_foreground(window, tcod.white)

    # [{ verticalIndex: 1, displayText: 'blah blah }]

    lines = generate_character_screen_lines(player)
    print('HERE Lines:, ', lines)
    print('***************')
    for line in lines:
        print("flasjfaoisefen", line)
        tcod.console_print_rect_ex(window, 0, line.verticalIndex, character_screen_width, character_screen_height, tcod.BKGND_NONE, tcod.LEFT, line.displayText)

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    tcod.console_blit(window, 0, 0, character_screen_width,
                      character_screen_height, 0, x, y, 1.0, 0.7)

def generate_character_screen_lines(player):
    lines = []

    lines.append({ 'verticalIndex': 1, 'displayText': 'Character Stats' })
    lines.append({ 'verticalIndex': 2, 'displayText': f'Level: {player.level.current_level}' })
    lines.append({ 'verticalIndex': 3, 'displayText': f'Maximum HP: {player.fighter.max_hp}' })
    lines.append({ 'verticalIndex': 4, 'displayText': f'Attack: {player.fighter.power}' })
    lines.append({ 'verticalIndex': 5, 'displayText': f'Defense: {player.fighter.defense}' })
    lines.append({ 'verticalIndex': 6, 'displayText': f'Experience to Level Up: {player.level.experience_to_next_level - player.level.current_xp}' })

    lines.append({ 'verticalIndex': 8, 'displayText': 'Character Equipment' })
    for idx, equipmentSlot in enumerate(['main_hand', 'off_hand', 'helmet', 'armor', 'ring', 'amulet']):
        equipment = getattr(player.equipment, equipmentSlot)
        equipmentName = 'None'
        if (equipment):
            #print(equipment)
            equipmentName = equipment.name
        label = equipmentSlot
        displayText = f'{label}: {equipmentName}'

        lines.append({ 'verticalIndex': 9 + idx, 'displayText': displayText })

    return lines


