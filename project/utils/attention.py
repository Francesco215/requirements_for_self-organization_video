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


colors_num = 15
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

spacing = 0.05


def calc_radius2(circles_num):
    return ((config.frame_width / circles_num) / 2) - spacing


def position_circles(circles2):
    total_width = sum(circle.get_width() for circle in circles2) + spacing * len(circles2)
    start_x = -(total_width / 2)
    for circle in circles2:
        circle.next_to(ORIGIN, RIGHT, buff=0)
        circle.shift(start_x * RIGHT)
        start_x += circle.get_width() + spacing


def tokens_to_variables(item):
    words2circles = []
    circles = []
    vars = []
    circles2 = []
    radius = calc_radius2(len(item['backgrounds']))
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

    position_circles(circles2)
    return {
        'words2circles': words2circles,
        'transformed_circles': circles,
        'radius': radius,
        'circles': circles2
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
def highlight_links(links_to_highlight, lines):
    animations=[]
    for line in lines:
        if line in links_to_highlight:
            animations+=[lines[line].animate.set_stroke(width=stroke_width*2)]
        else:
            animations+=[lines[line].animate.set_stroke(width=stroke_width/2, opacity=0.5)]

    return animations 

def normal_links(lines):
    
   return [lines[line].animate.set_stroke(width=stroke_width, opacity=1) for line in lines]

def fade_lines(lines):

   return [FadeOut(lines[line]) for line in lines]


def extend_chain(spins, delta: int, scene):
    g = VGroup(*spins['circles'])
    old_radius = spins['circles'][0][0].radius
    circles_num = len(spins['circles'])
    for _ in range(delta):
        circles_num += 1
        new_radius = calc_radius2(circles_num)
        scale = new_radius / old_radius
        scene.play(g.animate.scale(scale))
        scene.play(g.animate.shift(LEFT * (new_radius + spacing)))
        circle = Circle(
            radius=new_radius,
            fill_color=colors[circles_num % len(colors)],
            fill_opacity=1,
            stroke_width=0
        )

        var = MathTex("s_{" + str(circles_num - 1) + "}", font_size=g[-1][1].font_size)
        var.set_z_index(1)
        circle = VGroup(circle, var)
        circle.next_to(g[-1], RIGHT, buff=spacing)
        scene.play(FadeIn(circle))
        g.add(circle)
        old_radius = new_radius
    spins['circles'] = g


def draw_arrows_for_chain(links, spins):
    link_matrix = []
    for i in range(len(spins['circles'])):
        row = []
        for j in range(len(spins['circles'])):
            if (i, j) in links:
                v = 1
            else:
                v = 0
            row.append(v)
        link_matrix.append(row)
    g = VGroup(*spins['circles'])
    arrows = []
    for i, row in enumerate(link_matrix):
        for j, val in enumerate(row):
            if val == 1:
                c_i = g[i][0]
                c_j = g[j][0]
                radius = c_i.radius
                x_1, y_1, _ = c_i.get_center()
                x_2, y_2, _ = c_j.get_center()
                start, end = sorted([
                    (x_2, y_2 + radius, 0),
                    (x_1, y_1 + radius, 0)
                ], key=lambda p: p[0], reverse=True)
                arc = ArcBetweenPoints(
                    start=start,
                    end=end,
                    stroke_color=YELLOW
                )
                arc.add_tip()
                spins['circles'][i].add(arc)
                arrows += [Create(arc)]
    spins['circles'] = g
    return arrows


def make_square(start, end, color, spins):
    left = spins['circles'][start]
    right = spins['circles'][end]
    x_l, _, _ = left.get_corner(UL)
    x_r, _, _ = right.get_corner(UR)
    side_length = x_r - x_l
    square = Square(
        side_length=side_length,
        color=color,
        stroke_width=0,
        fill_color=color,
        fill_opacity=1
    )
    x_center = x_l + (side_length / 2)
    _, y, _ = left.get_center()
    square.move_to((x_center, y, 0))
    return square
