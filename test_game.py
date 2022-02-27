from before import ASK_FOR_NUMBERS_OF_PLAYERS, EMPTY_AMOUNT, EMPTY_SPACE, NOT_EVEN_IN_THE_OCEAN, YOU_DID_NOT_TYPE, battleship_run, Game
import pytest


@pytest.fixture
def mock_input(monkeypatch):
    return lambda inputs: monkeypatch.setattr('builtins.input', lambda _: inputs.pop(0))


@pytest.fixture
def game():
    return Game(2)


def test_game_init_ships():
    game = Game(2)
    assert game.current_player == 1
    assert game.player_list == [5, 5]
    assert game.guess_col == 0
    assert game.guess_row == 0


def test_game_create_table(game: Game):
    assert game.create_matrix(2, 2) == [[EMPTY_SPACE, EMPTY_SPACE],
                                        [EMPTY_SPACE, EMPTY_SPACE]]

    assert game.create_matrix(1, 2) == [[EMPTY_SPACE, EMPTY_SPACE]]

    assert game.create_matrix(2, 1) == [[EMPTY_SPACE],
                                        [EMPTY_SPACE]]

    assert game.create_matrix(3, 3) == [[EMPTY_SPACE] * 3] * 3

    assert game.create_matrix(5, 5) == [[EMPTY_SPACE] * 5] * 5


class TestGameLogic:

    def test_game_init(self, game: Game, mock_input):

        expected = {
            'board': game.create_matrix(5, 5),
            'winner': None,
            'current_player': {
                'name': 1,
                'guesses_left': 5,
            },
            'draw': False,
        }

        result = game.init()

        assert result == expected

    def test_game_logic_player_1_win(self, game: Game, mock_input):
        mock_input(['1', '1'])
        game.ship_col = 0
        game.ship_row = 0

        board = game.create_matrix(5, 5)
        board[0][0] = 'S'

        expected = {
            'board': board,
            'winner': 1,
            'current_player': {
                'name': 1,
                'guesses_left': 5,
            },
            'draw': False,
        }

        result = game.game_logic()

        assert result == expected

    def test_game_logic_player_2_win(self, game: Game, mock_input):
        mock_input(['2', '2', '1', '1'])
        game.ship_col = 0
        game.ship_row = 0

        board = game.create_matrix(5, 5)
        board[1][1] = 'X'

        expected = {
            'board': board,
            'winner': None,
            'current_player': {
                'name': 2,
                'guesses_left': 5,
            },
            'draw': False,
        }

        result = game.game_logic()

        assert result == expected

        board[0][0] = 'S'

        expected = {
            'board': board,
            'winner': 2,
            'current_player': {
                'name': 2,
                'guesses_left': 5,
            },
            'draw': False,
        }

        result = game.game_logic()

        assert result == expected

    def test_game_logic_player_1_win_at_second_play(self, game: Game, mock_input):
        mock_input(['3', '3', '2', '2', '1', '1'])
        game.ship_col = 0
        game.ship_row = 0

        board = game.create_matrix(5, 5)
        board[0][0] = 'S'
        board[1][1] = 'X'
        board[2][2] = 'X'

        expected = {
            'board': board,
            'winner': 1,
            'current_player': {
                'name': 1,
                'guesses_left': 4,
            },
            'draw': False,
        }

        result = game.game_logic()
