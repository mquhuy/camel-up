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

    def reset_bets(self):
        self.bets = {camel: False for camel in CAMELS}

    def win_leg_bet(self, pos):
        if pos > 2:
            return
        print("Player {} wins the bet at pos {}".format(self.name, pos + 1))
        self.earn_points(LEG_BET_PRIZES[pos])

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
        game.roll_pyramid_dice()
        game.rollers.append(self)
        return True

    def bet_leg(self, camel, game):
        print("Player {} bet that camel {} wins the leg".format(self.name, camel.name))
        if (len(game.betting_tiles[camel]) < len(LEG_BET_PRIZES)) and not (self.bets[camel.name]):
            game.betting_tiles[camel].append(self)
            self.bets[camel.name] = True
            return True
        else:
            print("Cannot bet since all the bets were taken")
            return False

    def bet_game_winning_camel(self, camel, game):
        print("Player {} bet that camel {} wins the game".format(self.name, camel.name))
        if (not (self.final_bets[camel.name])):
            game.final_bet_winning_camel[camel].append(self)
            self.final_bets[camel.name] = True
            return True
        else:
            print("Cannot bet since all the bets were taken")
            return False

    def bet_game_losing_camel(self, camel, game):
        print("Player {} bet that camel {} loses the game".format(self.name, camel.name))
        if (not (self.final_bets[camel.name])):
            game.final_bet_losing_camel[camel].append(self)
            self.final_bets[camel.name] = True
            return True
        else:
            print("Cannot bet since all the bets were taken")
            return False

    def set_desert(self, game, space, state):
        if not game.can_put_desert(self, space):
            print("Player {} cannot put desert on space {}.".format(self.name, space.id))
            return False
        print("Player {} puts desert on space {} with state {}.".format(self.name, space.id, state))
        self.desert_space = space
        space.set_desert(self, state)
        return True

    def take_turn(self, game, kargs=[]):
        if not self.is_human:
            choice = random.randrange(5)
            space_idx = random.randrange(16)
            state = random.choice([-1, 1])
            camel_idx = random.randrange(5)
            actions = (choice, space_idx, state, camel_idx)
        else:
            actions = kargs
        return self.perform_turn_actions(game, actions)

    def perform_turn_actions(self, game, actions):
        turn_success = False
        action_choice, space_idx, state, camel_idx = actions
        camel = game.camels[camel_idx]
        space = game.spaces[space_idx]
        if action_choice == 0:
            turn_success = self.roll_dice(game)
        elif action_choice == 1:
            turn_success = self.bet_leg(camel, game)
        elif action_choice == 2:
            turn_success = self.bet_game_winning_camel(camel, game)
        elif action_choice == 3:
            turn_success = self.bet_game_losing_camel(camel, game)
        elif action_choice == 4:
            turn_success = self.set_desert(game, space, state)
        return turn_success
