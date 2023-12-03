from manim import *

import pickle

from utils.utils import bool2color, update_colors2, logistic
from utils.grid import Grid, make_grid, tracking_boundaries, update_circle_grid, circles_to_squares, add_boundaries, zoom_out
from utils.GLOBAL_VALUES import *


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


        slider=Line(start=5*RIGHT+2.6*DOWN,end=5*RIGHT+0.4*UP, color=temperature_color)

        pointer=Triangle().scale(0.2).set_stroke(width=0.2).rotate(-90*DEGREES).set_fill(color=temperature_color,opacity=1)
        temp_tex=MathTex('T').next_to(pointer,LEFT).set_color(temperature_color)

        pointer_position=4.5*RIGHT+0.2*UP
        t_pointer=VGroup(pointer,temp_tex).move_to(pointer_position)

        self.play(Create(slider))
        self.play(Create(pointer),Write(temp_tex))

        for t in np.linspace(-3, 10, 100):
            temperature = logistic(t, start_value=2., end_value=.5, transition_speed=1)
            pointer_movement = t_pointer.animate.move_to(logistic(t, end_value=pointer_position+2.6*DOWN, start_value=pointer_position, transition_speed=1))
            colors = ising.simulation_steps(temperature, 100)==1

            self.play(pointer_movement, *update_colors2(grid, 'squares', colors), run_time=0.1, rate_function=linear)

        animations, _ = add_boundaries(grid, stroke_width=10)
        self.play(*animations)

class Peiels2D(Scene):
    def construct(self):
        shape = (10, 20)
        # Create a 10x20 array filled with zeros
        array = [[-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1,  1,  1,  1,  1,  1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1,  1,  1,  1,  1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1,  1,  1,  1,  1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1,  1,  1,  1,  1,  1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1,  1,  1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1,  1,  1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]

        array=np.array(array)

        ising = Ising2D(shape, starting_state=array)
        
        grid = make_grid(ising.state == 1, self, radius=0.2)

        circles_to_squares(grid, self)

        self.wait(1)

        free_energy=MathTex('\Delta','F','=','\Delta','E','-','T','\Delta','S').shift(3*UP)
        free_energy[1].set_color(hamiltonian_color)
        free_energy[4].set_color(hamiltonian_color)
        free_energy[6].set_color(temperature_color)
        free_energy[8].set_color(entropy_color)

        self.play(Write(free_energy))        
        self.wait(1)

        annotation=MathTex('\Delta', 'E', '=2J','\mathcal P').shift(3*DOWN)
        annotation[1].set_color(hamiltonian_color)
        annotation[3].set_color(domain_barrier_color)
        self.play(Write(annotation))
        self.wait(1)
        tracking_boundaries(grid, self)

        target=MathTex('\Delta','F','=','2J','\mathcal P','-','T','\Delta','S').next_to(free_energy,0)
        target[1].set_color(hamiltonian_color)
        target[4].set_color(domain_barrier_color)
        target[6].set_color(temperature_color)
        target[8].set_color(entropy_color)

        self.play(Transform(free_energy,target))
        self.wait(1)

        target=MathTex('\Omega','(','\mathcal P',')','\le 3^','\mathcal P').next_to(annotation,0)
        target[0].set_color(entropy_color)
        target[2].set_color(domain_barrier_color)
        target[-1].set_color(domain_barrier_color)

        self.play(Transform(annotation,target))
        self.wait(1)

        target=MathTex('\Delta','S','\le', '\mathcal P','\log 3').next_to(annotation,0)

        target[1].set_color(entropy_color)
        target[3].set_color(domain_barrier_color)
        self.play(Transform(annotation,target))
        self.wait(1)


        target=MathTex('\Delta','F','\ge','2J','\mathcal P','-','T','\mathcal P','\log 3').next_to(free_energy,0)
        target[1].set_color(hamiltonian_color)
        target[4].set_color(domain_barrier_color)
        target[6].set_color(temperature_color)
        target[-2].set_color(domain_barrier_color)

        self.play(Transform(free_energy,target), FadeOut(annotation))
        self.wait(1)


        target=MathTex('\Delta','F','\ge','\mathcal P','(2J-','T','\log3)').next_to(free_energy,0)
        target[1].set_color(hamiltonian_color)
        target[3].set_color(domain_barrier_color)
        target[5].set_color(temperature_color)

        self.play(Transform(free_energy,target))
        self.wait(1)

        annotation=MathTex('T','\le \\frac{2J}{\log 3}').next_to(annotation,0)
        annotation[0].set_color(temperature_color)
        self.play(Write(annotation))
        self.wait(1)



        self.wait(2)

