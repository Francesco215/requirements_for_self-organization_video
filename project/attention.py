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

        fade_out= fade_lines(attention['lines'])
        self.play(*fade_out)
        self.wait(1)

        self.play(*unroll_chain(chain))
        self.wait(2)


class RollAndUnroll(Scene):
    def construct(self):
        words = ['Many', ' words ', ' map', ' to', ' one', ' token']
        item = tokenization(
            [random.choice(words) for _ in range(10)]
        )
        self.play(item['create'], run_time=2)
        self.play(*item['colorize'], run_time=2)

        item2 = tokens_to_variables(item)
        self.play(FadeOut(item['text_obj']))
        self.play(*item2['words2circles'], run_time=2)
        item3 = roll_chain(item2)
        self.play(*item3['anims'], run_time=2)
        self.play(*unroll_chain(item3), run_time=2)
        self.wait(2)