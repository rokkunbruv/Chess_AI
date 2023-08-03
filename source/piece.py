# STORES METHODS FOR PIECE CONFIG

import os

from constants import PIECE_SIZE

class Piece:
    def __init__(self, type, color, value, x_pos, y_pos, image = None, image_rect = None):
        self.type = type
        self.color = color
        value_sign = 1 if color == 'white' else -1 # sets how the pieces are going to move for each color (white = -1, black = +1)
        self.value = value * value_sign # positive value for white pieces and negative value for black pieces
        self.moves = [] # lists valid moves of the piece
        self.moved = False
        self.image = image # stores the image path
        self.set_image()
        self.image_rect = image_rect
        self.capture = False  # set to True if a piece captured an enemy
        self.captured = False # set to True if a piece gets captured by enemy
        # sets current x and y pos of the piece
        self.pos = (x_pos, y_pos)

    # updates current pos of the piece
    def update_pos(self, x_pos, y_pos):
        self.pos = (x_pos, y_pos)

    # assigns self.image to image path
    def set_image(self, size=PIECE_SIZE):
        self.image = os.path.join(f'assets/images/imgs-{size}px/{self.color}_{self.type}.png')

    # adds valid moves to self.moves
    def add_moves(self, move):
        self.moves.append(move)

    # clears moves in self.moves
    def clear_moves(self):
        self.moves = []

# class pieces
class Pawn(Piece):
    def __init__(self, color, x_pos, y_pos):
        self.direction = -1 if color == 'white' else 1

        # en passant states
        self.en_passant = False
        self.captured_by_en_pass = False

        # promoted pawn states
        self.promoted = False

        super().__init__('pawn', color, 1.0, x_pos, y_pos) # value of pawn = 1.0

class Knight(Piece):
    def __init__(self, color, x_pos, y_pos):
        super().__init__('knight', color, 3.0, x_pos, y_pos) # value of knight = 3.0

class Bishop(Piece):
    def __init__(self, color, x_pos, y_pos):
        super().__init__('bishop', color, 3.001, x_pos, y_pos) # value of bishop = 3.0, bishop's value slightly higher than knight, thus 3.001

class Rook(Piece):
    def __init__(self, color, x_pos, y_pos):
        super().__init__('rook', color, 5.0, x_pos, y_pos) # value of rook = 5.0

class Queen(Piece):
    def __init__(self, color, x_pos, y_pos):
        super().__init__('queen', color, 9.0, x_pos, y_pos) # value of queen = 9.0

class King(Piece):
    def __init__(self, color, x_pos, y_pos):
        # set left_rook and right_rook for castling
        self.can_castle = True
        self.left_rook = None
        self.right_rook = None

        super().__init__('king', color, 10000.0, x_pos, y_pos) # value of king = any extreme large value (e.g. 10000)
