import time
import numpy as np
import pygame


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

        # Collect some basic information
        self.stats = {
            'used_columns': {i: 0 for i in range(0, 7)},
            'win_direction': {
                'h': 0,
                'v': 0,
                'd': 0,
                'i': 0
            },
            'winning_player': {
                1: 0,
                -1: 0
            },
            'win_turn_count': [],
            'draw': 0,
            'win_moves': []
        }

        self.player_stats = {
            1: {
                'used_columns': {i: 0 for i in range(0, 7)},
                'turns_played': 0,
                'move_hist': []
            },
            -1: {
                'used_columns': {i: 0 for i in range(0, 7)},
                'turns_played': 0,
                'move_hist': []
            },
        }

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
            i = results.index(4)

            if i in [0, 1, 2]:
                self.stats['win_direction']['h'] += 1

            elif i == 3:
                self.stats['win_direction']['v'] += 1

            elif i in [5, 6, 7]:
                self.stats['win_direction']['d'] += 1

            elif i in [4, 8, 9]:
                self.stats['win_direction']['i'] += 1

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

            self.player_stats[self.player]['used_columns'][column] += 1
            self.player_stats[self.player]['turns_played'] += 1
            self.player_stats[self.player]['move_hist'].append(column)

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
        self.player_stats = {
            1: {
                'used_columns': {i: 0 for i in range(0, 7)},
                'turns_played': 0,
                'move_hist': []
            },
            -1: {
                'used_columns': {i: 0 for i in range(0, 7)},
                'turns_played': 0,
                'move_hist': []
            },
        }

    def play_a_game(self, p1='npc', winners_print=True):
        """Two players can play a game.

        :note: The player name 'npc' makes the player to be a computer.

        :param p1: Name for player 1
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
            if p1 == 'npc':
                # A npc game with all random moves

                while not self.game_finished:
                    self.random_move()

                if self.game_finished:

                    self.stats['winning_player'][self.player] += 1
                    self.stats['win_turn_count'].append(self.player_stats[self.player]['turns_played'])

                    for key, value in self.player_stats[self.player]['used_columns'].items():
                        self.stats['used_columns'][key] += value

                    if self.is_draw:
                        self.stats['draw'] += 1
                    else:
                        self.stats['win_moves'].append(self.player_stats[self.player]['move_hist'])

                    if winners_print:
                        self.print_game_field()
                        if not self.is_draw:
                            print("Player '{}' won the game!".format(self.symbols[self.player]))
                        else:
                            print("The game ended in a draw.")

            else:
                # Human vs. npc
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

    ######################
    # PyGame definitions #
    ######################

    def startgame(self):
        """All initiations for GUI"""

        # Initiate PyGame
        pygame.init()
        pygame.display.set_caption('Connect4')

        # Color definitions for PyGame
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (125, 125, 125)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)

        # PyGame basic screen setup
        self.SQUARESIZE = 100
        self.WIDTH = 7 * self.SQUARESIZE
        self.HEIGHT = (6 + 1) * self.SQUARESIZE
        self.SCREEN = pygame.display.set_mode([self.WIDTH, self.HEIGHT])

        # Additional setups for PyGame
        self.LARGE_TEXT = pygame.font.Font('freesansbold.ttf', 115)
        self.SMALL_TEXT = pygame.font.Font("freesansbold.ttf", 20)
        self.CLOCK = pygame.time.Clock()

        self.start_gui()

    def start_gui_game(self):
        """Creates a view of Connect4 using PyGame."""
        self.reset_game()
        self._draw_board()
        self._play_gui_game()

    def start_gui(self):
        """Realizes the 'main menu' of the game.

        Inspired by PyGame tutorial 10 from Santex (Start Menu)
        """

        intro = True
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quitgame()

            self.SCREEN.fill(self.BLACK)
            TextSurf, TextRect = self._text_objects("Connect4", self.LARGE_TEXT, self.BLUE)
            TextRect.center = ((self.WIDTH/2), (self.HEIGHT/2))
            self.SCREEN.blit(TextSurf, TextRect)

            # Keep track of the mouse
            mouse = pygame.mouse.get_pos()

            # Keep track of mouse action
            click = pygame.mouse.get_pressed()

            # Computer vs. Computer
            self._button((250, 400, 150, 50), self.GRAY, "C. vs. C.", mouse, click, self.start_gui_game)

            # Human vs. Computer
            self._button((250, 475, 150, 50), self.GRAY, "P. vs. C.", mouse, click)

            # About
            self._button((250, 550, 150, 50), self.GRAY, "About", mouse, click)

            # Quit
            self._button((250, 625, 150, 50), self.GRAY, "Quit", mouse, click, self._quitgame)

            pygame.display.update()
            self.CLOCK.tick()

    def _end_screen(self):
        """End screen definition that shows the winner."""

        end_screen = True

        background_colors = {
            'draw': self.WHITE,
            'Y': self.YELLOW,
            'R': self.RED
        }

        if self.is_draw:
            background = background_colors['draw']
            text = "DRAW"
        else:
            background = background_colors[self.symbols[self.player]]
            text = self.symbols[self.player] + " winns!"

        while end_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quitgame()

            TextSurf, TextRect = self._text_objects(text, self.LARGE_TEXT, background)
            TextRect.center = ((self.WIDTH / 2), 55)
            self.SCREEN.blit(TextSurf, TextRect)
            pygame.display.update()

            # Keep track of the mouse
            mouse = pygame.mouse.get_pos()

            # Keep track of mouse action
            click = pygame.mouse.get_pressed()

            self._button((590, 15, 100, 50), self.GRAY, "Back", mouse, click, self.start_gui)

            pygame.display.update()
            self.CLOCK.tick()

    def _play_gui_game(self):
        """Plays a gui game

        This function was inspired by the Connect4 for Python tutorial by
        Keith Galli (YouTube).
        """

        while not self.game_finished:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self._quitgame()

            time.sleep(1)

            self.random_move()
            self._draw_board()

        if self.game_finished:
            # Wait 2 sec. for observer to realize winning :P
            #time.sleep(5)
            print("{} won the game!".format(self.symbols[self.player]))
            self._end_screen()

    def _draw_board(self):
        """Draws the game board

        This function was inspired by the Connect4 for Python tutorial by
        Keith Galli (YouTube).
        """
        radius = int(self.SQUARESIZE / 2 - 5)

        for c in range(7):
            for r in range(6):
                # definition of a ractangle in the GUI
                rectangle = (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE)
                circle = (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2))
                pygame.draw.rect(self.SCREEN, self.BLUE, rectangle)
                if self.game_field[r][c] == 0:
                    pygame.draw.circle(self.SCREEN, self.BLACK, circle, radius)
                elif self.game_field[r][c] == 1:
                    pygame.draw.circle(self.SCREEN, self.YELLOW, circle, radius)
                else:
                    pygame.draw.circle(self.SCREEN, self.RED, circle, radius)

        pygame.display.update()

    def _text_objects(self, text, font, color):
        """Creates a text object for PyGame.

        :param text: The text that should be displayed.
        :param font: PyGame font to use for the text.
        :param color: The color of the text.
        """

        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def _button(self, size, color, text, mouse, click, action=None):
        """Function to add buttons to the PyGame instance.

        :param size: The size of the button (rectangle definition)
        :param color: The color to use for the button.
        :param text: The text to display on the button
        :param mouse: Keep track of mouse position
        :param click: Keep track of mouse action
        :param action: What should be the action to perform on a click.
        """
        # (150,450,100,50)

        if size[0] + size[2] > mouse[0] > size[0] and size[1] + size[3] > mouse[1] > size[1]:
            brighter_color = [code+50 if code+50 < 256 else 255 for code in color]
            pygame.draw.rect(self.SCREEN, brighter_color, size)

            if click[0] == 1 and action is not None:
                action()

        else:
            pygame.draw.rect(self.SCREEN, color, size)

        textSurf, textRect = self._text_objects(text, self.SMALL_TEXT, self.WHITE)
        textRect.center = ((size[0] + (size[2] / 2)), (size[1] + (size[3] / 2)))
        self.SCREEN.blit(textSurf, textRect)

    def _quitgame(self):
        """Helper function for quitting game."""
        pygame.quit()
        quit()

if __name__ == '__main__':
    """Start Connect4 GUI calculation."""
    connect_four_game = ConnectFour()
    connect_four_game.startgame()
