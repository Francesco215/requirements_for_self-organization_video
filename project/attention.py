import random

from utils.attention import *


class ColorText(Scene):
    def construct(self):
        # plane = NumberPlane()
        # self.add(plane)

        #words = ['Many',' words ',' map',' to',' one',' token']
        words = ['Chapter',' 1',':',' To',' you',',',' ','200','0',' years',' later']
        
        item = tokenization(words)
        self.play(item['create'], run_time=2)
        self.play(*item['colorize'], run_time=2)

        item2 = tokens_to_variables(item)
        self.play(FadeOut(item['text_obj']))
        self.play(*item2['words2circles'], run_time=2)
        item4 = roll_chain(item2)
        self.play(*item4['anims'], run_time=2)

        circles_num = len(item2['circles'])
        line = np.random.randint(2, size=(circles_num, circles_num))
        item3 = connect_tokens(item2['circles'], line)
        self.play(*item3['animations'], run_time=2)
        self.wait()

        links = []
        connections = list(item3['lines'].keys())
        for _ in range(3):
            links.append(random.choice(connections))

        anim1 = highlight_links(links, item3['lines'])
        self.play(*anim1)
        # for r in rotations:
        #     self.play(*r)
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