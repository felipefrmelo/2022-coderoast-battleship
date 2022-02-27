# Battleship Attempt 2

# Imports
import copy as c
import os
import random as rand

"""
Defining the Game class to make it easier to 
understand the code further in the project
"""


EMPTY_SPACE = 'O'


NOT_EVEN_IN_THE_OCEAN = "That's not even in the ocean! Try again."

YOU_DID_NOT_TYPE = "You didn't type anything! Try again"


class Game(object):
    def __init__(self, players, ship_row=rand.randint(0, 4), ship_col=rand.randint(0, 4)):
        self.guesses = 5
        self.player_list = []
        for player in range(players):
            self.player_list.append(self.guesses)
        self.current_player = 1
        self.board = self.create_matrix(5, 5)
        self.ship_row = ship_row
        self.ship_col = ship_col
        self.guess_row = 0
        self.guess_col = 0

    """
    Defining the many methods that makes the game work,
    starting with the create_matrix where we take in the 
    boards max x and max y to define its size.
    """

    def create_matrix(self, max_x, max_y):
        return [[EMPTY_SPACE for _ in range(max_y)] for _ in range(max_x)]

    """
    Defining the print_board function, here I respresent
    x as rows
    y as colums
    """

    def init(self):
        return self.makeState()

    def makeState(self, winner=None):
        return {
            "board": self.board,
            'current_player': {
                'name': self.current_player,
                'guesses_left': self.player_list[self.current_player - 1]
            },
            'winner': winner,
            'draw': sum(self.player_list) == 0
        }

    def print_board(self, board_in):
        x = 0
        y = 0
        for column in board_in:
            y = 0
            for row in column:
                if y == 0:
                    print(" ", row, end=" ")
                elif y == len(board_in[x]):
                    print("", row, end="")
                else:
                    print(row, end=" ")
                y += 1
            print()
            x += 1
        return None

    def board_to_str(self, board_in) -> str:
        b_str = ""
        for row in self.board:
            b_str += " ".join(row)
            b_str += "\n"
        return b_str

    """
    To avoid repeating the same code twice, I made the user_input method more generalized
    and made a seperate method to take care of if its row or column thats being inputed.
    That way I can make a robust input check without having to repeat code.
    I also use recursive methods here to avoid using while loops.
    """

    def user_input(self):
        line = input("")
        if len(line) == 0:
            print(YOU_DID_NOT_TYPE, end="")
            return self.user_input()

        is_in_the_ocean = 0 < int(line) <= len(self.board)
        if not is_in_the_ocean:
            print(NOT_EVEN_IN_THE_OCEAN, end="")
            return self.user_input()

        return int(line)

    """
    I wanted to avoid retyping code as much as possible
    so I did the above function and then created player_guesses
    to take user input and sort it into guesses for row and column
    As of writing this comment I'm avoiding writing any game logic in the function.
    """

    def player_guesses(self):
        if self.player_list[self.current_player - 1] == 0:
            return False
        else:
            print(
                "Player {} has {} guesses left.".format(
                    self.current_player, self.player_list[self.current_player - 1])
            )

            print("Player {}: Guess row: ".format(self.current_player), end="")
            self.guess_row = self.user_input() - 1

            print("Player {}: Guess column: ".format(
                self.current_player), end="")
            self.guess_col = self.user_input() - 1

            if self.board[self.guess_row][self.guess_col] == "X":
                print("You've already guessed on that row! Try again.")
                return self.player_guesses()
            else:
                return None

    """
    Seperating out the game_logic to try to make the main function as readable as possible.
    This is also an exercise to practice writing recursive code instead of using while loops.
    """

    @property
    def isWinner(self):
        return self.guess_row == self.ship_row and self.guess_col == self.ship_col

    def game_logic(self):
        self.player_guesses()

        # I first did -1 here and spread out in the code. Very bad and confusing.

        if (self.isWinner):
            self.board[self.guess_row][self.guess_col] = "S"
            return self.makeState(winner=self.current_player)

        print("Sorry, you missed!")
        self.board[self.guess_row][self.guess_col] = "X"
        self.player_list[self.current_player - 1] -= 1

        if len(self.player_list) > 1:
            self.current_player += 1
        if self.current_player > len(self.player_list):
            self.current_player = 1

        return self.makeState()

    """
    Keeping the main function simple and easy to read by handling game logic
    above and using return to see the condition of the game.
    """

    def main(self):

        state = self.init()
        self.print_board(state['board'])
        while True:

            state = self.game_logic()

            self.print_board(state['board'])
            if state['draw']:
                print("It's a draw!")
                break
            elif state['winner']:
                print("Player {} wins!".format(state['winner']))
                break
            else:
                continue


"""
Defining the run function here to easier handle player input.
Doing it this way avoids using confusing while loops entirely.
"""


ASK_FOR_NUMBERS_OF_PLAYERS = "Please enter how many players are going to play: "


CAN_NOT_NEGATIVE_VALUE = "You can't have a negative amount of players. Try again.\n\n"


EMPTY_AMOUNT = "You didn't type any player amount! Try again.\n\n"


def battleship_run():
    print(ASK_FOR_NUMBERS_OF_PLAYERS, end="")
    players = input("")
    if len(players) > 0:
        if int(players) < 0:
            print(CAN_NOT_NEGATIVE_VALUE, end="")
            return battleship_run()
        else:
            return int(players)
    else:
        print(EMPTY_AMOUNT, end="")
        return battleship_run()


"""
Here is all that is left outside of functions and the game class. 
Pretty easy to read if you ask me.
"""

if __name__ == "__main__":
    os.system("clear")
    battleship = Game(battleship_run())
    battleship.main()
