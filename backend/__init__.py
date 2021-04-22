from flask import Flask
from flask_socketio import SocketIO, emit
import time

try:
    from .game_logic import game
    import utils
except (ImportError, ValueError):
    from game_logic import game
    from . import utils


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
        utils.emit_info(io, "registration-result",
                        {"registered": str(success),
                         "id": new_id,
                         "name": name})

    @io.on('start', namespace='/message')
    def start_game(_param):
        utils.emit_info(io, "game-start", {})
        g.game_state = "play"
        utils.update_all_game_info(io, g)
        time.sleep(20)
        g.start_game()
        utils.bot_running(io, g)
        g.game_state = "result"
        utils.send_game_result(io, g)

    @io.on('reset', namespace='/message')
    def reset_game():
        del g

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
        utils.update_all_game_info(io, g)

    @io.on('disconnect', namespace='/message')
    def message_disconnect():
        print("[Frontend] Disconnected with Websocket")

    return app
