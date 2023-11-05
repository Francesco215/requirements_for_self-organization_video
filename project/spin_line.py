from manim import *

import numpy as np

from GLOBAL_VALUES import spin_color, hamiltonian_color
from spin_grid import make_grid, update_circle_grid

def make_domain_barrier(len:int,barrier:int)->np.array:
    assert 0<=barrier<=len, "Barrier must be between 0 and len, got barrier={}".format(barrier)
    return (np.arange(len)>=barrier).reshape(1,len)

def first_nonzero(bool_array:np.array)->int:
    for i in range(len(bool_array)):
        if bool_array[i]==1: 
            return i

    return len(bool_array)


def make_random_chain(len:int)->np.array:
    return np.random.randint(low=0,high=2,size=[1,len])==0


chain_lenght=9

class SpinLine(Scene):
    def construct(self):

        state=make_random_chain(chain_lenght)
        grid=make_grid(state, self)
        circles=grid['circles']
        arrows=grid['arrows']

        self.play(Create(circles,run_time=3), Create(arrows,run_time=3)) #maybe change the speed of animation here
        self.wait(1)

        hamiltonian=MathTex('H','=-J\sum_i','s_is_{i+1}').next_to(circles,UP*3)
        hamiltonian[0].set_color(hamiltonian_color)
        hamiltonian[2].set_color(spin_color)

        lines=VGroup()
        for i in range(len(circles)-1):
            lines.add(Line(
                start=circles[i].get_edge_center(RIGHT),
                end=circles[i+1].get_edge_center(LEFT),
                color=ORANGE,
                stroke_width=7))

        self.play(Write(hamiltonian),Create(lines))
        self.wait(1)

        state=make_domain_barrier(chain_lenght,chain_lenght)
        self.play(*update_circle_grid(grid, state, self, random_rotation=False))
        self.wait(1)

        self.play(FadeOut(hamiltonian))
        energy=MathTex('E','=0').next_to(circles,UP*5)
        energy[0].set_color(hamiltonian_color)

        self.play(Write(energy))
        self.wait(2)

        b=4
        state=make_domain_barrier(chain_lenght,b)
        target_energy=MathTex('E','=J').next_to(energy,0)
        target_energy[0].set_color(hamiltonian_color)

        midpoint=(circles[b-1].get_center() + circles[b].get_center())/2        
        domain_barrier=Line(midpoint+UP,midpoint+DOWN)
        self.play(Create(domain_barrier),Transform(energy,target_energy),*update_circle_grid(grid, state, self, random_rotation=False))
        self.wait(1)

        