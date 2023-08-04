# undoes moves in board
# i made this function as its own module since this function can get messy

'''TANGINA MO PISTENG GIATAY NGANONG NAG COMPSCI MAN KO TTTTTTTTTTTTT_____________TTTTTTTTTTTTTTTTTT'''
'''YAYYYYYYYY ITT FINALLY WORKED!!!!! I LOVE COMPSCI BEST COURSE!!!!!!!!!!!!!!!!!1'''

from piece import *

# handles all undoing events
def undo(board):
    # selects most recent move
    move = board.record_of_moves[-1]

    # undoes move
    piece = board.tiles[move.initial[0]][move.initial[1]].piece = move.piece

    # updates location of piece
    piece.update_tile(move.initial[0], move.initial[1])

    # resurrects captured piece if any
    res_piece = board.tiles[move.final[0]][move.final[1]].piece = move.captured_piece

    # undoes en passant
    if isinstance(res_piece, Pawn):
        if res_piece.captured_by_enpas:
            # switches captured pawn from captured tile (where the pawn capturing captured pawn went)
            # back to where its supposed to be
            board.tiles[move.final[0]][move.final[1]].piece = None
            res_piece = board.tiles[move.final[0] + res_piece.direction][move.final[1]].piece = move.captured_piece
            
            # resets res_piece states
            res_piece.captured_by_enpas = False
            board.enable_en_passant(res_piece)

    # else if a piece was resurrected
    elif res_piece:
        # update loc of resurrected pieces
        res_piece.update_tile(move.final[0], move.final[1])
        
    # undoes castle
    if isinstance(piece, King):
        # selects what kind of castling move
        cas_move = None

        # select castling move
        if piece.check_castle(move):
            if piece.color == 'white':
                cas_move = board.white_castle
            else:
                cas_move = board.black_castle

        if cas_move:
            # switches rook back to orig pos
            board.tiles[cas_move.final[0]][cas_move.final[1]].piece = None
            rook = board.tiles[cas_move.initial[0]][cas_move.initial[1]].piece = cas_move.piece
            rook.update_tile(cas_move.initial[0], cas_move.initial[1])

            # rook back in starting pos
            rook.moved = False

            if piece.color == 'white':
                board.white_castle = None
            else:
                board.black_castle = None

    # if enemy piece was captured
    if move.capture:
        # brings back resurrected piece to pieces_on_board
        res_piece.captured = False
        board.update_pieces_on_board(res_piece)

        piece.capture = False
    
    # sets piece.moved to False if goes back to starting tile
    if move.from_starting_tile:
        piece.moved = False

    # deletes undone move
    del board.record_of_moves[-1]
