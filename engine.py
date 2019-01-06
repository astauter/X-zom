import libtcodpy as libtcod

from entity import Entity
from input_handlers import handle_keys

def main():
    #how to define a function in python

    screen_width = 80
    screen_height = 50
    #variables for screen size

    player = Entity(int(screen_width / 2), int(screen_height /2), '@', libtcod.white)
    #putting player in the middle of the screen, int() is used because python 3 doesnt auto truncate so we need int() to remove the float
    npc = Entity(int(screen_width /2 -5), int(screen_height /2), '@', libtcod.yellow)
    entities = [npc, player]
    #"list" that will hold all entities on the map


    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    # telling which font to use 'arial10x10' is the actual file we are importing, the other two are telling which type of file we are reading in this case a greyscale file with TCOD layout

    libtcod.console_init_root(screen_width, screen_height, 'X-ZOM', False)
    #creates the screen from width and height, with title and whether to go fullscreen or not

    con = libtcod.console_new(screen_width, screen_height)

    key = libtcod.Key()
    mouse = libtcod.Mouse()
    #variable who hold our keyboard and mouse input

    while not libtcod.console_is_window_closed():
        #game loop; won't end until we close the screen
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)
        #will update key and mouse variables with the user inputs

        libtcod.console_set_default_foreground(con, libtcod.white)
        libtcod.console_put_char(con, player.x, player.y, player.char, libtcod.BKGND_NONE)
            #0 refers to console we are printing to, next are the x and y coordinates, next is the symbol we are printing, then the background
        libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

        libtcod.console_put_char(con, player.x, player.y, ' ', libtcod.BKGND_NONE)
            #second version to clear the console behind us i think


        #libtcod.console_set_default_foreground(0, libtcod.red)
            #sets the color for our symbol, 0 is the console we are drawing to?

        libtcod.console_flush()
        #puts everything on the screen

        action = handle_keys(key)

        move = action.get('move')
        #get() returns the value for the specified key if the key is in the dictionary
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')

        if move:
            dx, dy = move
            player.move(dx, dy)

        if exit:
            return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())


        #key = libtcod.console_check_for_keypress()
        #if key.vk == libtcod.KEY_ESCAPE:
        #    return True
        #allows an exit by hitting an excape. if excape was hit, we return true and leave the loop

if __name__ == '__main__':
    main()
