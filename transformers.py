from manimlib.imports import *
import os
import pyclbr


SVG_IMAGE_DIR = "/Users/thomwolf/Library/Mobile Documents/com~apple~CloudDocs/Work/transformers/SVG/"


class Park(SVGMobject):
    CONFIG = {
        "color" : BLUE_E,
        "file_name_prefix": "stick_man",
        "stroke_width" : 2,
        "stroke_color" : WHITE,
        "fill_opacity" : 1.0,
        "height" : 3,
    }
    def __init__(self, **kwargs):
        digest_config(self, kwargs)
        self.parts_named = False
        try:
            svg_file = os.path.join(
                SVG_IMAGE_DIR,
                "park.svg"
            )
            SVGMobject.__init__(self, file_name=svg_file, **kwargs)
        except:
            warnings.warn("No %s design with mode %s" %
                            (self.file_name_prefix, mode))
            svg_file = os.path.join(
                SVG_IMAGE_DIR,
                "stick_man_plain.svg",
            )
            SVGMobject.__init__(self, mode="plain", file_name=svg_file, **kwargs)


    def name_parts(self):
        self.head = self.submobjects[HEAD_INDEX]
        self.body = self.submobjects[BODY_INDEX]
        self.arms = self.submobjects[ARMS_INDEX]
        self.legs = self.submobjects[LEGS_INDEX]
        self.parts_named = True

    def init_colors(self):
        SVGMobject.init_colors(self)
        if not self.parts_named:
            self.name_parts()
        self.head.set_fill(self.color, opacity = 1)
        self.body.set_fill(RED, opacity = 1)
        self.arms.set_fill(YELLOW, opacity = 1)
        self.legs.set_fill(BLUE, opacity = 1)
        return self


class OpeningSentence(Scene):
    #Adding text on the screen
    def construct(self):
        # park = SVGMobject(os.path.join(SVG_IMAGE_DIR, "Fichier 8.svg"))
        # self.add(park)

        # minivan1 = SVGMobject(file_name=os.path.join(SVG_IMAGE_DIR, "minivan.svg"), mode="plain")
        # minivan2 = SVGMobject(file_name=os.path.join(SVG_IMAGE_DIR, "minivan.svg"), mode="plain")
        # minivan1.next_to(park, RIGHT)
        # minivan2.next_to(minivan1, RIGHT)

        # self.add(minivan1, minivan2)

        ipt = "Minivans park near the park"
        ipts = ["Minivans"," park"," near"," the"," park"]

        text = TextMobject(*ipts)

        self.play(Write(text))
        self.wait(.5)

        fb1 = SurroundingRectangle(text[0], buff = 0.5*SMALL_BUFF)
        fb2 = SurroundingRectangle(text[1], buff = 0.5*SMALL_BUFF, color = BLUE)
        fb3 = SurroundingRectangle(text[4], buff = 0.5*SMALL_BUFF, color = BLUE)

        self.play(ShowCreation(fb1))

        self.wait(2)

        fbs = VGroup(fb2, fb3)

        self.play(FadeOut(fb1), ShowCreation(fbs))

        self.wait(2)

        self.play(FadeOut(fbs))


class SecondSentence(Scene):
    #Adding text on the screen
    def construct(self):

        allt = TextMobject("Minivans"," park"," near"," the"," park")

        mnvs = TextMobject("Mini"," \#van"," \#s")
        mnvs.next_to(allt[1], direction=LEFT)

        CLS = TextMobject("[CLS]")
        CLS.next_to(mnvs, direction=LEFT)

        SEP = TextMobject("[SEP]")
        SEP.next_to(allt[-1], direction=RIGHT)

        final_toks = [CLS] + [t for t in mnvs] + [t for t in allt[1:]] + [SEP]
        height = max(t.get_height() for t in final_toks) + SMALL_BUFF
        fb1 = []
        for i, t in enumerate(final_toks):
            r = Rectangle(width=t.get_width() + SMALL_BUFF, height = height, color=BLUE_E)
            r.align_to(t.get_right() + 0.5*SMALL_BUFF, direction=RIGHT)
            fb1.append(r)
            n = TextMobject(str(i + 1))
            n.next_to(r, direction=DOWN)
            fb1.append(n)

        vg = VGroup(*fb1)
        vg2 = VGroup(*fb1[1::2])

        self.add(allt)

        tok1 = Title("1. Tokenization")

        self.play(GrowFromCenter(tok1))

        self.wait(2)

        tok2 = TextMobject("1. Tokenization")
        tok2.to_corner(LEFT+UP)

        tokab = TextMobject("Finite size vocabulary", fill_color=LIGHT_BROWN)
        tokab.scale(0.75)
        tokab.to_corner(RIGHT+UP)
        tokac = TextMobject("Open ended corpus", fill_color=LIGHT_BROWN)
        tokac.scale(0.75)
        tokac.next_to(tokab, direction=DOWN)

        bull = BulletedList("split complex words", "add special tokens", "convert to vocabulary indices")
        bull.scale(0.75)
        bull.next_to(tok2, direction=DOWN, aligned_edge=LEFT)
        bull.shift((RIGHT + DOWN)* MED_SMALL_BUFF)

        vg3 = VGroup(tokab, tokac)

        self.play(Transform(tok1, tok2))
        self.play(FadeIn(tokab))
        self.play(FadeIn(tokac))

        self.wait(2)

        self.play(FadeIn(bull[0]))
        # ipts2 = ["Mini"," \#van"," \#s"," park"," near"," the"," park"]
        # text_split = TextMobject(*ipts2)
        self.play(Transform(allt[0], mnvs))

        self.wait(2)

        self.play(FadeIn(bull[1]))

        self.play(GrowFromCenter(CLS), GrowFromCenter(SEP))

        self.wait()

        self.play(ShowCreation(vg))

        self.wait()

        self.play(FadeOut(vg))

        self.play(FadeIn(bull[2]))
