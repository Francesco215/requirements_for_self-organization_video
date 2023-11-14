import numpy as np


def get_neighbors(state, ic, jc, window_size):
    neighbors = []
    shape=state.shape
    for di in range(-window_size, window_size + 1):
        for dj in range(-window_size, window_size + 1):
            neighbors.append(((ic + di)%shape[0], (jc + dj)%shape[1]))
    return neighbors

def energy_2d_hopfield(ic,jc,state:np.array, patterns:np.array, neighborhood:list , J: float) -> float:
    delta_E=0
    for i,j in neighborhood:
        interaction=np.dot(patterns[:,i,j],patterns[:,ic,jc])
        delta_E+=interaction*state[i,j]

    delta_E*=2*state[ic,jc]*J

    return delta_E

class FC_Hopfield:
    def __init__(self,patterns,starting_state=None):
        # make sure that patterns is all made of +1 or -1 values
        assert np.all(patterns==1 or patterns==-1)
        self.shape = patterns.shape
        if starting_state is not None:
            assert patterns.shape == starting_state.shape
        else:
            starting_state = np.random.choice([-1, 1], size=self.shape)


        self.overlaps=np.matmul(self.patterns,self.starting_state)
        self.J=-1

    def simulation_steps(self, temperature:float, n_steps:int, window_size:int)->np.array:
        for _ in range(n_steps):
            # Select a random site in the chain
            ic = np.random.randint(0, self.shape[0])
            jc = np.random.randint(0, self.shape[1])

            neighbors=get_neighbors(self.state,ic,jc,window_size)
            # Calculate the energy change if we flip the spin at the selected site

            delta_E=energy_2d_hopfield(ic,jc,self.overlaps,self.patterns,neighbors,self.J)

            if delta_E < 0 or np.random.rand() < np.exp(-delta_E / temperature):
                # Accept the flip with a certain probability
                self.state[ic,jc] *= -1