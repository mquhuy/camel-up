import time

def handle_actions(game, actions):
    game.send_action_info(actions, game.current_player)
    game.update_all_game_info()
    time.sleep(2)
    game.next_player()
    game.update_players_info()
    game.report()

def run_a_game(game):
    while not game.check_end_leg():
        if game.current_player.is_human:
            return
        turn_success = False
        while not turn_success:
            turn_success, actions = game.current_player.take_turn(game)
        handle_actions(game, actions)
    game.leg_scoring_round()
    game.update_all_game_info()
    if game.winning_camel is None:
        game.init_leg()
        return run_a_game(game)
    game.losing_camel = game.orders[-1]
    game.game_scoring_round()
    game.determine_game_result()
    game.game_state = "result"
    game.update_all_game_info()
    game.send_game_result()
