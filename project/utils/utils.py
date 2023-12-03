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
            animations.append(obj.animate.set_color(color))

    return animations


def update_colors2(grid, key, new_state: np.array) -> list[Animation]:
    anims = update_colors(grid[key], new_state)
    grid[key] = VGroup()
    for anim in anims:
        grid[key].add(anim.mobject)
    return anims


def update_fill(group: VGroup, new_state: np.array) -> list[Animation]:
    animations=[]
    for obj, state in zip(group, new_state.flatten()):
        color = bool2color(state)
        if obj.color != color:
            animations.append(obj.animate.set_fill(color))

    return animations



def small_world(N, K, beta):
    # Create a regular ring lattice
    G = np.zeros((N, N), dtype=int)
    for i in range(N):
        for j in range(1, K // 2 + 1):
            G[i, (i + j) % N] = 1
            G[i, (i - j) % N] = 1
    
    # Rewire edges with probability beta
    for i in range(N):
        for j in range(1, K // 2 + 1):
            if np.random.rand() < beta:
                G[i, (i + j) % N] = 0
                new_neighbor = np.random.choice(np.setdiff1d(np.arange(N), [i, (i + j) % N]))
                G[i, new_neighbor] = 1
    
    return G
