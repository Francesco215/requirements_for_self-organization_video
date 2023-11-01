from manim import *
spin_color=BLUE


class Ising(Scene):
    def construct(self):
        circle_1 = Circle(radius=1)  # create a circle
        circle_1.set_fill(WHITE, opacity=0.5)  # set the color and transparency
        self.play(Create(circle_1))  # show the circle on screen

        arrow_1=Arrow(start=DOWN*.7, end=UP*.7, buff=0, color=spin_color) # create a spin arrow
        self.play(Create(arrow_1))  # show the spin arrow

        text_1=MathTex("s","=+1").next_to(circle_1,UP)
        text_1[0].set_color(spin_color)
        self.play(Write(text_1))

        target_text_1=MathTex("s","=-1").next_to(text_1,0)
        target_text_1[0].set_color(spin_color)
        self.play(Rotate(arrow_1, angle=PI), Transform(text_1,target_text_1)) # rotate the spin arrow by 180 degrees
        self.wait(1) # wait for 1 second

        target_text_1=MathTex("s","=+1").next_to(text_1,0)
        target_text_1[0].set_color(spin_color)
        self.play(Rotate(arrow_1, angle=PI), Transform(text_1,target_text_1)) # rotate the spin arrow back by 180 degrees
        spin_1=VGroup(circle_1,arrow_1,text_1)        

        self.play(spin_1.animate.shift(LEFT*2))

        target_text_1=MathTex("s_1","=+1").next_to(text_1,0)
        target_text_1[0].set_color(spin_color)
        circle_2 = Circle(radius=1).move_to(RIGHT*2)
        circle_2.set_fill(WHITE, opacity=0.5)
        arrow_2=Arrow(start=DOWN*.7, end=UP*.7, buff=0, color=spin_color).next_to(circle_2,0)
        text_2=MathTex("s_2","=+1").next_to(circle_2,UP)
        text_2[0].set_color(spin_color)
        self.play(Create(circle_2), Create(arrow_2),Transform(text_1,target_text_1), Write(text_2))

        spin_2 = VGroup(circle_2, arrow_2, text_2)

        self.wait(1)


        line=Line(start=circle_1.get_edge_center(RIGHT), end=circle_2.get_edge_center(LEFT),color=ORANGE)
        h= MathTex("H",color=ORANGE)
        rest=MathTex("=-Js_1s_2").next_to(h,RIGHT)
        hamiltonian=VGroup(h,rest).next_to(line,UP*10)
        self.play(Create(line), Write(hamiltonian))

        