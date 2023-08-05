# STORES ALL METHODS FOR COMPUTER PLAYER

import random

from board import Board
from constants import *

class Computer:
    def __init__(self, color):
        self.color = color
        self.move = None
        self.piece = None
        
    # sets move of piece
    def set_move(self, board):
        self._random_select(board)

    # checks if selected piece has valid moves
    def _if_can_move(self, piece, board):
        piece.calc_moves(board)

        if piece.valid_moves == []:
            can_move = False
        else:
            can_move = True
        
        return can_move
    
    '''RANDOM (easy difficulty???)'''
    # randomly selects a piece (and a move at a same time) on the board
    def _random_select(self, board):
        while True:
            # randomly selects row and col
            row = random.randrange(0, ROWS)
            col = random.randrange(0, COLS)

            # select piece
            self.piece = board.tiles[row][col].piece

            # if piece exists and it's the same color
            if self.piece != None and self.piece.color == self.color:
                # randomly selects a move if can move
                if self._if_can_move(self.piece, board):
                    self._random_move()
                    self.piece.clear_moves()
                    break
                # else clear moves
                else:
                    self.piece.clear_moves()
            # else continue randomly selecting piece
            else:
                continue

    # randomly selects a valid move from the selected piece
    def _random_move(self):
        length = len(self.piece.valid_moves)
        index = random.randrange(0, length)

        self.move = self.piece.valid_moves[index]