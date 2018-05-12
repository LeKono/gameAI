import time
import numpy as np
import pygame
import math


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

        if max(results) >= 4:
            i = results.index(max(results))

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

    def play_a_game(self, winners_print=True):
        """Two players can play a game.

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
        """Initiates all class variables needed for GUI implementation to run.
        The initiations are done here so there will be no PyGame interference while
        using ConnectFour on console."""

        # Initiate PyGame
        pygame.init()
        pygame.display.set_caption('Connect4')

        # Screen loop variables
        self.intro = False
        self.end = False

        # Color definitions for PyGame
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (125, 125, 125)
        self.BLUE = (0, 0, 255)
        self.RED = (255, 0, 0)
        self.YELLOW = (255, 255, 0)

        # Mapping for player colors
        self.PLAYER_COLOR = {
            1: self.YELLOW,  # Player one token color
            -1: self.RED,    # Player two token color
            0: self.BLACK    # Empty field color
        }

        # Game field definitions
        self.SQUARESIZE = 100
        self.CIRCLE_RADIUS = int(self.SQUARESIZE / 2 - 5)

        # PyGame basic screen setup for Connect4
        self.WIDTH = 7 * self.SQUARESIZE
        self.HEIGHT = (6 + 1) * self.SQUARESIZE
        self.SCREEN = pygame.display.set_mode([self.WIDTH, self.HEIGHT])

        # Additional setups for PyGame
        self.LARGE_TEXT = pygame.font.Font('freesansbold.ttf', 115)
        self.SMALL_TEXT = pygame.font.Font("freesansbold.ttf", 20)
        self.CLOCK = pygame.time.Clock()

        # Start game with the intro screen
        self.intro_screen()

    def intro_screen(self):
        """Realizes the 'main menu' of the game.

        Inspired by PyGame tutorial 10 from Santex (Start Menu)
        """

        # stop end screen loop if it is running
        self.end = False

        # start intro loop
        self.intro = True

        while self.intro_screen:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitgame()

            self.SCREEN.fill(self.BLACK)
            TextSurf, TextRect = self.text_object("Connect4", self.LARGE_TEXT, self.WHITE)
            TextRect.center = ((self.WIDTH/2), 100)
            self.SCREEN.blit(TextSurf, TextRect)

            # Keep track of the mouse
            mouse = pygame.mouse.get_pos()

            # Keep track of mouse action
            click = pygame.mouse.get_pressed()

            # Computer vs. Computer
            self.button((250, 200, 150, 50), self.GRAY, "E.vs.E.", mouse, click, self.start_gui_game)

            # Human vs. Computer
            self.button((250, 275, 150, 50), self.GRAY, "P.vs.E.", mouse, click, self.start_gui_game, ['pve'])

            # Human vs. Human
            self.button((250, 350, 150, 50), self.GRAY, "P.vs.P.", mouse, click, self.start_gui_game, ['pvp'])

            # Quit
            self.button((250, 425, 150, 50), self.GRAY, "Quit", mouse, click, self.quitgame)

            pygame.display.update()
            self.CLOCK.tick()

    def game_screen(self, mode):
        """Plays a gui game

        This function was inspired by the Connect4 for Python tutorial by
        Keith Galli (YouTube).

        :param mode: Parameter to set the mode of the game. This can be one of:
                        - eve: Environment vs. Environment
                        - pve: Player vs. Environment
                        - pvp: Player vs. Player
        """
        # Stop intro screen loop if still running
        self.intro = False

        eve = False
        pve = False
        pvp = False

        # Set the Flag for pve or pvp
        if mode == 'eve':
            eve = True
        elif mode == 'pve':
            pve = True
        elif mode == 'pvp':
            pvp = True
        else:
            raise Exception("Unknown mode '{}' for GUI game!".format(mode))

        # Game loop
        while not self.game_finished:

            for event in pygame.event.get():
                # Quit game by 'x' button
                if event.type == pygame.QUIT:
                    self.quitgame()

            if pvp or (pve and self.player == 1):
                self.player_move()
            else:
                self.random_move()

            # Update the game field
            self.update_board()

            if eve:
                # Wait one second, that way it is easier to follow for observers
                time.sleep(1)

        if self.game_finished:
            # Console output of who won the game
            print("{} won the game!".format(self.symbols[self.player]))

            # Game endscreen
            self.end_screen()

    def end_screen(self):
        """End screen definition that shows the winner."""

        # Start end screen loop
        self.end = True

        if self.is_draw:
            text_color = self.WHITE
            text = "DRAW!"
        else:
            text_color = self.PLAYER_COLOR[self.player]
            text = self.symbols[self.player] + " winns!"

        while self.end:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quitgame()

            TextSurf, TextRect = self.text_object(text, self.LARGE_TEXT, text_color)
            TextRect.center = ((self.WIDTH / 2), 55)
            self.SCREEN.blit(TextSurf, TextRect)
            pygame.display.update()

            # Keep track of the mouse
            mouse = pygame.mouse.get_pos()

            # Keep track of mouse action
            click = pygame.mouse.get_pressed()

            self.button((590, 15, 100, 50), self.GRAY, "Back", mouse, click, self.intro_screen)

            pygame.display.update()
            self.CLOCK.tick()

    def quitgame(self):
        """Helper function for quitting game."""
        pygame.quit()
        quit()

    def start_gui_game(self, mode='eve'):
        """Creates a view of Connect4 using PyGame.

        :param mode: Parameter to set the mode of the game. This can be one of:
                        - eve: Environment vs. Environment
                        - pve: Player vs. Environment
                        - pvp: Player vs. Player
        """
        self.reset_game()
        self.update_board()
        self.game_screen(mode)

    def update_board(self):
        """Draws the game board

        This function was inspired by the Connect4 for Python tutorial by
        Keith Galli (YouTube).
        """
        # Clear top row
        pygame.draw.rect(self.SCREEN, self.BLACK, (0, 0, self.WIDTH, self.SQUARESIZE))

        # Loop over columns and rows
        for c in range(7):
            for r in range(6):
                # definition of a ractangle and circle for the GUI
                rectangle = (c * self.SQUARESIZE, r * self.SQUARESIZE + self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE)
                circle = (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(r * self.SQUARESIZE + self.SQUARESIZE + self.SQUARESIZE / 2))

                # Draw blue rectangles (represents the game field)
                pygame.draw.rect(self.SCREEN, self.BLUE, rectangle)

                # Draw circles to represent cell state
                # Check self.PLAYER_COLOR for color schema
                pygame.draw.circle(self.SCREEN, self.PLAYER_COLOR[self.game_field[r][c]], circle, self.CIRCLE_RADIUS)

        pygame.display.update()

    def text_object(self, text, font, color):
        """Creates a text object for PyGame.

        :param text: The text that should be displayed.
        :param font: PyGame font to use for the text.
        :param color: The color of the text.
        """
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()

    def button(self, rect, color, text, mouse, click, action=None, action_parameters=None):
        """Function to wrap a simple way to create buttons using PyGame.

        :param rect: The size of the button (rectangle definition)
        :param color: The color to use for the button.
        :param text: The text to display on the button
        :param mouse: Keep track of mouse position
        :param click: Keep track of mouse action
        :param action: What should be the action to perform on a click.
        :param action_parameters: List of values to pipe into action. Careful usage! Needs knowledge of called action!
        """
        if rect[0] + rect[2] > mouse[0] > rect[0] and rect[1] + rect[3] > mouse[1] > rect[1]:
            # If the mouse is on the rectangle draw a brighter one
            brighter_color = [code+50 if code+50 < 256 else 255 for code in color]
            pygame.draw.rect(self.SCREEN, brighter_color, rect)

            if click[0] == 1 and action is not None:
                if action_parameters is not None:
                    action(*action_parameters)
                else:
                    action()

        else:
            pygame.draw.rect(self.SCREEN, color, rect)

        textSurf, textRect = self.text_object(text, self.SMALL_TEXT, self.WHITE)
        textRect.center = ((rect[0] + (rect[2] / 2)), (rect[1] + (rect[3] / 2)))
        self.SCREEN.blit(textSurf, textRect)

    def player_move(self):
        """Method for a player move. Shows the player a preview where the token would go on click
        and handles placement."""

        valid_move = False
        while not valid_move:
            # Keeping track of all events happening on the game screen
            for event in pygame.event.get():
                # Quit game by 'x' button
                if event.type == pygame.QUIT:
                    self.quitgame()

                # Player moves the mouse (token placement preview)
                if event.type == pygame.MOUSEMOTION:
                    # Clear top row
                    pygame.draw.rect(self.SCREEN, self.BLACK, (0, 0, self.WIDTH, self.SQUARESIZE))

                    # X position of mouse
                    x_position = event.pos[0]

                    # Draw the right token color for the player on mouse position
                    pygame.draw.circle(
                        self.SCREEN,
                        self.PLAYER_COLOR[self.player],
                        (x_position, int(self.SQUARESIZE/2)),
                        self.CIRCLE_RADIUS
                    )
                    # Update view
                    pygame.display.update()

                # Player presses the mouse button (puts a token)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # X position of mouse
                    x_position = event.pos[0]

                    # Rounded column number (0, 1, ..., 6)
                    column = int(math.floor(x_position / self.SQUARESIZE))
                    valid_move = self.make_a_move(column)

                    # Clear top row
                    pygame.draw.rect(self.SCREEN, self.BLACK, (0, 0, self.WIDTH, self.SQUARESIZE))

                    # Update view
                    pygame.display.update()



if __name__ == '__main__':
    """Start Connect4 GUI"""
    connect_four_game = ConnectFour()
    connect_four_game.startgame()
