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
        
        self.pieces_on_board = []

        self.record_of_moves = []

        self.black_king = None
        self.white_king = None

        # creates board and add pieces to board
        self._create()
        self._add_pieces()

    # moves piece from initial pos to final pos stored in move obj
    def move(self, move):
        piece = move.piece
        
        # since piece hasnt captured anything yet, it is first initialized to False
        piece.capture = False

        # set coords of move
        initial = move.initial
        final = move.final

        '''add piece.castle if undo castling is buggy'''
        if isinstance(piece, King):
            if piece.check_castle(move): 
                castle_move(self, move)

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
        if temp_c:
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
            print('h')
            check_state = True
        elif knight_check(self, king):
            check_state = True
        elif king_check(self, king):
            check_state = True

        if check_state:
            king.check = True
        else:
            king.check = False

        print(check_state)
        return check_state

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

    # checks for potential stalemate / checkmate
    def cant_move(self, piece):
        temp_board = copy.deepcopy(self)
        
        # checks if the enemy can still move (if not, checkmate = True; else, False)
        for p in temp_board.pieces_on_board:
            if p.color != piece.color:
                temp_board.calc_moves(p, p.pos[0], p.pos[1], bool=True)

                for move in p.moves:
                    if temp_board.valid_move(p, move):
                        self.enemy_cant_move = False
                        return
        self.enemy_cant_move = True
                
       # saves moves made to record_of_moves
    
    # saves move done to record_of_moves
    def save_moves(self, move):
        self.record_of_moves.append(move)

    # add pieces on board to self.pieces_on_board
    def update_pieces_on_board(self, piece):
        if piece.captured:
            self.pieces_on_board.remove(piece)
        else:
            self.pieces_on_board.append(piece)

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

        fen(self, fen_str)

    # add valid moves to piece.moves if king isn't in check
    def _if_check(self, piece, move, bool, rook=None, rook_move=None):
        # add castling moves to valid moves
        if rook and rook_move:
            if bool:
                if not self.in_check(piece, move) and not self.in_check(rook, rook_move):
                    rook.add_moves(rook_move)
                    piece.add_moves(move)
                else:
                    self.king_check = True
                    # disables king to castle when get checked
                    piece.can_castle = False
            else:
                rook.add_moves(rook_move)
                piece.add_moves(move)
        # add all other normal moves to valid moves
        else:
            if bool:
                # add moves if king isn't check
                if not self.in_check(piece, move):
                    piece.add_moves(move)
                else:
                    self.king_check = True

                    # disables king to castle when get checked
                    if isinstance(piece, King):
                        piece.can_castle = False
            # checks for any potential checks
            else:
                piece.add_moves(move)

    # see if enemy will get checked because of that move (for checkmate purposes)
    def _see_if_check_enemy(self, piece, move):
        for p in self.pieces_on_board:
            if p.color == piece.color:
                self.calc_moves(piece, p.pos[0], p.pos[1], bool=False)

                for move in piece.moves:
                    if isinstance(move.final.piece, King):
                        return True
        return False
    
    # checks whether the piece is already on initial location when undo
    def _reset_moved(self, move):
        # automatically set reset_moved to False if record_of_moves is empty
        if self.record_of_moves == []:
            return False
        # checks the first instance of the piece, if the move of the first instance recorded on record_of_moves
        # is same as move, returns False
        if move:
            for m in self.record_of_moves:
                if m[1] == move[1]:
                    return False
        else: return True
    
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
        board.move(king.q_castle)
    elif king.k_castle:
        board.move(king.k_castle)
    else:
        '''ERROOOR!'''
        pass

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
                else:
                    break
                    
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
            break
    
    return False

