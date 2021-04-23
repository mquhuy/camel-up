import time

def generate_players_info(game):
    return {"Players": [{'id': p.p_id, 'name': p.name,
                         'points': p.points,
                         'current': (p.p_id == game.current_player().p_id),
                         'leg_bets': [{"camel": camel, "bet": bet}
                                      for camel, bet in p.leg_bets.items()]}
                        for p in game.players]}


def generate_board_info(game):
    return {
        "spaces": {s.id+1: {'id': s.id+1,
                            'camels': [c.name for c in s.camels],
                            'desert': s.desert_state,
                            'desertP': s.desert_player.name
                                       if s.desert_player
                                       is not None else None}
                   for s in game.spaces},
        }


def generate_leg_betting_info(game):
    return {
        "leg_betting_tiles": [{'camel': camel, 'bet': bet[0] if bet else 0}
                              for camel, bet in game.betting_tiles.items()]
    }


def generate_game_result_info(game):
    info = {
        'winning_camel': game.winning_camel.name,
        'game_state': 'result',
        'scoring': [{"name": name, "points": points}
                    for name, points in game.final_scores.items()]}
    info.update(generate_game_state_info(game))
    return info


def generate_game_state_info(game):
    return {"game_state": game.game_state}


def generate_all_game_info(game):
    info = generate_board_info(game)
    info.update(generate_leg_betting_info(game))
    info.update(generate_players_info(game))
    info.update(generate_game_state_info(game))
    return info


def emit_info(io_instance, info_type, info, room=None):
    info.update({"type": info_type})
    if room is not None:
        io_instance.emit("info", info, to=room)
    else:
        io_instance.emit("info", info, namespace="/message")


def send_action_info(io_instance, actions, player, room=None):
    actions.update({"player": player.name})
    emit_info(io_instance, "action", {"action": actions}, room)


def update_players_info(io_instance, game, room=None):
    print("Sending update player info")
    info = generate_players_info(game)
    info.update(generate_leg_betting_info(game))
    emit_info(io_instance, "players", info, room)


def update_leg_betting_info(io_instance, game, room=None):
    info = generate_leg_betting_info(game)
    print("Sending update leg betting info")
    emit_info(io_instance, "betting-tiles", info, room)


def update_board_info(io_instance, game, room=None):
    print("Sending update player info")
    info = generate_board_info(game)
    info.update(generate_leg_betting_info(game))
    emit_info(io_instance, "board", info, room)


def update_all_game_info(io_instance, game, room=None):
    info = generate_all_game_info(game)
    emit_info(io_instance, "all", info, room)


def send_game_result(io_instance, game, room=None):
    info = generate_game_result_info(game)
    emit_info(io_instance, "game-end-result", info, room)


def handle_actions(io_instance, game, actions):
    send_action_info(io_instance, actions, game.current_player())
    update_all_game_info(io_instance, game)
    time.sleep(2)
    game.next_player()
    update_players_info(io_instance, game)


def run_a_game(io_instance, game):
    while not game.check_end_leg():
        if game.current_player().is_human:
            return
        turn_success = False
        while not turn_success:
            turn_success, actions = game.current_player().take_turn(game)
        handle_actions(io_instance, game, actions)
    game.leg_scoring_round()
    update_all_game_info(io_instance, game)
    if game.winning_camel is None:
        game.init_leg()
        return run_a_game(io_instance, game)
    game.losing_camel = game.orders[-1]
    game.game_scoring_round()
    game.determine_game_result()
    game.game_state = "result"
    update_all_game_info(io_instance, game)
    send_game_result(io_instance, game)
