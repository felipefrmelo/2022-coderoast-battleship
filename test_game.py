from before import ASK_FOR_NUMBERS_OF_PLAYERS, EMPTY_AMOUNT, EMPTY_SPACE, battleship_run, Game
import pytest


@pytest.fixture
def mock_input(monkeypatch):
    return lambda inputs: monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))


@pytest.fixture
def assert_print_output(capsys):
    def print_output(output):
        captured = capsys.readouterr().out
        assert captured == output
    return print_output


def test_battleship_run(mock_input, assert_print_output):

    inputs = ['1', '2', '', '2']
    mock_input(inputs)
    players = battleship_run()
    assert_print_output(ASK_FOR_NUMBERS_OF_PLAYERS)
    assert players == 1

    players = battleship_run()

    assert_print_output(ASK_FOR_NUMBERS_OF_PLAYERS)
    assert players == 2

    players = battleship_run()

    assert_print_output(ASK_FOR_NUMBERS_OF_PLAYERS +
                        EMPTY_AMOUNT + ASK_FOR_NUMBERS_OF_PLAYERS)
    assert players == 2


def test_game_create_table():
    game = Game(2)
    assert game.create_matrix(2, 2) == [[EMPTY_SPACE, EMPTY_SPACE],
                                        [EMPTY_SPACE, EMPTY_SPACE]]

    assert game.create_matrix(1, 2) == [[EMPTY_SPACE, EMPTY_SPACE]]

    assert game.create_matrix(2, 1) == [[EMPTY_SPACE],
                                        [EMPTY_SPACE]]

    assert game.create_matrix(3, 3) == [[EMPTY_SPACE] * 3] * 3

    assert game.create_matrix(5, 5) == [[EMPTY_SPACE] * 5] * 5
