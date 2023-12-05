import math


from manim import *
from .utils import *
from .GLOBAL_VALUES import *
from .attention import calc_radius


def polar(angle):
    return np.array([np.cos(angle),np.sin(angle),0])

def draw_circles(state: np.array, big_radius=5) -> VGroup:
    num_circles = len(state)
    angles = np.linspace(0, 2 * PI, num_circles, endpoint=False)
    circles = VGroup()

    small_radius=big_radius/calc_radius(1,num_circles,0.3)

    for color, angle in zip(state.flatten(), angles):
        circles.add(Circle(
                radius=small_radius,
                stroke_width=1,
                stroke_color=WHITE,
                fill_color=bool2color(color),
                fill_opacity=1,
            ).move_to(big_radius*polar(angle))
        )
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

def connect_circles(circles,connectivity_matrix):
    lines=VGroup()
    for i in range(len(connectivity_matrix)):
        for j in range(len(connectivity_matrix)):
            if connectivity_matrix[i][j]==1:
                lines.add(Line(circles[i].get_center(),circles[j].get_center(), stroke_color=hamiltonian_color, z_index=-1))
    return lines.set_z_index(-1)