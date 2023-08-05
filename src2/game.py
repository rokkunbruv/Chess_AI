# CONTAINS ALL METHODS FOR RENDERING EVENTS TO SCREEN

import pygame
from constants import *
from board import Board
from dragger import Dragger
from config import Config
from tile import Tile

class Game:
    def __init__(self):
        self.turn = 'white' # white first to move
        self.hover_tile = None
        self.winner = None
        self.loser = None
        self.end_game = False

        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    # draws chess board
    def show_bg(self, surface):
        theme = self.config.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark
                
                pygame.draw.rect(surface, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

                # render rank coordinates
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light

                    label = self.config.font.render(str(ROWS-row), 1, color)
                    label_pos = (5, 5 + row * TILE_SIZE)

                    surface.blit(label, label_pos)

                # render file coordinates
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light

                    label = self.config.font.render(Tile.get_alphacol(col), 1, color)
                    label_pos = (col * TILE_SIZE + TILE_SIZE - 20, HEIGHT - 20)

                    surface.blit(label, label_pos)

    # draws pieces on board
    def show_pieces(self, surface, board):
        for piece in board.pieces_on_board:
            if piece is not self.dragger.piece:
                piece.set_image(size = PIECE_SIZE)

                image = pygame.image.load(piece.image)
                image = pygame.transform.scale(image, (PIECE_SIZE, PIECE_SIZE))

                image_center = piece.col * TILE_SIZE + TILE_SIZE // 2, piece.row * TILE_SIZE + TILE_SIZE // 2
                piece.image_rect = image.get_rect(center=image_center)
                surface.blit(image, piece.image_rect)

    # colors tiles with red to show valid moves that the piece can do
    def show_moves(self, surface):
        # checks if the piece is being dragged
        theme = self.config.theme
        
        if self.dragger.dragging:
            piece = self.dragger.piece

            for move in piece.valid_moves:
                color = theme.moves.light if (move.final[0] + move.final[1]) % 2 == 0 else theme.moves.dark
                
                pygame.draw.rect(surface, color, [move.final[1] * TILE_SIZE, move.final[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE])

    # shows how the piece moves from previous to new location
    def show_last_moves(self, surface):
        theme = self.config.theme

        if self.board.record_of_moves != []:
            last_move = self.board.record_of_moves[-1]

            initial = last_move.initial
            final = last_move.final

            for pos in [initial, final]:
                color = theme.trace.light if (pos[0] + pos[1]) % 2 == 0 else theme.trace.dark

                pygame.draw.rect(surface, color, [pos[1] * TILE_SIZE, pos[0] * TILE_SIZE, TILE_SIZE, TILE_SIZE])

    # display hover tile
    def show_hover(self, surface):
        theme = self.config.theme

        if self.hover_tile:
            color = theme.hover

            pygame.draw.rect(surface, color, [self.hover_tile.col * TILE_SIZE, self.hover_tile.row * TILE_SIZE, TILE_SIZE, TILE_SIZE], width=3)

    '''FIX LATER'''
    def promotion(self):
        piece = None
        loop = False

        '''TEMPORARY COZ IDK HOW PYGAME WORKS'''
        # select piece
        print('Choose what piece to promote:')
        print("'Q' - Queen        'R' - Rook")
        print("'B' - Bishop       'N' - Knight")
        print("'X' - Cancel")

        return piece

    # switches player turn
    def next_turn(self):
        self.turn = 'white' if self.turn == 'black' else 'black'

    # declare winner through check mate
    def declare_winner_by_mate(self):
        self.winner = self.turn

        self.loser = 'white' if self.winner == 'black' else 'black'

        self.end_game = True

        print('The winner is', self.winner)
        print('The loser is', self.loser)
        print('Press r to restart')

    # declare stalemate
    def declare_stalemate(self):
        self.end_game = True

        print('Stalemate')

    # set hovered tile to be hover tile
    def set_hover(self, row, col):
        self.hover_tile = self.board.tiles[col][row]

    # switch between available themes
    def change_theme(self):
        self.config.change_theme()

    # play piece movement sound
    def play_sound(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()

    # reset game initialization
    def reset(self):
        self.__init__()

