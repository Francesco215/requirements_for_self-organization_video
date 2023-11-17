import numpy as np
from manim import *
from functools import partial

Grid = dict[str, VGroup]
from .GLOBAL_VALUES import *
from .utils import bool2color, bool2direction
import random

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

    circles = [Circle(radius=radius, fill_color=circle_fill_color, fill_opacity=circle_fill_opacity) for _ in range(columns * rows)]
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
    squares = VGroup()
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
        squares.add(square)
        eq_position(square, circle)
        animations.append(Transform(circle, square, rate_func=smooth, run_time=3))
    grid['squares'] = squares
    scene.play(*animations)
    arrows_fade_out = []
    for arrow in grid['arrows']:
        arrows_fade_out.append(FadeOut(arrow, run_time=1))
    scene.play(*arrows_fade_out)


def restore_shape(ls, shape):
    rows, columns = shape
    idx = 0
    table = []
    for _ in range(rows):
        row = []
        for _ in range(columns):
            row.append(ls[idx])
            idx += 1
        table.append(row)
    return table


def get_neighbours(objects: list[Mobject], shape):
    rows, columns = shape
    table = restore_shape(objects, shape)

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
        start2 = square.get_corner(start)
        end2 = square.get_corner(end)
        line = Line(
            start=start2,
            end=end2,
            color=hamiltonian_color,
            stroke_width=2
        )
        grid['boundaries'].add(line)
        animations.append(Create(line))
        return line

    squares_as_table = restore_shape(grid['squares'], grid['shape'])
    neighbours_as_table = restore_shape(get_neighbours(grid['squares'], grid['shape']), grid['shape'])
    square2borders = {}
    for x, (squares_row, neighbours_row) in enumerate(zip(squares_as_table, neighbours_as_table)):
        for y, (square, neighbours) in enumerate(zip(squares_row, neighbours_row)):
            k = (x, y)
            add2 = lambda v: square2borders.setdefault(k, []).append(v)
            left, right, top, down = neighbours
            if left is None or left.color != square.color:
                add2(add(UP + LEFT, DOWN + LEFT))
            if right is None or right.color != square.color:
                add2(add(UP + RIGHT, DOWN + RIGHT))
            if top is None or top.color != square.color:
                add2(add(UP + LEFT, UP + RIGHT))
            if down is None or down.color != square.color:
                add2(add(DOWN + LEFT, DOWN + RIGHT))
    return animations, square2borders


def zoom_out(grid, scale) -> list[Animation]:
    zoom_out = []
    for k in grid.keys():
        group = grid[k]
        if not isinstance(group, VGroup):
            continue

        anim = group.animate.scale(scale)
        zoom_out.append(anim)
        grid[k] = anim.mobject
    return zoom_out


def dfs(grid, row, col, visited, island):
    if row < 0 or col < 0 or row >= len(grid) or col >= len(grid[0]) or visited[row][col] or grid[row][col] == 0:
        return

    visited[row][col] = True
    island.append((row, col))

    dfs(grid, row + 1, col, visited, island)
    dfs(grid, row - 1, col, visited, island)
    dfs(grid, row, col + 1, visited, island)
    dfs(grid, row, col - 1, visited, island)


def find_islands(grid):
    table = restore_shape(grid['squares'], grid['shape'])
    as_ones_and_zeros = []
    for row in table:
        tmp = []
        for square in row:
            if square.color.get_hex_l().upper() == WHITE:
                tmp.append(1)
            else:
                tmp.append(0)
        as_ones_and_zeros.append(tmp)
    grid = as_ones_and_zeros

    if not grid:
        return []

    rows, cols = len(grid), len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    islands = []

    for row in range(rows):
        for col in range(cols):
            if not visited[row][col] and grid[row][col] == 1:
                island = []
                dfs(grid, row, col, visited, island)
                islands.append(island)

    return islands, as_ones_and_zeros


def remove_line(line, storage):
    keys_to_remove = []
    for k in storage.keys():
        v = storage[k]
        try:
            v.remove(line)
        except:
            pass
        if not v:
            keys_to_remove.append(k)
    for k in keys_to_remove:
        del storage[k]


def as_key(start_or_end):
    r = []
    for v in start_or_end:
        r.append(round(v, 1))
    return tuple(r)


