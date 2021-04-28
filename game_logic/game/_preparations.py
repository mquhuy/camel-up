import copy
import random
import string
import names
from ..config import LEG_BET_PRIZES
from ..player import Player

def generate_new_id(self, existing_list, prefix=""):
    # Generate an id that does not exist in current list
    letters = string.ascii_lowercase
    while True:
        random_id = ( ''.join(random.choice(letters) for i in range(5)))
        new_id = prefix + random_id
        if new_id not in existing_list:
            return new_id

def init_playing_order(self):
    print("Shuffling playing order")
    self.playing_order = list(self.players.keys())
    random.shuffle(self.playing_order)
    self.playing_queue = copy.deepcopy(self.playing_order)
    self.next_player()

def reset_dices(self):
    self.pyramid_dices = copy.deepcopy(list(self.camels.keys()))
    self.betting_tiles = {camel_name: [prize for prize in LEG_BET_PRIZES]
                          for camel_name in self.camels}
    self.rollers = []
    self.roll_results = []

def register(self, new_player_name, human=True):
    print("Registering player {}".format(new_player_name))
    player_names = [player.name for player in self.players.values()]
    if new_player_name in player_names:
        return (False, "player name existed")
    new_id = self.generate_new_id(self.players.keys())
    self.players[new_id] = Player(new_player_name, new_id, human)
    return (True, str(new_id))

def set_expected_n_players(self, n_players):
    self.expected_n_players = n_players

def check_enough_players(self):
    registered_players = [1 for player in self.players.values()
                          if player.is_human and player.ready]
    return sum(registered_players) == self.expected_n_players

def init_bots(self, n_bots):
    if n_bots <= 0:
        return
    i = 1
    while True:
        name = names.get_first_name()
        result, _ = self.register(name, False)
        if result:
            i += 1
        if i > n_bots:
            break

def roll_init_dice(self):
    return {camel: random.randrange(3) + 1 for camel in self.camels.keys()}

def reset(self, keep_players=True):
    # Reset the game state to prepare for a new game with same players
    if keep_players:
        for player in self.players.values():
            player.reset()
        self.game_state = "initialization"
    else:
        self.players = {}
        self.game_state = "registration"
    for camel in self.camels.values():
        camel.reset()
    for space in self.spaces.values():
        space.reset()
    self.final_space.reset()
    self.final_winning_deck = {camel_name: [] for camel_name in self.camels}
    self.final_losing_deck = {camel_name: [] for camel_name in self.camels}
    self.winning_camel = None
    self.losing_camel = None
    self.playing_order = None
    self.reset_dices()

