import random

from utils.attention import *
from utils.GLOBAL_VALUES import *

class ColorText(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)

        #words = ['Many',' words ',' map',' to',' one',' token']
        words = ['Chapter',' 1',':',' To',' you',', ','200','0',' years',' later']
        
        tokens = tokenization(words)
        self.play(tokens['create'], run_time=2)
        self.play(*tokens['colorize'], run_time=2)

        spins = tokens_to_variables(tokens)
        self.play(FadeOut(tokens['text_obj']))
        self.play(*spins['words2circles'], run_time=2)
        for circle in spins['transformed_circles']:
            self.remove(circle)
        self.wait()

        spin_tex=MathTex('s_i','\in \mathbb R^n').shift(2*UP)
        spin_tex[0].set_color(spin_color)
        self.play(Write(spin_tex))
        self.wait()
        self.play(FadeOut(spin_tex))

        chain = roll_chain(spins)
        self.play(*chain['anims'], run_time=2)

        circles_num = len(spins['circles'])
        line=np.ones((circles_num,circles_num))
        for i in range(circles_num):
            for j in range(i,circles_num):
                line[i,j]=0

        attention = connect_tokens(spins['circles'], line)
        self.play(*attention['animations'], run_time=2)
        self.wait()

        links = [(len(words)-1,i) for i in range(len(words))]

        anim1 = highlight_links(links, attention['lines'])
        self.play(*anim1)

        anim2 = normal_links(attention['lines'])
        self.play(*anim2)
        self.wait(1)
        
        O_tex=MathTex('~ O(','N','^2)').shift(4*RIGHT)
        O_tex[1].set_color(spin_color)
        self.play(Write(O_tex))
        self.wait(1)
        self.play(Wiggle(O_tex[1]))
        self.wait(1)

        fade_out= fade_lines(attention['lines'])
        self.play(*fade_out,FadeOut(O_tex))
        self.wait(1)

        self.play(*unroll_chain(chain))
        extend_chain(spins, 5, self)
        self.wait(2)


class ExtendChanDrawLines(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)

        words = ['Chapter', ' 1', ':', ' To', ' you', ', ', '200', '0', ' years', ' later']

        tokens = tokenization(words)
        self.play(tokens['create'], run_time=2)
        self.play(*tokens['colorize'], run_time=2)
        spins = tokens_to_variables(tokens)
        self.play(FadeOut(tokens['text_obj']))
        self.play(*spins['words2circles'], run_time=2)
        arrows = draw_arrows_for_chain([(i,9) for i in range(9)], spins)
        self.play(*arrows)
        for circle in spins['transformed_circles']:
            self.remove(circle)
        extend_chain(spins, 3, self)
        square = make_square(2, 4, BLUE, spins)
        self.play(Create(square))
        self.wait(2)
