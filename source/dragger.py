# CONTAINS METHODS FOR DRAGGING LOGIC

import pygame

from constants import *

class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging = False
        self.mouse_x = 0
        self.mouse_y = 0
        self.initial_row = 0
        self.initial_col = 0
    
    # draws the dragging piece (enlarged image)
    def update_blit(self, surface):
        self.piece.set_image(ENLARGED_PIECE_SIZE)
        image = self.piece.image

        load_image = pygame.image.load(image)
        load_image = pygame.transform.scale(load_image, (ENLARGED_PIECE_SIZE, ENLARGED_PIECE_SIZE))

        image_center = (self.mouse_x, self.mouse_y)
        self.piece.image_rect = load_image.get_rect(center = image_center)

        surface.blit(load_image, self.piece.image_rect)

    # updates position of dragger object
    def update_mouse(self, pos):
        self.mouse_x, self.mouse_y = pos

    # sets x (col) and y (row) coordinate from current position
    def save_initial(self, pos):
        self.initial_row = pos[1] // TILE_SIZE
        self.initial_col = pos[0] // TILE_SIZE

    # drags the piece selected
    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True
    
    # method when piece is undragged
    def undrag_piece(self):
        self.piece = None
        self.dragging = False