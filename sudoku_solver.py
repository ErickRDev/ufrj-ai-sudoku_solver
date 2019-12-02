import copy
import random

from random import randrange
from prettytable import PrettyTable


class SudokuBoardSolver():
    """ Sudoku puzzle solver """

    def __init__(self, filled_states, debug_mode):
        """ Initializes board """
        self.debug_mode = debug_mode
        self.configuration = [[0] * 9 for x in range(9)]
        self.repetitions = 0
        self.immutable_coords = set()

        if not filled_states:
            raise Exception("Err::missing filled_states matrix")

        for state in filled_states:
            # normalizing the coordinates to 0-based indexes
            coords = (state[0][0] - 1, state[0][1] -1)

            # filling cell
            self.configuration[coords[0]][coords[1]] = state[1]

            # adding to immutable coords set
            self.immutable_coords.add(coords)

        self.print_configuration()

        # generating initial configuration
        for i in range(9):
            for j in range(9):
                if (i, j) in self.immutable_coords:
                    continue
                self.configuration[i][j] = randrange(1, 10)

        self.print_configuration()

        # calculating repetitions in initial board configuration
        self.repetitions = SudokuBoardSolver.count_repetitions(self.configuration)


    def print_configuration(self):
        """ Pretty-prints board configuration """
        print(f"Repetitions={self.repetitions}")

        p = PrettyTable()
        for row in self.configuration:
            p.add_row(row)

        print(p.get_string(header=False))
        print()


    def climb_hill(self):
        """ Performs an iteration of the hillclimbing algorithm """
        improved = False

        for i in range(9):
            for j in range(9):
                if (i, j) in self.immutable_coords:
                    continue

                # cloning to candidate configuration
                configuration = copy.deepcopy(self.configuration)

                for value in range(1, 10):
                    if value == configuration[i][j]:
                        continue

                    configuration[i][j] = value
                    repetitions = SudokuBoardSolver.count_repetitions(configuration)

                    improved = repetitions < self.repetitions

                    if self.debug_mode:
                        print(f"Value {value} on coords: ({i}, {j}) yielded {repetitions} repetitions (best: {self.repetitions})")

                    # verifying if we minimized the amount of repetitions with candidate move
                    if improved:
                        self.configuration = configuration
                        self.repetitions = repetitions
                        return True

        # we return false if we didn't manage to find gains
        #   by climbing the function hill
        return False


    def solve_puzzle(self):
        """ Attempts to solve the puzzle """
        while True:
            improved = self.climb_hill()

            # printing board configuration after each move
            self.print_configuration()

            if not improved: 
                break


    @staticmethod
    def count_repetitions(board_configuration):
        """ 
            Counts the repetitions found in the supplied board configuration 
            The repetitions are counted in three different ways:
                1. By row
                2. By column
                3. By square
        """
        row_repetitions = 0
        col_repetitions = 0
        sqr_repetitions = 0

        for row in range(9):
            counts = [0] * 9
            for col in range(9):
                counts[board_configuration[row][col] - 1] += 1
            row_repetitions += sum(map(lambda x: x - 1 if x > 1 else 0, counts))

        for col in range(9):
            counts = [0] * 9
            for row in range(9):
                counts[board_configuration[row][col] - 1] += 1
            col_repetitions += sum(map(lambda x: x - 1 if x > 1 else 0, counts))

        for initial_row in range(0, 9, 3):
            for initial_col in range(0, 9, 3):
                counts = [0] * 9
                for row in range(initial_row, initial_row + 3):
                    for col in range(initial_col, initial_col + 3):
                        counts[board_configuration[row][col] - 1] += 1
                sqr_repetitions += sum(map(lambda x: x - 1 if x > 1 else 0, counts))

        return row_repetitions + col_repetitions + sqr_repetitions


def run():
    """ Naive hillclimbing implementation to solve sudoku puzzles """
    # initial filled states for this puzzle instance
    FILLED_STATES = [
        ((1, 4), 7),
        ((2, 1), 1),
        ((3, 4), 4),
        ((3, 5), 3),
        ((3, 7), 2),
        ((4, 9), 6),
        ((5, 4), 5),
        ((5, 6), 9),
        ((6, 7), 4),
        ((6, 8), 1),
        ((6, 9), 8),
        ((7, 5), 8),
        ((7, 6), 1),
        ((8, 3), 2),
        ((8, 8), 5),
        ((9, 2), 4),
        ((9, 7), 3)
    ]

    board_solver = SudokuBoardSolver(FILLED_STATES, debug_mode=False)
    board_solver.solve_puzzle()


if __name__ == "__main__":
    run()