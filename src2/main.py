# MAIN PROGRAM

import pygame
import sys

from constants import *
from game import Game
from move import Move
from piece import *
from undo import undo

from computer import Computer

from engine import Engine

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
    
    def main_loop(self):
        # renaming commonly used objects from other classes for readability purposes
        screen = self.screen
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        # initialize Computers
        computer_w = Computer('white')
        computer_b = Computer('black')
        # True to enable computer vs computer
        com_vs_com = False
        count = 0

        # initialize Engine
        engine = Engine()
        # True to enable engine
        enable_en = False
        

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

            if len(board.pieces_on_board) == 3:
                com_vs_com = False
            if board.test == True:
                com_vs_com = False

            # computer movements
            if com_vs_com:
                if not game.end_game:
                    if game.turn == computer_w.color:
                        self._computer_turn(computer_w, board, game, screen, count)
                        count += 1
                    elif game.turn == computer_b.color:
                        self._computer_turn(computer_b, board, game, screen, count)
                        count += 1

            # engine calculation
            if enable_en:
                num = engine.move_generation(2, self, screen, game, board)
                print(num)
                enable_en = False
                
            for event in pygame.event.get():
                # PLAYER CAN'T MOVE IF COMPUTER / ENGINE IS STILL OPERATING
                
                # if you press mouse left-click
                # cannot click piece if computer vs computer is still running, engine calculation is still ongoing
                # and game has officially ended
                if event.type == pygame.MOUSEBUTTONDOWN and not com_vs_com and not enable_en and not game.end_game:
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
                elif event.type == pygame.MOUSEMOTION and not com_vs_com and not enable_en:
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
                elif event.type == pygame.MOUSEBUTTONUP and not com_vs_com and not enable_en:
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
                                board.move(move, game)

                                # play piece sound (if captured, play move_captured, else play move_sound)
                                game.play_sound(captured)

                                # scans the board if enemy king in check
                                in_check = board.scan_check(move)

                                # saves the moves into board.record_of_moves
                                board.save_moves(move)

                                # removes record of captured piece from the board
                                board.captured_piece = None

                                # declares check mate if enemy cant move and king in check
                                if board.cant_move(dragger.piece.color) and in_check:
                                    game.declare_winner_by_mate()
                                # declares stalemate if enemy cant move
                                elif board.cant_move(dragger.piece.color):
                                    game.declare_stalemate()
                                # declares draw
                                elif board.draw():
                                    game.declare_draw()

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
                    if event.key == pygame.K_u and not com_vs_com and not enable_en:
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
                        com_vs_com = False
                        count = 0

                    # click 'c' to enable computer vs computer
                    # turn off computer vs computer & restart by pressing 'c' again

                    # only enable computer vs computer if player didn't touch
                    # any pieces on board
                    if event.key == pygame.K_c and board.record_of_moves == [] and not enable_en:
                        # restart if computer vs computer is on
                        if com_vs_com:
                            game.reset()

                            # restart initialization
                            screen = self.screen
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                            com_vs_com = False
                        # else enable it
                        else:
                            com_vs_com = True

                    # click 'e' to execute engine
                    if event.key == pygame.K_e and board.record_of_moves == [] and not com_vs_com:
                        if enable_en:
                            game.reset()

                            # restart initialization
                            screen = self.screen
                            game = self.game
                            board = self.game.board
                            dragger = self.game.dragger
                            enable_en = False
                        else:
                            enable_en = True

                # quit game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

    # allows computer to perform moves in board
    def _computer_turn(self, computer, board, game, screen, count):
        # computer selects piece
        computer.set_move(board)

        # set captured piece if it exists
        captured = computer.move.captured_piece

        # sets en_passant state of the pawn being moved to True
        board.enable_en_passant(computer.move.piece)

        # moves piece to the new location
        board.move(computer.move, game)

        # play piece sound (if captured, play move_captured, else play move_sound)
        game.play_sound(captured)

        # scans the board if enemy king in check
        in_check = board.scan_check(computer.move)

        # saves the moves into board.record_of_moves
        board.save_moves(computer.move)

        # removes record of captured piece from the board
        board.captured_piece = None

        # declare check mate if enemy cant move and king in check
        if board.cant_move(computer.move.piece.color) and in_check:
            game.declare_winner_by_mate()
            print(count)
        # declare stalemate if enemy cant move
        elif board.cant_move(computer.move.piece.color):
            game.declare_stalemate()
            print(count)
        # declare draw if only kings on board
        elif board.draw(game):
            game.declare_draw()
            print(count)

        # updates everything
        game.show_bg(screen)
        game.show_last_moves(screen)
        game.show_pieces(screen, board)

        game.next_turn()


main = Main()
main.main_loop()
