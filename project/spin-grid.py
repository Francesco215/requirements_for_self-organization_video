import numpy as np

from manim import VMobject

"""
    Take this code as a rough blueprint, I have written it whithout using classes, but if you prefer to do it in a object oriented way feel free to do so
"""


def MakeGrid(starting_state:np.array) -> VMobject:
    """This function creates the VMobject representing the grid
    
    It draws the grid of circles with the specified starting configuration.

    For each element of the grid, if the starting state is zero,
    then the arrow will point down, else it will point up

    Args:
        starting_state (np.array): the starting configuration of the grid. dtype=bool 

    Returns:
        VMobject: the VM object representing the grid
    """


def UpdateCircleGrid(grid:VMobject, new_state:np.array) -> VMobject:
    """It updates the grid made of circles and animates fluidly the transition of the arrows flipping over

    Args:
        grid (VMobject): the grid originally created with the MakeGrid function
        new_state (np.array): the new configuration of the grid

    Returns:
        VMobject: the updated grid
    """

def CirclesToSquares(grid:VMobject) -> VMobject:
    """It turns the grid made of circles and arrows in to a square grid similar to the one in the website
    It animates fluidly the transition.

    If the element of the state configuration is equal to 0, the color of the square must be black,
    else it must be white.

    So, circles with the arrow pointing down will turn into black squares
    and circles with arrow pointing up will turno int o white squares.
    

    Args:
        grid (VMobject): the grid

    Returns:
        VMobject: the updated grid
    """    

def UpdateSquareGrid(grid:VMobject, new_state:np.array) -> VMobject:
    """It updates the grid made of squares and animates the transition of the squares changing color

    Args:
        grid (VMobject): the grid originally created with the MakeGrid function
        new_state (np.array): the new configuration of the grid

    Returns:
        VMobject: the updated grid
    """
    


