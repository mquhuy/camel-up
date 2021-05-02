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
            CORS_HEADER = "Content-Type"
    )
    io = SocketIO(app, path='/backend/socket.io', cors_allowed_origins='*')
    games = {}

    @io.on('register', namespace='/message')
    def register_player(data):
        g = game.Game(io_instance=io)
        g.set_game_id()
        n_bots = data["nBots"]
        n_players = data["nPlayers"]
        g.init_bots(int(n_bots))
        g.set_expected_n_players(n_players)
        name = data["name"]
        _, new_id = g.register(name)
        g.next_stage()
        join_room(new_id)
        join_room(g.id)
        g.send_registered_success(new_id)
        g.update_all_game_info()
        games[str(g.id)] = g

    @io.on('start', namespace='/message')
    def check_ready(param):
        g = games[str(param["game_id"])]
        if g.expected_n_players == 0:
            return start_game(g)
        player = g.players[param["id"]]
        player.mark_ready()
        g.update_personal_info(player=player)
        if g.check_enough_players():
            start_game(g)

    def start_game(g):
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
        g = games.get(str(param["game_id"]), None)
        g.reset()
        for p in g.players.values():
            g.update_personal_info(player=p)
        g.update_all_game_info()

    @io.on('end_game', namespace='/message')
    def end_game(param):
        game_id = str(param["game_id"])
        player_id = param["id"]
        g = games.get(game_id, None)
        if g is not None:
            g.send_destruct_command(player_id)
            del g
            del games[game_id]

    @io.on('next_player', namespace='/message')
    def next_player(data):
        g = games.get(str(data["game_id"]), None)
        g.next_player()
        current_player = g.current_player.name
        g.io.emit('info', {'type': 'current_player',
                           'info': current_player}, namespace='/message')

    @io.on('action_choice', namespace='/message')
    def execute_action(package):
        g = games.get(str(package["game_id"]), None)
        turn_success, actions = g.current_player.take_turn(g, package["actions"])
        if not turn_success:
            g.emit_info("action-error", {"error": actions["log"]}, room=package["id"])
            return
        utils.handle_actions(g, actions)
        g.update_personal_info(player=g.players[package["id"]])
        g.update_all_game_info()
        g.emit_info("action-success", {})
        utils.run_a_game(g)

    @io.on('join', namespace="/message")
    def join_game(data):
        g = games[str(data["game_id"])]
        if g is not None:
            player = g.players.get(data["id"], None)
            if player is not None:
                join_room(player.p_id)
                join_room(g.id)
                g.update_player_info(player=player)
            else:
                success, new_id = g.register(data["name"])
                if not success:
                    room = "tmp"
                    join_room(room)
                    g.emit_info("registration-error", {"error": new_id}, room=room)
                    leave_room(room)
                else:
                    player = g.players[new_id]
                    join_room(player.p_id)
                    join_room(g.id)
                    g.send_registered_success(player.p_id)
                    g.update_personal_info(player=player)
        else:
            room = "tmp"
            join_room(room)
            g.emit_info("registration-error", {"error": "game id not existed"}, room=room)
            leave_room(room)

    @io.on('reConnect', namespace='/message')
    def reconnect_player(connect_player):
        g = games.get(str(connect_player["game_id"]), None)
        if g is None:
            g = game.Game(io_instance=io)
            room = "tmp"
            join_room(room)
            g.emit_info("registration-error",
                        {"registered": False,
                         "id": "",
                         "name": ""}, room=room)
            leave_room(room)
            del g
            return
        player = g.players.get(connect_player["id"], None)
        if player is None:
            room = "tmp"
            join_room(room)
            g.emit_info("registration-error",
                        {"registered": False,
                         "id": "",
                         "name": ""}, room=room)
            leave_room(room)
            return g.update_all_game_info()
        room = player.p_id
        join_room(room)
        g.emit_info("registration-success",
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
