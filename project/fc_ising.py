import math

from manim import *

from utils.GLOBAL_VALUES import * 
from utils.utils import *

from simulations.fully_connected import FC_Ising
from utils.FC_ising import *


simulation_frames=300
class FullyConnected(Scene):
    def construct(self):
        ising=FC_Ising(20)
        colors = ising.state==1
        circles = draw_circles(colors,big_radius=3).shift(2*LEFT)
        self.play(Create(circles))
        self.wait(1)

        ising_lines=np.ones((len(circles),len(circles)))
        for i in range(len(circles)):
            for j in range(len(circles)):
                if i<j: ising_lines[i,j]=0

        all_lines=connect_circles(circles,ising_lines, stroke_width=2)

        self.play(Create(all_lines))
        self.wait()
        hamiltonian=MathTex('H','=\\frac JN\sum_{ij}','s_is_j').shift(4*RIGHT,2*UP)
        hamiltonian[0].set_color(hamiltonian_color)
        hamiltonian[2].set_color(spin_color)

        self.play(Write(hamiltonian))
        self.play(Wiggle(hamiltonian[2]))

        slider=Line(start=5*RIGHT+2.6*DOWN,end=5*RIGHT+0.4*UP)

        pointer=Triangle().scale(0.2).set_stroke(width=0.2).rotate(-90*DEGREES).set_fill(color=temperature_color,opacity=1)
        temp_tex=MathTex('T').next_to(pointer,LEFT).set_color(temperature_color)

        pointer_position=4.5*RIGHT+0.2*UP
        t_pointer=VGroup(pointer,temp_tex).move_to(pointer_position)

        self.play(Create(slider))
        self.play(Create(pointer),Write(temp_tex))

        for t in np.linspace(-10, 10, simulation_frames):
            temperature = logistic(t, start_value=8., end_value=.9, transition_speed=1)
            pointer_movement = t_pointer.animate.move_to(logistic(t, end_value=pointer_position+2*DOWN, start_value=pointer_position, transition_speed=1))
            colors = ising.simulation_steps(temperature, 5)

            # Use there rate_func to control the animation substeps
            self.play(pointer_movement, *update_fill(circles, colors), run_time=0.1, rate_func=linear)



        self.play(FadeOut(circles,all_lines))
        self.play(t_pointer.animate.move_to(pointer_position))
        self.wait()



        ising=FC_Ising(100)
        colors = ising.state==1
        circles = draw_circles(colors,big_radius=3).shift(2*LEFT)
        self.play(Create(circles))
        self.wait(1)


        for i in range(10):
            idx=np.random.randint(0,len(circles))
            lines, destinations, create, uncreate = lines2circle(circles, idx)
            # maby pick other run_time to make animation smoother
            self.play(*create, run_time=0.2, rate_func=linear)
            flying = []
            for line, dst in zip(lines, destinations):
                flying.append(line.animate.shift(dst - line.get_end()))
            self.play(*flying, run_time=0.5, rate_func=linear)

            for line in lines:
                start_point = line.get_start()
                end_point = line.get_end()
                line.put_start_and_end_on(end_point, start_point)

            self.play(*uncreate, run_time=0.1, rate_func=linear)

        for t in np.linspace(-10, 10, simulation_frames):
            temperature = logistic(t, start_value=8., end_value=.9, transition_speed=1)
            pointer_movement = t_pointer.animate.move_to(logistic(t, end_value=pointer_position+2*DOWN, start_value=pointer_position, transition_speed=1))
            colors = ising.simulation_steps(temperature, 5)

            # Use there rate_func to control the animation substeps
            self.play(pointer_movement, *update_fill(circles, colors), run_time=0.1, rate_func=linear)

        self.wait()