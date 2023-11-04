from manim import *

import numpy as np

from GLOBAL_VALUES import spin_color, hamiltonian_color
from spin_grid import make_grid 

def first_nonzero(bool_array:np.array)->int:
    for i in range(len(bool_array)):
        if bool_array[i]==1: 
            return i

    return len(bool_array)

class SpinLine(Scene):
    def construct(self):

        starting_state=np.array([[0,0,0,0,1,1,1,1,1]],dtype='bool')
        grid=make_grid(starting_state, self)
        circles=grid['circles']
        arrows=grid['arrows']

        self.play(Create(grid['circles']))

        b=first_nonzero(starting_state[0])
        midpoint=(circles[b-1].get_center() + circles[b].get_center())/2
        
        domain_barrier=Line(midpoint+UP,midpoint+DOWN)

        self.play(Create(domain_barrier))
        self.wait(1)