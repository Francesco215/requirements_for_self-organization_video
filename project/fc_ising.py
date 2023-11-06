import math

from utils import *


def get_distance_between_centers(circles: VGroup, angles: np.array) -> float:
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
            stroke_color=BLACK,
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
        lines.add(Line(target_center, dst, color=BLACK, stroke_width=1))
    return lines


class Test(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)
        colors = np.random.choice([True, False], size=(100, 1))
        white_background = Rectangle(width=self.camera.frame_width, height=self.camera.frame_height, fill_color=WHITE, fill_opacity=1)
        circles = draw_circles(colors)
        lines = lines2circle(circles, 3)
        self.add(white_background, lines, circles)  # line should be before circles (to avoid crossing circle border)
        for _ in range(5):
            colors = np.random.choice([True, False], size=(100, 1))
            self.play(*update_colors(circles, colors))
            self.wait(1)


