import random
from fc_ising import draw_circles
from simulations.ising_general import GeneralIsing
from simulations.fully_connected import FC_Ising

from utils.FC_ising import connect_circles,logistic,update_fill
from utils.attention import *
from utils.GLOBAL_VALUES import *
from utils.matrix_maker import small_world, big_diag

simulation_frames=300

class ColorText(MovingCameraScene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)

        window_size=8
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

        connection_colors=np.random.choice(magma_colors,(100,100))
        attention = connect_tokens(spins['circles'], line, connection_colors)
        self.play(*attention['animations'], run_time=2)
        self.wait()

        links = [(len(words)-1,i) for i in range(len(words))]

        anim1 = highlight_links(links, attention['lines'])
        self.play(*anim1)

        anim2 = normal_links(attention['lines'])
        self.play(*anim2)
        self.wait(1)
        
        #TODO: shift left graph
        O_tex=MathTex('~ O(','N','^2)').shift(4*RIGHT)
        O_tex[1].set_color(spin_color)
        self.play(VGroup(*spins['circles'],attention['lines_vgroup']).animate.shift(2*LEFT),Write(O_tex))
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

        new_last_spin=30
        self.play(extend_chain(spins, new_last_spin-last_spin, self.camera))


        n_circles=len(spins['circles'])
        last_spin=new_last_spin
        arrows_anim, arcs = draw_arrows_for_chain([(i,last_spin) for i in range(last_spin)], spins, connection_colors)
        self.play(*arrows_anim)
        self.wait()
        start_spin=n_circles-window_size
        self.play(*[FadeOut(arcs[i]) for i in range(start_spin)])
        self.wait()
        rectangle_anim,rectangle= make_square(start_spin, len(arcs), hamiltonian_color, spins)
        self.play(
            *[FadeOut(arcs[i]) for i in range(start_spin,len(arcs))],
            rectangle_anim
            )
        self.wait()        


        #now the window slides from the start to the end
        arrow=None
        for end_spin in range(1,len(spins['circles'])):
            start_spin=np.max([end_spin-window_size,0])
            _, new_rectangle=make_square(start_spin, end_spin, hamiltonian_color, spins)
            animations=[Transform(rectangle,new_rectangle)]
            if start_spin==5:
                bottom_of_spin=spins['circles'][2][0].get_bottom()
                arrow=Arrow(bottom_of_spin+1.5*DOWN, bottom_of_spin)
                animations.append(Create(arrow))
            if start_spin==n_circles-window_size-5: #maybe it's not necessary
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
        chain = roll_chain(spins,1.5)
        self.play(*chain['anims'], run_time=2)
        self.wait()
        # sw_lines=small_world(n_circles,4,0.7) #TODO: modify from here
        sw_lines=big_diag(n_circles,7)

        attention = connect_tokens(spins['circles'], sw_lines, connection_colors)
        
        self.play(*attention['animations'], run_time=2)
        self.wait()

        #here i draw the equivalent ising model
        n_ising_spins=100
        ising_lines = big_diag(n_ising_spins,2)
        ising=GeneralIsing(n_ising_spins, ising_lines) #It should really be a small world ising model, but the time evolution should look the same to the naked eye
        ising_colors = ising.state==1
        big_radius=chain['radius']
        ising_circles = draw_circles(ising_colors, big_radius=big_radius).next_to(spins['circles'],2*RIGHT*big_radius)
        self.play(Create(ising_circles))
        self.wait()

        lines=connect_circles(ising_circles,ising_lines)
        self.play(Create(lines))
        self.wait()


        links = [(0,i%n_circles) for i in range(-10,10)]
        anim1 = highlight_links(links, attention['lines'])
        self.play(*anim1)
        self.wait()
        anim2 = normal_links(attention['lines'])
        self.play(*anim2)
        self.wait()



        #here i add the temperature slider and start the simulation
        slider=Line(start=big_radius*DOWN*0.7,end=big_radius*UP*0.7, stroke_width=15).next_to(ising_circles,big_radius*2.5*RIGHT)

        pointer=Triangle().scale(0.5).set_stroke(width=0.2).rotate(-90*DEGREES).set_fill(color=temperature_color,opacity=1)
        temp_tex=MathTex('T').next_to(pointer,LEFT*2).set_color(temperature_color).scale(2.5)

        pointer_position=slider.get_x()*RIGHT+LEFT + big_radius*UP*0.5 
        t_pointer=VGroup(pointer,temp_tex).move_to(pointer_position)

        self.play(Create(slider))
        self.play(Create(pointer),Write(temp_tex))


        for t in np.linspace(-10, 10, simulation_frames):
            temperature = logistic(t, start_value=50., end_value=.9, transition_speed=1)
            pointer_movement = t_pointer.animate.move_to(logistic(t, end_value=pointer_position+big_radius*DOWN, start_value=pointer_position, transition_speed=1))
            colors = ising.simulation_steps(temperature, 5)

            # Use there rate_func to control the animation substeps
            self.play(pointer_movement, *update_fill(ising_circles, colors), run_time=0.1, rate_func=linear)

        self.wait()

        fade_out_lines=[FadeOut(attention['lines'][x]) for x in attention['lines']]
        self.play(FadeOut(lines), *fade_out_lines)
        ising_lines=small_world(n_ising_spins)
        ising=GeneralIsing(n_ising_spins,ising_lines)
        colors=ising.state==1
        lines=connect_circles(ising_circles,ising_lines)
        

        sw_lines=small_world(n_circles)

        attention = connect_tokens(spins['circles'], sw_lines, connection_colors)
        
        self.play(*update_fill(ising_circles, colors),t_pointer.animate.move_to(pointer_position))
        self.wait()
        self.play(*[Create(line) for line in lines],*attention['animations'], run_time=2)
        self.wait()





        for t in np.linspace(-10, 10, simulation_frames):
            temperature = logistic(t, start_value=20., end_value=.9, transition_speed=1)
            pointer_movement = t_pointer.animate.move_to(logistic(t, end_value=pointer_position+big_radius*DOWN, start_value=pointer_position, transition_speed=1))
            colors = ising.simulation_steps(temperature, 5)

            # Use there rate_func to control the animation substeps
            self.play(pointer_movement, *update_fill(ising_circles, colors), run_time=0.1, rate_func=linear)

        self.wait()

