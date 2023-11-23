from manim import *

from utils.attention import tokenization, tokens_to_variables


class ColorText(Scene):
    def construct(self):
        item = tokenization(
            ['Many',' words ',' map',' to',' one',' token']
        )
        self.play(item['create'], run_time=2)
        self.play(*item['colorize'], run_time=2)

        item2 = tokens_to_variables(item)
        self.play(FadeOut(item['text_obj']))
        self.play(*item2['words2circles'], run_time=2)
        self.play(*item2['vars'])
        self.wait(2)