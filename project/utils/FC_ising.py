import math


from manim import *
from .utils import *
from .GLOBAL_VALUES import *




def get_distance_between_centers(circles: VGroup|list, angles: np.array) -> float:
    assert len(circles) >= 2

    x1, y1, _ = circles[0].get_center()
    x2, y2, _ = circles[1].get_center()
    radii = circles[0].radius
    while math.sqrt((x2 - x1) ** 2 + (y2 - y1)**2) < circles[0].radius * 2:
        radii += 0.1
        for circle, angle in zip(circles[0:2], angles):
            circle.move_to(radii * np.array([np.cos(angle), np.sin(angle), 0]))
        x1, y1, _ = circles[0].get_center()
        x2, y2, _ = circles[1].get_center()
    return radii


def draw_circles(state: np.array) -> VGroup:
    num_circles = len(state)
    assert num_circles == 100  # change raidus if number is different
    radius = 0.115
    circles = VGroup()
    for color in state.flatten():
        circles.add(Circle(
            radius=radius,
            stroke_width=1,
            stroke_color=WHITE,
            fill_color=bool2color(color),
            fill_opacity=1,
        ))
    angles = np.linspace(0, 2 * PI, num_circles, endpoint=False)
    radii = [get_distance_between_centers(circles, angles)] * num_circles
    for circle, angle, r in zip(circles, angles, radii):
        circle.move_to(r * np.array([np.cos(angle), np.sin(angle), 0]))
    return circles


def pick_alpha(target_center, dst, distance):
    direction_vector = dst - target_center
    normalized_direction = direction_vector / np.linalg.norm(direction_vector)
    end = target_center + normalized_direction * distance
    alpha = np.linalg.norm(end - target_center) / np.linalg.norm(direction_vector)
    return alpha


def lines2circle(circles: VGroup, target_idx: int) -> VGroup:
    target = circles[target_idx]
    target_center = target.get_center()
    lines = VGroup()
    destinations = []
    create = []
    uncreate = []
    travel_distance = []
    for i, circle in enumerate(circles):
        if i == target_idx:
            continue
        dst = circle.get_center()
        destinations.append(dst)
        end = interpolate(target_center, dst, pick_alpha(target_center, dst, 0.5))
        line = Line(target_center, end, color=hamiltonian_color, stroke_width=1)
        travel_distance.append(np.linalg.norm(target_center - dst) - 2 * line.get_length())
        lines.add(line)
        create.append(Create(line))
        uncreate.append(Uncreate(line))

    return lines, destinations, create, uncreate

