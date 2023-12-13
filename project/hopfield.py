from utils.GLOBAL_VALUES import *
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
        labels = ax.get_axis_labels(x_label="",y_label="E").set_color(hamiltonian_color)
        t = ValueTracker(4.7)

        graph = ax.plot(energy_landscape, color=ORANGE)

        initial_point = [ax.coords_to_point(t.get_value(), energy_landscape(t.get_value()))]
        dot = Dot(point=initial_point)

        dot.add_updater(lambda x: x.move_to(ax.coords_to_point(t.get_value(), energy_landscape(t.get_value()))))
        x_space = np.linspace(*ax.x_range[:2],200)
        minimum_index = ((x_space-patterns[1])**2).argmin()+1

        self.play(FadeIn(ax))
        self.play(Write(labels))
        self.play(Create(graph))
        self.wait()

        coords=[ax.coords_to_point(p,-0.2) for p in patterns]
        letters=[Text(l).shift(c) for l,c in zip(['C','S','A','U'],coords)]

        
        self.play(LaggedStart(*[Write(l) for l in letters],lag_ratio=0.4,run_time=3))
        


        self.play(Create(dot))
        self.wait()
        self.play(t.animate.set_value(x_space[minimum_index]),run_time=3)
        self.wait()


from numpy.random import randint
def random_binary_string():
    return f'{randint(2**8):8b}'.replace(' ','0')

class AddressTable(Scene):
    def construct(self):
        addresses=['0x'+random_binary_string() for _ in range(10)]
        values   =[     random_binary_string() for _ in range(10)]
        table=np.transpose(np.array([addresses,values]))

        table_tex=Table(table, col_labels=[Text('Address'),Text('Value')]).scale(0.5)

        self.play(Write(table_tex))
        self.wait()

        self.play(Wiggle(table_tex.get_entries((7,0))))
        self.wait()


        self.play(Wiggle(table_tex.get_entries((6,1))))
        self.wait()
        
class Equations(Scene):
    def construct(self):
        hopfield_title=Text('Hopfield Network').shift(2*UP)
        self.play(Write(hopfield_title))
        self.wait()

        hamiltonian=MathTex('H','=','-','\sum_{ij}','W_{ij}','s_is_j')
        hamiltonian[0].set_color(hamiltonian_color)
        hamiltonian[-1].set_color(spin_color)
        self.play(Write(hamiltonian))
        self.wait()

        

        hop=VGroup(hopfield_title,hamiltonian)
        self.play(hop.animate.shift(3*LEFT))

        
        ising_title=Text('Ising Model').shift(2*UP)
        ising_hamiltonian=MathTex('H','=-\sum_{ij}','J','s_is_j')
        ising_hamiltonian[0].set_color(hamiltonian_color)
        ising_hamiltonian[-1].set_color(spin_color)
        ising=VGroup(ising_title,ising_hamiltonian).shift(3*RIGHT)
        self.play(Write(ising_title),Write(ising_hamiltonian))
        self.wait()

        self.play(Indicate(hamiltonian[-2]))
        self.wait()
        self.play(Indicate(ising_hamiltonian[-2]))
        self.wait()


        inter_matrix=MathTex('W_{ij}','=','X_i^TX_j').shift(3*LEFT+2*DOWN)
        self.play(Write(inter_matrix))
        self.wait()
        self.play(Wiggle(inter_matrix[0]))
        self.wait()
        self.play(Wiggle(inter_matrix[-1]))
        self.wait()


        self.play(FadeOut(ising))
        self.wait()

        #derivative of the energy
        warning_text=Text('Oversimplification!').set_color(RED).shift(3.5*UP)
        self.play(Write(warning_text))
        self.wait()

        target_text=MathTex('-{\partial ','H','\over\partial','s_i','}=','\sum_{j}','W_{ij}','s_j').shift(3*LEFT)
        target_text[1].set_color(hamiltonian_color)
        target_text[3].set_color(spin_color)
        target_text[-1].set_color(spin_color)
        self.play(Transform(hamiltonian,target_text))#this is ugly to look at 
        self.wait()


        target_text=MathTex('\Delta','s_i','\\approx','\sum_{j}','W_{ij}','s_j').shift(3*LEFT)
        target_text[1].set_color(spin_color)
        target_text[-1].set_color(spin_color)
        self.play(Transform(hamiltonian,target_text)) 
        self.wait()

        trasformer_title=Text('Attention').shift(2*UP)
        update_rule=MathTex('\Delta','s_i','\\approx','\sum_j','A_','{ij}','V_j')
        update_rule[1].set_color(spin_color)
        update_rule[-1].set_color(spin_color)
        attention=MathTex('A_{ij}=','\sigma','(K_i^TQ_j)').shift(2*DOWN)

        tr=VGroup(trasformer_title,update_rule,attention).shift(3*RIGHT)

        self.play(Write(trasformer_title),Write(update_rule),Write(attention))
        self.wait()


        target_text=MathTex('\Delta','s_i','\\approx','\sum_{j}','(X_i^TX_j)','s_j').shift(3*LEFT)
        target_text[1].set_color(spin_color)
        target_text[-1].set_color(spin_color)
        self.play(Transform(hamiltonian,target_text),Transform(inter_matrix[-1],target_text[-2]))
        self.play(FadeOut(inter_matrix)) 
        self.wait()
        



        target_text=MathTex('\Delta','s_i','\\approx','\sum_j','\sigma','(K_i^TQ_j)','V_j').shift(3*RIGHT)
        target_text[1].set_color(spin_color)
        target_text[-1].set_color(spin_color)

        self.play(Transform(update_rule,target_text),Transform(attention[-1],target_text[-2]),Transform(attention[-2],target_text[-3]))
        self.play(FadeOut(attention))
        self.wait()

        self.play(Indicate(update_rule[-3],2))
        self.wait()

class SimpleTitle(Scene):
    def construct(self):
        title= Text('Hopfield Networks')
        self.play(Write(title))
        self.wait()