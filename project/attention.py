import random
from fc_ising import draw_circles
from simulations.fully_connected import FC_Ising

from utils.attention import *
from utils.GLOBAL_VALUES import *
from utils.utils import small_world
class ColorText(MovingCameraScene):
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

        for circle in spins['transformed_circles']:
            self.remove(circle)
        chain = roll_chain(spins)
        self.play(*chain['anims'], run_time=2)

        circles_num = len(spins['circles'])
        line=np.ones((circles_num,circles_num))
        for i in range(circles_num):
            for j in range(i,circles_num):
                line[i,j]=0

        connection_colors=np.random.choice(magma_colors,(20,20))
        attention = connect_tokens(spins['circles'], line, connection_colors)
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
        self.wait()
        last_spin=9
        arrows_anim, arcs = draw_arrows_for_chain([(i,last_spin) for i in range(last_spin)], spins, connection_colors)
        self.play(*arrows_anim)
        self.wait()
        self.play(FadeOut(arcs))
        self.wait()
        self.play(extend_chain(spins, 8, self.camera))


        last_spin=17
        arrows_anim, arcs = draw_arrows_for_chain([(i,last_spin) for i in range(last_spin)], spins, connection_colors)
        self.play(*arrows_anim)
        self.wait()
        start_spin=9
        self.play(*[FadeOut(arcs[i]) for i in range(start_spin)])
        self.wait()
        rectangle_anim,rectangle= make_square(start_spin, len(arcs), hamiltonian_color, spins)
        self.play(
            *[FadeOut(arcs[i]) for i in range(start_spin,len(arcs))],
            rectangle_anim
            )
        self.wait()        


        #now the window slides from the start to the end
        window_size=8
        arrow=None
        for end_spin in range(1,len(spins['circles'])):
            start_spin=np.max([end_spin-window_size,0])
            _, new_rectangle=make_square(start_spin, end_spin, hamiltonian_color, spins)
            animations=[Transform(rectangle,new_rectangle)]
            if start_spin==5:
                bottom_of_spin=spins['circles'][2][0].get_bottom()
                arrow=Arrow(bottom_of_spin+1.5*DOWN, bottom_of_spin)
                animations.append(Create(arrow))
            if start_spin==8: #maybe it's not necessary
                animations.append(FadeOut(arrow))
            self.play(*animations)
         
        self.wait()

        #here i talk about the fact the the interactions are not important
        self.play(FadeOut(rectangle),*[FadeIn(arcs[i]) for i in range(start_spin,len(arcs))])
        for _ in range(10):
            self.play(*[arc.animate.set_color(np.random.choice(magma_colors)) for arc in arcs[start_spin:]],run_time=0.5)
        self.wait()
        self.play(*[FadeOut(arcs[i]) for i in range(start_spin,len(arcs))])
        self.wait()



        #here i talk about topology required
        n_circles=len(spins['circles'])
        chain = roll_chain(spins)
        self.play(*chain['anims'], run_time=2)
        self.wait()
        sw_lines=small_world(n_circles,4,0.7)
        attention = connect_tokens(spins['circles'], sw_lines, connection_colors)
        
        self.play(*attention['animations'], run_time=2)
        self.wait()

        #here i draw the equivalent ising model
        n_ising_spins=100
        ising=FC_Ising(n_ising_spins)
        ising_colors = ising.state==1
        ising_circles = draw_circles(ising_colors).shift(10*RIGHT)
        self.play(Create(ising_circles))
        self.wait()

        ising_lines=small_world(n_ising_spins,4,0.7)
        