class PlotGraph(Scene):
    def construct(self):
        n_nodes = 15 
        edges = small_world(n_nodes)
        nodes = [1 for _ in range(n_nodes)]
        graph = plot_network(nodes, edges, 0.3).shift(LEFT)        
        ising=GeneralIsing(n_nodes,edges)
        nodes=ising.state==1
        

        self.play(Create(graph),run_time=3)
        self.wait()



class MovingVertices(Scene):
    def construct(self):
        n_nodes = 15 
        edges = small_world(n_nodes)
        nodes = [random.choice([0, 1]) for _ in range(n_nodes)]
        graph = plot_network(nodes, edges, 0.3).shift(LEFT)        
        ising=GeneralIsing(n_nodes,edges)
        nodes=ising.state==1
        
        #here i add the temperature slider and start the simulation
        big_radius=3
        slider=Line(start=big_radius*DOWN*0.7,end=big_radius*UP*0.7).shift(5*RIGHT)

        pointer=Triangle().scale(0.5).set_stroke(width=0.2).rotate(-90*DEGREES).set_fill(color=temperature_color,opacity=1)
        temp_tex=MathTex('T').next_to(pointer,LEFT*2).set_color(temperature_color).scale(2.5)

        pointer_position=slider.get_x()*RIGHT+LEFT*0.5 + big_radius*UP*0.5 
        t_pointer=VGroup(pointer,temp_tex).move_to(pointer_position).scale(0.4)

        self.play(Create(graph))
        self.wait()
        self.play(Create(slider))
        self.play(Create(pointer),Write(temp_tex))
        self.wait()


        for t in np.linspace(-10, 10, 300):
            temperature = logistic(t, start_value=20., end_value=.9, transition_speed=1)
            pointer_movement = t_pointer.animate.move_to(logistic(t, end_value=pointer_position+big_radius*DOWN, start_value=pointer_position, transition_speed=1))
            colors = ising.simulation_steps(temperature, 5)

            # Use there rate_func to control the animation substeps
            self.play(pointer_movement, *update_fill_for_graph(graph, colors), run_time=0.1, rate_func=linear)
            # self.play(*update_fill_for_graph(graph, colors), run_time=2)

        self.wait()


class Question(Scene):
    def construct(self):
        myBaseTemplate = TexTemplate(
            documentclass="\documentclass[preview]{standalone}"
        )
        myBaseTemplate.add_to_preamble(r"\usepackage{ragged2e}")

        text=Tex("\\justifying{Can we generate text in such a way that every element of the sequence looks to just a few other elements without doing any compromise in terms of the quality of the text?}",
                 tex_template=myBaseTemplate).scale(0.8)
        self.play(Write(text),run_time=8)