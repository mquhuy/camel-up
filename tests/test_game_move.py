import pytest
from game_logic.game import Game
from game_logic.player import Player


def test_move_to_space_16_not_end_game():
    game = Game()
    game.players['p1'] = Player('P1', 'p1')
    game.move('white', 16)
    assert game.winning_camel is None
    assert game.camels['white'].position_id == 16


def test_move_past_space_16_ends_game():
    game = Game()
    game.players['p1'] = Player('P1', 'p1')
    game.move('white', 17)
    assert game.winning_camel == 'white'
    assert game.final_space.get_top_camel() == 'white'
