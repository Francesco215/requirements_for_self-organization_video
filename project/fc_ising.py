import math

from manim import *

from utils.GLOBAL_VALUES import * 
from utils.utils import *


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


from simulations.fully_connected import FC_Ising

ising=FC_Ising(100)

class FullyConnected(Scene):
    def construct(self):
        colors = ising.state==1
        circles = draw_circles(colors).shift(2*LEFT)
        self.play(Create(circles))
        for _ in range(5):
            idx=np.random.randint(0,len(circles))
            lines, destinations, create, uncreate = lines2circle(circles, idx)
            # maby pick other run_time to make animation smoother
            self.play(*create, run_time=0.2, rate_func=linear)
            flying = []
            for line, dst in zip(lines, destinations):
                flying.append(line.animate.shift(dst - line.get_end()))
            self.play(*flying, run_time=0.5, rate_func=linear)

            for line in lines:
                start_point = line.get_start()
                end_point = line.get_end()
                line.put_start_and_end_on(end_point, start_point)

            self.play(*uncreate, run_time=0.1, rate_func=linear)
        hamiltonian=MathTex('H','=J\sum_{i,j}','s_is_j').shift(4*RIGHT,2*UP)
        hamiltonian[0].set_color(hamiltonian_color)
        hamiltonian[2].set_color(spin_color)

        self.play(Write(hamiltonian))
        self.play(Wiggle(hamiltonian[2]))

        slider=Line(start=5*RIGHT+2.6*DOWN,end=5*RIGHT+0.4*UP)

        pointer=Triangle().scale(0.2).set_stroke(width=0.2).rotate(-90*DEGREES).set_fill(color=temperature_color,opacity=1)
        temp_tex=MathTex('T').next_to(pointer,LEFT).set_color(temperature_color)

        pointer_position=4.5*RIGHT+0.2*UP
        t_pointer=VGroup(pointer,temp_tex).move_to(pointer_position)

        self.play(Create(slider))
        self.play(Create(pointer),Write(temp_tex))

        for t in np.linspace(-10, 10, 1000):
            temperature = logistic(t, start_value=2., end_value=.9, transition_speed=1)
            pointer_movement = t_pointer.animate.move_to(logistic(t, end_value=pointer_position+2.6*DOWN, start_value=pointer_position, transition_speed=1))
            colors = ising.simulation_steps(temperature, 5)

            # Use there rate_func to control the animation substeps
            self.play(pointer_movement, *update_colors(circles, colors), run_time=0.1, rate_func=linear)





