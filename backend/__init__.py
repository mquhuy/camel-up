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
    g.set_game_id()
    g.set_io_instance(io)

    @io.on('register', namespace='/message')
    def register_player(data):
        name = data["name"]
        n_bots = data["nBots"]
        n_players = data["nPlayers"]
        if g.game_state == "registration":
            g.init_bots(int(n_bots))
            g.set_expected_n_players(n_players)
        print("Received name: " + name)
        if name != "":
            success, new_id = g.register(name)
        else:
            success, new_id = True, "-100"
        join_room(new_id)
        g.game_state = "initialization"
        g.emit_info("registration-result",
                    {"registered": str(success),
                     "game_state": g.game_state,
                     "id": new_id,
                     "name": name}, room=new_id)
        g.update_all_game_info()

    @io.on('start', namespace='/message')
    def check_ready(param):
        g.players[param["id"]].mark_ready()
        if g.check_enough_players():
            start_game()

    def start_game():
        g.emit_info("game-start", {})
        g.init_playing_order()
        g.start_game()
        g.update_all_game_info()
        for player in g.players.values():
            if player.is_human:
                g.update_personal_info(player=player)
        time.sleep(5)
        g.init_leg()
        utils.run_a_game(g)

    @io.on('reset', namespace='/message')
    def reset_game(param):
        print(param)
        g.reset()
        g.update_all_game_info()

    @io.on('new_game', namespace='/message')
    def new_game(param):
        g.reset(False)
        g.update_all_game_info()


    @io.on('next_player', namespace='/message')
    def next_player():
        g.next_player()
        current_player = g.current_player.name
        print(current_player)
        g.io.emit('info', {'type': 'current_player',
                           'info': current_player}, namespace='/message')

    @io.on('action_choice', namespace='/message')
    def execute_action(package):
        turn_success, actions = g.current_player.take_turn(g, package["actions"])
        if not turn_success:
            g.emit_info("action-error", {"error": actions["log"]})
            return
        utils.handle_actions(g, actions)
        g.update_personal_info(player=g.players[package["id"]])
        g.emit_info("action-success", {})
        utils.run_a_game(g)


    @io.on('reConnect', namespace='/message')
    def reconnect_player(connect_player):
        player = g.players.get(connect_player["id"], None)
        if player is None:
            room = "tmp"
            join_room(room)
            g.emit_info("registration-result",
                        {"registered": False,
                         "id": "",
                         "name": ""}, room=room)
            leave_room(room)
            return g.update_all_game_info()
        room = player.p_id
        join_room(room)
        g.emit_info("registration-result",
                    {"registered": True,
                     "id": player.p_id,
                     "name": player.name}, room=room)
        g.update_all_game_info(room)
        g.update_personal_info(player=player)


    @io.on('connect', namespace='/message')
    def message_connect():
        print("[Frontend] Connected with Websocket")

    @io.on('disconnect', namespace='/message')
    def message_disconnect():
        print("[Frontend] Disconnected with Websocket")

    return app
