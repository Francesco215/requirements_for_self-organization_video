import random

from manim import *

from utils.attention import tokenization, tokens_to_variables, roll_chain


class ColorText(Scene):
    def construct(self):
        words = ['Many',' words ',' map',' to',' one',' token']
        item = tokenization(
            [random.choice(words) for _ in range(10)]
        )
        self.play(item['create'], run_time=2)
        self.play(*item['colorize'], run_time=2)

        item2 = tokens_to_variables(item)
        self.play(FadeOut(item['text_obj']))
        self.play(*item2['words2circles'], run_time=2)
        anims = roll_chain(item2)
        self.play(*anims, run_time=2)
        self.wait(2)