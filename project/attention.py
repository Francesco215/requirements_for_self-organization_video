from manim import *


from utils.utils import bool2color, update_colors2, logistic
from utils.grid import Grid, make_grid, tracking_boundaries, update_circle_grid, circles_to_squares, add_boundaries, zoom_out
from utils.GLOBAL_VALUES import *
from utils.attention import tokenization

class ColorText(Scene):
    def construct(self):
        create, colorize = tokenization(
            ['Many',' words ',' map',' to',' one',' token']
        )
        self.play(create, run_time=2)
        self.play(*colorize, run_time=2)
        self.wait(2)