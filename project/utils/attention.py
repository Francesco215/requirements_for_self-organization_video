import random

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
    init_positions = []
    for i, obj in enumerate(item['circles']):
        angle = i * angle_increment
        x = circle_radius * np.cos(np.deg2rad(angle))
        y = circle_radius * np.sin(np.deg2rad(angle))
        init_positions.append({
            'circle': obj,
            'position': obj.get_center()
        })
        anims.append(ApplyMethod(obj.move_to, [x, y, 0]))
    return {
        'anims': anims,
        'init_positions': init_positions
    }


def unroll_chain(item):
    anims = []
    for v in item['init_positions']:
        anims.append(
            ApplyMethod(v['circle'].move_to, v['position'])
        )
    return anims


def connect_tokens(circles, line):
    lines = {}
    animations = []
    for i, row in enumerate(line):
        for j, val in enumerate(row):
            if val == 1:
                c_i = circles[i]
                c_j = circles[j]
                line = Line(
                    c_i.get_center(),
                    c_j.get_center(),
                    color=random.choice(colors)
                )
                lines[(i, j)] = line
                animations.append(Create(line))
    return {
        'lines': lines,
        'animations': animations
    }


def highlight_links(links, lines):
    highlited = VGroup()
    highlited_keys = []
    for i, j in links:
        k1 = (i, j)
        k2 = (j, i)
        if k1 in lines:
            highlited.add(lines[k1])
            highlited_keys += [k1, k2]
        elif k2 in lines:
            highlited.add(lines[k2])
            highlited_keys += [k1, k2]
    not_highlighted = VGroup(*[lines[k] for k in set(lines.keys()) - set(highlited_keys)])
    init_width = highlited[0].stroke_width

    angel = round(PI / 50, 2)
    rotations = []
    multiplier = 1
    about_points = [line.get_center() for line in highlited]
    for _ in range(10):
        tmp = []
        for line, about_point in zip(highlited, about_points):
            tmp.append(
                Rotating(
                    line,
                    radians=angel*multiplier,
                    run_time=0.5,
                    about_point=about_point,
                    rate_func=linear
                )
            )
        rotations.append(tmp)
        if multiplier > 0:
            multiplier = -2
        else:
            multiplier = 2

    return (
        [
            highlited.animate.set_stroke(width=2 * init_width),
            not_highlighted.animate.set_stroke(width=init_width / 2, opacity=0.5),
        ],
        rotations
    )
