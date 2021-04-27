def init_leg(self):
    self.reset_dices()
    for player in self.players.values():
        player.reset_bets()
    for space in self.spaces.values():
        space.remove_desert()
    for player in self.players.values():
        player.remove_desert()

def check_end_leg(self):
    return (len(self.pyramid_dices) == 0 or self.winning_camel is not None)


def determine_leg_result(self):
    orders = {name: camel.position_id
                     + self.get_space(camel.position_id).camels.index(name)/10
              for name, camel in self.camels.items()}
    self.orders = sorted(orders, key=orders.get, reverse=True)

def leg_scoring_round(self):
    self.determine_leg_result()
    for player in self.players.values():
        player.leg_bet_scoring(self.orders)
    for player in self.rollers:
        player.earn_points(1, "rolling the dice")
