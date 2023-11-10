from manim import *


def bool2direction(bool):
    return UP if bool else DOWN


def bool2color(bool):
    return WHITE if bool else BLACK


def update_colors(group: VGroup, new_state: np.array) -> list[Animation]:
    animations = []
    for obj, state in zip(group, new_state.flatten()):
        color = bool2color(state)
        if obj.color != color:
            animations += [ApplyMethod(obj.set_color, color, rate_func=smooth, run_time=1),
                           ]

    return animations


def update_colors2(grid, key, new_state: np.array) -> list[Animation]:
    anims = update_colors(grid[key], new_state)
    grid[key] = VGroup()
    for anim in anims:
        grid[key].add(anim.mobject)
    return anims