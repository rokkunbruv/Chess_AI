
from piece import *

def fen(board, fen_str=''):
    row = 0
    col = 0
    
    for index in range(len(fen_str)): 
        c = fen_str[index]

        if c.isalpha():
            color = 'white' if c.isupper() else 'black'

        if c.upper() == 'P':
            board.tiles[row][col].piece = Pawn(color, row, col)
        elif c.upper() == 'R':
            board.tiles[row][col].piece = Rook(color, row, col)
        elif c.upper() == 'N':
            board.tiles[row][col].piece = Knight(color, row, col)
        elif c.upper() == 'B':
            board.tiles[row][col].piece = Bishop(color, row, col)
        elif c.upper() == 'Q':
            board.tiles[row][col].piece = Queen(color, row, col)
        elif c.upper() == 'K':
            board.tiles[row][col].piece = King(color, row, col)

            if color == 'white':
                board.white_king = board.tiles[row][col].piece
            else:
                board.black_king = board.tiles[row][col].piece
        elif c == '/':
            row += 1
            col = 0
            continue
        else:
            c = int(c)
            col += (c-1)
            continue
        
        board.tiles[row][col].piece.update_tile(row, col)
        board.update_pieces_on_board(board.tiles[row][col].piece)
        col += 1
        