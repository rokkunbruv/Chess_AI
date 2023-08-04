# CHESS_AI v1.1
# STORES METHODS FOR PIECE CONFIG

import os

from constants import PIECE_SIZE
from move import Move

class Piece:
    def __init__(self, type, color, value, row, col, image = None, image_rect = None, sym = ''):
        # piece characteristics
        self.type = type
        self.color = color
        value_sign = 1 if color == 'white' else -1 # sets how the pieces are going to move for each color (white = -1, black = +1)
        self.value = value * value_sign # positive value for white pieces and negative value for black pieces
        self.sym = sym # sets the symbol name of piece (for printing out move in Move class)
        
        # piece events tracking
        self.valid_moves = [] # lists valid moves of the piece
        self.moved = False
        self.capture = False  # set to True if a piece captured an enemy
        self.captured = False # set to True if a piece gets captured by enemy
        # sets current x and y pos of the piece
        self.tile = (row, col)
        self.check = False # set to True if piece threatens enemy king

        # piece rendering
        self.image = image # stores the image path
        self.set_image()
        self.image_rect = image_rect
        
    # updates current pos of the piece
    def update_tile(self, row, col):
        self.tile = (row, col)

    # adds valid moves to self.moves
    def add_moves(self, move, board):
        # appends move to valid moves if move doesnt cause any checks
        if not board.check(move):
            self.valid_moves.append(move)

    # clears moves in self.moves
    def clear_moves(self):
        self.valid_moves = []

    # assigns self.image to image path
    def set_image(self, size=PIECE_SIZE):
        self.image = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.type}.png')

    # returns row
    @property
    def row(self):
        return self.tile[0]

    # returns col
    @property
    def col(self):
        return self.tile[1]

# class pieces
class Pawn(Piece):
    def __init__(self, color, row, col):
        self.direction = -1 if color == 'white' else 1

        # en passant states
        self.enable_enpas = False # when True, an enemy pawn can capture that pawn that enables en pas by en passant
        self.captured_by_enpas = False

        # promoted pawn states
        self.promoted = False

        super().__init__('pawn', color, 1.0, row, col) # value of pawn = 1.0

    def calc_moves(self, board):
        # checks if pawn has moved so that it can move two tiles
        steps = 1 if self.moved else 2
            
        # movement
        start = self.row + self.direction
        end = self.row + (self.direction * (1 + steps))
        for r_move in range(start, end, self.direction):
            if board.in_range(r_move):
                if board.tiles[r_move][self.col].is_empty():
                    # set initial pos
                    initial = (self.row, self.col)
                    # set final pos
                    final = (r_move, self.col)
                    # set initial and final pos to move obj
                    move = Move(self, initial, final)
                    # add move
                    self.add_moves(move, board)
                else:
                    break
            else:
                break

        # capture
        r_move = self.row + self.direction
        c_captures = [self.col-1, self.col+1]

        for c_move in c_captures:
            if board.in_range(r_move, c_move):
                if board.tiles[r_move][c_move].has_rival(self.color):
                    # set captured piece
                    c = board.tiles[r_move][c_move].piece
                    # set initial pos
                    initial = (self.row, self.col)
                    # set final pos
                    final = (r_move, c_move)
                    # set initial and final pos to move obj
                    move = Move(self, initial, final, captured_piece = c)
                    # add move
                    self.add_moves(move, board)

        # en passant logic
        # self.enable_enpas - being modified in main
        r_enpas = 3 if self.color == 'white' else 4
        if self.can_i_do_enpas(board) and r_enpas == self.row:
            r_move = r_enpas + self.direction
            
            for c_move in (self.col-1, self.col+1):
                if board.in_range(c_move):   
                    if board.tiles[r_enpas][c_move].has_rival(self.color):
                        # set captured piece
                        c = board.tiles[r_enpas][c_move].piece
                        
                        # ensures that captured pawn has been recently moved
                        # otherwise you cant do en passant
                        if not c.enable_enpas:
                            continue

                        # id like to call this as a pretty clever way for that enemy pawn to be actually captured
                        '''pls examine this code tho when you get problems on your undo function (undoing en pas)'''
                        board.tiles[r_enpas][c_move].piece = None
                        c = board.tiles[r_move][c_move].piece = c

                        c.captured_by_enpas = True

                        # set initial pos
                        initial = (self.row, self.col)
                        # set final pos
                        final = (r_move, c_move)
                        # set initial and final pos to move obj
                        move = Move(self, initial, final, captured_piece = c)
                        # add move
                        self.add_moves(move, board)    

    # checks if pawn can do en pas
    def can_i_do_enpas(self, board):
        # cant do en pas if no moves are being made
        if board.record_of_moves == []:
            return False
        # set recent move
        move = board.record_of_moves[-1]
        #  cant do en passant if enemy pawn didnt move
        if not isinstance(move.piece, Pawn):
            return False
        # return true if enemy pawn moved 2 squares else false
        diff = abs(move.final[0] - move.initial[0])
        return True if diff == 2 else False

    # promote a pawn
    # will only run if pawn has reached to other side of board
    def promotion(self, board, upgrade='queen'):
        board.pieces_on_board.remove(self)
        
        if upgrade == 'rook':
            self = Rook(self.color, self.row, self.col)
        elif upgrade == 'knight':
            self = Knight(self.color, self.row, self.col)
        elif upgrade == 'bishop':
            self = Bishop(self.color, self.row, self.col)
        elif upgrade == 'queen':
            self = Queen(self.color, self.row, self.col)
        # error
        else:
            pass

        board.pieces_on_board.append(self)

    # allows for pawn promotion
    def check_promotion(self):
        end = 0 if self.color == 'white' else 7
        return True if self.row == end else False

