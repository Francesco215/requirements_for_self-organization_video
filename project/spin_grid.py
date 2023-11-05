import random
from typing import Dict

from manim import *

from GLOBAL_VALUES import spin_color, hamiltonian_color, circle_fill_color, circle_fill_opacity

"""
    Take this code as a rough blueprint, I have written it whithout using classes, but if you prefer to do it in a object oriented way feel free to do so
"""

Grid = dict[str, VGroup]


def bool2direction(bool):
    return UP if bool else DOWN

def bool2color(bool):
    return WHITE if bool else BLACK


def eq_position(src, dst):
    src.shift(dst.get_center() - src.get_center())


def make_grid(starting_state: np.array, scene: Scene) -> Grid:
    """This function creates the VMobject representing the grid

    It draws the grid of circles with the specified starting configuration.

    For each element of the grid, if the starting state is zero,
    then the arrow will point down, else it will point up

    Args:
        starting_state (np.array): the starting configuration of the grid. dtype=bool

    Returns:
        dict[VMobject]: A dictionary containing the grid, arrows and labels 

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

    circles = [Circle(color=BLUE, radius=radius, fill_color=circle_fill_color, fill_opacity=circle_fill_opacity) for _ in range(columns * rows)]
    circles_group = VGroup(*circles)
    circles_group.arrange_in_grid(rows, columns, buff=between_space)
    arrows_group = VGroup()
    for arrow_direction, circle in zip(starting_state.flatten(), circles):
        arrow = Arrow(start=ORIGIN, end=bool2direction(arrow_direction)*radius, buff=radius, color=spin_color)
        eq_position(arrow, circle)
        arrows_group.add(arrow)

    return {
        'circles': circles_group,
        'arrows': arrows_group,
        'between_space': between_space
    }


def update_circle_grid(grid: Grid, new_state: np.array, scene: Scene, random_rotation=True)->list[Animation]:
    """It updates the grid made of circles and animates fluidly the transition of the arrows flipping over

    Args:
        grid (VGroup): the grid originally created with the MakeGrid function
        new_state (np.array): the new configuration of the grid. dtype=bool

    Returns:
        list[Animation]: a list of animations to be played in the scene
    """
    animations = []
    for arrow_direction, arrow in zip(new_state.flatten(), grid['arrows']):
        expected_direction = bool2direction(arrow_direction)
        actual_direction = arrow.get_unit_vector()
        if np.dot(expected_direction, actual_direction)<0:
            clockwise_or_not = 1 if random.choice([True, False]) and random_rotation else -1
            animations.append(
                Rotate(arrow, angle=PI * clockwise_or_not, run_time=2, rate_func=smooth)
            )
    return animations


def circles_to_squares(grid: Grid, scene: Scene):
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
    animations = []
    squares = []
    for circle, arrow in zip(grid['circles'], grid['arrows']):
        if (arrow.get_unit_vector() == UP).all():
            color = WHITE
        else:
            color = BLACK
        square = Square(
            color=color,
            side_length=circle.radius * 2 + grid['between_space'],
            fill_color=color,
            fill_opacity=1
        )
        squares.append(square)
        eq_position(square, circle)
        animations.append(Transform(circle, square, rate_func=smooth, run_time=3))
    grid['squares'] = squares
    scene.play(*animations)
    arrows_fade_out = []
    for arrow in grid['arrows']:
        arrows_fade_out.append(FadeOut(arrow, run_time=1))
    scene.play(*arrows_fade_out)


def update_square_grid(grid: Grid, new_state: np.array, scene: Scene)->list[Animation]:
    """It updates the grid made of squares and animates the transition of the squares changing color

    Args:
        grid (VMobject): the grid originally created with the MakeGrid function
        new_state (np.array): the new configuration of the grid

    Returns:
        list[Animation]: the list of animations
    """
    animations = []
    for square, state in zip(grid['squares'], new_state.flatten()):
        color = bool2color(state)
        if square.color != color:
            animations.append(ApplyMethod(square.set_color, color, rate_func=smooth, run_time=3))
    return animations


class Test(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)

        starting_state = np.random.choice([True, False], size=(5, 10))
        grid = make_grid(starting_state, self)
        self.wait(1)
        new_state = np.random.choice([True, False], size=(5, 10))
        update_circle_grid(grid, new_state, self)
        self.wait(1)
        circles_to_squares(grid, self)
        self.wait(1)
        new_state2 = np.random.choice([True, False], size=(5, 10))
        self.animate(*update_square_grid(grid, new_state2, self))
        self.wait(1)