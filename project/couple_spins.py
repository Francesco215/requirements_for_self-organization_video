from manim import *

from utils.GLOBAL_VALUES import spin_color, hamiltonian_color


def rotate_spin(self, text, arrow, angle, index):
    if angle==PI:
        target_text=MathTex(f"s_{index}","=-1").next_to(text,0)
    else:
        target_text=MathTex(f"s_{index}","=+1").next_to(text,0)
    target_text[0].set_color(spin_color)
    return Rotate(arrow, angle=angle), Transform(text,target_text)


def change_hamiltonian(self, hamiltonian, sign):
    if sign == "+":
        target_hamiltonian=MathTex('H','=-J','s_1','\cdot','s_2','=+J').next_to(hamiltonian,0)
    else:
        target_hamiltonian=MathTex('H','=-J','s_1','\cdot','s_2','=-J').next_to(hamiltonian,0)

    target_hamiltonian[0].set_color(hamiltonian_color)
    target_hamiltonian[2].set_color(spin_color)
    target_hamiltonian[-2].set_color(spin_color)

    self.play(Transform(hamiltonian,target_hamiltonian))    


class CoupleSpins(Scene):
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
        hamiltonian=MathTex('H','=','-J','s_1','\cdot','s_2').next_to(line,UP*10)
        hamiltonian[0].set_color(hamiltonian_color)
        hamiltonian[-3].set_color(spin_color)
        hamiltonian[-1].set_color(spin_color)
        self.play(Create(line), Write(hamiltonian))
        self.wait(1)

        self.play(Wiggle(hamiltonian[2]))
        self.wait()

        self.play(Wiggle(hamiltonian[-3]),Wiggle(hamiltonian[-1]))


        energy=MathTex('=-J').next_to(hamiltonian,RIGHT)
        H=VGroup(hamiltonian,energy)

        self.play(Write(energy))
        self.play(H.animate.shift(LEFT/2))
        self.wait(1)

        target_energy=MathTex('=+J').next_to(energy,0)
        self.play(Transform(energy,target_energy),*rotate_spin(self, text_1, arrow_1, PI, 1))
        self.wait(1)


        self.play(*[mobject.animate.shift(2*LEFT) for mobject in self.mobjects])

        
        higher_energy_level=Line(RIGHT*3+UP,RIGHT*5+UP, color=hamiltonian_color)
        higher_energy=MathTex('+J').next_to(higher_energy_level,RIGHT)
        lower_energy_level=Line(RIGHT*3+DOWN,RIGHT*5+DOWN, color=hamiltonian_color, stroke_width=10)
        lower_energy=MathTex('-J').next_to(lower_energy_level,RIGHT)

        self.play(Create(lower_energy_level), Create(higher_energy_level), Write(higher_energy), Write(lower_energy))

        high_to_low_arrow=Arrow(higher_energy_level.get_edge_center(DOWN)+ LEFT/2,lower_energy_level.get_edge_center(UP)+ LEFT/2, stroke_width=8)
        low_to_high_arrow=Arrow(lower_energy_level.get_edge_center(DOWN)+ RIGHT/2,higher_energy_level.get_edge_center(UP)+ RIGHT/2, stroke_width=3)
        self.play(Create(high_to_low_arrow), Create(low_to_high_arrow))

        target_energy=MathTex('=-J').next_to(energy,0)
        self.play(Transform(energy,target_energy),*rotate_spin(self, text_1, arrow_1, PI, 1))
        self.play(Wiggle(lower_energy_level,scale_value=1.2))
        self.wait(1) 