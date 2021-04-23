import random
try:
    from .config import CAMELS, LEG_BET_PRIZES
except (ImportError, ValueError):
    from config import CAMELS, LEG_BET_PRIZES


class Player:
    def __init__(self, name, player_id, is_human=False):
        self.name = name
        self.p_id = player_id
        self.points = 0
        self.reset_bets()
        self.final_bets = {camel: False for camel in CAMELS}
        self.desert_space = None
        self.is_human = is_human

    def reset(self):
        self.points = 0
        self.final_bets = {camel: False for camel in CAMELS}
        self.reset_bets()
        self.desert_space = None

    def reset_bets(self):
        self.leg_bets = {camel: [] for camel in CAMELS}

    def earn_points(self, points, reason=""):
        if reason != "":
            print("Player {} earns {} points for reason: {}".format(self.name, points, reason))
        self.points += points

    def lose_points(self, points, reason=""):
        if reason != "":
            print("Player {} loses {} points for reason: {}".format(self.name, points, reason))
        self.points -= points
        self.points = max(self.points, 0)

    def roll_dice(self, game):
        print("Player {} rolling dice".format(self.name))
        camel, steps = game.roll_pyramid_dice()
        game.rollers.append(self)
        return True, camel, steps

    def bet_leg(self, camel_name, game):
        print("Player {} bet that camel {} wins the leg".format(self.name, camel_name))
        if len(game.betting_tiles[camel_name]) > 0:
            self.leg_bets[camel_name].append(game.betting_tiles[camel_name].pop(0))
            return True, ""
        return False, "Cannot bet since all the bets were taken"

    def leg_bet_scoring(self, orders):
        for camel, points in self.leg_bets.items():
            if camel == orders[0].name and len(points) > 0:
                self.earn_points(sum(points), "leg betting winner")
            elif camel == orders[1].name and len(points) > 0:
                self.earn_points(len(points), "leg betting second place")
            elif len(points) > 0:
                self.lose_points(len(points), "losing the leg bet")

    def bet_game_winning_camel(self, camel_name, game):
        print("Player {} bets that camel {} wins the game".format(self.name, camel_name))
        if (not (self.final_bets[camel_name])):
            game.final_bet_winning_camel[camel_name].append(self)
            self.final_bets[camel_name] = True
            return True, ""
        else:
            return False, "Cannot bet since all the bets were taken"

    def bet_game_losing_camel(self, camel_name, game):
        print("Player {} bet that camel {} loses the game".format(self.name, camel_name))
        if (not (self.final_bets[camel_name])):
            game.final_bet_losing_camel[camel_name].append(self)
            self.final_bets[camel_name] = True
            return True, ""
        else:
            return False, "Cannot bet since all the bets were taken"

    def set_desert(self, game, space, state):
        if not game.can_put_desert(self, space):
            return False, "Player {} cannot put desert on space {}.".format(self.name, space.id)
        if self.desert_space is not None:
            self.desert_space.remove_desert()
        self.desert_space = space
        space.set_desert(self, state)
        return True, "Player {} puts desert on space {} with state {}.".format(self.name, space.id, state)

    def remove_desert(self):
        self.desert_space = None

    def take_turn(self, game, kargs=[]):
        choices = ["roll", "bet leg", "bet end win", "bet end lose", "set desert"]
        if not self.is_human:
            choice_idx = random.randrange(len(choices))
            space_idx = random.randrange(16)
            state = random.choice([-1, 1])
            camel_name = random.choice(CAMELS)
        else:
            choice_idx, space_idx, state, camel_name = kargs
        choice = choices[choice_idx]
        camel = game.find_camel_with_name(camel_name)
        space = game.spaces[space_idx]
        actions = (choice, space, state, camel)
        return self.perform_turn_actions(game, actions)

    def perform_turn_actions(self, game, actions):
        turn_success = False
        action_choice, space, state, camel = actions
        steps = None
        log = ""
        if action_choice == "roll":
            turn_success, camel, steps = self.roll_dice(game)
        elif action_choice == "bet leg":
            turn_success, log = self.bet_leg(camel.name, game)
        elif action_choice == "bet end win":
            turn_success, log = self.bet_game_winning_camel(camel.name, game)
        elif action_choice == "bet end lose":
            turn_success, log = self.bet_game_losing_camel(camel.name, game)
        elif action_choice == "set desert":
            turn_success, log = self.set_desert(game, space, state)
        return turn_success, {'action': action_choice,
                              'spaceIdx': space.id + 1,
                              'state': state,
                              'camel': camel.name,
                              'roll_num': steps,
                              'log': log}
