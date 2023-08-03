# LISTS ALL NECESSARY CONSTANT FOR EASY EDITING

# Dimensions
WIDTH = 640
HEIGHT = 640
PIECE_SIZE = 60
ENLARGED_PIECE_SIZE = 80

# Rows and Columns
ROWS = 8
COLS = 8
FILES = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h')
RANKS = ('8', '7', '6', '5', '4', '3', '2', '1') # col = 1 corresponds to rank 8

# Set tile size
TILE_SIZE = WIDTH // COLS

FONT = 'monospace'

class Green:
    LIGHT_TILE = (234, 255, 200) # light green
    DARK_TILE = (119, 135, 88) # dark green
    LIGHT_MOVE = (244, 247, 116) # light yellow
    DARK_MOVE = (172, 195, 51) # dark yellow
    LIGHT_VALID = '#C86464' # light red
    DARK_VALID = '#C84646' # dark red

    HOVER = (180, 180, 180) # gray

    MOVE_SOUND_PATH = 'assets/sounds/move.wav'
    CAPTURE_SOUND_PATH = 'assets/sounds/capture.wav'

class Brown:
    LIGHT_TILE = (234, 209, 166) # light green
    DARK_TILE = (165, 117, 80) # dark green
    LIGHT_MOVE = (245, 234, 100) # light yellow
    DARK_MOVE = (209, 185, 59) # dark yellow
    LIGHT_VALID = '#C86464' # light red
    DARK_VALID = '#C84646' # dark red

    HOVER = (180, 180, 180) # gray

    MOVE_SOUND_PATH = 'assets/sounds/move.wav'
    CAPTURE_SOUND_PATH = 'assets/sounds/capture.wav'

class Blue:
    LIGHT_TILE = (229, 228, 200) # light green
    DARK_TILE = (60, 95, 135) # dark green
    LIGHT_MOVE = (123, 187, 227) # light yellow
    DARK_MOVE = (43, 119, 191) # dark yellow
    LIGHT_VALID = '#C86464' # light red
    DARK_VALID = '#C84646' # dark red

    HOVER = (180, 180, 180) # gray

    MOVE_SOUND_PATH = 'assets/sounds/move.wav'
    CAPTURE_SOUND_PATH = 'assets/sounds/capture.wav'

class Gray:
    LIGHT_TILE = (120, 119, 118) # light green
    DARK_TILE = (86, 85, 84) # dark green
    LIGHT_MOVE = (99, 126, 143) # light yellow
    DARK_MOVE = (82, 102, 128) # dark yellow
    LIGHT_VALID = '#C86464' # light red
    DARK_VALID = '#C84646' # dark red

    HOVER = (180, 180, 180) # gray

    MOVE_SOUND_PATH = 'assets/sounds/move.wav'
    CAPTURE_SOUND_PATH = 'assets/sounds/capture.wav'