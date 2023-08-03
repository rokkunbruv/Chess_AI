from color import Color

class Theme:
    def __init__(self, light_bg, dark_bg, # board colors
                        light_trace, dark_trace, # highlights initial and final moves
                        light_moves, dark_moves, # highlights available valid moves
                        hover, 
                        move_sound, capture_sound): 
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)
        self.hover = hover
        self.move_sound = move_sound
        self.capture_sound = capture_sound