class Rook(Piece):
    def __init__(self, color, row, col):
        super().__init__('rook', color, 5.0, row, col, sym = 'R') # value of rook = 5.0

    def calc_moves(self, board):
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        
        move_linear(self, board, directions)

class Knight(Piece):
    def __init__(self, color, row, col):
        super().__init__('knight', color, 3.0, row, col, sym = 'N') # value of knight = 3.0

    def calc_moves(self, board):
        # possible knight moves
        pms = [ (self.row-2,self.col+1),
                (self.row-2,self.col-1),
                (self.row+2,self.col+1),
                (self.row+2,self.col-1), 
                (self.row-1,self.col+2),
                (self.row-1,self.col-2),
                (self.row+1,self.col+2),
                (self.row+1,self.col-2)
                ]
            
        for pm in pms:
            r_pm, c_pm = pm

            if board.in_range(r_pm, c_pm):
                if board.tiles[r_pm][c_pm].is_empty_or_rival(self.color):
                    c = board.tiles[r_pm][c_pm].piece
                        
                    initial = (self.row, self.col)

                    final = (r_pm, c_pm)

                    move = Move(self, initial, final, captured_piece = c)
                        
                    self.add_moves(move, board)

class Bishop(Piece):
    def __init__(self, color, row, col):
        super().__init__('bishop', color, 3.001, row, col, sym = 'B') # value of bishop = 3.0, bishop's value slightly higher than knight, thus 3.001

    def calc_moves(self, board):
        directions = [(-1,1), (-1,-1), (1,1), (1,-1)]
        
        move_linear(self, board, directions)

class Queen(Piece):
    def __init__(self, color, row, col):
        super().__init__('queen', color, 9.0, row, col, sym = 'Q') # value of queen = 9.0

    def calc_moves(self, board):
        directions = [(-1,1), (-1,-1), (1,1), (1,-1),
                        (-1,0), (1,0), (0,-1), (0,1)]
        
        move_linear(self, board, directions)

