class Space:
    def __init__(self, space_id):
        self.id = space_id
        self.camels = []
        self.desert_player = None
        self.desert_state = 0

    def get_top_camel(self):
        # The camels appears later on the list stack on top of the former.
        if len(self.camels) <= 0:
            return None
        return self.camels[-1]

    def remove_camel(self, camel):
        if camel in self.camels:
            camel_idx = self.camels.index(camel)
            self.camels = self.camels[:camel_idx]

    def get_stacks(self, camel):
        if camel not in self.camels:
            return []
        return self.camels[self.camels.index(camel):]

    def append_camel(self, camel):
        if not camel in self.camels:
            self.camels.append(camel)

    def print_camels(self):
        return " ".join(self.camels)

    def set_desert(self, player, state):
        self.desert_player = player
        self.desert_state = state

    def remove_desert(self):
        self.desert_player = None
        self.desert_state = 0

    def reset(self):
        self.camels = []
        self.desert_player = None
        self.desert_state = 0


class Camel:
    def __init__(self, name):
        self.position_id = 0
        self.name = name

    def pos_id(self):
        return self.position_id

    def set_position(self, space_id):
        self.position_id = space_id

    def reset(self):
        self.position_id = 0
