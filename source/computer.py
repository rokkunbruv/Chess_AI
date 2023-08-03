# STORES ALL METHODS FOR COMPUTER PLAYER

import random

from board import Board
from constants import *

class Computer:
    def __init__(self, color):
        self.color = color
        self.move = None
        self.piece = None
        self.board = None
        self.tile = None
        self.move_row = 0
        self.move_col = 0
        
    def select_piece(self, board):
        self._random_select(board)

    def move_piece(self):
        self._random_move()

    def _if_can_move(self, piece, row, col):
        self.board.calc_moves(piece, row, col, bool=True)

        if piece.moves == []:
            return False
        else:
            return True
    
    '''RANDOM (easy difficulty???)'''
    # randomly selects a piece on the board
    def _random_select(self, board):
        while True:
            row = random.randrange(0, ROWS)
            col = random.randrange(0, COLS)

            self.tile = board[row][col]

            if self.tile.has_piece() and self.tile.has_friend(self.color):
                if self._if_can_move(self.tile.piece, row, col):
                    self.move_row = row
                    self.move_col = col
                    break
            else:
                continue

        self.piece = self.tile.piece

    # randomly selects a valid move from the selected piece
    def _random_move(self):
        length = len(self.piece.moves)
        index = random.randrange(0, length)

        self.move = self.piece.moves[index]