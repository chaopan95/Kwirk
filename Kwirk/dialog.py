# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from model import GameModel, data_map


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.resize(730, 310)
        Dialog.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        Dialog.setFocusPolicy(QtCore.Qt.NoFocus)
        Dialog.setAcceptDrops(False)
        Dialog.setLayoutDirection(QtCore.Qt.LeftToRight)

        self.icon_size = 30  # image size
        # origin point
        self.x0 = 10
        self.y0 = 30

        self.pushButton_up = QtWidgets.QPushButton(Dialog)
        self.pushButton_up.setGeometry(QtCore.QRect(580, 60, 60, 60))
        self.pushButton_up.setObjectName("pushButton_up")
        self.pushButton_left = QtWidgets.QPushButton(Dialog)
        self.pushButton_left.setGeometry(QtCore.QRect(520, 120, 60, 60))
        self.pushButton_left.setObjectName("pushButton_left")
        self.pushButton_right = QtWidgets.QPushButton(Dialog)
        self.pushButton_right.setGeometry(QtCore.QRect(640, 120, 60, 60))
        self.pushButton_right.setObjectName("pushButton_right")
        self.pushButton_down = QtWidgets.QPushButton(Dialog)
        self.pushButton_down.setGeometry(QtCore.QRect(580, 180, 60, 60))
        self.pushButton_down.setObjectName("pushButton_down")

        self.player_icon = QtWidgets.QLabel(Dialog)
        self.player_icon.setEnabled(True)
        self.player_icon.setGeometry(QtCore.QRect(580, 120, 60, 60))
        self.player_icon.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.player_icon.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.player_icon.setAutoFillBackground(False)
        self.player_icon.setFrameShadow(QtWidgets.QFrame.Plain)
        self.player_icon.setText("")
        self.player_icon.setPixmap(QtGui.QPixmap("images/char1.png"))
        self.player_icon.setAlignment(QtCore.Qt.AlignCenter)
        self.player_icon.setObjectName("player_icon")

        # New instance
        g = GameModel(data_map())

        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(570, 250, 80, 32))

        # At most 4 players
        self.players = {}
        for num in ["1", "2", "3", "4"]:
            if num in g._coors_players.keys():
                h, w = g._coors_players[num]
                x = self.x0 + self.icon_size * w
                y = self.y0 + self.icon_size * h
                player = QtWidgets.QLabel(Dialog)
                player.setGeometry(QtCore.QRect(x, y, self.icon_size,
                                                self.icon_size))
                player.setFrameShape(QtWidgets.QFrame.NoFrame)
                path = "images/char{}.png".format(num)
                player.setPixmap(QtGui.QPixmap(path))
                self.players[num] = player
                icon_player = QtGui.QIcon()
                icon_player.addPixmap(QtGui.QPixmap(path), QtGui.QIcon.Normal,
                                      QtGui.QIcon.On)
                self.comboBox.addItem(icon_player, "player{}".format(num))

        self.turnstiles = {}
        self.holes = []
        self.deep_holes = []
        self.crates = []

        # Travel all the map to construct our game model. For each point,
        # we upload an image to represente it.
        for h in range(g._height):
            for w in range(g._width):
                x = self.x0 + self.icon_size * w
                y = self.y0 + self.icon_size * h
                # Wall
                if g._grid[h][w] == "#":
                    wall = QtWidgets.QLabel(Dialog)
                    wall.setGeometry(QtCore.QRect(x, y, self.icon_size,
                                                  self.icon_size))
                    wall.setFrameShape(QtWidgets.QFrame.NoFrame)
                    wall.setPixmap(QtGui.QPixmap("images/wall.png"))
                # Door
                if g._grid[h][w] == "@":
                    self.door = QtWidgets.QLabel(Dialog)
                    self.door.setGeometry(QtCore.QRect(x, y, self.icon_size,
                                                       self.icon_size))
                    self.door.setFrameShape(QtWidgets.QFrame.NoFrame)
                    self.door.setPixmap(QtGui.QPixmap("images/door.png"))
                    self.door.setObjectName("label_door")
                # turnstile block
                if g._grid[h][w] == "%":
                    turnstile = QtWidgets.QLabel(Dialog)
                    turnstile.setGeometry(QtCore.QRect(x, y, self.icon_size,
                                                       self.icon_size))
                    turnstile.setFrameShape(QtWidgets.QFrame.NoFrame)
                    path = "images/turnstile_block.png"
                    turnstile.setPixmap(QtGui.QPixmap(path))
                    directions = {"U": [-1, 0], "R": [0, 1], "D": [1, 0],
                                  "L": [0, -1]}
                    value = {}
                    # For each turnstile block, it has at most 4 axis
                    for d in directions.keys():
                        delta_h, delta_w = directions[d]
                        x_axis = self.x0 + self.icon_size * (w + delta_w)
                        y_axis = self.y0 + self.icon_size * (h + delta_h)
                        label = QtWidgets.QLabel(Dialog)
                        label.setGeometry(QtCore.QRect(x_axis, y_axis,
                                                       self.icon_size,
                                                       self.icon_size))
                        if g._grid[h + delta_h][w + delta_w] == "'":
                            path_label = "images/turnstile_axis.png"
                        else:
                            path_label = "images/empty.png"
                        label.setPixmap(QtGui.QPixmap(path_label))
                        value[d] = label
                    self.turnstiles[turnstile] = value
                # 1-depth hole
                if g._grid[h][w] == "o":
                    hole = QtWidgets.QLabel(Dialog)
                    hole.setGeometry(QtCore.QRect(x, y, self.icon_size,
                                                  self.icon_size))
                    hole.setFrameShape(QtWidgets.QFrame.NoFrame)
                    hole.setPixmap(QtGui.QPixmap("images/hole.png"))
                    self.holes.append(hole)
                # 2-depth hole
                if g._grid[h][w] == "O":
                    deep_hole = QtWidgets.QLabel(Dialog)
                    deep_hole.setGeometry(QtCore.QRect(x, y, self.icon_size,
                                                       self.icon_size))
                    deep_hole.setFrameShape(QtWidgets.QFrame.NoFrame)
                    deep_hole.setPixmap(QtGui.QPixmap("images/deep_hole.png"))
                    self.deep_holes.append(deep_hole)
                # Crate
                if g._grid[h][w] == "*":
                    crate = QtWidgets.QLabel(Dialog)
                    crate.setGeometry(QtCore.QRect(x, y, self.icon_size,
                                                   self.icon_size))
                    crate.setFrameShape(QtWidgets.QFrame.NoFrame)
                    crate.setPixmap(QtGui.QPixmap("images/crate.png"))
                    self.crates.append(crate)
                # Space
                if g._grid[h][w] == " ":
                    empty = QtWidgets.QLabel(Dialog)
                    empty.setGeometry(QtCore.QRect(x, y, self.icon_size,
                                                   self.icon_size))
                    empty.setFrameShape(QtWidgets.QFrame.NoFrame)
                    empty.setPixmap(QtGui.QPixmap("images/empty.png"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        '''
        Translate above UI to python codes
        '''
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Kwirk"))
        self.pushButton_up.setText(_translate("Dialog", "^"))
        self.pushButton_left.setText(_translate("Dialog", "<"))
        self.pushButton_right.setText(_translate("Dialog", ">"))
        self.pushButton_down.setText(_translate("Dialog", "v"))
