from manim import *

import numpy as np

from utils.GLOBAL_VALUES import spin_color, hamiltonian_color, temperature_color, entropy_color
from utils.grid import make_grid, update_circle_grid
from simulations.fully_connected import make_random_chain

def make_domain_barrier(len:int,barrier:int)->np.array:
    assert 0<=barrier<=len, "Barrier must be between 0 and len, got barrier={}".format(barrier)
    return (np.arange(len)>=barrier).reshape(1,len)

def first_nonzero(bool_array:np.array)->int:
    for i in range(len(bool_array)):
        if bool_array[i]==1: 
            return i

    return len(bool_array)



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
        self.play(*update_circle_grid(grid, state, random_rotation=False))
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
        self.play(Create(domain_barrier),Transform(energy,target_energy),*update_circle_grid(grid, state, random_rotation=False))
        self.wait(1)

        # you would think the system would tend in the state where all the spins are aligned,
        # however when you introduce some noise that can be parametrized by the temperature
        # what is actually minimized is the Free energy

        free_energy=MathTex('F','=','E','-','T','S').next_to(energy,0)
        free_energy[0].set_color(hamiltonian_color)
        free_energy[2].set_color(hamiltonian_color)
        free_energy[4].set_color(temperature_color)
        free_energy[5].set_color(entropy_color)

        self.play(Transform(energy,free_energy))
        self.wait(1)

        # in the free energy there is this new term that has to be taken in account
        self.play(Wiggle(energy[4]),Wiggle(energy[5]))
        self.wait(1)

        text=None
        for b in range(chain_lenght-1):
            midpoint=(circles[b].get_center() + circles[b+1].get_center())/2 
            state=make_domain_barrier(chain_lenght,b+1) 
            self.play(domain_barrier.animate.set_x(midpoint[0]),*update_circle_grid(grid,state,random_rotation=False))

            if b==3:
                text=MathTex('S','=\log(N-1)').next_to(circles,DOWN*3)
                text[0].set_color(entropy_color)
                self.play(Write(text))


        free_energy=MathTex('F','=','J','-','T','\log(N-1)').next_to(energy,0)
        free_energy[0].set_color(hamiltonian_color)
        free_energy[2].set_color(hamiltonian_color)
        free_energy[4].set_color(temperature_color)
        free_energy[5].set_color(entropy_color)

        self.play(Transform(energy,free_energy))
        self.wait(1)

        self.play(FadeOut(text))

        text=MathTex('\Delta','F','<0').next_to(text,0)
        text[1].set_color(hamiltonian_color)
        self.play(Write(text))
        self.wait(1)


        free_energy=MathTex('J','<','T','\log(N-1)').next_to(energy,0)
        free_energy[0].set_color(hamiltonian_color)
        free_energy[2].set_color(temperature_color)
        free_energy[3].set_color(entropy_color)
        self.play(Transform(energy,free_energy))
        self.wait(1)