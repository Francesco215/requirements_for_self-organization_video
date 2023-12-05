import numpy as np  


def general_energy(state, W, J):
    return J*np.dot(state.T, W @ state)

class GeneralIsing:
    def __init__(self, lenght:int, connectivity_matrix:np.array, starting_state:np.array=None):
        """This initialize the ising model class.

        the hamiltonian is -J\sum_ijs_is_j

        Args:
            len (int): the number of elements in the ising model 
            connectivity_matrix: the connectivity matrix, dtype=np.bool, shape: (len,len)
            starting_state (np.array, optional): The starting state. only valid values are +1 or -1
        """
        
        self.length = lenght
        self.W = connectivity_matrix
        assert self.W.shape==(lenght,lenght)
         
        if starting_state is not None:
            assert lenght==lenght(starting_state), "Starting state must be of length {}, got length {}".format(lenght,lenght(starting_state))
        else:
            starting_state = np.random.randint(low=0,high=2,size=(lenght))*2-1

        self.state=starting_state

        self.J=-1.0
        self.spin_sum = starting_state.sum()
        self.energy = general_energy(self.state, self.W, self.J) 

    def __len__(self):
        return self.length

    def simulation_steps(self, temperature:float, n_steps:int)->np.array:
        for _ in range(n_steps):
            # Select a random site in the chain
            site = np.random.randint(0, self.length)

            # Calculate the energy change if we flip the spin at the selected site
            new_state=np.copy(self.state)
            new_state[site]*=-1
            new_energy= general_energy(new_state,self.W,self.J)

            delta_E = new_energy - self.energy

            if delta_E < 0 or np.random.rand() < np.exp(-delta_E / temperature):
                # Accept the flip with a certain probability
                self.state[site] *= -1
                self.energy = new_energy

        return self.state == 1 #returns a bool array


