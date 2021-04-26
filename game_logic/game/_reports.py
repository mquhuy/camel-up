def report(self):
    print("Current Positions:")
    for camel in self.camels.values():
        print("Camel {} is at pos {}".format(camel.name, camel.pos_id()))

    print("Stacking situation:")
    for space in self.spaces.values():
        print("Space id {}, camels {}".format(space.id, space.print_camels()))
    if self.winning_camel is not None:
        print("The winning camel is {}".format(self.winning_camel))
        self.determine_game_result()
        print("Scoring table:")
        print(self.final_scores)

def generate_players_info(self):
    if self.players == {} or self.playing_order is None:
        return {}
    return {"Players": [self.generate_personal_info(self.players[p])
                        for p in self.playing_order]}

def generate_board_info(self):
    return {
        "spaces": {s_id: {'id': s_id,
                          'camels': s.camels,
                          'desert': s.desert_state,
                          'desertP': s.desert_player.name
                                     if s.desert_player
                                     is not None else None,
                          'desertable': self.can_put_desert(self.current_player, s_id)}
                   for s_id, s in self.spaces.items()},
        }

def generate_leg_betting_info(self):
    return {
      "leg_betting_tiles": [{'camel': camel, 'bet': bet[0] if bet else 0}
                              for camel, bet in self.betting_tiles.items()]
    }

def generate_game_result_info(self):
    if self.winning_camel is None:
        return {}
    info = {
        'winning_camel': self.winning_camel,
        'game_state': self.game_state,
        'scoring': [{"name": name, "points": points}
                    for name, points in self.final_scores.items()]}
    return info

def generate_game_state_info(self):
    return {"game_state": self.game_state}

def generate_personal_info(self, player):
    return {'id': player.p_id, 'name': player.name,
            'points': player.points,
            'current': (player == self.current_player),
            'leg_bets': [{"camel": camel, "bet": bet}
                          for camel, bet in player.leg_bets.items()]}

def generate_all_game_info(self):
    info = self.generate_board_info()
    info.update(self.generate_leg_betting_info())
    info.update(self.generate_players_info())
    info.update(self.generate_game_state_info())
    info.update(self.generate_game_result_info())
    return info
