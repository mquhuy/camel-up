from ..config import FINAL_BET_WINNER_PRIZES

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

    final_rewarding(self.final_winning_deck, "winning")
    final_rewarding(self.final_losing_deck, "losing")

def determine_game_result(self):
    self.scores = {player.name: player.points for player in self.players.values()}
    orders = sorted(self.scores, key=self.scores.get, reverse=True)
    self.winning_player = orders[0]
    self.final_scores = {player: self.scores[player] for player in orders}

def declare_winning_camel(self):
    self.winning_camel = self.final_space.get_top_camel()
    self.determine_game_result()
