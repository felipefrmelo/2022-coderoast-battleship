from before import ASK_FOR_NUMBERS_OF_PLAYERS, EMPTY_AMOUNT, EMPTY_SPACE, NOT_EVEN_IN_THE_OCEAN, YOU_DID_NOT_TYPE, battleship_run, Game
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


@pytest.fixture
def game():
    return Game(2)


def test_game_init_ships():
    game = Game(2)
    assert game.current_player == 1
    assert game.player_list == [5, 5]
    assert game.guess_col == 0
    assert game.guess_row == 0


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


def test_game_create_table(game: Game):
    assert game.create_matrix(2, 2) == [[EMPTY_SPACE, EMPTY_SPACE],
                                        [EMPTY_SPACE, EMPTY_SPACE]]

    assert game.create_matrix(1, 2) == [[EMPTY_SPACE, EMPTY_SPACE]]

    assert game.create_matrix(2, 1) == [[EMPTY_SPACE],
                                        [EMPTY_SPACE]]

    assert game.create_matrix(3, 3) == [[EMPTY_SPACE] * 3] * 3

    assert game.create_matrix(5, 5) == [[EMPTY_SPACE] * 5] * 5


def test_game_user_input(mock_input, assert_print_output, game: Game):

    inputs = ['1', '6', '1', '', '1', '-1', '1']
    mock_input(inputs)

    user_input = game.user_input()
    assert user_input == 1

    user_input = game.user_input()

    assert_print_output(NOT_EVEN_IN_THE_OCEAN)

    game.user_input()

    assert_print_output(YOU_DID_NOT_TYPE)

    game.user_input()
    assert_print_output(NOT_EVEN_IN_THE_OCEAN)
