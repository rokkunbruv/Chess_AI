import pygame
import sys

from constants import *
from game import Game

class Engine:
    def __init__(self):
        self.num_of_pos = 0
        pass
        

    def move_generation(self, depth, main, screen, game, board):
        if depth == 0:
            game.reset()
            screen = main.screen
            game = main.game
            board = main.game.board
            
            return 1

        #num_of_pos = 0
        for piece in board.pieces_on_board:
            #print(self.num_of_pos)
            #print(piece.color, piece.pos, end=' ')
            #if board.captured_piece:
            #    print(board.captured_piece.color)
            if piece.color == game.turn:
                piece.calc_moves(board)
                if piece.valid_moves != []:
                    for move in piece.valid_moves:
                        board.move(move)

                        game.next_turn()

                        self.num_of_pos += self.move_generation(depth-1, main, screen, game, board)

        return self.num_of_pos

        