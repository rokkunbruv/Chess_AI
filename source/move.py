# MOVE CLASS RESPONSIBLE FOR STORING INITIAL LOCATION AND FINAL LOCATION FOR EVERY MOVE DONE

from constants import FILES, RANKS
from piece import *

class Move:
    def __init__(self, initial, final):
        self.initial = initial
        self.final = final

    # prints the move
    def print_move(self, board, piece, captured):
        file = FILES[self.final.col]
        rank = RANKS[self.final.row]
        check = ''
        p = ''

        # adds '+' to move if king in check
        if board.king_check:
            check = '+'

        # set p to corresponding piece being move
        if isinstance(piece, King):
            p = 'K'
        elif isinstance(piece, Queen):
            p = 'Q'
        elif isinstance(piece, Rook):
            p = 'R'
        elif isinstance(piece, Knight):
            p = 'N'
        elif isinstance(piece, Bishop):
            p = 'B'
        elif isinstance(piece, Pawn):
            p = FILES[self.initial.col]

        coords = file + rank + check
        
        # notation when piece captured an enemy
        '''if captured:
            print(p + 'x' + coords)
        else:
            if isinstance(piece, Pawn):
                print(coords)
            else:
                print(p + coords)'''

    # displays initial and final locations of the piece being moved
    def __str__(self):
        s = ''
        s += f'({self.initial.col}, {self.initial.row})'
        s += f' -> ({self.final.col}, {self.final.row})'

        return s
    
    # allows checking if the move you're going to do is in valid moves
    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
    
