from manim import *

def gaussian(x,pattern):
    return -np.exp(-(x-pattern)**2/.5)

patterns=[2,5.6,7,8.7]
def energy_landscape(x):
    out=1.05
    for pattern in patterns:
        out+=gaussian(x,pattern)
    return out

class Hop(Scene):

    def construct(self):
        ax = Axes(
            x_range=[0, 10], y_range=[-0.2, 1.1, 10], axis_config={"include_tip": False}
        )
        labels = ax.get_axis_labels(x_label="",y_label="E")

        t = ValueTracker(3.9)

        graph = ax.plot(energy_landscape, color=ORANGE)

        initial_point = [ax.coords_to_point(t.get_value(), energy_landscape(t.get_value()))]
        dot = Dot(point=initial_point)

        dot.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), energy_landscape(t.get_value()))))
        x_space = np.linspace(*ax.x_range[:2],200)
        minimum_index = ((x_space-patterns[1])**2).argmin()

        self.add(ax, labels, graph, dot)
        self.play(t.animate.set_value(x_space[minimum_index]))
        self.wait()