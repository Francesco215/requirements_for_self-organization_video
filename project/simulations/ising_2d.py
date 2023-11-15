import numpy as np

def energy_2D_ising(state: np.array, J: float) -> float:
    """
    Calculate the energy of a 2D Ising model state.
    :param state: 2D array representing the Ising model configuration (-1 or 1 spins)
    :param J: Interaction strength (positive for ferromagnetic, negative for antiferromagnetic)
    :return: Energy of the system
    """
    neighbors_sum = np.roll(state, 1, axis=0) + np.roll(state, -1, axis=0) + \
                    np.roll(state, 1, axis=1) + np.roll(state, -1, axis=1)
    return -J * np.sum(state * neighbors_sum)


class Ising2D:


    def __init__(self, shape, starting_state=None):
        """
            Represents a 2D Ising model simulation.

            Parameters:
            - shape (tuple): The shape of the 2D lattice.
            - starting_state (numpy.ndarray, optional): The initial state of the lattice. If not provided,
            a random configuration will be generated.
            
            Attributes:
            - shape (tuple): The shape of the 2D lattice.
            - state (numpy.ndarray): The current state of the lattice.
            - J (float): Interaction strength parameter.
            - energy (float): The total energy of the system.

            Methods:
            - simulation_steps(temperature: float, n_steps: int) -> numpy.ndarray:
            Performs Monte Carlo simulation steps on the Ising model for a given number of steps and temperature.
            Returns the updated state after the simulation.
        """
        self.shape = shape
        if starting_state is not None:
            assert shape == starting_state.shape
        else:
            starting_state = np.random.choice([-1, 1], size=shape)

        self.state = starting_state
        self.J = -np.log(1 + np.sqrt(2)) / 2
        self.energy = energy_2D_ising(starting_state, self.J)

    def simulation_steps(self, temperature: float, n_steps: int) -> np.ndarray:
        """
            Perform Monte Carlo simulation steps on the Ising model.

            Parameters:
            - temperature (float): The temperature of the system.
            - n_steps (int): The number of simulation steps to perform.

            Returns:
            - numpy.ndarray: The updated state after the simulation.
        """
        for _ in range(n_steps):
            i, j = np.random.randint(self.shape)
            delta_energy = -2 * self.J * self.state[i, j] * (
                    self.state[(i + 1) % self.shape[0], j] + self.state[(i - 1) % self.shape[0], j] + \
                    self.state[i, (j + 1) % self.shape[1]] + self.state[i, (j - 1) % self.shape[1]])
            if delta_energy < 0 or np.random.rand() < np.exp(-delta_energy / temperature):
                # Accept the new state with a probability related to the change in energy
                self.state[i,j] *= -1
                self.energy += delta_energy

        return self.state