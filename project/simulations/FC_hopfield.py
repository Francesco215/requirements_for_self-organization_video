import numpy as np
import einops 

def squeeze(x:np.array)->np.array:
    """ merges the last two dimentions """
    return einops.rearrange(x,'... h w -> ... (h w)')

def hopfield_energy(overlaps:np.array, J=1):
    return np.sum(overlaps**2)*J

class FC_Hopfield:
    def __init__(self,patterns,starting_state=None):
        #make sure that patterns is all made of +1 or -1 values
        assert np.all(patterns==1 or patterns==-1)
        self.shape = patterns.shape
        if starting_state is not None:
            assert patterns.shape == starting_state.shape
        else:
            starting_state = np.random.choice([-1, 1], size=shape)

        self.state = squeeze(starting_state)
        self.patterns=squeeze(patterns)
        self.lenght=self.shape[0]*self.shape[1]

        self.overlaps=np.matmul(self.patterns,self.starting_state)
        self.J=-1
        self.energy=hopfield_energy(self.overlaps,self.J)

    
    def simulation_steps(self, temperature:float, n_steps:int)->np.array:
        for _ in range(n_steps):
            # Select a random site in the chain
            site = np.random.randint(0, self.lenght)

            # Calculate the energy change if we flip the spin at the selected site
            new_overlaps=self.overlaps-2*self.state[site]*self.patterns[:,site]
            new_energy=hopfield_energy(new_overlaps,self.J)

            delta_E=new_energy-self.energy

            if delta_E < 0 or np.random.rand() < np.exp(-delta_E / temperature):
                # Accept the flip with a certain probability
                self.state[site] *= -1
                self.energy = new_energy
                self.overlaps = new_overlaps