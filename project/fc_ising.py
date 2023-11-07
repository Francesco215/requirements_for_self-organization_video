import math

from manim import *

from utils import *
from GLOBAL_VALUES import hamiltonian_color, spin_color



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


def lines2circle(circles: VGroup, target_idx: int) -> VGroup:
    target = circles[target_idx]
    target_center = target.get_center()
    lines = VGroup()
    for i, circle in enumerate(circles):
        if i == target_idx:
            continue
        dst = circle.get_center()
        lines.add(Line(target_center, dst, color=hamiltonian_color, stroke_width=1))
    return lines

def LaserBullets(circles: VGroup, target_idx:int) -> Animation:
    lines=lines2circle(circles,target_idx)
    return [Create(line) for line in lines], [Uncreate(line, reverse=False) for line in lines] #the reverse arguements seems to do nothing




class FullyConnected(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)
        colors = np.random.choice([True, False], size=(100, 1))
        # white_background = Rectangle(width=self.camera.frame_width, height=self.camera.frame_height, fill_color=WHITE, fill_opacity=1)
        circles = draw_circles(colors)
        self.play(Create(circles))  # line should be before circles (to avoid crossing circle border)
        for _ in range(5):
            idx=np.random.randint(0,len(circles))
            make_bullets,disappear_bullets=LaserBullets(circles,idx)
            self.play(*make_bullets)  # line should be before circles (to avoid crossing circle border)
            self.play(*disappear_bullets, run_time=0.5)  # line should be before circles (to avoid crossing circle border)

        hamiltonian=MathTex('H','=J\sum_{i,j}','s_is_j')
        hamiltonian[0].set_color(hamiltonian_color)
        hamiltonian[2].set_color(spin_color)

        self.play(Write(hamiltonian))

        for _ in range(5):
            colors = np.random.choice([True, False], size=(100, 1))
            self.play(*update_colors(circles, colors),run_time=0.1)
            self.wait(0.3)