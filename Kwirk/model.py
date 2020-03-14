# Chao PAN

import numpy as np
from PyQt5.QtWidgets import QMessageBox


class GameModel:
    """
    Set up a game model
    Coordinates as follows
    o------->w
    |
    |
    |
    v
    h
    Establish rules
    """
    def __init__(self, dataMap, is_test=False):
        # Construct a grid with a 2-D array
        self._grid = self.parse_map(dataMap)
        # Size of grid map (height, width)
        self._height, self._width = self._grid.shape
        # Check map
        self._elements = self.check_map()
        # Coordinates of player
        self._coors_players = self.get_coordinates_players()
        # Is a test
        self._is_test = is_test
        # A possible solution
        self._test_orders = "1vvvvv>>>>>>^^^<^>>>>vvv<^^<^>>>>vvvvv>>"

    # Creat a map of grid with a input data
    def parse_map(self, dataMap):
        '''
        We put our game in a 2-D array as a map, in order to construct
        the array we have to read a source data.
        '''
        # Empty list for stocking the map of game
        grid = []
        for line in dataMap:  # Travel each line of input data
            value = []
            for s in line:  # Split a string into single characters
                value.append(s)
            grid.append(value)
        return np.array(grid)  # In a format of array

    # Check a map si it satisfies the requirements
    def check_map(self):
        '''
        A grid must be at least 5-cell wide and 5-cell high,
        must contain at most 4 characters and one exit, and
        have walls on the borders
        Finally, return a dictionary for reserving all elements
        of this game, as well as their appearing numbers
        '''
        # Check the size of map
        assert self._height >= 5, "invalid height"
        assert self._width >= 5, "invalid width"

        '''
        In my computer, ° is not recognized, so it is replaced with '
        '''
        # Initialise all possible elements with 0 for their appearing times
        elements = {"1": 0, "2": 0, "3": 0, "4": 0, "@": 0, "#": 0, "o": 0,
                    "O": 0, "*": 0, "#": 0, " ": 0, "%": 0, "'": 0}
        # Travel all of the map to check if there is some invalid elements and
        # to count their appearing times
        for h in range(self._height):
            for w in range(self._width):
                # All borders are covered with walls
                if h == 0 or h == self._height - 1 or \
                   w == 0 or w == self._width - 1:
                    assert self._grid[h][w] == "#", "No wall on the border"
                else:
                    # Check some invalid elements
                    assert self._grid[h][w] in elements.keys(), \
                           "Elements {} non recognized".format(
                                                              self._grid[h][w])
                elements[self._grid[h][w]] += 1  # Count

        # Check there is only one door
        assert elements["@"], "No door"
        assert elements["@"] == 1, "More than one door"

        # Check there is only one character 1
        assert elements["1"], "No character 1"
        assert elements["1"] == 1, "More than one character 1"

        # Check is there is other characters, their number must be 1
        for ele in ["2", "3", "4"]:
            if elements[ele] > 1:
                assert False, "More than one character {}".format(ele)

        return elements

    def get_coordinates_players(self):
        '''
        Put the coordinates of all players in to a dictionary
        '''
        coordinates = {}
        for player in ["1", "2", "3", "4"]:
            if self._elements[player]:
                h, w = np.nonzero(self._grid[:, :] == player)
                coordinates[player] = (h[0], w[0])
        return coordinates

    # Introductions of game
    def preamble(self):
        '''
        Give some introductions and indications for our game
        '''
        print("Welcome to our game!\n")
        self.print_map()
        print("Before you start playing, here are some elements:")
        print("1, 2, 3 and 4 for the players")
        print("# for a wall")
        print("o for a 1-depth hole")
        print("O for a 2-depth hole")
        print("* for a crate")
        print("% for a crate and ' for its wings")
        print("@ for the door")
        print("(space) for an empty cell\n")
        print("How to win?\nTry to arrive at the gate!\n")
        print("Warm tips:")
        print("You can move either horizontally or vertically")
        self.print_valid_orders()
        print("You can fill a hole by pushing a crate into it,")
        print("then both the crate and the hole disappear,")
        print("but for a 2-depth hole 'O', it will become 1-depth 'o'")
        print("Last but not least, you can input like 1vv or 2>>1^2>")
        print("If you want to quit our game, input quit")
        print("Now let's begin!!\n")
        self.print_map()

    # Valid orders
    def print_valid_orders(self):
        """
        Give out all legal operations in our game
        """
        s1 = "-----------Attention: Only four orders allowed-----------\n"
        s2 = "> for an horizontal move towards right\n"
        s3 = "< for an horizontal move towards left\n"
        s4 = "^ for a vertical move towards top\n"
        s5 = "v for a vertical move towards bottom\n"
        s6 = "By the way, don\' forget to input the number of player"
        QMessageBox.information(None, "Tips",
                                "{}{}{}{}{}{}".format(s1, s2, s3, s4, s5, s6),
                                QMessageBox.Ok)

    def print_map(self):
        '''
        Print current map grid after each order of player
        Show the position of player
        '''
        print("Game map:")
        for h in range(self._height):
            print("".join(self._grid[h, :].tolist()))
        print()  # Print a blank line


def data_map():
    map_path = "map.txt"
    file = open(map_path)
    # Source data map containing all information of grid
    dataMap = [line.strip() for line in file.readlines()]
    file.close()
    return dataMap
