import math
from simulations.ising_general import GeneralIsing
from utils.matrix_maker import big_diag

from utils.utils import bool2color, logistic
from utils.GLOBAL_VALUES import hamiltonian_color, spin_color, temperature_color

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
    recursive[1] += 4 * (i // (2 * nSH + 2))
    return recursive


def create_snake(spins, scene, numSpinsHorizontal, raidus, stroke_width, space_between, segment_width):
    group = VGroup()
    circles=VGroup()
    lines=VGroup()
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
            stroke_color=WHITE,
            fill_color=color,
            fill_opacity=1,
        )
        circle.move_to([x, y, 0])
        group.add(circle)
        circles.add(circle)
        if prev_circle:
            line=Line(
                prev_circle.get_center(),
                circle.get_center(),
                stroke_width=segment_width,
                stroke_color=hamiltonian_color,
                z_index=-1
            )
            group.add(line)
            lines.add(line).set_z_index(-1)
        prev_circle = circle
    center_of_scene = scene.camera.frame_center
    shift_vector = center_of_scene - group.get_center()
    group.shift(shift_vector)
    return group,circles,lines


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
        n_ising_spins=50
        spins = np.random.randint(2, size=n_ising_spins)

        snake,cicles,lines = create_snake(spins, self, 10, 0.3, 2, 0.15,7)
        snake.shift(LEFT)
        self.play(Create(cicles))
        self.wait()
        
        hamiltonian=MathTex('H','=-J\sum_i','s_is_{i+1}').shift(3.5*RIGHT+2.7*UP)
        hamiltonian[0].set_color(hamiltonian_color)
        hamiltonian[2].set_color(spin_color)

        self.play(Write(hamiltonian))
        self.play(Create(lines))
        self.wait()



        slider=Line(start=5*RIGHT+2.6*DOWN,end=5*RIGHT+0.4*UP)

        pointer=Triangle().scale(0.2).set_stroke(width=0.2).rotate(-90*DEGREES).set_fill(color=temperature_color,opacity=1)
        temp_tex=MathTex('T').next_to(pointer,LEFT).set_color(temperature_color)

        pointer_position=4.5*RIGHT+0.2*UP
        t_pointer=VGroup(pointer,temp_tex).move_to(pointer_position)

        self.play(Create(slider))
        self.play(Create(pointer),Write(temp_tex))

        simulation_frames=300
        ising_lines = big_diag(n_ising_spins,2)
        ising=GeneralIsing(n_ising_spins, ising_lines) #It should really be a small world ising model, but the time evolution should look the same to the naked eye

        for t in np.linspace(-10, 10, simulation_frames):
            temperature = logistic(t, start_value=8., end_value=.9, transition_speed=1)
            pointer_movement = t_pointer.animate.move_to(logistic(t, end_value=pointer_position+2*DOWN, start_value=pointer_position, transition_speed=1))
            colors = ising.simulation_steps(temperature, 5)

            # Use there rate_func to control the animation substeps
            self.play(pointer_movement, *update_snake_colors(snake, colors), run_time=0.1, rate_func=linear)


        self.wait(2)