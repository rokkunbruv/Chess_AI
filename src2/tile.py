# CONTAINS METHODS FOR CHECKING STATE OF TILE (IF IT'S EMPTY OR CONTAIN FRIENDLY OR RIVAL PIECE)

class Tile:
    
    # file labels
    ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5:'f', 6: 'g', 7: 'h'}
    
    def __init__(self, row, col, piece = None):
        self.row = row
        self.col = col
        self.piece = piece
        self.alphacols = self.ALPHACOLS[col]

    # allows comparing tile object and dragger object
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    # checks if the tile contains a piece
    def has_piece(self):
        return self.piece != None
    
    # checks if the tile is empty / doesn't have a piece
    def is_empty(self):
        return not self.has_piece()
    
    # checks if the tile contains a friendly piece
    def has_friend(self, color):
        return self.has_piece() and self.piece.color == color
    
    # checks if the tile contains an enemy piece
    def has_rival(self, color):
        return self.has_piece() and self.piece.color != color
    
    # checks if the tile is empty or contains an enemy piece
    def is_empty_or_rival(self, color):
        return self.is_empty() or self.has_rival(color)
    
    # selects file label from ALPHACOL dict
    @staticmethod
    def get_alphacol(col):
        ALPHACOLS = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5:'f', 6: 'g', 7: 'h'}

        return ALPHACOLS[col]