class King(Piece):
    def __init__(self, color, row, col):
        # castling attributes
        self.can_castle = True # false if king cant perform castle anymore
        self.q_castle = None # stores rook move in queen castling
        self.k_castle = None # stores rook move in king castling
        self.castled = False # true if king has performed castling

        # king under check
        self.check = False

        super().__init__('king', color, 10000.0, row, col, sym = 'K') # value of king = any extreme large value (e.g. 10000)

    def calc_moves(self, board):
        self.q_castle = None
        self.k_castle = None
        
        pms = [ (self.row-1,self.col), # up
                (self.row+1,self.col), # down
                (self.row,self.col-1), # left
                (self.row,self.col+1), # right
                (self.row-1,self.col-1), # up left
                (self.row+1,self.col-1), # down left
                (self.row-1,self.col+1), # up right
                (self.row+1,self.col+1) # down right
                ]
            
        for pm in pms:
            r_pm, c_pm = pm

            if board.in_range(r_pm, c_pm):
                if board.tiles[r_pm][c_pm].is_empty_or_rival(self.color):
                    # set captured piece
                    c = board.tiles[r_pm][c_pm].piece
                    # set initial pos
                    initial = (self.row, self.col)
                    # set final pos
                    final = (r_pm, c_pm)
                    # set initial and final pos to move obj
                    move = Move(self, initial, final, captured_piece = c)
                    # add move
                    self.add_moves(move, board)     

        '''y'know, i can make this more modular, but i'll stick to this one cos it kept
            on screaming errors'''
        # castling logic
        if not self.moved and self.can_castle and not self.check:
            # queen side castling (long castle)
            l_rook = board.tiles[self.row][0].piece
            if isinstance(l_rook, Rook) and not l_rook.moved:
                for c_range in range(1, 4):
                    # castling is not possible because there are pieces in between ?
                    if board.tiles[self.row][c_range].has_piece():
                        break

                    # rook move
                    initial = (l_rook.row, l_rook.col)
                    final = (l_rook.row, l_rook.col+3)
                    self.q_castle = Move(l_rook, initial, final)
                    
                    # king move
                    initial = (self.row, self.col)
                    final = (self.row, self.col-2)
                    move = Move(self, initial, final)

                    # this code prevents king from castling thru check
                    if board.check(move):
                        break
                    
                    if c_range == 3:
                        # add move
                        self.add_moves(move, board)
                    
            
            # king side castling (short castle)
            r_rook = board.tiles[self.row][7].piece
            if isinstance(r_rook, Rook) and not r_rook.moved:
                for c_range in range(5, 7):
                    # castling is not possible because there are pieces in between ?
                    if board.tiles[self.row][c_range].has_piece():
                        break

                    # rook move
                    initial = (r_rook.row, r_rook.col)
                    final = (r_rook.row, r_rook.col-2)
                    self.k_castle = Move(r_rook, initial, final)

                    # king move
                    initial = (self.row, self.col)
                    final = (self.row, self.col+2)
                    move = Move(self, initial, final)
                    
                    # this code prevents king from castling thru check
                    if board.check(move):
                        break

                    if c_range == 6:
                        # add move
                        self.add_moves(move, board)

    # check if king has performed a castling move
    def check_castle(self, move):
        return abs(move.final[1] - move.initial[1]) == 2

# function dedicated for queen, rook, & bishop calc_moves
def move_linear(piece, board, directions):
    for dir in directions:
        # set x and y directions
        r_dir, c_dir = dir

        # set possible moves
        r_pm = piece.row + r_dir
        c_pm = piece.col + c_dir

        # record moves one by one
        while True:
            # checks if possible move in range and possible move doesnt contain friend
            if board.in_range(r_pm, c_pm) and not board.tiles[r_pm][c_pm].has_friend(piece.color):
                
                c = board.tiles[r_pm][c_pm].piece
                        
                initial = (piece.row, piece.col)

                final = (r_pm, c_pm)

                move = Move(piece, initial, final, captured_piece = c)

                piece.add_moves(move, board)

                # breaks loop if enemy piece detected (capture)
                if c != None:
                    break

                # increment
                r_pm = r_pm + r_dir
                c_pm = c_pm + c_dir
            # exits loop if out of range or friend detected
            else:
                break










