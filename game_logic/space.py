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
            self.camels.remove(camel)

    def get_stacks(self, camel):
        if camel not in self.camels:
            return []
        return self.camels[self.camels.index(camel):]

    def add_camels(self, camel):
        if camel.position is None:
            stacks = [camel]
        else:
            stacks = camel.position.get_stacks(camel)
        for camel in stacks:
            camel.set_position(self)

    def print_camels(self):
        return_str = ""
        for camel in self.camels:
            return_str += camel.name + " "
        return return_str

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
        self.position = None
        self.name = name

    def pos_id(self):
        if self.position is None:
            return -1
        return self.position.id

    def set_position(self, space):
        if self.position is not None:
            self.position.remove_camel(self)
        self.position = space
        if not self in space.camels:
            space.camels.append(self)

    def reset(self):
        self.position = None
