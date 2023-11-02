from typing import Dict, List

from manim import *

"""
    Take this code as a rough blueprint, I have written it whithout using classes, but if you prefer to do it in a object oriented way feel free to do so
"""

Grid = Dict[str, VGroup]


def bool2direction(bool):
    return UP if bool else DOWN


def make_grid(starting_state: np.array) -> Grid:
    """This function creates the VMobject representing the grid

    It draws the grid of circles with the specified starting configuration.

    For each element of the grid, if the starting state is zero,
    then the arrow will point down, else it will point up

    Args:
        starting_state (np.array): the starting configuration of the grid. dtype=bool

    Returns:
        VGroup: the VM object representing the grid
    """

    rows, columns = starting_state.shape
    screen_width = config["frame_width"]
    screen_height = config["frame_height"]

    if columns > rows:
        bigger_dimension = columns
        screen_size = screen_width
    else:
        bigger_dimension = rows
        screen_size = screen_height

    radius = 1
    between_space = 0.2
    while bigger_dimension * (radius * 2) > (screen_size - (bigger_dimension * between_space)):
        radius -= 0.05

    circles = [Circle(color=BLUE, radius=radius) for _ in range(columns * rows)]
    circles_group = VGroup(*circles)
    circles_group.arrange_in_grid(rows, columns, buff=between_space)
    arrows_group = VGroup()
    for arrow_direction, circle in zip(starting_state.flatten(), circles):
        arrow = Arrow(start=ORIGIN, end=bool2direction(arrow_direction), buff=radius)
        arrow.shift(circle.get_center() - arrow.get_center())
        arrows_group.add(arrow)
    return {
        'circles': circles_group,
        'arrows': arrows_group
    }


def update_circle_grid(grid: Grid, new_state: np.array) -> List[Animation]:
    """It updates the grid made of circles and animates fluidly the transition of the arrows flipping over

    Args:
        grid (VGroup): the grid originally created with the MakeGrid function
        new_state (np.array): the new configuration of the grid

    Returns:
        VGroup: the updated grid
    """
    animations = []
    for arrow_direction, arrow in zip(new_state.flatten(), grid['arrows']):
        expected_direction = bool2direction(arrow_direction)
        actual_direction = arrow.get_unit_vector()
        if (expected_direction != actual_direction).any():
            animations.append(
                Rotate(arrow, angle=PI, run_time=2, rate_func=smooth)
            )
    return animations


class Test(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)

        starting_state = np.random.choice([True, False], size=(5, 10))
        grid = make_grid(starting_state)
        for group in grid.values():
            self.add(group)
        new_state = np.random.choice([True, False], size=(5, 10))
        animations = update_circle_grid(grid, new_state)
        self.play(*animations)
        self.wait(1)


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
    