def create_paths(island_lines):
    paths = []
    k = list(island_lines.keys())[0]
    line = island_lines[k][0]
    path = [line]
    remove_line(line, island_lines)
    while True:
        start = as_key(line.get_start())
        end = as_key(line.get_end())
        if start in island_lines:
            line = island_lines[start][0]
            remove_line(line, island_lines)
            path.append(line)
        elif end in island_lines:
            line = island_lines[end][0]
            remove_line(line, island_lines)
            path.append(line)
        elif not island_lines:
            paths.append(path)
            break
        else:
            # holes
            paths.append(path)
            paths += create_paths(island_lines)
            break
    return paths


def connect_lines(path):
    prev = path[0]
    result = []
    for curr in path[1:]:
        s_x_1, s_y_1, _ = prev.get_start()
        e_x_1, e_y_1, _ = prev.get_end()
        s_x_2, s_y_2, _ = curr.get_start()
        e_x_2, e_y_2, _ = curr.get_end()
        case_1 = round(s_x_1, 1) == round(s_x_2, 1) and round(e_x_1, 1) == round(e_x_2, 1)
        case_2 = round(s_y_1, 1) == round(s_y_2, 1) and round(e_y_1, 1) == round(e_y_2, 1)
        if case_1 or case_2:
            if as_key(prev.get_start()) == as_key(curr.get_end()):
                prev = Line(prev.get_end(), curr.get_start())
            elif as_key(prev.get_end()) == as_key(curr.get_start()):
                prev = Line(prev.get_start(), curr.get_end())
            elif as_key(prev.get_start()) == as_key(curr.get_start()):
                prev = Line(prev.get_end(), curr.get_end())
            elif as_key(prev.get_end()) == as_key(curr.get_end()):
                prev = Line(prev.get_start(), curr.get_start())
        else:
            result.append(prev)
            prev = curr
    result.append(prev)
    return result


def tracking_boundaries(grid, scene):
    _, square2borders = add_boundaries(grid)
    islands, as_ones_and_zeros = find_islands(grid)

    how_many = None
    if how_many is not None:
        as_ones_and_zeros2 = []
        for row in as_ones_and_zeros:
            tmp = []
            for v in row:
                if v == 0:
                    tmp.append(10)
                else:
                    tmp.append(v)
            as_ones_and_zeros2.append(tmp)
        idx = 11
        for island in islands:
            for i, j in island:
                as_ones_and_zeros2[i][j] = idx
            idx += 1

    islands_grouped_by_lines = []
    for island in islands:
        lines = {}
        for square in island:
            borders = square2borders.get(square)
            if borders is None:
                continue
            for line in borders:
                lines.setdefault(as_key(line.get_start()), []).append(line)
                lines.setdefault(as_key(line.get_end()), []).append(line)
        islands_grouped_by_lines.append(lines)

    paths = []
    for island_lines in islands_grouped_by_lines:
        paths += create_paths(island_lines)

    idx2dot = {}
    steps = {}
    for idx, path in enumerate(paths[:how_many]):
        path2 = VMobject(color=hamiltonian_color)
        dot = Dot(color=hamiltonian_color)

        if how_many is not None:
            for l in path:
                l.color = GREEN
                scene.add(l)

        line1 = path[0]
        line2 = path[1]
        if as_key(line1.get_start()) != as_key(line2.get_start()) and as_key(line1.get_start()) != as_key(line2.get_end()):
            init_position = line1.get_start()
        else:
            init_position = line1.get_end()

        dot.move_to(init_position)
        path2.set_points_as_corners([dot.get_center(), dot.get_center()])
        scene.add(path2, dot)

        def update_path(dot, path3):
            previous_path = path3.copy()
            previous_path.add_points_as_corners([dot.get_center()])
            path3.become(previous_path)

        path2.add_updater(partial(update_path, dot))

        current_position = as_key(init_position)
        for step, line in enumerate(connect_lines(path)):
            if current_position != as_key(line.get_start()):
                move_to = line.get_start()
            else:
                move_to = line.get_end()
            steps.setdefault(step, []).append((idx, move_to))
            current_position = as_key(move_to)
        idx2dot[idx] = dot

    for k in sorted(steps.keys()):
        step = steps[k]
        tmp = []
        for idx, move_to in step:
            anim = idx2dot[idx].animate.move_to(move_to)
            tmp.append(anim)

        scene.play(*tmp, rate_func=linear, run_time=0.5)