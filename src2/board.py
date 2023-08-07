# CHESS_AI v1.1
# LISTS ALL METHODS FOR BOARD EVENTS

# GUIDE ON VARIABLES:
# self.tiles - serves as the internal representation of chess board of the program
#            - stores 8 lists (rows), which each list storing 8 objs (columns)
# self.last_move - stores the previous move done (move obj: stores initial and final locations)
# *testing* parameter - disables castling feature and en passant capture sound if program foresee future events
#                     for scanning for potential checks (if set to True; if False, move() proceeds normally)
# self._if_check() - checks if king is not check, calc_moves() can add all valid moves as usual,
#                    if king is check or is about to get checked, calc_moves() can only add valid moves to prevent check
# *bool* parameter - if False, enables temp_board to check for any potential checks, if True, adds valid moves if
#                    king isn't check
# self.record_of_moves - a list containing the history of moves being played in the board
# a move in self.record_of_moves - a tuple: (current turn, piece being moved, (initial x pos, initial y pos),
#                                           (final x pos, final y pos), (has the piece captured anything, if so what piece else None))

import copy
import os

from constants import *
from tile import Tile
from piece import *
from fen import fen

class Board():
    def __init__(self):
        self.tiles = [[0 for row in range(ROWS)] for col in range(COLS)]
        self.enemy_cant_move = False # determines if next player can't move anymore
        self.king_check = False # determines if king is in check
        
        self.pieces_on_board = [] # keeps track of alive pieces
        self.record_of_moves = [] # keeps track of moves done

        self.black_king = None # keeps track of black king
        self.white_king = None # keeps track of white king

        # keeps track of castling moves done 
        self.white_castle = None 
        self.black_castle = None

        # 50-move rule tracker
        self.fifty_count = 0

        self.test = False

        # creates board and add pieces to board
        self._create()
        self._add_pieces()

    # moves piece from initial pos to final pos stored in move obj
    def move(self, move, game=None):
        piece = move.piece
        
        # since piece hasnt captured anything yet, it is first initialized to False
        piece.capture = False

        # set coords of move
        initial = move.initial
        final = move.final

        # moves rook if perform castling
        if isinstance(piece, King):
            if piece.check_castle(move): 
                cas_move = castle_move(self, move)

                # save castling move to board
                if piece.color == 'white':
                    self.white_castle = cas_move
                else:
                    self.black_castle = cas_move

        # assigns captured piece to be added to self.record_of_moves
        if move.capture:
            # piece has captured enemy
            piece.capture = True
            # store captured piece
            self.captured_piece = move.captured_piece
            # enemy piece is being captured
            self.captured_piece.captured = True
            # removes captured piece from pieces_on_board
            self.update_pieces_on_board(self.captured_piece)

        # transfers piece in self.tiles to new location in self.tiles
        self.tiles[initial[0]][initial[1]].piece = None
        self.tiles[final[0]][final[1]].piece = piece
        # updates pos of piece
        self.tiles[final[0]][final[1]].piece.update_tile(final[0], final[1])

        # update king trackers
        if isinstance(self.tiles[final[0]][final[1]].piece, King):
            if self.tiles[final[0]][final[1]].piece.color == 'white':
                self.white_king = self.tiles[final[0]][final[1]].piece
            else:
                self.black_king = self.tiles[final[0]][final[1]].piece

        # pawn promotion
        if isinstance(self.tiles[final[0]][final[1]].piece, Pawn):
            pawn = self.tiles[final[0]][final[1]].piece

            # check if pawn promoted
            if pawn.check_promotion():
                '''FIX LATER'''
                #type = game.promotion()
                
                # set pawn promoted to true
                pawn.promoted = True

                # set promoted piece
                promoted_piece = pawn.promotion(self)

                # save promoted pawn
                move.promote = pawn

                # replace pawn with promoted piece
                self.tiles[final[0]][final[1]].piece = move.piece = promoted_piece
                move.piece.update_tile(final[0], final[1])

        # significies that the piece has moved
        if not piece.moved:
            move.from_starting_tile = True
            piece.moved = True

        # clears list of valid moves for selected piece
        piece.clear_moves()

    # filters moves thatll lead to check AND only allow valid moves that will disable a check
    def check(self, move):
        check_state = False
        # MINI MOVE METHOD

        # temporarily stores captured piece (still works even when no piece are captured)
        temp_c = self.tiles[move.final[0]][move.final[1]].piece

        # temporarily executes move
        self.tiles[move.initial[0]][move.initial[1]].piece = None
        self.tiles[move.final[0]][move.final[1]].piece = move.piece
        # updates pos of piece (thisll help with the check calculation)
        self.tiles[move.final[0]][move.final[1]].piece.update_tile(move.final[0], move.final[1])

        # removes captured piece from pieces_on_board
        if temp_c != None:
            temp_c.captured = True
            self.update_pieces_on_board(temp_c)

        # set king
        if move.piece.color == 'white':
            if isinstance(move.piece, King):
                p = move.piece
            else:
                p = self.white_king
        else:
            if isinstance(move.piece, King):
                p = move.piece
            else:
                p = self.black_king

        '''BRO I HOPE TO GOD THIS ALGO WONT GIVE ME A TON OF BUGS
            PLS PLS PLS IT MAGICALLY WORK FOR SOME REASON PLS DONT
            FAIL ME ONEGAI SENPAI UWU'''

        '''HUGE SHOUTOUT btw to rcgldr at stack overflow for giving me an idea on how to approach 
            check scanning more efficiently (you can find their comment at
            https://stackoverflow.com/questions/53924729/is-there-a-way-to-speed-up-a-detect-
            check-method-in-chess/53924967#53924967?newreg=d2a9c4c1bbc84b15a6848b73470bb99b)
        '''
        # scan threats
        if linear_check(self, p):
            check_state = True
        elif diagonal_check(self, p):
            check_state = True
        elif knight_check(self, p):
            check_state = True
        elif king_check(self, p):
            check_state = True

        if check_state:
            p.check = True
        else:
            p.check = False
            
                        
        # MINI MOVE METHOD

        # now that we've done the check calculation, we can bring back the piece to where it should be
        self.tiles[move.initial[0]][move.initial[1]].piece = move.piece
        self.tiles[move.final[0]][move.final[1]].piece = temp_c
        # dont forget to update the pos of the piece otherwise youll get a lot of bugs
        self.tiles[move.initial[0]][move.initial[1]].piece.update_tile(move.initial[0], move.initial[1])

        # reverses piece being captured
        if temp_c:
            temp_c.captured = False
            self.update_pieces_on_board(temp_c)

        return check_state

    # scans board for check after move is executed
    def scan_check(self, move):
        check_state = False
        
        if move.piece.color == 'white':
            king = self.black_king
        else:
            king = self.white_king

        if linear_check(self, king):
            check_state = True
        elif diagonal_check(self, king):
            check_state = True
        elif knight_check(self, king):
            check_state = True
        elif king_check(self, king):
            check_state = True

        if check_state:
            king.check = True
        else:
            king.check = False

        return check_state

    # checks if enemy has no valid moves
    def cant_move(self, color):
        # set enemy color
        enemy_color = 'black' if color == 'white' else 'white'

        # set king
        if enemy_color == 'white':
            king = self.white_king
        else:
            king = self.black_king
        
        # return False if king has valid moves
        king.calc_moves(self)
        if king.valid_moves != []:
            king.clear_moves()
            return False
        king.clear_moves()

        # else check all enemy pieces on board except king
        for enemy in self.pieces_on_board:
            if enemy.color == enemy_color and not isinstance(enemy, King):
                # generate valid moves
                enemy.calc_moves(self)

                # return False if enemy has valid moves
                if enemy.valid_moves != []:
                    enemy.clear_moves()
                    return False
                
                # else clear moves and try again
                enemy.clear_moves()
        
        # return True if no valid moves were generated
        return True

    # checks if the location you're dragging the piece to is a valid square
    def valid_move(self, piece, move):
        return move in piece.valid_moves
   
    # set en_passant state to True to only the pawn that has recently moved
    def enable_en_passant(self, piece):
        # automatically ends function when piece isn't pawn
        if not isinstance(piece, Pawn):
            return
        
        # sets all other pawns in board en_passant state to False
        for p in self.pieces_on_board:
            if isinstance(p, Pawn):
                p.enable_enpas = False

        piece.enable_enpas = True
    
    # saves move done to record_of_moves
    def save_moves(self, move):
        self.record_of_moves.append(move)

    # add pieces on board to self.pieces_on_board
    def update_pieces_on_board(self, piece):
        if piece.captured:
            try:
                self.pieces_on_board.remove(piece)
            except ValueError:
                print(True if piece in self.pieces_on_board else False)
                self.test = True
        else:
            self.pieces_on_board.append(piece)

    # scans the board for any draw possibilities
    def draw(self, game):

        # king vs king draw
        if len(self.pieces_on_board) == 2:
            game.draw_type = 'king vs king'
            return True
        
        # king vs king w/ bishop or knight draw
        elif len(self.pieces_on_board) == 4 or len(self.pieces_on_board) == 3:
            game.draw_type = 'insufficient material'
            
            knights = bishops = []
            
            for piece in self.pieces_on_board:
                if isinstance(piece, Bishop):
                    bishops.append(piece)
                elif isinstance(piece, Knight):
                    knights.append(piece)
                elif isinstance(piece, King):
                    continue
                else:
                    break
            
            if knights != [] or bishops != []:
                if len(knights) == 2:
                    return True
                elif len(bishops) == 2:
                    if bishops[0].color != bishops[1].color:
                        if bishops[0].row % 2 != bishops[1].row % 2:
                            return True
                        else:
                            False
                    else:
                        return False
                else:
                    return True
            
        # declare draw by threefold repetition
        elif len(self.record_of_moves) >= 9:
            game.draw_type = 'threefold repetition'
            if self.record_of_moves[-5].initial == self.record_of_moves[-1].initial:
                if self.record_of_moves[-5].initial == self.record_of_moves[-9].initial:
                    return True

        # keeps track of 50-move rule
        elif self.record_of_moves != []:
            game.draw_type = 'exceeding 50 moves'
            # get recent move
            move = self.record_of_moves[-1]
            # add 1 to fifty count if it's not a pawn move and it didnt capture any piece
            if not isinstance(move.piece, Pawn) or not move.capture:
                self.fifty_count += 1
            else:
                self.fifty_count = 0

            if self.fifty_count == 50:
                return True
                
        return False

    # adds tile objects inside self.tiles
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.tiles[row][col] = Tile(row, col)

    # adds pieces to self.tiles
    def _add_pieces(self):
        # standard pos
        fen_str='rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'

        # check stalemate mechanic
        #fen_str = 'k7/3Q/8/8/8/8/8/8K'

        # check 'disable enpas when pawn is pinned' mechanic
        #fen_str = '8/2pp6/8/KP5r/1R5p2k/8/4P4/8'

        # check king capture promoted pawn protected by knight bug
        #fen_str = '8/4N2Pk1/8/8/8/8/8/K7'

        # check king capture enemy king at corner bug
        #fen_str = 'k7/8/2K6/8/8/8/8/8'

        fen(self, fen_str)
    
    @staticmethod
    def in_range(*args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True
        
# moves the rook in case of a castle
def castle_move(board, move):
    king = move.piece

    if king.q_castle:
        cas_move = king.q_castle
    elif king.k_castle:
        cas_move = king.k_castle
    else:
        '''ERROOOR!'''
        pass

    board.move(cas_move)

    return cas_move

# checks linear directions (n,s,e,w) for king threats
def linear_check(board, king):
    # scans vertical and horizontal directions of king for threats
    for line in [[1,0], [-1,0], [0,1], [0,-1]]:
        # reset initial pos of king
        r = king.row
        c = king.col

        while True:
            # increment every tile for each direction
            r = r + line[0]
            c = c + line[1]

            # ensures that it falls within board
            if board.in_range(r, c):
                # grabs the piece on that tile
                threat = board.tiles[r][c].piece
                # checks if there's actually a piece there (piece = None if the tile is empty)
                if threat != None:
                    # checks if that piece is your opponent
                    if threat.color != king.color:
                        # if that piece is a queen or a rook then theyre checking you
                        if isinstance(threat, Queen) or isinstance(threat, Rook):
                            return True
                        # else they wont threathen you and its safe to say that your king is good
                        else:
                            break
                    # else they arent a threat to your king
                    else:
                        break
            # if you move out of bounds then its time to move on to next direction
            else:
                break
    
    return False

# check diagonal directions for king threats
def diagonal_check(board, king):
    # the same logic as w/ vertical & horizontal directions
    for line in [[1,1], [-1,1], [1,-1], [-1,-1]]:
        r = king.row
        c = king.col

        while True:
            r = r + line[0]
            c = c + line[1]

            if board.in_range(r, c):
                threat = board.tiles[r][c].piece
                if threat != None:
                    if threat.color != king.color:
                        # this time it checks whether the potential threat is a queen or a bishop
                        # and if so yes your king is in check
                        if isinstance(threat, Queen) or isinstance(threat, Bishop):
                            return True
                        # since this checks for potential threats diagonally, might as well check
                        # for any pawn and king threats since they can capture diagonally
                        # the abs(r - p.row) == 1 is there to check when enemy pawn / king is protecting
                        # a tile within the king's range of movement
                        elif (isinstance(threat, Pawn) or isinstance(threat, King)) and abs(r - king.row) == 1:
                            return True
                        # else then that piece wont threaten you so ur good
                        else:
                            break
                    else:
                        break
            else:
                break
                
    return False

# check if knights threaten king
def knight_check(board, king):
    # looks for enemy knights on piecs_on_board
    for knight in board.pieces_on_board:
        if isinstance(knight, Knight) and knight.color != king.color:
            # basically calc_moves of knight but much faster coz it gets rid of the move initialization
            # thing and this code eliminates bugs than using calc_moves
            # which causes a bug (your knight fsr have normal valid moves when king in check but when you 
            # press them again then suddenly they have the valid moves when king in check, yeah weird)
            for target in [(-2,-1), (2,-1), (-2,1), (2,1), (-1,-2), (1,-2), (-1,2), (1,2)]:
                r = knight.row + target[0]
                c = knight.col + target[1]

                # if target square contains your king then your king in check
                if board.in_range(r, c):
                    if board.tiles[r][c].piece == king:
                        return True
                    
    return False

# prevents kings from going near each other
def king_check(board, king):
    # scans range of your king
    for range in [(1,1), (-1,1), (1,-1), (-1,-1), (1,0), (0,1), (-1,0), (0,-1)]:
        r = king.row + range[0]
        c = king.col + range[1]

        if board.in_range(r, c):
            k = board.tiles[r][c].piece
            if k:
                # if enemy king is within your king range then your king cant go there
                # thus check_state = True
                if isinstance(k, King) and king.color != k.color:
                    return True
        else:
            continue
    
    return False

