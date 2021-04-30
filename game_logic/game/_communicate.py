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
    info.update(self.generate_basic_info())
    if room is not None:
        self.io.emit("info", info, to=room, namespace="/message")
    elif self.id is not None:
        self.io.emit("info", info, to=self.id, namespace="/message")
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

def update_personal_info(self, player=None, player_id=None):
    if player is None:
        player = self.players.get(player_id, None)
    player_info = self.generate_personal_info(player)
    player_info.update(player.generate_bet_deck())
    self.emit_info("personal", player_info, room=player_info["id"])

def send_registered_success(self, player_id):
    player = self.players.get(player_id, None)
    self.emit_info("registration-success",
                    {"registered": True,
                     "game_stage": self.game_stage,
                     "id": player.p_id,
                     "game_id": self.id,
                     "name": player.name}, room=player.p_id)

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

def send_destruct_command(self):
    self.emit_info("game-deletion", {})

