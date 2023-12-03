import random
import math

from manim import *
from matplotlib import pyplot as plt

from utils.grid import eq_position


vir = plt.get_cmap("viridis")
mag = plt.get_cmap("magma")

def get_manim_color(value, cmap=vir):
    # value from 0 to 1
    r, g, b, _ = cmap(value)
    return rgb_to_color([r, g, b])


colors_num = 15
viridis_colors = [get_manim_color(v / colors_num) for v in range(colors_num)]
magma_colors = [get_manim_color(v, mag) for v in np.linspace(0.2,1,colors_num)]

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
        color = viridis_colors[i % len(viridis_colors)]
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



def calc_radius(circles_radius, circles_num, spacing=0.03):
    return (circles_radius+spacing)/np.sin(PI/circles_num)

def roll_chain(item, x_translation=0):
    circle_radius = calc_radius(item['radius'],  len(item['circles']))
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
        anims.append(ApplyMethod(obj.move_to, [x+x_translation, y, 0]))
    return {
        'anims': anims,
        'init_positions': init_positions,
        'radius': circle_radius
    }


def unroll_chain(item):
    anims = []
    for v in item['init_positions']:
        anims.append(
            ApplyMethod(v['circle'].move_to, v['position'])
        )
    return anims

def connect_tokens(circles, line, colors):
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
                    color=colors[i][j]
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


def extend_chain(spins, delta: int, camera):
    g = VGroup(*spins['circles'])
    old_radius = spins['circles'][0][0].radius
    circles_num = len(spins['circles'])
    draw_cicles_anim_group = []
    for _ in range(delta):
        circles_num += 1
        circle = Circle(
            radius=old_radius,
            fill_color=viridis_colors[circles_num % len(viridis_colors)],
            fill_opacity=1,
            stroke_width=0
        )
        var = MathTex("s_{" + str(circles_num - 1) + "}", font_size=g[-1][1].font_size)
        var.set_z_index(1)
        spin = VGroup(circle, var)
        spin.next_to(g[-1], RIGHT, buff=spacing)
        draw_cicles_anim_group.append(Create(circle))
        draw_cicles_anim_group.append(Write(var))
        g.add(spin)
    spins['circles'] = g
    center=np.array([g.get_center()[0],0,0])
    camera_anim=camera.frame.animate.move_to(center).set(width=g.width+old_radius)
    camera_anim=AnimationGroup(camera_anim,run_time=3)
    drawing_anim=LaggedStart(*draw_cicles_anim_group,lag_ratio=0.1,run_time=3)
    return LaggedStart(camera_anim,drawing_anim,lag_ratio=0.3) 


def draw_arrows_for_chain(links, spins, colors):
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
    arcs=VGroup()
    animations = []
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
                    stroke_color=colors[i][j]
                )
                arc.add_tip()
                arcs.add(arc)
                animations += [Create(arc)]
    spins['circles'] = g
    return animations, arcs


def make_square(start, end, color, spins):
    left = spins['circles'][start][0]
    right = spins['circles'][end][0]
    spins['circle_start'] = start
    rectangle = SurroundingRectangle(
        VGroup(left, right),
        color=color,
        buff=0.05
    )
    return FadeIn(rectangle), rectangle


def translate_square(steps: int, spins):
    new_circle_start = spins['circle_start'] + steps
    new_x = spins['circles'][new_circle_start][0].get_corner(UL) - 0.05
    old_x = spins['rectangle'].get_corner(UL)
    delta = new_x - old_x
    spins['circle_start'] = new_circle_start
    return spins['rectangle'].animate.shift(RIGHT * delta)