import math

from utils.utils import bool2color
from utils.GLOBAL_VALUES import hamiltonian_color

from manim import *


def serpentine(i, nSH):
    if i < nSH:
        return [i, 0]
    if i == nSH:
        return [nSH - 1, 1]
    if i <= 2 * nSH:
        return [2 * nSH-i, 2]
    if i == 2 * nSH + 1:
        return [0, 3]

    recursive = serpentine(i % (2 * (nSH + 1)), nSH)
    recursive[1] += 4 * math.floor(i / (2 * nSH + 2))
    return recursive


def create_snake(spins, scene, numSpinsHorizontal, raidus, stroke_width, space_between):
    group = VGroup()
    diameter = raidus * 2
    prev_circle = None
    for i, spin in enumerate(spins):
        color = bool2color(spin)
        x, y = serpentine(i, numSpinsHorizontal)
        x *= (diameter + space_between)
        y *= (diameter + space_between)
        circle = Circle(
            radius=raidus,
            stroke_width=stroke_width,
            stroke_color=hamiltonian_color,
            fill_color=color,
            fill_opacity=1,
        )
        circle.move_to([x, y, 0])
        group.add(circle)
        if prev_circle:
            group.add(Line(
                prev_circle.get_center(),
                circle.get_center(),
                stroke_width=stroke_width,
                stroke_color=hamiltonian_color,
                z_index=-1
            ))
        prev_circle = circle
    center_of_scene = scene.camera.frame_center
    shift_vector = center_of_scene - group.get_center()
    group.shift(shift_vector)
    return group


def update_snake_colors(snake, spins):
    circles = [item for item in snake if isinstance(item, Circle)]
    animations = []
    for obj, state in zip(circles, spins):
        color = bool2color(state)
        if obj.color != color:
            animations.append(obj.animate.set_fill(color))
    return animations


class SnakeIsing(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)
        spins = np.random.randint(2, size=50)
        snake = create_snake(spins, self, 10, 0.3, 2, 0.05)
        self.play(Create(snake))
        for _ in range(4):
            spins = np.random.randint(2, size=50)
            anims = update_snake_colors(snake, spins)
            self.play(*anims)
        self.wait(2)