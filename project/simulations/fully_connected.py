import numpy as np  

def make_random_chain(len:int)->np.array:
    return np.random.randint(low=0,high=2,size=[1,len])==0


def energy_fully_connected(spin_sum:float, J:float)->float:
    return -J*(spin_sum)**2 

class FullyConnected:
    def __init__(self, len:int, starting_state:np.array=None):
        """This initialize the ising model class.

        the hamiltonian is -J\sum_ijs_is_j

        Args:
            len (int): _description_
            starting_state (np.array, optional): _description_. Defaults to None.
        """
        
        self.lenght = len
        if starting_state is not None:
            assert len==len(starting_state), "Starting state must be of length {}, got length {}".format(len,len(starting_state))
        else:
            starting_state = np.random.randint(low=0,high=2,size=[1,len])*2-1

        self.state=starting_state

        self.J=-1.0
        self.spin_sum = starting_state.sum()
        self.energy = energy_fully_connected(self.spin_sum, self.J)

    def simulation_steps(self, temperature, n_steps):
        for _ in range(n_steps):
            # Select a random site in the chain
            site = np.random.randint(0, self.length)

            # Calculate the energy change if we flip the spin at the selected site
            new_spin_sum = self.spin_sum - 2*self.state[0, site]
            new_energy= energy_fully_connected(new_spin_sum, self.J)

            delta_E = new_energy - self.energy

            if delta_E < 0 or np.random.rand() < np.exp(-delta_E / temperature):
                # Accept the flip with a certain probability
                self.state[0, site] *= -1
                self.energy = new_energy
                self.spin_sum = new_spin_sum

        return self.state == 1 #returns a bool array