import enum
import random

try:
    from ..space import Space, Camel
    from ..player import Player
    from ..config import CAMELS, FINAL_BET_WINNER_PRIZES, LEG_BET_PRIZES
except(ImportError, ValueError):
    from space import Space, Camel
    from player import Player
    from config import CAMELS, FINAL_BET_WINNER_PRIZES, LEG_BET_PRIZES


class Game:
   def __init__(self, n_bots=0):
        self.players = {}
        self.camels = {camel_name: Camel(camel_name) for camel_name in CAMELS}
        self.spaces = {space_id: Space(space_id) for space_id in range(1, 17)}
        self.final_space = Space(17)
        self.winning_camel = None
        self.losing_camel = None
        self.final_winning_deck = {camel_name: [] for camel_name in self.camels}
        self.final_losing_deck = {camel_name: [] for camel_name in self.camels}
        self.last_bet_winner = None
        self.last_bet_loser = None
        self.init_bots(n_bots)
        self.game_state = "registration"
        self.playing_order = None
        self.current_player = None
        self.reset_dices()
        self.id = None
        self.io = None
        self.expected_n_players = 0
        self.roll_results = []

   # Leg
   from ._preparations import \
           generate_new_id, \
           init_playing_order, \
           reset_dices, \
           register, \
           set_expected_n_players, \
           check_enough_players, \
           init_bots, \
           roll_init_dice, \
           reset

   from ._leg import \
           init_leg, \
           check_end_leg, \
           determine_leg_result, \
           leg_scoring_round

   from ._actions import \
           roll_pyramid_dice, \
           start_game, \
           move, \
           move_camel_to_space, \
           next_player, \
           run_leg, \
           can_put_desert

   from ._reports import \
           report, \
           generate_players_info, \
           generate_board_info, \
           generate_leg_betting_info, \
           generate_game_result_info, \
           generate_game_state_info, \
           generate_all_game_info, \
           generate_personal_info, \
           get_space

   from ._stages import \
           game_scoring_round, \
           determine_game_result, \
           declare_winning_camel

   from ._communicate import \
           set_game_id, \
           set_io_instance, \
           emit_info, \
           send_action_info, \
           update_players_info, \
           update_personal_info, \
           update_leg_betting_info, \
           update_board_info, \
           update_all_game_info, \
           send_game_result


if __name__ == "__main__":
   g = Game(5)
   g.start()
