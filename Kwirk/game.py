# Chao PAN

import sys
from PyQt5.QtWidgets import QMessageBox, QApplication, QDialog
from PyQt5.QtGui import QPixmap

from dialog import Ui_Dialog
from model import GameModel, data_map


class Game(Ui_Dialog, GameModel):
    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        self.pushButton_down.clicked.connect(lambda:
                                             self.move(self.pushButton_down))
        self.pushButton_up.clicked.connect(lambda:
                                           self.move(self.pushButton_up))
        self.pushButton_left.clicked.connect(lambda:
                                             self.move(self.pushButton_left))
        self.pushButton_right.clicked.connect(lambda:
                                              self.move(self.pushButton_right))
        self.comboBox.activated[str].connect(self.alter_player)
        self.player = self.players["1"]

    def alter_player(self, text):
        '''
        In the comboBox, when we choose a player, this function will be
        triggered.
        '''
        path = "images/char{}.png".format(text[-1])
        self.player_icon.setPixmap(QPixmap(path))
        self.player = self.players[text[-1]]

    def convert_unit(self, w, h):
        """
        To convert the coordinates. We have two types of coordinates,
        one is for txt file, the other is for GUI
        """
        return self.x0 + self.icon_size * w, self.y0 + self.icon_size * h

    def move(self, btn):
        p = self.player.pos()
        x, y = p.x(), p.y()
        order = btn.text()
        step = 30
        player = self.comboBox.currentText()[-1]

        h, w = self._coors_players[player]
        if order == "v":
            # We meet a turnstile
            if self._grid[h + 1][w] == "'":
                # Try to move down
                if self.is_ok_to_move(h + 1, w, order, player):
                    # For current position, we change '1' to ' '
                    self._grid[h][w] = " "
                    # Change the coordinates of player
                    self._coors_players[player] = (h + 2, w)
                    self.player.move(x, y + 2 * step)
            else:
                # Try to move down
                if self.is_ok_to_move(h + 1, w, order, player):
                    # For current position, we change '1' to ' '
                    self._grid[h][w] = " "
                    # Change the coordinates of player
                    self._coors_players[player] = (h + 1, w)
                    self.player.move(x, y + step)
        elif order == "^":
            # We meet a turnstile
            if self._grid[h - 1][w] == "'":
                # Try to move up
                if self.is_ok_to_move(h - 1, w, order, player):
                    # For current position, we change '1' to ' '
                    self._grid[h][w] = " "
                    # Change the coordinates of player
                    self._coors_players[player] = (h - 2, w)
                    self.player.move(x, y - 2 * step)
            else:
                # Try to move up
                if self.is_ok_to_move(h - 1, w, order, player):
                    # For current position, we change '1' to ' '
                    self._grid[h][w] = " "
                    # Change the coordinates of player
                    self._coors_players[player] = (h - 1, w)
                    self.player.move(x, y - step)
        elif order == "<":
            # We meet a turnstile
            if self._grid[h][w - 1] == "'":
                # Try to move left
                if self.is_ok_to_move(h, w - 1, order, player):
                    # For current position, we change '1' to ' '
                    self._grid[h][w] = " "
                    # Change the coordinates of player
                    self._coors_players[player] = (h, w - 2)
                    self.player.move(x - 2*step, y)
            else:
                # Try to move left
                if self.is_ok_to_move(h, w - 1, order, player):
                    # For current position, we change '1' to ' '
                    self._grid[h][w] = " "
                    # Change the coordinates of player
                    self._coors_players[player] = (h, w - 1)
                    self.player.move(x - step, y)

        elif order == ">":
            # We meet a turnstile
            if self._grid[h][w + 1] == "'":
                # Try to move right
                if self.is_ok_to_move(h, w + 1, order, player):
                    # For current position, we change '1' to ' '
                    self._grid[h][w] = " "
                    # Change the coordinates of player
                    self._coors_players[player] = (h, w + 2)
                    self.player.move(x + 2*step, y)
            else:
                if self.is_ok_to_move(h, w + 1, order, player):
                    # For current position, we change '1' to ' '
                    self._grid[h][w] = " "
                    # Change the coordinates of player
                    self._coors_players[player] = (h, w + 1)
                    self.player.move(x + step, y)
        else:
            QMessageBox().warning(None, "Warnning", "Input error",
                                  QMessageBox.Ok)
            self.print_valid_orders()

        if self.is_game_over():
            QMessageBox.information(None, "Game Over",
                                    "Congratulations! You win!",
                                    QMessageBox.Ok)
            sys.exit()

    # Check if it's ok to push a crate
    def is_ok_to_push_crate(self, h, w, next_h, next_w, player):
        '''
        When we come across a crate, the next element of crate is only
        hole('o' or 'O') or space(' '), we can move; otherwise we cannot
        move
        '''
        next_value = self._grid[next_h][next_w]  # Next elements of crate
        if next_value == " ":  # Space
            self._grid[next_h][next_w] = '*'  # Push the crate
            self._grid[h][w] = player  # Charachter goes forward
            for crate in self.crates:
                pos = crate.pos()
                x, y = pos.x(), pos.y()
                xc, yc = self.convert_unit(w, h)
                if xc == x and yc == y:
                    xn, yn = self.convert_unit(next_w, next_h)
                    crate.move(xn, yn)
                    break
            return True  # Move successfully
        elif next_value == "o":  # Hole
            self._grid[next_h][next_w] = " "  # Fill this fole with the crate
            self._grid[h][w] = player  # Character goes forward
            for crate in self.crates:
                pos = crate.pos()
                x, y = pos.x(), pos.y()
                xc, yc = self.convert_unit(w, h)
                if xc == x and yc == y:
                    xn, yn = self.convert_unit(next_w, next_h)
                    crate.setPixmap(QPixmap("images/empty.png"))
                    self.crates.remove(crate)
                    break
            for hole in self.holes:
                pos = hole.pos()
                xc, yc = self.convert_unit(next_w, next_h)
                if pos.x() == xc and pos.y() == yc:
                    hole.setPixmap(QPixmap("images/empty.png"))
                    self.holes.remove(hole)
                    break
            return True
        elif next_value == "O":
            self._grid[next_h][next_w] = "o"
            self._grid[h][w] = player
            for crate in self.crates:
                pos = crate.pos()
                x, y = pos.x(), pos.y()
                xc, yc = self.convert_unit(w, h)
                if xc == x and yc == y:
                    xn, yn = self.convert_unit(next_w, next_h)
                    crate.setPixmap(QPixmap("images/empty.png"))
                    self.crates.remove(crate)
                    break
            for deep_hole in self.deep_holes:
                pos = deep_hole.pos()
                xc, yc = self.convert_unit(next_w, next_h)
                if pos.x() == xc and pos.y() == yc:
                    deep_hole.setPixmap(QPixmap("images/hole.png"))
                    self.deep_holes.remove(deep_hole)
                    self.holes.append(deep_hole)
                    break
            return True
        else:
            QMessageBox.warning(None, "Warnning", "Cannot push the crate",
                                QMessageBox.Ok)
            return False  # Cannot push the crate

    # Rotate a turnstile
    def rotate_turnstile(self, coor_turnstile, clockwise):
        '''
        Find a turnstile and rotate it either clockwisely
        or counterclockwisely
        '''
        # Coordinates of turnstile
        h, w = coor_turnstile
        xc, yc = self.convert_unit(w, h)
        assert self._grid[h][w] == "%", "Error for turnstile"

        for turnstile in self.turnstiles.keys():
            pos = turnstile.pos()
            if xc == pos.x() and yc == pos.y():
                break
        axis = self.turnstiles[turnstile]
        R = axis["R"]
        D = axis["D"]
        L = axis["L"]
        U = axis["U"]
        # 2 directions
        if clockwise:
            temp = self._grid[h][w + 1]
            self._grid[h][w + 1] = self._grid[h - 1][w]
            self._grid[h - 1][w] = self._grid[h][w - 1]
            self._grid[h][w - 1] = self._grid[h + 1][w]
            self._grid[h + 1][w] = temp

            x_R, y_R = R.pos().x(), R.pos().y()
            R.move(D.pos().x(), D.pos().y())
            D.move(L.pos().x(), L.pos().y())
            L.move(U.pos().x(), U.pos().y())
            U.move(x_R, y_R)
            self.turnstiles[turnstile]["R"] = U
            self.turnstiles[turnstile]["U"] = L
            self.turnstiles[turnstile]["L"] = D
            self.turnstiles[turnstile]["D"] = R
        else:
            temp = self._grid[h][w + 1]
            self._grid[h][w + 1] = self._grid[h + 1][w]
            self._grid[h + 1][w] = self._grid[h][w - 1]
            self._grid[h][w - 1] = self._grid[h - 1][w]
            self._grid[h - 1][w] = temp

            x_R, y_R = R.pos().x(), R.pos().y()
            R.move(U.pos().x(), U.pos().y())
            U.move(L.pos().x(), L.pos().y())
            L.move(D.pos().x(), D.pos().y())
            D.move(x_R, y_R)
            self.turnstiles[turnstile]["R"] = D
            self.turnstiles[turnstile]["D"] = L
            self.turnstiles[turnstile]["L"] = U
            self.turnstiles[turnstile]["U"] = R

    # Check if it is ok to move
    def is_ok_to_move(self, h, w, order, player):
        """
        According to the order, we try to move and we check
        if it is legal for move on
        h, w mean the coordinates of next step for a player
        This function retrun True or False
        True means we can move, False means we cannot move
        """
        # Get the value for current coordinates
        value = self._grid[h][w]
        # We meet a wall
        if value == '#':
            QMessageBox.warning(None, "Warnning", "Cannot go through the wall",
                                QMessageBox.Ok)
            return False
        elif value in self._coors_players.keys():
            QMessageBox.warning(None, "Warnning",
                                "Cannot move on because of another player",
                                QMessageBox.Ok)
            return False
        elif value == "%":
            QMessageBox.warning(None, "Warnning",
                                "Cannot go through a turnstile",
                                QMessageBox.Ok)
            return False
        # We meet hole
        elif value in ["o", "O"]:
            s1 = "Cannot pass over a hole"
            s2 = "But you can fill it with a crate"
            s3 = "For 1-depth hole, both crate an hole"
            s4 = "For 2-depth hole, it need 2 crate to be filled"
            QMessageBox.warning(None, "Warnning",
                                "{}\n{}\n{}\n{}".format(s1, s2, s3, s4),
                                QMessageBox.Ok)
            return False
        # We meet a crate
        elif value == "*":
            if order == ">":  # Move right
                # Try to push crate
                return self.is_ok_to_push_crate(h, w, h, w + 1, player)
            elif order == "<":  # Move left
                return self.is_ok_to_push_crate(h, w, h, w - 1, player)
            elif order == "^":  # Move up
                return self.is_ok_to_push_crate(h, w, h - 1, w, player)
            elif order == "v":  # Move down
                return self.is_ok_to_push_crate(h, w, h + 1, w, player)
            else:  # Out of valid orders
                return False
        elif value == "'":
            if order == ">":
                if self._grid[h][w + 1] == " " and self._grid[h + 1][w] == "%":
                    # Rotate turnstile clockwisely
                    self.rotate_turnstile([h + 1, w], True)
                    self._grid[h][w + 1] = player
                elif self._grid[h][w + 1] == " " and \
                        self._grid[h - 1][w] == "%":
                    # Rotate turnstile counterclockwisely
                    self.rotate_turnstile([h - 1, w], False)
                    self._grid[h][w + 1] = player
                else:
                    QMessageBox.warning(None, "Warnning",
                                        "Cannot go through a turnstile",
                                        QMessageBox.Ok)
                    return False
            elif order == "<":
                if self._grid[h][w - 1] == " " and self._grid[h + 1][w] == "%":
                    # Rotate counterclockwisely
                    self.rotate_turnstile([h + 1, w], False)
                    self._grid[h][w - 1] = player
                elif self._grid[h][w - 1] == " " and \
                        self._grid[h - 1][w] == "%":
                    # Rsotate clockwisely
                    self.rotate_turnstile([h - 1, w], True)
                    self._grid[h][w - 1] = player
                else:
                    QMessageBox.warning(None, "Warnning",
                                        "Cannot go through a turnstile",
                                        QMessageBox.Ok)
                    return False
            elif order == "^":
                if self._grid[h - 1][w] == " " and self._grid[h][w + 1] == "%":
                    # Clockwisely
                    self.rotate_turnstile([h, w + 1], True)
                    self._grid[h - 1][w] = player
                elif self._grid[h - 1][w] == " " and \
                        self._grid[h][w - 1] == "%":
                    # Counterclockwisely
                    self.rotate_turnstile([h, w - 1], False)
                    self._grid[h - 1][w] = player
                else:
                    QMessageBox.warning(None, "Warnning",
                                        "Cannot go through a turnstile",
                                        QMessageBox.Ok)
                    return False
            elif order == "v":
                if self._grid[h + 1][w] == " " and self._grid[h][w + 1] == "%":
                    # Rotate counterclockwisely
                    self.rotate_turnstile([h, w + 1], False)
                    self._grid[h + 1][w] = player
                elif self._grid[h + 1][w] == " " and\
                        self._grid[h][w - 1] == "%":
                    # Rotate clockwisely
                    self.rotate_turnstile([h, w - 1], True)
                    self._grid[h + 1][w] = player
                else:
                    QMessageBox.warning(None, "Warnning",
                                        "Cannot go through a turnstile",
                                        QMessageBox.Ok)
                    return False
            else:  # Out of valid orders
                return False
            return True
        else:  # We come across '@' or ' '
            self._grid[h][w] = player
            return True

    # Check if our game is over
    def is_game_over(self):
        '''
        Any player arrives at the door, our game is over
        '''
        pos_door = self.door.pos()
        x_door = pos_door.x()
        y_door = pos_door.y()
        for num in self._coors_players.keys():
            player = self.players[num]
            x_player = player.pos().x()
            y_player = player.pos().y()
            if x_door == x_player and y_door == y_player:
                return True
        return False


class Dialog(QDialog):
    def closeEvent(self, event):
        """
        Rewrite closeEvent
        :param event: close() trigger event
        :return: None
        """
        reply = QMessageBox.question(self, "QUIT", "Do you want to quit game?",
                                     QMessageBox.Yes | QMessageBox.No,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


def main():
    app = QApplication(sys.argv)
    Form = Dialog()
    ui = Game(data_map())
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
