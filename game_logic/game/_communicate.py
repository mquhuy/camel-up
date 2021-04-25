# This file includes function related to communication between game logic and the front end

import time

def set_game_id(self, game_id=None):
    if game_id is None:
        game_id = time.time()
    self.id = game_id
    self.room = game_id

def set_io_instance(self, io_instance):
    self.io = io_instance

def emit_info(self, info_type, info, room=None):
    info.update({"type": info_type})
    if room is not None:
        self.io.emit("info", info, to=room, namespace="/message")
    else:
        self.io.emit("info", info, namespace="/message")

def send_action_info(self, actions, player, room=None):
    actions.update({"player": player.name})
    self.emit_info("action", {"action": actions}, room)

def update_players_info(self, room=None):
    print("Sending update player info")
    info = self.generate_players_info()
    info.update(self.generate_leg_betting_info())
    self.emit_info("players", info, room)

def update_personal_info(self, player=None, player_info=None):
    if player is not None:
        player_info = self.generate_personal_info(player)
    self.emit_info("personal", player_info, room=player_info["id"])

def update_leg_betting_info(self, room=None):
    info = self.generate_leg_betting_info()
    print("Sending update leg betting info")
    self.emit_info("betting-tiles", info, room)

def update_board_info(self, room=None):
    print("Sending update player info")
    info = self.generate_board_info()
    info.update(self.generate_leg_betting_info())
    self.emit_info("board", info, room)

def update_all_game_info(self, room=None):
    info = self.generate_all_game_info()
    self.emit_info("all", info, room)

def send_game_result(self, room=None):
    info = self.generate_game_result_info()
    self.emit_info("game-end-result", info, room)

