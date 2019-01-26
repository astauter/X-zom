import dill

from entity import Entity

from game_states import GameStates

from game_messages import MessageLog

from map_objects.game_map import GameMap

def save_game(player, entities, game_map, message_log, game_state):
  data = {
    'player_index': entities.index(player),
    'entities': entities,
    'game_map': game_map,
    'message_log': message_log,
    'game_state': game_state
  }

  with open('save_game', 'wb') as save_file:
    dill.dump(data, save_file)

def load_game():
  with open('save_game', 'rb') as save_file:
    data = dill.load(save_file)

  player_index = data['player_index']
  entities = data['entities']
  game_map = data['game_map']
  message_log = data['message_log']
  game_state = data['game_state']

  player = entities[player_index]

  return player, entities, game_map, message_log, game_state
