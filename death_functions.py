import tcod as tcod
from random import randint

from game_messages import Message
from game_states import GameStates
from render_functions import RenderOrder


def kill_player(player):
    player.char = '%'
    player.color = tcod.dark_red

    death_messages = ['You suck', "ha ha", "You died!", "try again, buddy"]
    death_message = death_messages[randint(0, len(death_messages) - 1)]

    return Message(death_message, tcod.red), GameStates.PLAYER_DEAD


def kill_monster(monster):
    death_message = Message('{0} is dead!'.format(
        monster.name.capitalize()), tcod.dark_red)

    monster.char = '%'
    monster.color = tcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = 'remains of ' + monster.name
    monster.render_order = RenderOrder.CORPSE

    return death_message
