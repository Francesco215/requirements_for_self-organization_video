from functools import partial

from manim import *


def logistic(x, start_value, end_value, transition_speed = 1):
    return start_value + (end_value - start_value) / (1 + np.exp(-transition_speed * x )) 

def bool2direction(bool):
    return UP if bool else DOWN


def bool2color(bool):
    return WHITE if bool else BLACK


def update_colors(group: VGroup, new_state: np.array) -> list[Animation]:
    animations=[]
    for obj, state in zip(group, new_state.flatten()):
        color = bool2color(state)
        if obj.color != color:
            animations.append(obj.animate.set_fill(color))

    return animations


def update_colors2(grid, key, new_state: np.array) -> list[Animation]:
    anims = update_colors(grid[key], new_state)
    grid[key] = VGroup()
    for anim in anims:
        grid[key].add(anim.mobject)
    return anims


