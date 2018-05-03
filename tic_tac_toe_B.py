import numpy as np


class TicTacToe:

    def __init__(self):
        """Setup a instance of Tic-Tac-Toe game."""

        self.S = np.zeros((3, 3), dtype=int)
        self.p = 1
        self.symbols = {1: 'x', -1: 'o', 0: ' '}

    def move_still_possible(self):
        """Checks if a move is still possible."""
        return not (self.S[self.S == 0].size == 0)

    def move_at_random(self):
        """Make a random move."""
        xs, ys = np.where(self.S == 0)
        i = np.random.permutation(np.arange(xs.size))[0]
        self.S[xs[i], ys[i]] = self.p

    def move_was_winning_move(self):
        """Checks if a move was a winning move."""

        if np.max((np.sum(self.S, axis=0)) * self.p) == 3:
            return True

        if np.max((np.sum(self.S, axis=1)) * self.p) == 3:
            return True

        if (np.sum(np.diag(self.S)) * self.p) == 3:
            return True

        if (np.sum(np.diag(np.rot90(self.S))) * self.p) == 3:
            return True

        return False

    def print_game_state(self):
        """Prints the game state."""
        B = np.copy(self.S).astype(object)
        for n in [-1, 0, 1]:
            B[B == n] = self.symbols[n]
        print(B)

    def play_a_game(self, print_every_step=True, random=True):
        """Let two computer players play a game.

        :param print_every_step: Determines if everything should be printed (handy for tournament).
        :param random: Determines if the game is played with random moves.
        """

        if random:

            # initialize flag that indicates win
            noWinnerYet = True
            mvcntr = 1

            while self.move_still_possible() and noWinnerYet:
                # get player symbol
                name = self.symbols[self.p]

                # let player move at random
                self.move_at_random()

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

            if noWinnerYet:
                return None, True
            else:
                return self.p, False

        else:
            # Not yet implemented
            pass

    def reset_game(self):
        """Resets the game for another round."""
        self.S = np.zeros((3, 3), dtype=int)
        self.p = 1

    def play_a_tournament(self, laps=1000, printing_modulo=100, random=True):
        """Lets two computer players play a tournament.

        :param laps: Number of laps to play at the tournament.
        :param printing_modulo: Modulo to print out the state of the tournament.
        :param random: Determines if the tournament is played with random moves.
        """
        wins = {
            1: 0,  # Wins of player 1
            -1: 0,  # Wins of player -1
            0: 0  # Draws
        }

        for l in range(0, laps):
            winner, draw = self.play_a_game(print_every_step=False, random=random)
            if draw:
                wins[0] += 1
            else:
                wins[winner] += 1

            if not l % printing_modulo:
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


if __name__ == '__main__':
    """If the file is started from console it will works exactly like the original version."""
    ttt = TicTacToe()
    ttt.play_a_game()
