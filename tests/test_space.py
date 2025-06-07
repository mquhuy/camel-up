from game_logic.space import Space


def test_get_top_camel_empty():
    space = Space(1)
    assert space.get_top_camel() is None


def test_get_top_camel_stack():
    space = Space(1)
    space.append_camel('white')
    space.append_camel('blue')
    assert space.get_top_camel() == 'blue'
