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
            side_length=circle.radius * 2 + grid['between_space'] + 0.01,
            stroke_width=0,
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


def add_boundaries(grid: Grid, stroke_width=2) -> list[Animation]:
    animations = []
    grid['boundaries'] = VGroup()
    def add(start, end):
        start2 = square.get_corner(start)
        end2 = square.get_corner(end)
        line = Line(
            start=start2,
            end=end2,
            color=hamiltonian_color,
            stroke_width=stroke_width
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
            add2 = lambda v, side: square2borders.setdefault(k, []).append((v, side))
            left, right, top, down = neighbours
            if left is None or left.color != square.color:
                add2(add(UP + LEFT, DOWN + LEFT), 'l')
            if right is None or right.color != square.color:
                add2(add(UP + RIGHT, DOWN + RIGHT), 'r')
            if top is None or top.color != square.color:
                add2(add(UP + LEFT, UP + RIGHT), 't')
            if down is None or down.color != square.color:
                add2(add(DOWN + LEFT, DOWN + RIGHT), 'd')
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


def create_paths(island_lines, idx, scene, debug):
    paths = []
    k = list(island_lines.keys())[0]
    square_id, line = island_lines[k][0]
    path = [line]
    head = as_key(line.get_start())
    remove_line((square_id, line), island_lines)
    while True:
        if head in island_lines:
            current_square_line = None
            for square_id2, line in island_lines[head]:
                if square_id2 == square_id:
                    current_square_line = line
                    break

            if current_square_line:
                line = current_square_line
            else:
                square_id, line = island_lines[head][0]

            remove_line((square_id, line), island_lines)
            if debug:
                number = Tex(str(idx), color=RED).scale(0.5)
                eq_position(number, line)
                scene.add(number)
                idx += 1
            path.append(line)
            if head == as_key(line.get_start()):
                head = as_key(line.get_end())
            else:
                head = as_key(line.get_start())
        elif not island_lines:
            paths.append(path)
            break
        else:
            # holes
            paths.append(path)
            paths += create_paths(island_lines, idx, scene, debug)
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


def get_intersection_point(line_1, line_2):
    common = set([as_key(line_1.get_start()), as_key(line_1.get_end())]).intersection(
        set([as_key(line_2.get_start()), as_key(line_2.get_end())])
    )
    return list(common)[0]


def find_corners(as_ones_and_zeros, square2borders):
    corners = []
    rows_num = len(as_ones_and_zeros)
    cols_num = len(as_ones_and_zeros[0])
    for i, row in enumerate(as_ones_and_zeros):
        for j, v in enumerate(row):
            if v == 1:
                squares_to_check = [
                    (0, {'white': (i - 1, j - 1), 'black': [(i - 1, j), (i, j - 1)]}),
                    (1, {'white': (i - 1, j + 1), 'black': [(i, j + 1), (i - 1, j)]}),
                    (2, {'white': (i + 1, j + 1), 'black': [(i, j + 1), (i + 1, j)]}),
                    (3, {'white': (i + 1, j - 1), 'black': [(i, j - 1), (i + 1, j)]})
                ]
                squares_to_check = [(idx, item) for idx, item in squares_to_check if item['white'][0] >= 0 and item['white'][1] >= 0 and item['white'][0] < rows_num and item['white'][1] < cols_num]
                tmp = []
                for idx, item in squares_to_check:
                    i2, j2 = item['white']
                    if as_ones_and_zeros[i2][j2] == 1 and all([as_ones_and_zeros[i3][j3] == 0 for i3, j3 in item['black']]):
                        tmp.append(idx)
                if tmp:
                    corners.append((i, j, tmp))

    corners2 = []
    for i, j, square_corners in corners:
        borders = square2borders[(i, j)]
        side2line = {}
        for line, side in borders:
            side2line[side] = line
        for corner in square_corners:
            if corner == 0:
                s1 = 'l'
                s2 = 't'
            elif corner == 1:
                s1 = 't'
                s2 = 'r'
            elif corner == 2:
                s1 = 'r'
                s2 = 'd'
            else:
                s1 = 'l'
                s2 = 'd'
            corners2.append(get_intersection_point(side2line[s1], side2line[s2]))
    return corners2


def shorten_line(start_or_end, line):
    start = line.get_start()
    end = line.get_end()
    s_x, s_y, _ = start
    e_x, e_y, _ = end
    delta = 0.13
    if s_x == e_x: # vertical line
        if start_or_end == 's':
            if s_y > e_y:
                start = np.array([s_x, s_y - delta, 0])
            else:
                start = np.array([s_x, s_y + delta, 0])
        else:
            if s_y > e_y:
                end = np.array([e_x, e_y + delta, 0])
            else:
                end = np.array([e_x, e_y - delta, 0])
    else:
        if start_or_end == 's':
            if s_x < e_x:
                start = np.array([s_x + delta, s_y, 0])
            else:
                start = np.array([s_x - delta, s_y, 0])
        else:
            if s_x < e_x:
                end = np.array([e_x - delta, e_y, 0])
            else:
                end = np.array([e_x + delta, e_y, 0])
    return Line(start, end)


def round_corners(path, corners):
    result = []
    prev = path[0]
    for curr in path[1:]:
        diag = []
        if as_key(prev.get_end()) in corners:
            if as_key(prev.get_end()) == as_key(curr.get_start()):
                prev = shorten_line('e', prev)
                curr = shorten_line('s', curr)
                diag.append(Line(prev.get_end(), curr.get_start()))
            elif as_key(prev.get_end()) == as_key(curr.get_end()):
                prev = shorten_line('e', prev)
                curr = shorten_line('e', curr)
                diag.append(Line(prev.get_end(), curr.get_end()))

        if as_key(prev.get_start()) in corners:
            if as_key(prev.get_start()) == as_key(curr.get_end()):
                prev = shorten_line('s', prev)
                curr = shorten_line('e', curr)
                diag.append(Line(prev.get_start(), curr.get_end()))
            elif as_key(prev.get_start()) == as_key(curr.get_start()):
                prev = shorten_line('s', prev)
                curr = shorten_line('s', curr)
                diag.append(Line(prev.get_start(), curr.get_start()))

        result.append(prev)
        result += diag
        prev = curr
    result.append(curr)
    return result


def tracking_boundaries(grid, scene):
    _, square2borders = add_boundaries(grid)
    islands, as_ones_and_zeros = find_islands(grid)
    debug = False

    corners = find_corners(as_ones_and_zeros, square2borders)
    if debug:
        for point in corners:
            dot = Dot(color=GREEN)
            dot.move_to(point)
            scene.add(dot)

    how_many = None
    if debug:
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
        square_id = 0
        for square in island:
            borders = square2borders.get(square)
            if borders is None:
                continue
            for line, _ in borders:
                lines.setdefault(as_key(line.get_start()), []).append((square_id, line))
                lines.setdefault(as_key(line.get_end()), []).append((square_id, line))
            square_id += 1
        islands_grouped_by_lines.append(lines)

    paths = []
    for island_lines in islands_grouped_by_lines:
        paths += create_paths(island_lines, 1, scene, debug)

    idx2dot = {}
    steps = {}
    for idx, path in enumerate(paths[:how_many]):
        path2 = VMobject(color=hamiltonian_color)
        dot = Dot(color=hamiltonian_color)

        if debug:
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
        path = connect_lines(path)
        path = round_corners(path, corners)
        for step, line in enumerate(path):
            if current_position != as_key(line.get_start()):
                move_to = line.get_start()
            else:
                move_to = line.get_end()
            steps.setdefault(step, []).append((idx, move_to))
            current_position = as_key(move_to)
        idx2dot[idx] = dot

    removed_dots = []
    for k in sorted(steps.keys()):
        step = steps[k]
        tmp = []
        used_dots = []
        for idx, move_to in step:
            anim = idx2dot[idx].animate.move_to(move_to)
            tmp.append(anim)
            used_dots.append(idx)
        scene.play(*tmp, rate_func=linear, run_time=0.5)
        dots_to_remove = set(idx2dot.keys()) - set(used_dots) - set(removed_dots)
        for idx in dots_to_remove:
            scene.remove(idx2dot[idx])
            removed_dots.append(idx)
    for idx in used_dots:
        scene.remove(idx2dot[idx])