import random
import math

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
    font_size = DEFAULT_FONT_SIZE
    screen_width = config.frame_width
    margins = 0.1
    while True:
        tmp = Text(''.join(text), font_size=font_size)
        x_l, _, _ = tmp.get_corner(UL)
        x_r, _, _ = tmp.get_corner(UR)
        width = x_r - x_l
        if width + margins < screen_width:
            break
        else:
            font_size -= 1

    text_obj = Text(''.join(text), font_size=font_size).set_z_index(1)
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
    spacing = 0.05
    radius = ((config.frame_width / len(item['backgrounds'])) / 2) - spacing
    for i, background in enumerate(item['backgrounds']):
        circle = Circle(
            radius=radius,
            fill_color=background.fill_color,
            fill_opacity=1,
            stroke_width=0
        )
        var = MathTex("s_{" + str(i) + "}")  # font_size=DEFAULT_FONT_SIZE * 0.7
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

    total_width = sum(circle.get_width() for circle in circles2) + spacing * len(circles2)
    start_x = -(total_width / 2)
    for circle in circles2:
        circle.next_to(ORIGIN, RIGHT, buff=0)
        circle.shift(start_x * RIGHT)
        start_x += circle.get_width() + spacing
    return {
        'words2circles': words2circles,
        'circles': circles,
        'radius': radius
    }


def circles_intersect(center1, center2, radius):
    distance = math.sqrt((center1[0] - center2[0])**2 + (center1[1] - center2[1])**2)
    return distance < 2 * radius


def calc_radius(item, circles_num):
    circle_radius = 1
    angle_increment = 360 / circles_num
    while True:
        x1 = circle_radius * np.cos(np.deg2rad(0))
        y1 = circle_radius * np.sin(np.deg2rad(0))

        x2 = circle_radius * np.cos(np.deg2rad(angle_increment))
        y2 = circle_radius * np.sin(np.deg2rad(angle_increment))

        if circles_intersect([x1, y1],[x2, y2], item['radius']):
            circle_radius += 0.05
        else:
            break
    return circle_radius


def roll_chain(item):
    circle_radius = calc_radius(item,  len(item['circles']))
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
                ).set_z_index(-1)
                lines[(i, j)] = line
                animations.append(Create(line))
    return {
        'lines': lines,
        'animations': animations
    }

stroke_width=4 #manim default stroke width
def highlight_links(links, lines):
    animations=[]
    for line in lines:
        if line in links:
            animations+=[lines[line].animate.set_stroke(width=stroke_width*2)]
        else:
            animations+=[lines[line].animate.set_stroke(width=stroke_width/2, opacity=0.5)]

    return animations 

def normal_links(lines):
    
   return [lines[line].animate.set_stroke(width=stroke_width) for line in lines]