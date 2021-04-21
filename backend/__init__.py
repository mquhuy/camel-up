from flask import Flask
from flask_socketio import SocketIO, emit
import time

try:
    from .game_logic import game
except (ImportError, ValueError):
    from game_logic import game


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
    )

    io = SocketIO(app, path='/backend/socket.io')
    g = game.Game()


    @io.on('register', namespace='/message')
    def register_player(data):
        print(data)
        name = data["name"]
        n_players = data["nP"]
        print(n_players)
        g.initialize_players(int(n_players))
        print("Received name: " + name)
        if name != "":
            success, new_id = g.register(name)
        else:
            success, new_id = True, 100
        io.emit('info', {"type": "registration_result",
                         "registered": str(success),
                         "player_id": new_id,
                         "player_name": name}, namespace='/message')

    def update_players_info():
        print("Sending update player info")
        io.emit('info', {"type": "players",
            "Players": [{'id': p.p_id, 'name': p.name,
                        'points': p.points,
                        'current': (p.p_id == g.current_player().p_id)}
                        for p in g.players],
                         "currentP": g.current_player().p_id,
                         }, namespace='/message')

    def update_board_info():
        print("Sending update player info")
        io.emit('info', {"type": "board",
                         "spaces": {s.id+1: {'id': s.id+1,
                                             'camels': [c.name for c in s.camels],
                                             'desert': s.desert_state,
                                             'desertP': s.desert_player.name
                                                        if s.desert_player
                                                        is not None else None}
                                    for s in g.spaces},
                        }, namespace='/message')

    def send_game_result():
        io.emit('info', {'type': 'result',
                         'winning_camel': g.winning_camel.name,
                         'winning_player': g.winning_player}, namespace='/message')

    def send_action_info(actions, player):
        actions.update({"type": "action", "player": player.name})
        io.emit('info', actions, namespace='/message')

    @io.on('start', namespace='/message')
    def start_game(_param):
        g.start_game()
        update_players_info()
        bot_running()
        io.emit('info', {'type': 'game_end'})

    @io.on('reset', namespace='/message')
    def reset_game():
        del g

    def bot_running():
        while not g.current_player().is_human and g.winning_camel is None:
            g.init_leg()
            while not g.check_end_leg():
                turn_success = False
                while not turn_success:
                    turn_success, actions = g.current_player().take_turn(g)
                send_action_info(actions, g.current_player())
                update_players_info()
                time.sleep(5)
                update_board_info()
                time.sleep(5)
                g.next_player()
            g.leg_scoring_round()
            update_players_info()
            update_board_info()
        g.losing_camel = g.orders[-1]
        g.game_scoring_round()
        g.determine_game_result()
        update_players_info()
        update_board_info()
        send_game_result()
        g.game_on = False

    @io.on('next_player', namespace='/message')
    def next_player():
        g.next_player()
        current_player = g.current_player().name
        print(current_player)
        io.emit('info', {'type': 'current_player',
                         'info': current_player}, namespace='/message')

    @io.on('connect', namespace='/message')
    def message_connect():
        print("[Frontend] Connected with Websocket")
        update_players_info()
        update_board_info()

    @io.on('disconnect', namespace='/message')
    def message_disconnect():
        print("[Frontend] Disconnected with Websocket")

    return app
