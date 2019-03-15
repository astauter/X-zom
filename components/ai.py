import tcod as tcod

from random import randint

from game_messages import Message


class BasicMonster:
    def __init__(self, owner=None):
        self.owner = owner

    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner

        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                monster.move_astar(target, entities, game_map)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

        return results

    def __repr__(self):
        return f'BasicMonster AI'


class RangedMonster:
    def __init__(self, attack_range, owner=None):
        self.attack_range = attack_range
        self.owner = owner

    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner

        if tcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2 and monster.distance_to(target) <= self.attack_range and target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                results.extend(attack_results)

            elif monster.distance_to(target) > self.attack_range:
                monster.move_astar(target, entities, game_map)

            else:
                could_move = monster.move_away(
                    target.x, target.y, game_map, entities)
                if not could_move:
                    attack_results = monster.fighter.attack(target)
                    results.extend(attack_results)

        return results


class HunterMonster:
    def __init__(self, attack_range, alt_attack, owner=None):
        self.attack_range = attack_range
        self.alt_attack = alt_attack
        self.owner = owner

    def take_turn(self, target, fov_map, game_map, entities):
        results = []
        monster = self.owner

        if monster.distance_to(target) >= 2 and monster.distance_to(target) <= self.attack_range and target.fighter.hp > 0:
            attack_results = monster.fighter.attack(target, self.alt_attack)
            results.extend(attack_results)
        elif monster.distance_to(target) < 2 and target.fighter.hp > 0:
            attack_results = monster.fighter.attack(target)
            results.extend(attack_results)
        else:
            monster.move_astar(target, entities, game_map)

        return results


class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10, owner=None):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns
        self.owner = owner

    def take_turn(self, target, fov_map, game_map, entities):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message(
                f'The {self.owner.name} is no longer confused!', tcod.fuchsia)})
        return results


class ParalyzedMonster:
    def __init__(self, previous_ai, number_of_turns=None, owner=None):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns
        self.owner = owner

    def take_turn(self, *args):
        results = []

        return results

    def __repr__(self):
        return f'Previous AI: {self.previous_ai}, # of turns {self.number_of_turns}'
