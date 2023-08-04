# MOVE CLASS RESPONSIBLE FOR STORING INITIAL LOCATION AND FINAL LOCATION FOR EVERY MOVE DONE

from constants import FILES, RANKS

class Move:
    def __init__(self, piece, initial, final, captured_piece = None):
        self.piece = piece
        
        # keeps track of initial and final pos
        self.initial = initial
        self.final = final

        # keeps track of captured piece
        self.captured_piece = captured_piece
        self.capture = True if self.captured_piece != None else False

        # True when initial pos is starting pos of piece
        self.from_starting_tile = False

    # prints the move in algebraic notation
    def algebra_not(self, board):
        file = FILES[self.final[1]]
        rank = RANKS[self.final[0]]
        check = ''

        # adds '+' to move if enemy king in check
        if self.piece.color == 'white':
            king = board.black_king
        else:
            king = board.white_king

        if king.check:
            check = '+'

        coords = file + rank + check
        
        # notation when piece captured an enemy
        if self.capture:
            if self.piece.sym == '':
                self.piece.sym = FILES[self.initial[1]]
            print(self.piece.sym + 'x' + coords)
        else:
            print(self.piece.sym + coords)

    # prints move
    def __str__(self):
        piece_info = f'Piece: {self.piece.type}'
        movement = f'From {self.initial} to {self.final}'
        captured = ''
        if self.capture:
            captured = f'Capturing {self.captured_piece.color} {self.captured_piece.type}'

        return piece_info + movement + captured
    
    # allows checking if the move you're going to do is in valid moves
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
