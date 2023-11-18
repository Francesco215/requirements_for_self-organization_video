from manim import *

import pickle

from utils.utils import bool2color, update_colors2
from utils.grid import Grid, make_grid, update_circle_grid, circles_to_squares, add_boundaries, zoom_out, tracking_boundaries
"""
    Take this code as a rough blueprint, I have written it whithout using classes, but if you prefer to do it in a object oriented way feel free to do so
"""


class Test(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)
        square=Square(2, fill_color=RED,fill_opacity=1)
        self.play(Create(square))
        self.wait(1)
        self.play(square.animate.scale(0.5))
        self.wait(1)
        self.play(square.animate.set_color(GREEN))
        self.wait(1)


from simulations.ising_2d import Ising2D



class Ising_2D(Scene):
    def construct(self):
        shape = (10,20)
        ising=Ising2D(shape)

        grid=make_grid(ising.state==1,self,radius=0.7)

        self.play(Create(grid['circles']),Create(grid['arrows']))
        self.wait(1)
        for _ in range(3):
            ising.simulation_steps(1,100)
            self.play(*update_circle_grid(grid, ising.state==1))

        circles_to_squares(grid,self)
        grid.pop('arrows')
        self.play(*zoom_out(grid,scale=.7), run_time=5)
        self.wait(1)
        #here the color is changed in the square as if it was never zoomed out
        animation=grid['squares'][73].animate.set_color(RED)
        self.play(animation)
        #here the boundaries are drawn as if the grid never zoomed out
        tracking_boundaries(grid, self)


class TrackingBoundaries(Scene):
    def construct(self):
        shape = (10, 20)
        ising = Ising2D(shape)

        grid = make_grid(ising.state == 1, self, radius=0.2)
        # with open('/home/nikos/aaa.pickle', 'wb') as f:
        #    pickle.dump(grid, f)

        # with open('/home/nikos/aaa.pickle', 'rb') as f:
        #    grid = pickle.load(f)

        circles_to_squares(grid, self)
        # grid2 = NumberPlane()
        # self.add(grid2)
        tracking_boundaries(grid, self)
        self.wait(2)