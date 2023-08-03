import pygame
import sys

from constants import *
from game import Game

class Engine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.board = self.game.board
        self.dragger = self.game.dragger
        self.num_of_pos = 0

    def engine_loop(self):
        while True:
            game = self.game
            board = self.board
            dragger = self.dragger
            screen = self.screen

            game.show_bg(screen)
            game.show_last_moves(screen)
            game.show_moves(screen)
            game.show_pieces(screen, board)
            game.show_hover(screen)
            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        print(self.move_generation(2, screen, game, board))
            
            pygame.display.update()

    def move_generation(self, depth, screen, game, board):
        if depth == 0:
            self.num_of_pos += 1

        #num_of_pos = 0
        for piece in board.pieces_on_board:
            #print(self.num_of_pos)
            print(piece.color, piece.pos, end=' ')
            if board.captured_piece:
                print(board.captured_piece.color)
            if piece.color == game.turn:
                board.calc_moves(piece, piece.pos[0], piece.pos[1])
                if piece.moves != []:
                    for move in piece.moves:
                        board.move(piece, move)
                        #print(game.turn)

                        game.next_turn()

                        self.move_generation(depth-1, screen, game, board)

        return self.num_of_pos

engine = Engine()
engine.engine_loop()
        