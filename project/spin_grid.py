import random

from manim import *

from GLOBAL_VALUES import spin_color, hamiltonian_color, circle_fill_color, circle_fill_opacity
from utils import bool2direction, update_colors2

"""
    Take this code as a rough blueprint, I have written it whithout using classes, but if you prefer to do it in a object oriented way feel free to do so
"""

Grid = dict[str, VGroup]


def eq_position(src, dst):
    src.shift(dst.get_center() - src.get_center())


def make_grid(starting_state: np.array, scene: Scene, radius=None) -> Grid:
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
    between_space = 0.2

    if radius is None:
        screen_width = config["frame_width"]
        screen_height = config["frame_height"]

        if columns > rows:
            bigger_dimension = columns
            screen_size = screen_width
        else:
            bigger_dimension = rows
            screen_size = screen_height
        radius = 1
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
        'between_space': between_space,
        'shape': starting_state.shape
    }


def update_circle_grid(grid: Grid, new_state: np.array, random_rotation=True)->list[Animation]:
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
            stroke_width=2,
            stroke_color=color,
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


def get_neighbours(objects: list[Mobject], shape):
    rows, columns = shape
    idx = 0
    table = []
    for _ in range(rows):
        row = []
        for _ in range(columns):
            row.append(objects[idx])
            idx += 1
        table.append(row)

    result = []
    for row_idx, row in enumerate(table):
        for col_idx, val in enumerate(row):
            if col_idx == 0:
                left = None
            else:
                left = table[row_idx][col_idx - 1]
            if col_idx == (columns - 1):
                right = None
            else:
                right = table[row_idx][col_idx + 1]
            if row_idx == 0:
                top = None
            else:
                top = table[row_idx - 1][col_idx]
            if row_idx == (rows - 1):
                down = None
            else:
                down = table[row_idx + 1][col_idx]
            result.append((left, right, top, down))
    return result


def add_boundaries(grid: Grid) -> list[Animation]:
    animations = []
    grid['boundaries'] = VGroup()
    def add(start, end):
        line = Line(
            start=square.get_corner(start),
            end=square.get_corner(end),
            color=hamiltonian_color,
            stroke_width=2
        )
        grid['boundaries'].add(line)
        animations.append(Create(line))

    for square, neighbours in zip(grid['squares'], get_neighbours(grid['squares'], grid['shape'])):
        left, right, top, down = neighbours
        if left is None or left.color != square.color:
            add(UP + LEFT, DOWN + LEFT)
        if right is None or right.color != square.color:
            add(UP + RIGHT, DOWN + RIGHT)
        if top is None or top.color != square.color:
            add(UP + LEFT, UP + RIGHT)
        if down is None or down.color != square.color:
            add(DOWN + LEFT, DOWN + RIGHT)

    return animations


def zoom_out(grid) -> list[Animation]:
    zoom_out = []
    for obj in grid.values():
        if isinstance(obj, VGroup):
            zoom_out.append(obj.animate.scale(0.2))
    return zoom_out


class Test(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)

        size = (40, 80)
        starting_state = np.random.choice([True, False], size=size)
        grid = make_grid(starting_state, self, radius=0.5)
        self.wait(1)
        new_state = np.random.choice([True, False], size=size)
        update_circle_grid(grid, new_state)
        self.wait(1)
        circles_to_squares(grid, self)
        self.wait(1)
        new_state2 = np.random.choice([True, False], size=size)
        anims = update_colors2(grid, 'squares', new_state2)
        self.play(*anims)
        self.play(*add_boundaries(grid))
        self.play(*zoom_out(grid), run_time=5)
        self.wait(1)