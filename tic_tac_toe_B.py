import json

import numpy as np
import matplotlib.pyplot as plt


class TicTacToe:

    def __init__(self):
        """Setup a instance of Tic-Tac-Toe game."""

        # Game field
        self.S = np.zeros((3, 3), dtype=int)

        # Keep track of statistics for game field (S_stats) and overall winning / loosing (game_stats)
        self.S_stats = np.zeros((3, 3), dtype=int)
        self.game_stats = {
            1: 0,
            -1: 0,
            0: 0
        }

        # A counter for how many games where played on the instance
        self.games_played = 0
        self.tournaments_played = 0

        # Starting player
        self.p = 1

        # Mapping of player-id to symbol
        self.symbols = {1: 'x', -1: 'o', 0: ' '}

        # Variable to hold probabilities
        self.probability_data = None

    def move_still_possible(self):
        """Checks if a move is still possible."""
        return not (self.S[self.S == 0].size == 0)

    def move_at_random(self):
        """Make a random move."""
        xs, ys = np.where(self.S == 0)
        i = np.random.permutation(np.arange(xs.size))[0]
        self.S[xs[i], ys[i]] = self.p

    def move_using_probability(self, evaluate_move=False):
        """Makes a move based on the probability of a cell to be a winning candidate.

        :param evaluate_move: Flag to set if the move should be evaluated.
        """
        xs, ys = np.where(self.S == 0)

        # Initialisation for a maximal statistical value
        best_probability = 0

        # Get the highest win participation cell from the statistical data
        if not evaluate_move or np.sum(self.S) == 0:
            for i in range(xs.size):
                best_probability = np.max([best_probability, self.probability_data['p'][(3*xs[i] + ys[i])]])

            x, y = self.probability_data['mapping'][self.probability_data['p'].index(best_probability)]

        else:
            # Evaluate
            field_sums = [
                np.sum(self.S, axis=0),
                np.sum(self.S, axis=1),
                np.sum(np.diag(self.S)),
                np.sum(np.diag(np.rot90(self.S)))
            ]

            x, y = None, None #self.probability_data['mapping'][self.probability_data['p'].index(best_probability)]

        self.S[x, y] = self.p

    def move_was_winning_move(self):
        """Checks if a move was a winning move."""

        game_won = False

        if np.max((np.sum(self.S, axis=0)) * self.p) == 3:
            self._update_stats("v")
            game_won = True

        if np.max((np.sum(self.S, axis=1)) * self.p) == 3:
            self._update_stats("h")
            game_won = True

        if (np.sum(np.diag(self.S)) * self.p) == 3:
            self._update_stats("d")
            game_won = True

        if (np.sum(np.diag(np.rot90(self.S))) * self.p) == 3:
            self._update_stats("i")
            game_won = True

        return game_won

    def _update_stats(self, alignment):
        """Helper method to update statistics about cells that contributed to a win.

        :param alignment: One of:
                            - (v)ertical
                            - (h)orizontal
                            - (d)iagonal
                            - (i)nverse diagonal
        """
        # ToDo: This is a more or less ugly solution -> Check for a better implementation

        if alignment == "v":
            vertical_sum = (np.sum(self.S, axis=0)) * self.p
            column_index = np.argmax(vertical_sum)
            for row in range(0, 3):
                self.S_stats[row][column_index] += 1

        elif alignment == "h":
            horizontal_sum = (np.sum(self.S, axis=1)) * self.p
            row_index = np.argmax(horizontal_sum)
            for column in range(0, 3):
                self.S_stats[row_index][column] += 1

        elif alignment == "d":
            for index in range(0, 3):
                self.S_stats[index][index] += 1

        elif alignment == "i":
            for row, column in [(2, 0), (1, 1), (0, 2)]:
                self.S_stats[row][column] += 1

        else:
            raise Exception("Invalid argument for alignment parameter: '{}'".format(alignment))

    def play_a_game(self, print_every_step=True, random=True, x_player_method="p"):
        """Let two computer players play a game.

        :param print_every_step: Determines if everything should be printed (handy for tournament).
        :param random: Determines if the game is played with random moves.
        :param x_player_method: If random is False this parameter determines which approach player X should use:
                                - (p)robabilistic
                                - (h)euristic

        :returns: None if game was a draw or the player who won.
        """
        # initialize flag that indicates win
        noWinnerYet = True
        mvcntr = 1

        while self.move_still_possible() and noWinnerYet:
            # get player symbol
            name = self.symbols[self.p]

            if random or self.p == -1:
                # let player move at random
                self.move_at_random()
            else:
                if x_player_method == "p":
                    self.move_using_probability()
                elif x_player_method == "h":
                    pass
                else:
                    raise Exception("Invalid value for x_player_method: '{}'".format(x_player_method))

            if print_every_step:
                # A little cheating here, the move happens before the print,
                # but this way only one check for print_every_step is needed.
                print('%s moves' % name)
                # print current game state
                self.print_game_state()

            # evaluate game state
            if self.move_was_winning_move():
                if print_every_step:
                    print('player %s wins after %d moves' % (name, mvcntr))

                noWinnerYet = False
            else:
                # switch player and increase move counter
                self.p *= -1
                mvcntr += 1

        self.games_played += 1

        if noWinnerYet:
            self.game_stats[0] += 1
            return None
        else:
            self.game_stats[self.p] += 1
            return self.p

    def reset_game(self):
        """Resets the game for another round."""
        self.S = np.zeros((3, 3), dtype=int)
        self.p = 1

    def play_a_tournament(self, laps=1000, printing_modulo=100, random=True):
        """Lets two computer players play a tournament.

        :param laps: Number of laps to play at the tournament.
        :param printing_modulo: Modulo to print out the state of the tournament.
        :param random: Determines if the tournament is played with random moves.

        :returns: Stats dict for this tournament.
        """
        tournament_statistics = {
            1: 0,  # Wins of player 1
            -1: 0,  # Wins of player -1
            0: 0  # Draws
        }

        for l in range(0, laps):
            winner = self.play_a_game(print_every_step=False, random=random)
            if winner is None:
                tournament_statistics[0] += 1
            else:
                tournament_statistics[winner] += 1

            if not l % printing_modulo:
                print("=== Lap: {} ===\n'{}'\t{}\n'{}'\t{}\nDRAW\t{}".format(l,
                                                                             self.symbols[1],
                                                                             tournament_statistics[1],
                                                                             self.symbols[-1],
                                                                             tournament_statistics[-1],
                                                                             tournament_statistics[0]))
            self.reset_game()

        print("Tournament results in: \n'{}'\t{}\n'{}'\t{}\nDRAW\t{}".format(self.symbols[1],
                                                                             tournament_statistics[1],
                                                                             self.symbols[-1],
                                                                             tournament_statistics[-1],
                                                                             tournament_statistics[0]))

        self.tournaments_played += 1

        return tournament_statistics

    def print_game_state(self):
        """Prints the game state."""
        B = np.copy(self.S).astype(object)
        for n in [-1, 0, 1]:
            B[B == n] = self.symbols[n]
        print(B)

    def print_overall_statistics(self):
        """Prints all statistics for this instance"""

        print(
            """==== Overall statistics for this instance of TicTacToe ==== \n
            #Tournaments:\t{}\n
            #Games:\t{}\n\n
            Resulting in: \n
            #X-Wins:\t{}\n
            #O-Wins:\t{}\n
            #Draws:\t{}
            """.format(self.tournaments_played, self.games_played, self.game_stats[1], self.game_stats[-1], self.game_stats[0])
        )

    def plot_bar(self, label="TicTacToe Stats.", statistics=None):
        """Plots a histogram using matplotlib

        :param label: Label to use on the plot.
        :param statistics: If some statistics where collected outside of the instance it can be passed using
        this parameter. self.game_stats will be used otherwise.
        """
        # Setup values for x and y axis
        x = []
        y = []

        # If no statistics where given as parameter use self.game_stats
        if statistics is None:
            print("Setting stats to total")
            statistics = self.game_stats

        # Distribute keys and values to x and y lists
        for key, value in statistics.items():
            x.append(self.symbols[key] if self.symbols[key] != " " else "DRAW")
            y.append(value)

        plt.bar(x, y)
        plt.xlabel("Outcome")
        plt.ylabel("# of outcome")
        plt.title(label)
        plt.show()

    def normalize_statistics(self, store_to_file=True, filename="normalized_data"):
        """Takes the data collected ins self.S_stats and normalizes it to 1.

        :param store_to_file: Determines if normalization should be stored into a JSON file.
        :param filename: Name of file to store the normalization in.
        """
        total = np.sum(self.S_stats)
        norm = []
        mapping = {}
        for row in range(0, 3):
            for column in range(0, 3):
                cell_value = self.S_stats[row][column]
                norm.append(float(cell_value) / total)
                mapping[len(norm)-1] = (row, column)

        self.probability_data = {
            'mapping': mapping,
            'p': norm
        }

        if store_to_file:
            with open(filename+'.json', 'w') as outfile:
                json.dump(self.probability_data, outfile)

    def learn_from_statistics(self, filename="normalized_data"):
        """Reads data from JSON file that contains statistical information.

        :param filename: Name of file to store the normalization in.
        """

        with open(filename+".json") as infile:
            self.probability_data = json.load(infile)

if __name__ == '__main__':
    """If the file is started from console it will work exactly like the original version."""
    ttt = TicTacToe()
    ttt.play_a_game()