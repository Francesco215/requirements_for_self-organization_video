from manim import *
from matplotlib import pyplot as plt

cmap = plt.get_cmap("viridis")


def get_manim_color(value):
    # value from 0 to 1
    r, g, b, _ = cmap(value)
    return rgb_to_color([r, g, b])


colors_num = 10
colors = [get_manim_color(v / colors_num) for v in range(colors_num)]


def tokenization(text):
    text_obj = Text(''.join(text)).set_z_index(1)
    create = FadeIn(text_obj)
    background = BackgroundRectangle(text_obj, color=RED)
    top_left = background.get_corner(UL)+UP*0.1
    bottom_left = background.get_corner(DL)+DOWN*0.05
    _, y_top, _ = top_left
    _, y_bottom, _ = bottom_left
    colorize = []
    offset = 0
    prev_x_right = None
    for i, token in enumerate(text):
        color = colors[i % len(colors)]
        token_len = len(token.strip())
        background = BackgroundRectangle(text_obj[offset:][:token_len], color=color)
        x_left, _, _ = background.get_corner(UL)
        x_right, _, _ = background.get_corner(UR)
        if prev_x_right is not None:
            x_left = prev_x_right
        corners = [
            (x_left, y_bottom, 0),
            (x_right, y_bottom, 0),
            (x_right, y_top, 0),
            (x_left, y_top, 0)
        ]
        background.set_points_as_corners(corners)
        colorize.append(
            FadeIn(background)
        )
        offset += token_len
        prev_x_right = x_right
    return create, colorize
