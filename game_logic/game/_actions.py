import random

def roll_pyramid_dice(self):
    camel_index = random.randrange(len(self.pyramid_dices))
    camel_name = self.pyramid_dices.pop(camel_index)
    steps = random.randrange(3) + 1
    print("*** Roll dice: {} with step {}".format(camel_name, steps))
    self.roll_results.append({"die": camel_name, "number": steps})
    self.move(camel_name, steps)
    return camel_name, steps

def start_game(self):
    self.next_stage()
    init_locs = self.roll_init_dice()
    print("Initialized camel's starting position:")
    camel_names = list(init_locs.keys())
    random.shuffle(camel_names)
    for camel_name in camel_names:
        self.move(camel_name, init_locs[camel_name])

def move(self, camel_name, steps):
    new_pos = self.camels[camel_name].position_id + steps
    # Apply desert effect only if the space exists on the board
    if new_pos <= len(self.spaces) and self.spaces[new_pos].desert_state != 0:
        self.spaces[new_pos].desert_player.earn_points(1, "owning the desert")
        new_pos += self.spaces[new_pos].desert_state
    # Determine winning condition after desert effects
    if new_pos >= len(self.spaces):
        self.move_camel_to_space(camel_name, 17)
        self.declare_winning_camel()
        return
    self.report()
    self.move_camel_to_space(camel_name, new_pos)
    self.report()

def move_camel_to_space(self, camel_name, space_id):
    old_pos = self.camels[camel_name].position_id
    if old_pos == 0:
        stacks = [camel_name]
    else:
        stacks = self.spaces[old_pos].get_stacks(camel_name)
        self.spaces[old_pos].remove_camel(camel_name)
    space = self.get_space(space_id)
    for name in stacks:
        space.append_camel(name)
        self.camels[name].set_position(space_id)

def next_player(self):
    current_player_name = self.playing_queue.pop(0)
    self.playing_queue.append(current_player_name)
    self.current_player = self.players[current_player_name]

def run_leg(self):
    self.init_leg()
    while not self.check_end_leg():
        self.next_player()
        while True:
            if self.current_player.take_turn(self):
                break
        print("-------")
    self.leg_scoring_round()
    self.report()

def can_put_desert(self, player, space_id):
    """
    Determine if a player can put a desert
    """
    if player is None:
        return False
    space = self.spaces[space_id]
    if space.id <= 1:
        return False
    if space.desert_player is not None:
        return False
    if (self.spaces[space.id - 1].desert_player not in [None, player]):
        return False
    if (space.id < 16 and self.spaces[space.id + 1].desert_player not in [None, player]):
        return False
    if (len(space.camels) > 0):
        return False
    return True

