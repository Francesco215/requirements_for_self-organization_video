from manim import *

"""
    Take this code as a rough blueprint, I have written it whithout using classes, but if you prefer to do it in a object oriented way feel free to do so
"""


def make_grid(starting_state: np.array) -> VGroup:
    """This function creates the VMobject representing the grid
    
    It draws the grid of circles with the specified starting configuration.

    For each element of the grid, if the starting state is zero,
    then the arrow will point down, else it will point up

    Args:
        starting_state (np.array): the starting configuration of the grid. dtype=bool 

    Returns:
        VGroup: the VM object representing the grid
    """

    rows, columns = starting_state.shape
    screen_width = config["frame_width"]
    screen_height = config["frame_height"]

    if columns > rows:
        bigger_dimension = columns
        screen_size = screen_width
    else:
        bigger_dimension = rows
        screen_size = screen_height

    radius = 1
    between_space = 0.2
    while bigger_dimension * (radius * 2) > (screen_size - (bigger_dimension * between_space)):
        radius -= 0.05

    circles = [Circle(color=BLUE, radius=radius) for _ in range(columns * rows)]
    circles_group = VGroup(*circles)
    circles_group.arrange_in_grid(rows, columns, buff=between_space)
    for arrow_direction, circle in zip(starting_state.flatten(), circles):
        arrow = Arrow(start=ORIGIN, end=UP if arrow_direction else DOWN, buff=radius)
        arrow.shift(circle.get_center() - arrow.get_center())
        circles_group.add(arrow)
    return circles_group


class Test(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)

        starting_state = np.random.choice([True, False], size=(5, 10))
        print(starting_state)
        self.add(make_grid(starting_state))



def UpdateCircleGrid(grid:VMobject, new_state:np.array) -> VMobject:
    """It updates the grid made of circles and animates fluidly the transition of the arrows flipping over

    Args:
        grid (VMobject): the grid originally created with the MakeGrid function
        new_state (np.array): the new configuration of the grid

    Returns:
        VMobject: the updated grid
    """

def CirclesToSquares(grid:VMobject) -> VMobject:
    """It turns the grid made of circles and arrows in to a square grid similar to the one in the website
    It animates fluidly the transition.

    If the element of the state configuration is equal to 0, the color of the square must be black,
    else it must be white.

    So, circles with the arrow pointing down will turn into black squares
    and circles with arrow pointing up will turno int o white squares.
    

    Args:
        grid (VMobject): the grid

    Returns:
        VMobject: the updated grid
    """    

def UpdateSquareGrid(grid:VMobject, new_state:np.array) -> VMobject:
    """It updates the grid made of squares and animates the transition of the squares changing color

    Args:
        grid (VMobject): the grid originally created with the MakeGrid function
        new_state (np.array): the new configuration of the grid

    Returns:
        VMobject: the updated grid
    """
    


