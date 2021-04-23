from flask import Flask
from flask_socketio import SocketIO, emit, join_room, leave_room
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
        name = data["name"]
        n_players = data["nP"]
        g.initialize_players(int(n_players))
        print("Received name: " + name)
        if name != "":
            success, new_id = g.register(name)
        else:
            success, new_id = True, -100
        join_room(new_id)
        utils.emit_info(io, "registration-result",
                        {"registered": str(success),
                         "id": new_id,
                         "name": name}, room=new_id)

    @io.on('start', namespace='/message')
    def start_game(_param):
        utils.emit_info(io, "game-start", {})
        g.game_state = "play"
        utils.update_all_game_info(io, g)
        time.sleep(5)
        g.start_game()
        g.init_leg()
        utils.run_a_game(io, g)

    @io.on('reset', namespace='/message')
    def reset_game(param):
        print(param)
        g.reset()
        g.game_state = "replay"
        utils.update_all_game_info(io, g)

    @io.on('new_game', namespace='/message')
    def new_game(param):
        g.reset()
        g.players = []
        utils.update_all_game_info(io, g)


    @io.on('next_player', namespace='/message')
    def next_player():
        g.next_player()
        current_player = g.current_player().name
        print(current_player)
        io.emit('info', {'type': 'current_player',
                         'info': current_player}, namespace='/message')

    @io.on('action_choice', namespace='/message')
    def execute_action(package):
        _, actions = g.current_player().take_turn(g, package["actions"])
        utils.handle_actions(io, g, actions)
        utils.run_a_game(io, g)


    @io.on('reConnect', namespace='/message')
    def reconnect_player(connect_player):
        print(connect_player)
        player = g.find_player_with_id(connect_player['id'])
        room = connect_player['id']
        join_room(room)
        if player is None:
            return utils.update_all_game_info(io, g)
        utils.emit_info(io, "registration-result",
                        {"registered": True,
                         "id": player.id,
                         "name": player.p_name}, room=room)
        utils.update_all_game_info(io, g, room)


    @io.on('connect', namespace='/message')
    def message_connect():
        print("[Frontend] Connected with Websocket")

    @io.on('disconnect', namespace='/message')
    def message_disconnect():
        print("[Frontend] Disconnected with Websocket")

    return app
