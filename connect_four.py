import sys, time
import numpy as np
import pygame

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


class ConnectFour:

    def __init__(self, print_every_move=False):
        """Setup a fresh game of connect four"""
        # Game field initialization
        self.game_field = np.zeros((6, 7), dtype=int)

        # Helper dict to keep track of played tokens
        self.offset = {c: 5 for c in range(0, 7)}

        # Symbol mapping
        self.symbols = {1: 'Y', -1: 'R', 0: ' '}

        # Starting player
        self.player = 1

        # Bool to determine if a game was finished
        self.game_finished = False
        self.is_draw = False

        # Bool to determine if every move should be printed
        self.move_print = print_every_move

    def move_allowed(self, column):
        """Checks if a move is allowed

        :param column: Column to put the token
        """
        if column in range(0, 7):
            return self.offset[column] >= 0
        else:
            return False

    def winning_move(self, column):
        """Checks if a move was a winning move

        :param column: Column to put the token
        """
        row = self.offset[column]

        # Setup directions that may contain tokens
        right = True if column < 6 else False
        left = True if column > 0 else False
        up = True if row > 0 else False
        down = True if row < 5 else False

        tokens = {
            'r': 0,
            'l': 0,
            'd': 0,
            'ru': 0,
            'rd': 0,
            'lu': 0,
            'ld': 0
        }
        results = []

        # Check Right
        if right:
            tokens['r'] += self._token_count(row, column+1, horizontal_transit=1)
            results.append(tokens['r'] + 1)

        # Check left
        if left:
            tokens['l'] = self._token_count(row, column-1, horizontal_transit=-1)
            results.append(tokens['l'] + 1)
            results.append(tokens['r'] + tokens['l'] + 1)

        # Check down
        if down:
            tokens['d'] = self._token_count(row+1, column, vertical_transit=1)
            results.append(tokens['d'] + 1)

        # Check Top-Right
        if right and up:
            tokens['ru'] = self._token_count(row-1, column+1, vertical_transit=-1, horizontal_transit=+1)
            results.append(tokens['ru'] + 1)

        # Check Top-Left
        if left and up:
            tokens['lu'] = self._token_count(row-1, column-1, vertical_transit=-1, horizontal_transit=-1)
            results.append(tokens['lu'] + 1)

        # Check Bottom-Right
        if right and down:
            tokens['rd'] = self._token_count(row+1, column+1, vertical_transit=1, horizontal_transit=1)
            results.append(tokens['rd'] + 1)
            results.append(tokens['lu'] + tokens['rd'] + 1)

        # Check Bottom-Left
        if left and down:
            tokens['ld'] = self._token_count(row+1, column-1, vertical_transit=1, horizontal_transit=-1)
            results.append(tokens['ld'] + 1)
            results.append(tokens['ru'] + tokens['ld'] + 1)

        if 4 in results:
            return True
        else:
            return False

    def _token_count(self, row, column, vertical_transit=0, horizontal_transit=0):
        """Helper function that counts tokens.

        :param row: Row to start counting.
        :param column: Column to start counting.
        :param vertical_transit: Transition value for a vertical transition.
        :param horizontal_transit: Transition value for a horizontal transition.

        :returns: An int value of counted tokens (in line)"""
        count = 0
        while True:
            if row in range(0, 6) and column in range(0, 7) and self.game_field[row][column] == self.player:
                count += 1
                column += horizontal_transit
                row += vertical_transit
            else:
                break

        return count

    def make_a_move(self, column):
        """Put a token into a column

        :param column: Column to put the token
        """
        if self.move_allowed(column):
            # Put token
            self.game_field[self.offset[column]][column] = self.player

            self.game_finished = self.winning_move(column)

            if not self.game_finished:
                if self.move_print:
                    print("Player '{}' moved:".format(self.symbols[self.player]))
                    self.print_game_field()

                # Update offset dict
                self.offset[column] += -1

                # Switch player
                self.player *= -1

            # Determines if the game is a draw
            if 0 not in self.game_field:
                self.game_finished = True
                self.is_draw = True

            # Valid move was made
            return True

        else:
            # Move was invalid
            return False

    def random_move(self):
        """Makes a random move."""
        valid_move = False
        while not valid_move:
            valid_move = self.make_a_move(np.random.randint(0, 7))

    def print_game_field(self):
        """Method that prints the game field."""
        cp_field = np.copy(self.game_field).astype(object)
        for n in [-1, 0, 1]:
            cp_field[cp_field == n] = self.symbols[n]
        print(cp_field)

    def reset_game(self):
        """Resets the game state."""
        self.game_field = np.zeros((6, 7), dtype=int)
        self.offset = {c: 5 for c in range(0, 7)}
        self.player = 1
        self.game_finished = False
        self.is_draw = False

    def play_a_game(self, p1='npc', p2='npc', winners_print=True):
        """Two players can play a game.

        :note: The player name 'npc' makes the player to be a computer.

        :param p1: Name for player 1
        :param p2: Name for player 2
        :param winners_print: Bool to determine if winning game_field should be printed.

        :returns: Tuple of (Player who had last turn, bool if game was a draw)
        """

        if self.game_finished:
            self.print_game_field()
            if not self.is_draw:
                print("The game was finished! Player '{}' won.".format(self.symbols[self.player]))
            else:
                print("The game ended a draw!")
            print("You may want to reset the game to play a new one. Use .reset_game() method!")
        else:
            if p1 == p2 == 'npc':
                # A npc game with all random moves
                while not self.game_finished:
                    self.random_move()

                if self.game_finished and winners_print:
                    self.print_game_field()
                    if not self.is_draw:
                        print("Player '{}' won the game!".format(self.symbols[self.player]))
                    else:
                        print("The game ended in a draw.")

            elif p1 == 'npc':
                # A game with P1 as npc
                pass
            elif p2 == 'npc':
                # A game with P2 as npc
                pass
            else:
                # A game with 2 humans
                pass

        return self.player, self.is_draw

    def play_random_tournament(self, laps=1000, modulo=100):
        """Lets two NPC players play a random tournament.

        :param laps: determines how many laps should be played.
        :param modulo: Modulo value for iteravive printing
        """
        wins = {
            1: 0,   # Wins of player 1
            -1: 0,  # Wins of player -1
            0: 0    # Draws
        }

        for l in range(0, laps):
            winner, draw = self.play_a_game(winners_print=False)
            if draw:
                wins[0] += 1
            else:
                wins[winner] += 1
            if not l % modulo:
                print("=== Lap: {} ===\n'{}'\t{}\n'{}'\t{}\nDRAW\t{}".format(l,
                                                                             self.symbols[1],
                                                                             wins[1],
                                                                             self.symbols[-1],
                                                                             wins[-1],
                                                                             wins[0]))
            self.reset_game()

        print("Tournament results in: \n'{}'\t{}\n'{}'\t{}\nDRAW\t{}".format(self.symbols[1],
                                                                             wins[1],
                                                                             self.symbols[-1],
                                                                             wins[-1],
                                                                             wins[0]))

    def start_gui(self):
        """Creates a view of Connect4 using PyGame.
        This function was inspired by the Connect4 for Python tutorial by
        Keith Galli (YouTube)."""
        pygame.init()

        self._draw_board()

        while not self.game_finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            time.sleep(2)

            self.random_move()
            self._draw_board()

    def _draw_board(self):
        """Draws the game board"""
        squaresize = 100
        width = 7 * squaresize
        height = (6 + 1) * squaresize

        size = (width, height)
        radius = int(squaresize / 2 - 5)
        screen = pygame.display.set_mode(size)

        for c in range(7):
            for r in range(6):
                # definition of a ractangle in the GUI
                rectangle = (c * squaresize, r * squaresize + squaresize, squaresize, squaresize)
                circle = (int(c * squaresize + squaresize / 2), int(r * squaresize + squaresize + squaresize / 2))
                pygame.draw.rect(screen, BLUE, rectangle)
                if self.game_field[r][c] == 0:
                    pygame.draw.circle(screen, BLACK, circle, radius)
                elif self.game_field[r][c] == 1:
                    pygame.draw.circle(screen, YELLOW, circle, radius)
                else:
                    pygame.draw.circle(screen, RED, circle, radius)

        pygame.display.update()

if __name__ == '__main__':

    connect_four_game = ConnectFour()
    connect_four_game.start_gui()
