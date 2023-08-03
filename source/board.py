# LISTS ALL METHODS FOR PIECE MOVEMENT IN BOARD

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
from move import Move
from sound import Sound

class Board():
    def __init__(self):
        self.tiles = [[0 for row in range(ROWS)] for col in range(COLS)]
        self.last_move = None
        self.enemy_cant_move = False # determines if next player can't move anymore
        self.king_check = False # determines if king is in check
        self.captured_piece = None # stores the piece being captured for self.undo()
        self.record_of_moves = []
        self.pieces_on_board = []

        # creates board and add pieces to board
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    # moves piece from initial pos to final pos stored in move obj
    def move(self, piece, move, testing=False):
        # since piece hasnt captured anything yet, it is first initialized to False
        piece.capture = False
        
        initial = move.initial
        final = move.final

        # checks if enemy pawn moved two tiles from origin to enable en passant
        en_passant_empty = self.tiles[final.row][final.col].is_empty()

        # assigns captured piece to be added to self.record_of_moves
        if self.tiles[final.row][final.col].has_piece():
            piece.capture = True
            self.captured_piece = self.tiles[final.row][final.col].piece
            self.captured_piece.captured = True
            self.update_pieces_on_board(self.captured_piece)

        # transfers piece in self.tiles to new location in self.tiles
        self.tiles[initial.row][initial.col].piece = None
        self.tiles[final.row][final.col].piece = piece
        self.tiles[final.row][final.col].piece.update_pos(final.col, final.row)

        # contains special pawn moves
        if isinstance(piece, Pawn):
            # checks for en passant
            diff = final.col - initial.col

            # ensures that enemy pawn has moved two tiles
            if diff != 0 and en_passant_empty:
                # adds pawn being captured by en passant to self.record_of_moves as captured_piece
                self.captured_piece = self.tiles[initial.row][initial.col + diff].piece
                self.captured_piece.captured_by_en_pass = True
                self.captured_piece.captured = True
                piece.capture = True

                self.update_pieces_on_board(self.captured_piece)
                
                # en passant capture
                self.tiles[initial.row][initial.col + diff].piece = None
                self.tiles[final.row][final.col].piece = piece
                self.tiles[final.row][final.col].piece.update_pos(final.col, final.row)

                ''''''
                if not testing:
                    sound = Sound(os.path.join('assets/sounds/capture.wav'))
                    sound.play()
            else:
                # else check for promotion
                self.check_promotion(piece)

        # checks for king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                difference = final.col - initial.col
                ''''''
                rook = piece.left_rook if (difference < 0) else piece.right_rook
                ''''''
                self.save_moves(rook, rook.moves[-1])

                self.move(rook, rook.moves[-1])

                piece.can_castle = False

        # significies that the piece has moved
        piece.moved = True
        
        # checks if enemy king is in check (returns True if enemy king in check; else, False)
        self.king_check = self._see_if_check_enemy(piece, move)

        # clears list of valid moves for selected piece
        piece.clear_moves()

        # set new move done to be previous move
        self.last_move = move

    # checks if the location you're dragging the piece to is a valid square
    def valid_move(self, piece, move):
        return move in piece.moves

    # enable pawn promotion (queen only)
    def check_promotion(self, piece):
        # checks if pawns have reached to other side of board
        if piece.pos[1] == 0 or piece.pos[1] == 7:
            # change pawn to queen
            p = Queen(piece.color, piece.pos[0], piece.pos[1])
            p.promoted = True

            self.update_pieces_on_board(p)

    # check for castling
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
    
    # set en_passant state to True to only the pawn that has recently moved
    def set_true_en_passant(self, piece):

        # automatically ends function when piece isn't pawn
        if not isinstance(piece, Pawn):
            return
        
        # sets all other pawns in board en_passant state to False
        for p in self.pieces_on_board:
            if isinstance(p, Pawn):
                p.en_passant = False

        piece.en_passant = True

    def can_i_do_en_passant(self):
        if self.record_of_moves == []:
            return False
        
        move = self.record_of_moves[-1]
        diff = abs(move[3][1] - move[2][1])

        return True if diff == 2 else False

    # checks for check
    '''fix this'''
    def in_check(self, piece, move):
        # creates temporary piece and board to foresee future events
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)

        # scans for potential checks by looking into future
        temp_board.move(temp_piece, move, testing=True)

        # checks all rival pieces on board if they can cause checks
        for p in temp_board.pieces_on_board:
            if p.color != piece.color:        
                temp_board.calc_moves(p, p.pos[0], p.pos[1], bool=False)

                for m in p.moves:
                    if isinstance(m.final.piece, King):
                        return True
                    
        return False

        '''for row in range(ROWS):
            for col in range(COLS):
                # checks for rival piece
                if temp_board.tiles[row][col].has_rival(piece.color):
                    p = temp_board.tiles[row][col].piece

                    # calculate valid moves of rival piece
                    temp_board.calc_moves(p, row, col, bool=False)

                    # if one of valid moves of rival piece can capture King, king is in check
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
        
        # return False if no rival piece can cause check
        return False'''

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

        '''for row in range(ROWS):
            for col in range(COLS):
                if temp_board.tiles[row][col].has_rival(piece.color):
                    p = temp_board.tiles[row][col].piece

                    temp_board.calc_moves(p, row, col, bool=True)

                    for move in p.moves:
                        if temp_board.valid_move(p, move):
                            self.enemy_cant_move = False
                            return

        self.enemy_cant_move = True'''
                
    # main logic of valid move calculations
    def calc_moves(self, piece, row, col, bool=True):
        # includes en passant logic
        def pawn_moves():
            # checks if pawn has moved so that it can move two tiles
            steps = 1 if piece.moved else 2
            
            # movement
            start = row + piece.direction
            end = row + (piece.direction * (1 + steps))
            for move_row in range(start, end, piece.direction):
                if Tile.in_range(move_row):
                    if self.tiles[move_row][col].is_empty():
                        initial = Tile(row, col)
                        final = Tile(move_row, col)

                        move = Move(initial, final)
                        
                        self._if_check(piece, move, bool)
                    else:
                        break
                else:
                    break

            # capture
            possible_move_row = row + piece.direction
            possible_move_cols = [col-1, col+1]

            for possible_move_col in possible_move_cols:
                if Tile.in_range(possible_move_row, possible_move_col):
                    if self.tiles[possible_move_row][possible_move_col].has_rival(piece.color):
                        final_piece = self.tiles[possible_move_row][possible_move_col].piece
                        
                        initial = Tile(row, col)
                        final = Tile(possible_move_row, possible_move_col, final_piece)

                        move = Move(initial, final)

                        self._if_check(piece, move, bool)

            # en passant logic
            if self.can_i_do_en_passant():
                r = 3 if piece.color == 'white' else 4
                final_r = 2 if piece.color == 'white' else 5

                for c in (col-1, col+1):
                    if Tile.in_range(c) and row == r:   
                        if self.tiles[row][c].has_rival(piece.color):
                            p = self.tiles[row][c].piece

                            if isinstance(p, Pawn):
                                if p.en_passant:
                                    initial = Tile(row, col)
                                    final = Tile(final_r, c, p)

                                    move = Move(initial, final)

                                    self._if_check(piece, move, bool)
 
        def knight_moves():
            # possible knight moves
            possible_moves = [
                            (row-2,col+1),
                            (row-2,col-1),
                            (row+2,col+1),
                            (row+2,col-1), 
                            (row-1,col+2),
                            (row-1,col-2),
                            (row+1,col+2),
                            (row+1,col-2)
                            ]
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Tile.in_range(possible_move_row, possible_move_col):
                    if self.tiles[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        final_piece = self.tiles[possible_move_row][possible_move_col].piece
                        
                        initial = Tile(row, col)
                        final = Tile(possible_move_row, possible_move_col, final_piece)

                        move = Move(initial, final)
                        
                        self._if_check(piece, move, bool)

        # for rook, bishop, and queen
        def linear_moves(increments):
            for increment in increments:
                row_increment, col_increment = increment

                possible_move_row = row + row_increment
                possible_move_col = col + col_increment

                while True:
                    if Tile.in_range(possible_move_row, possible_move_col):
                        final_piece = self.tiles[possible_move_row][possible_move_col].piece
                        
                        initial = Tile(row, col)
                        final = Tile(possible_move_row, possible_move_col, final_piece)

                        move = Move(initial, final)

                        if self.tiles[possible_move_row][possible_move_col].is_empty():
                            self._if_check(piece, move, bool)

                        elif self.tiles[possible_move_row][possible_move_col].has_rival(piece.color):
                            self._if_check(piece, move, bool)

                            break

                        elif self.tiles[possible_move_row][possible_move_col].has_friend(piece.color):
                            break

                    else:
                        break

                    possible_move_row = possible_move_row + row_increment
                    possible_move_col = possible_move_col + col_increment
         
        # includes castling logic
        def king_moves():
            possible_moves = [
                            (row-1,col), # up
                            (row+1,col), # down
                            (row,col-1), # left
                            (row,col+1), # right
                            (row-1,col-1), # up left
                            (row+1,col-1), # down left
                            (row-1,col+1), # up right
                            (row+1,col+1) # down right
                            ]
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move

                if Tile.in_range(possible_move_row, possible_move_col):
                    if self.tiles[possible_move_row][possible_move_col].is_empty_or_rival(piece.color):
                        initial = Tile(row, col)
                        final = Tile(possible_move_row, possible_move_col)

                        move = Move(initial, final)

                        self._if_check(piece, move, bool)

            '''y'know, i can make this more modular, but i'll stick to this one cos it kept
               on screaming errors'''
            # castling logic
            if not piece.moved and piece.can_castle:
                # queen side castling (long castle)
                left_rook = self.tiles[row][0].piece
                if isinstance(left_rook, Rook) and not left_rook.moved:
                    for c in range(1, 4):
                        # castling is not possible because there are pieces in between ?
                        if self.tiles[row][c].has_piece():
                            break

                        if c == 3:
                            # adds left rook to king
                            piece.left_rook = left_rook

                            # rook move
                            initial = Tile(row, 0)
                            final = Tile(row, 3)
                            moveR = Move(initial, final)

                            # king move
                            initial = Tile(row, col)
                            final = Tile(row, 2)
                            moveK = Move(initial, final)

                            # check potencial checks
                            self._if_check(piece, moveK, bool, left_rook, moveR)

                # king castling (short castle)
                right_rook = self.tiles[row][7].piece
                if isinstance(right_rook, Rook) and not right_rook.moved:
                    for c in range(5, 7):
                        # castling is not possible because there are pieces in between ?
                        if self.tiles[row][c].has_piece():
                             break

                        if c == 6:
                            # adds right rook to king
                            piece.right_rook = right_rook

                            # rook move
                            initial = Tile(row, 7)
                            final = Tile(row, 5)
                            moveR = Move(initial, final)

                            # king move
                            initial = Tile(row, col)
                            final = Tile(row, 6)
                            moveK = Move(initial, final)

                            # check potencial checks
                            self._if_check(piece, moveK, bool, right_rook, moveR)
                                    
        # checks the type of piece and execute move calculation for that piecce
        if isinstance(piece, Pawn): 
            pawn_moves()
        elif isinstance(piece, Knight): 
            knight_moves()
        elif isinstance(piece, Bishop): 
            linear_moves([(-1,1), (-1,-1), (1,1), (1,-1)])
        elif isinstance(piece, Rook): 
            linear_moves([(-1,0), (1,0), (0,-1), (0,1)])
        elif isinstance(piece, Queen): 
            linear_moves([(-1,1), (-1,-1), (1,1), (1,-1),
                         (-1,0), (1,0), (0,-1), (0,1)])
        elif isinstance(piece, King): 
            king_moves()

    # saves moves made to record_of_moves
    def save_moves(self, piece, move,):
        tuple = (piece.color, # turn
                piece, # piece being moved
                (move.initial.col, move.initial.row), # initial tile
                (move.final.col, move.final.row), # final tile
                (piece.capture, # True if piece gets captured, else False
                self.captured_piece) # None in default; if piece.captured = True, stores enemy piece being captured
                )
        
        self.record_of_moves.append(tuple)

    # add pieces on board to self.pieces_on_board
    def update_pieces_on_board(self, piece):
        if piece.captured:
            self.pieces_on_board.remove(piece)
        else:
            self.pieces_on_board.append(piece)

    # undos the previous move done tangina mo kys sana youre one of the people who died in the oceangate submarine tangina mo
    # WARNING: VERY CRYPTIC. PROCEED WITH CAUTION
    def undo(self):
        move = self.record_of_moves[-1] # selects the last element of self.record_of_moves
        piece = move[1] # select piece
        initial = move[3] # selects initial move tuple
        final = move[2] # selects final move tuple

        en_passant_offset = 0 # this is for adding the pawn being captured by en passant back to board

        captured_piece = move[4][1] # selects captured piece
        revived_piece = None

        # undoes pawn promotion
        if isinstance(piece, Pawn):
            if piece.promoted:
                piece.promoted = False
                self.tiles[initial[1]][initial[0]].piece.captured = True
                self.update_pieces_on_board(self.tiles[initial[1]][initial[0]].piece)

        # transfers piece back to initial tile
        self.tiles[initial[1]][initial[0]].piece = None
        self.tiles[final[1]][final[0]].piece = piece
        self.tiles[final[1]][final[0]].piece.update_pos(final[0], final[1])

        # enables en passant when player didn't capture enemy pawn through en passant on prev move
        if len(self.record_of_moves) >= 2:
            if isinstance(self.record_of_moves[-2][1], Pawn):
                self.record_of_moves[-2][1].en_passant = True

        # brings back captured piece to board
        if move[4][0]:
            # brings back captured pawn by en passant to board
            if isinstance(captured_piece, Pawn) and isinstance(piece, Pawn):
                if piece.en_passant and captured_piece.captured_by_en_pass:
                    en_passant_offset = 1 if piece.color == 'white' else -1
                    captured_piece.en_passant = True
            
            # brings back captured piece to board
            self.tiles[initial[1]+en_passant_offset][initial[0]].piece = captured_piece
            revived_piece = self.tiles[initial[1]+en_passant_offset][initial[0]].piece
            revived_piece.update_pos(initial[0], initial[1]+en_passant_offset)

            revived_piece.captured = False
            self.update_pieces_on_board(revived_piece)

            # piece is now not captured by en pass
            if isinstance(revived_piece, Pawn):
                revived_piece.captured_by_en_pass = False

            # some reassignment to prevent some bugs
            piece.capture = False
            self.captured_piece = None

            # prevents that bug that disables castling when enemy captures rook, then I select the king, then
            # undoes it, which disables me to castle
            king = self.tiles[7][4].piece if captured_piece.color == 'white' else self.tiles[0][4]
            for y in (0, 7):
                x = 7 if captured_piece.color == 'white' else 0
                if isinstance(captured_piece, Rook) and self.tiles[x][y].piece == captured_piece:
                    king.can_castle = True

        # undoes castling
        if len(self.record_of_moves) >= 2: # doesn't throw error when len(self.record_of_moves) less than or eq to 2
            rook_move = self.record_of_moves[-2]
            i = rook_move[3]
            f = rook_move[2]

            if isinstance(piece, King) and rook_move[0] == piece.color:
                self.tiles[i[1]][i[0]].piece = None
                self.tiles[f[1]][f[0]].piece = rook_move[1]
                self.tiles[f[1]][f[0]].piece.update_pos(f[0], f[1])

                self.tiles[f[1]][f[0]].piece.moved = False

                self.tiles[final[1]][final[0]].piece.moves = []

                self.tiles[final[1]][final[0]].piece.can_castle = True

                del self.record_of_moves[-2]

        # sets piece.moved = False if piece went back to original location
        if not self._reset_moved(move):
            if isinstance(self.tiles[final[1]][final[0]].piece, Pawn):
                starting_row = 1 if self.tiles[final[1]][final[0]].piece.color == 'black' else 6
                if self.tiles[final[1]][final[0]].piece == self.tiles[starting_row][final[0]].piece:
                    self.tiles[final[1]][final[0]].piece.moved = False
            elif revived_piece:
                revived_piece.moved = False
            else:
                self.tiles[final[1]][final[0]].piece.moved = False

        # clears valid moves of undone piece
        self.tiles[final[1]][final[0]].piece.moves = []

        # remove previous move from self.record_of_moves
        del self.record_of_moves[-1]

    # adds tile objects inside self.tiles
    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.tiles[row][col] = Tile(row, col)

    # adds pieces to self.tiles
    def _add_pieces(self, color):
        '''# in case if you want to check if your stalemate logic works
        self.tiles[0][0] = Tile(0, 0, King('black'))
        self.tiles[7][7] = Tile(7, 7, King('white'))
        self.tiles[1][3] = Tile(1, 3, Queen('white'))'''

        '''# simulate pinned en passant
        self.tiles[1][2] = Tile(1, 2, Pawn('black'))
        self.tiles[2][3] = Tile(2, 3, Pawn('black'))
        self.tiles[3][0] = Tile(3, 0, King('white'))
        self.tiles[3][1] = Tile(3, 1, Pawn('white'))
        self.tiles[3][7] = Tile(3, 7, Rook('black'))
        self.tiles[4][1] = Tile(4, 1, Rook('white'))
        self.tiles[4][5] = Tile(4, 5, Pawn('black'))
        self.tiles[4][7] = Tile(4, 7, King('black'))
        self.tiles[6][4] = Tile(6, 4, Pawn('white'))
        self.tiles[3][1].piece.moved = True'''

        # add all pawns
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        for col in range(COLS):
            self.tiles[row_pawn][col] = Tile(row_pawn, col, Pawn(color, col, row_pawn))
            self.update_pieces_on_board(self.tiles[row_pawn][col].piece)

        # add all knights
        self.tiles[row_other][1] = Tile(row_other, 1, Knight(color, 1, row_other))
        self.tiles[row_other][6] = Tile(row_other, 6, Knight(color, 6, row_other))
        self.update_pieces_on_board(self.tiles[row_other][1].piece)
        self.update_pieces_on_board(self.tiles[row_other][6].piece)
    
        # add all bishops
        self.tiles[row_other][2] = Tile(row_other, 2, Bishop(color, 2, row_other))
        self.tiles[row_other][5] = Tile(row_other, 5, Bishop(color, 5, row_other))
        self.update_pieces_on_board(self.tiles[row_other][2].piece)
        self.update_pieces_on_board(self.tiles[row_other][5].piece)

        # add all rooks
        self.tiles[row_other][0] = Tile(row_other, 0, Rook(color, 0, row_other))
        self.tiles[row_other][7] = Tile(row_other, 7, Rook(color, 7, row_other))
        self.update_pieces_on_board(self.tiles[row_other][0].piece)
        self.update_pieces_on_board(self.tiles[row_other][7].piece)

        # adds queen
        self.tiles[row_other][3] = Tile(row_other, 3, Queen(color, 3, row_other))
        self.update_pieces_on_board(self.tiles[row_other][3].piece)

        # adds king
        self.tiles[row_other][4] = Tile(row_other, 4, King(color, 4, row_other))
        self.update_pieces_on_board(self.tiles[row_other][4].piece)

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
        
        '''for row in range(ROWS):
            for col in range(COLS):
                check_tile = self.tiles[row][col]

                if check_tile.has_friend(piece.color):
                    self.calc_moves(piece, row, col, bool=False)
                    
                    for move in piece.moves:
                        if isinstance(move.final.piece, King):
                            return True    
                        
        return False'''
    
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
                
        