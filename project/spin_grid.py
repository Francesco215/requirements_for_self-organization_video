from manim import *

from utils.utils import update_colors2
from utils.grid import Grid, make_grid, update_circle_grid, circles_to_squares, add_boundaries, zoom_out
"""
    Take this code as a rough blueprint, I have written it whithout using classes, but if you prefer to do it in a object oriented way feel free to do so
"""


class Test(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)

        size = (20, 40)
        starting_state = np.random.choice([True, False], size=size)
        grid = make_grid(starting_state, self, radius=0.3)
        self.wait(1)
        new_state = np.random.choice([True, False], size=size)
        update_circle_grid(grid, new_state)
        self.wait(1)
        circles_to_squares(grid, self)
        self.wait(1)
        new_state2 = np.random.choice([True, False], size=size)
        anims = update_colors2(grid, 'squares', new_state2)
        self.play(*anims)
        self.play(*add_boundaries(grid))
        self.play(*zoom_out(grid), run_time=5)
        self.wait(1)

from simulations.ising_2d import Ising2D



class Ising_2D(Scene):
    def construct(self):
        shape = (10,20)
        Ising2D(shape)

