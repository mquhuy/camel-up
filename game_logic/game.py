import enum
import random
import names

try:
    from .space import Space, Camel
    from .player import Player
    from .config import CAMELS, FINAL_BET_WINNER_PRIZES
except (ImportError, ValueError):
    from space import Space, Camel
    from player import Player
    from config import CAMELS, FINAL_BET_WINNER_PRIZES


class Game:
    def __init__(self, players=[], n_init_players=0):
        self.players = [Player(name, p_id) for p_id, name in enumerate(players)]
        self.camels = [Camel(camel_name) for camel_name in CAMELS]
        self.spaces = [Space(space_id) for space_id in range(16)]
        self.winning_camel = None
        self.losing_camel = None
        self.current_player_idx = 0
        self.final_bet_winning_camel = {camel: [] for camel in self.camels}
        self.final_bet_losing_camel = {camel: [] for camel in self.camels}
        self.initialize_players(n_init_players)
        self.game_on = False

    def start_game(self):
        self.game_on = True
        init_locs = self.roll_init_dice()
        print("Initialized camel's starting position:")
        camels = list(init_locs.keys())
        random.shuffle(camels)
        for camel in camels:
            self.move(camel, init_locs[camel])

    def initialize_players(self, n_players):
        n_players_to_create = n_players - len(self.players)
        if (n_players_to_create < 0):
            return
        i = 1
        while True:
            name = names.get_first_name()
            result, _ = self.register(name, False)
            if result:
                i += 1
            if i > n_players_to_create:
                break

    def register(self, new_player_name, human=True):
        new_id = len(self.players)
        names = [player.name for player in self.players]
        if new_player_name in names:
            return (False, "player name existed")
        self.players.append(Player(new_player_name, new_id, human))
        return (True, str(new_id))

    def move(self, camel, steps):
        new_pos = camel.pos_id() + steps
        if new_pos >= len(self.spaces):
            self.declare_winning_camel(camel)
            return
        if self.spaces[new_pos].desert_state != 0:
            self.spaces[new_pos].desert_player.earn_points(1, "owning the desert")
            new_pos += self.spaces[new_pos].desert_state
        if new_pos >= (len(self.spaces) - 1):
            self.declare_winning_camel(camel)
            return
        self.spaces[new_pos].add_camels(camel)

    def roll_init_dice(self):
        return {camel: random.randrange(3) + 1 for camel in self.camels}

    def declare_winning_camel(self, camel):
        self.winning_camel = camel.position.get_top_camel()
        self.spaces[-1].add_camels(camel)

    def next_player(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def current_player(self):
        if len(self.players) == 0:
            return None
        return self.players[self.current_player_idx]

    def run_leg(self):
        self.init_leg()
        while not self.check_end_leg():
            self.next_player()
            while True:
                if self.current_player().take_turn(self):
                    break
            print("-------")
        self.leg_scoring_round()
        self.report()

    # Leg
    def init_leg(self):
        self.pyramid_dices = self.camels.copy()
        self.betting_tiles = {camel: [] for camel in self.camels}
        self.rollers = []
        for player in self.players:
            player.reset_bets()

    def roll_pyramid_dice(self):
        camel_index = random.randrange(len(self.pyramid_dices))
        camel = self.pyramid_dices.pop(camel_index)
        steps = random.randrange(3) + 1
        print("*** Roll dice: {} with step {}".format(camel.name, steps))
        self.move(camel, steps)
        return camel, steps

    def check_end_leg(self):
        return (len(self.pyramid_dices) == 0 or self.winning_camel is not None)

    def determine_leg_result(self):
        orders = {camel: camel.position.id + camel.position.camels.index(camel)/10 for camel in self.camels}
        self.orders = sorted(orders, key=orders.get, reverse=True)

    def leg_scoring_round(self):
        self.determine_leg_result()
        for idx, player in enumerate(self.betting_tiles[self.orders[0]]):
            player.win_leg_bet(idx)
        for player in self.betting_tiles[self.orders[1]]:
            player.earn_points(1, "leg betting second place")
        for camel in self.orders[2:]:
            for player in self.betting_tiles[camel]:
                player.lose_points(1, "losing the leg bet")
        for player in self.rollers:
            player.earn_points(1, "rolling the dice")

    def game_scoring_round(self):
        def final_rewarding(betting_dict, betting_dict_name):
            reason = "betting final {} camel".format(betting_dict_name)
            for camel, betting_p in betting_dict.items():
                if camel == self.winning_camel:
                    for idx, player in enumerate(betting_p):
                        if idx < len(FINAL_BET_WINNER_PRIZES):
                            points = FINAL_BET_WINNER_PRIZES[idx]
                            player.earn_points(points, reason)
                        else:
                            player.earn_points(1, reason)
                else:
                    for player in betting_p:
                        player.lose_points(1, reason)

        final_rewarding(self.final_bet_winning_camel, "winning")
        final_rewarding(self.final_bet_losing_camel, "losing")

    def determine_game_result(self):
        self.scores = {player.name: player.points for player in self.players}
        orders = sorted(self.scores, key=self.scores.get, reverse=True)
        self.winning_player = orders[0]
        self.scores = {player: self.scores[player] for player in orders}
        print("Scoring table:")
        print(self.scores)

    def can_put_desert(self, player, space):
        if space.id == 0:
            return False
        if space.desert_player is not None:
            return False
        if (self.spaces[space.id - 1].desert_player not in [None, player] ):
            return False
        if (space.id < 15 and self.spaces[space.id + 1].desert_player not in [None, player]):
            return False
        if (len(space.camels) > 0):
            return False
        return True

    def report(self):
        print("Current Positions:")
        for camel in self.camels:
            print("Camel {} is at pos {}".format(camel.name, camel.pos_id()))

        print("Stacking situation:")
        for space in self.spaces:
            print("Space id {}, camels {}".format(space.id, space.print_camels()))
        if self.winning_camel is not None:
            print("The winning camel is {}".format(self.winning_camel.name))

        self.determine_game_result()

    def start(self):
        init_locs = self.roll_init_dice()
        print("Initialized camel's starting position:")
        camels = list(init_locs.keys())
        random.shuffle(camels)
        for camel in camels:
            self.move(camel, init_locs[camel])
        print("Shuffling playing order")
        random.shuffle(self.players)
        self.report()
        while self.winning_camel is None:
            self.run_leg()
            self.report()
            print("------------------- End leg ---------------------")
        self.losing_camel = self.orders[-1]
        self.game_scoring_round()
        self.determine_game_result()

if __name__ == "__main__":
    g = Game(n_init_players=5)
    g.start()
