# MAIN PROGRAM

import pygame
import sys

from constants import *
from game import Game
from tile import Tile
from move import Move
from piece import *
from undo import undo

#from computer import Computer

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()

        # enable player vs computer
        #self.computer = Computer('black')
        #self.computer2 = Computer('white')
    
    def main_loop(self):
        # renaming commonly used objects from other classes for readability purposes
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        '''computer = self.computer
        computer.board = board

        computer2 = self.computer2
        computer2.board = board'''

        # main pygame loop
        while True:
            # draws everything
            game.show_bg(screen)
            game.show_last_moves(screen)
            game.show_moves(screen)
            game.show_pieces(screen, board)
            game.show_hover(screen)
            if dragger.dragging:
                dragger.update_blit(screen)

            # computer movements
            '''if not game.end_game:
                if game.turn == computer.color:
                    self._computer_turn(computer, board, game, screen)
                    game.next_turn()

                elif game.turn == computer2.color:
                    self._computer_turn(computer2, board, game, screen)
                    game.next_turn()'''
                
            for event in pygame.event.get():
                # if you press mouse left-click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)

                    # stores the row and col location of the mouse cursor
                    clicked_row = dragger.mouse_y // TILE_SIZE
                    clicked_col = dragger.mouse_x // TILE_SIZE

                    # checks if the tile hovered by mouse has piece
                    if board.tiles[clicked_row][clicked_col].has_piece:
                        # picks that piece on self.tiles
                        piece = board.tiles[clicked_row][clicked_col].piece

                        # get rids of that bug when the piece is None fsr
                        if piece:
                            # checks that the current player can only select pieces and move
                            if piece.color == game.turn:
                                # calculate valid moves of the piece
                                piece.calc_moves(board)

                                # sets initial x and y pos of the piece
                                dragger.save_initial(event.pos)

                                # drags the selected piece
                                dragger.drag_piece(piece)

                                # updates the screen
                                game.show_bg(screen)
                                game.show_last_moves(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen, board)

                # when the mouse cursor is moving
                elif event.type == pygame.MOUSEMOTION:
                    # stores current row and col locations of mouse cursor
                    motion_row = event.pos[1] // TILE_SIZE
                    motion_col = event.pos[0] // TILE_SIZE
                    
                    if board.in_range(motion_row, motion_col):
                        # displays mouse hovering depending on the location of cursor
                        game.set_hover(motion_col, motion_row)

                        # constantly updates the pos of the dragging object
                        if dragger.dragging: # checks if a piece is currently dragged
                            dragger.update_mouse(event.pos)

                            # updates everything on screen
                            game.show_bg(screen)
                            game.show_last_moves(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen, board)
                            game.show_hover(screen)
                            dragger.update_blit(screen)

                # if you release mouse left-click
                elif event.type == pygame.MOUSEBUTTONUP:
                    # updates the current mouse pos
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)

                        # sets the row and col locations of the tile where you want to put the piece on
                        released_row = dragger.mouse_y // TILE_SIZE
                        released_col = dragger.mouse_x // TILE_SIZE

                        if board.in_range(released_row, released_col):
                            # stores piece being captured (None if dragger.piece only moved)
                            c = board.tiles[released_row][released_col].piece

                            # creates a move object that stores the initial tile pos and the final tile pos
                            # since you just performed a move
                            initial = (dragger.initial_row, dragger.initial_col)
                            final = (released_row, released_col)
                            move = Move(dragger.piece, initial, final, captured_piece = c)

                            # doesnt run when no valid moves are found
                            if board.valid_move(dragger.piece, move):
                                # checks if selected tile has piece (for playing sfx)
                                captured = board.tiles[released_row][released_col].has_piece()

                                # sets en_passant state of the pawn being moved to True
                                board.enable_en_passant(move.piece)

                                # moves piece to the new location
                                board.move(move)

                                # play piece sound (if captured, play move_captured, else play move_sound)
                                game.play_sound(captured)

                                # scans the board if enemy king in check
                                in_check = board.scan_check(move)

                                # saves the moves into board.record_of_moves
                                board.save_moves(move)

                                # removes record of captured piece from the board
                                board.captured_piece = None

                                # declare check mate if enemy cant move and king in check
                                if board.cant_move(dragger.piece.color) and in_check:
                                    game.declare_winner_by_mate()
                                # declare stalemate if enemy cant move
                                elif board.cant_move(dragger.piece.color):
                                    game.declare_stalemate()

                                # updates everything
                                game.show_bg(screen)
                                game.show_last_moves(screen)
                                game.show_pieces(screen, board)

                                # switches turn to other player
                                game.next_turn()

                            else: 
                                dragger.piece.clear_moves()
                    
                    # sets dragger to 'not activated' state, meaning a piece is currently not being dragged
                    dragger.undrag_piece()

                elif event.type == pygame.KEYDOWN:
                    # click 'u' to undo move
                    if event.key == pygame.K_u:
                        # undo won't work when a piece is currently being dragged and when there's nothing to undo
                        if not dragger.dragging and board.record_of_moves != []:
                            # undos the recent move
                            undo(board)

                            # switches back to the previous player
                            game.next_turn()

                    # click 't' to change theme
                    if event.key == pygame.K_t:
                        game.change_theme()

                    # click 'r' to reset game
                    if event.key == pygame.K_r:
                        game.reset()

                        # restart initialization
                        screen = self.screen
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                        record_of_moves = []

                # quit game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    def _computer_turn(self, computer, board, game, screen):
        # computer selects piece
        computer.select_piece(board.tiles)
                
        if computer.piece.color == game.turn:
                    
            board.calc_moves(computer.piece, computer.move_row, computer.move_col, bool=True)

            if computer.piece:
                computer.move_piece()

                captured = computer.tile.has_piece()

                board.move(computer.piece, computer.move)

                board.set_true_en_passant(computer.piece)

                game.play_sound(captured)

                piece = board.tiles[computer.move.final.row][computer.move.final.col].piece
                board.cant_move(piece)
                # declare winner if pieces can't move and king in check
                if board.enemy_cant_move and board.king_check:
                    game.declare_winner_by_mate()
                # declares stalemate if pieces can't move but king isn't in check
                elif board.enemy_cant_move:
                    game.declare_stalemate()

                # updates everything
                game.show_bg(screen)
                game.show_last_moves(screen)
                game.show_pieces(screen, board)


main = Main()
main.main_loop()
