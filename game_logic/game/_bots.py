def run_leg(self):
    """
    Run a complete leg (with bots only)
    """
    self.init_leg()
    while not self.check_end_leg():
        self.next_player()
        while True:
            if self.current_player.take_turn(self):
                break
        print("-------")
    self.leg_scoring_round()
    self.report()

def start(self):
    """
    Run a complete game with bots
    """
    self.start_game()
    self.init_playing_order()
    while self.winning_camel is None:
        self.run_leg()
        self.report()
        print("------------------- End leg ---------------------")
    self.game_stage = "result"
    self.losing_camel = self.orders[-1]
    self.game_scoring_round()
    self.determine_game_result()

