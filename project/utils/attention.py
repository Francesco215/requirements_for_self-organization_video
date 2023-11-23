from manim import *
from matplotlib import pyplot as plt

from utils.grid import eq_position


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
    backgrounds = []
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
        backgrounds.append(background)
    return {
        'create': create,
        'colorize': colorize,

        'text_obj': text_obj,
        'backgrounds': backgrounds,
    }


def tokens_to_variables(item):
    words2circles = []
    circles = []
    vars = []
    circles2 = []
    for i, background in enumerate(item['backgrounds']):
        _, y_top, _ = background.get_corner(UL)
        _, y_down, _ = background.get_corner(DL)
        radius = (y_top - y_down) / 2
        circle = Circle(
            radius=radius,
            fill_color=background.fill_color,
            fill_opacity=1,
            stroke_width=0
        )
        var = MathTex(f"s_{i}")
        circle = VGroup(var, circle)
        eq_position(circle, background)
        circle.add(var)
        circles2.append(circle)
        anim = Transform(
            background,
            circle,
            rate_func=smooth,
        )
        circles.append(anim.mobject)
        words2circles.append(anim)
        vars.append(FadeIn(var))

    for i, circle in enumerate(circles2):
        if i == 0:
            continue
        circle.next_to(circles2[i - 1], RIGHT, buff=0.1)
    return {
        'words2circles': words2circles,
        'circles': circles
    }


def roll_chain(item):
    circle_radius = 1.5
    angle_increment = 360 / len(item['circles'])
    anims = []
    for i, obj in enumerate(item['circles']):
        angle = i * angle_increment
        x = circle_radius * np.cos(np.deg2rad(angle))
        y = circle_radius * np.sin(np.deg2rad(angle))
        anims.append(ApplyMethod(obj.move_to, [x, y, 0]))
    return anims
