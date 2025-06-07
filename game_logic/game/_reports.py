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

def generate_basic_info(self):
    if self.id is None:
        return {}
    return {"game_id": self.id}

def generate_players_info(self):
    if self.players == {} or self.playing_order is None:
        return {}
    return {"Players": [self.generate_personal_info(self.players[p])
                        for p in self.playing_order]}

def generate_board_info(self):
    info = {
        "spaces": {s_id: {'id': s_id,
                          'camels': s.camels,
                          'desert': s.desert_state,
                          'desertP': s.desert_player.name
                                     if s.desert_player
                                     is not None else None,
                          'desertable': self.can_put_desert(self.current_player, s_id)}
                   for s_id, s in self.spaces.items()},
        }
    info["spaces"][1]["camels"] = (
        info["spaces"][1]["camels"] + list(self.final_space.camels)
    )
    info["last_bet_winner"] = self.last_bet_winner
    info["last_bet_loser"] = self.last_bet_loser
    return info

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
        'scoring': [{"name": name, "points": points}
                    for name, points in self.final_scores.items()]}
    info.update(self.generate_game_stage_info())
    return info

def generate_game_stage_info(self):
    return {"game_stage": self.game_stage}

def generate_personal_info(self, player):
    return {'id': player.p_id,
            'name': player.name,
            'points': player.points,
            'current': (player == self.current_player),
            'ready': player.ready,
            'leg_bets': [{"camel": camel, "bet": bet}
                          for camel, bet in player.leg_bets.items()],
            'registered': True}

def generate_all_game_info(self):
    info = self.generate_board_info()
    info.update(self.generate_leg_betting_info())
    info.update(self.generate_players_info())
    info.update(self.generate_game_stage_info())
    info.update(self.generate_game_result_info())
    info["roll_results"] = self.roll_results
    return info

def get_space(self, space_id):
    if space_id <= len(self.spaces):
        return self.spaces[space_id]
    return self.final_space
