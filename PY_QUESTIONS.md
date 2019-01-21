why do you have to specify the folder name when importing Tile in game_map.py (from map_objects.tile import Tile) when engine.py can import entity directly (from entity import Entity)?

In game_map.py, why does he keep track of the number of rooms with a separate variable when he could just use the length of the rooms list?

Why do we have to import tcod in fighter to use the Message class? Is it because the Message class uses it and we need to get the lib in the dependency tree? But I thought that the Message file imported it already?
