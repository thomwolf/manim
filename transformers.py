from manimlib.imports import *
import os
import pyclbr
import numpy as np


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

        self.play(FadeOut(vg3), FadeIn(bull[1]))

        self.play(GrowFromCenter(CLS), GrowFromCenter(SEP))

        self.wait()

        self.play(ShowCreation(vg))

        self.wait()

        self.play(FadeOut(vg))

        self.play(FadeIn(bull[2]))

        # final_title = TextMobject("convert to vocabulary indices").to_corner(LEFT+UP)
        # final_title.scale(0.75)
        # final_title.shift(LEFT* MED_SMALL_BUFF)

        toks = VGroup(CLS, *allt, SEP)

        self.play(FadeOutAndShift(tok1, direction=UP),
                  FadeOutAndShift(bull[0], direction=UP),
                  FadeOutAndShift(bull[1], direction=UP),
                  ApplyMethod(bull[2].to_corner, LEFT+UP),
                  ApplyMethod(toks.move_to, 2 * UP))

class ThirdSentence(Scene):
    #Adding text on the screen
    def construct(self):
        bull = BulletedList("convert to vocabulary indices")
        bull.scale(0.75)
        bull.to_corner(LEFT+UP)

        toks = TextMobject("Mini"," \#van"," \#s"," park"," near"," the"," park")
        toks.move_to(2.5 * UP)
        CLS = TextMobject("[CLS]")
        CLS.next_to(toks, direction=LEFT)
        SEP = TextMobject("[SEP]")
        SEP.next_to(toks, direction=RIGHT)

        alltoks = [CLS] + [t for t in toks] + [SEP]
        alltoks = VGroup(*alltoks)
        indices = TextMobject("101", "14393","5242","1116","2493","1485","1103","2493", "102", fill_color=BLUE_D)
        indices.scale(0.75)
        for t, i in zip(alltoks, indices):
            i.next_to(t, direction=DOWN)
            i.align_to(alltoks.get_bottom(), direction=DOWN)
            i.shift(0.5*DOWN)

        # vgi = VGroup(indices)
        # vgi.next_to(alltoks.get_center(), direction=DOWN)

        voc1 = ["[PAD]", "[CLS]", "[SEP]", "the", "\#s", "near", "park", "\#van", "Mini", '\#: ']
        voc2 = ["0", "101", "102", "1103", "1116", "1485", "2493", "5242", "14393", "28995"]
        vocab = []
        arr_and_dots = []
        for txt, idx in zip(voc1, voc2):
            arr = Arrow()
            dots = TextMobject("...")
            arr_and_dots += [arr, dots]
            vg = VGroup(TextMobject(txt, fill_color=RED_E),
                        arr,
                        TextMobject(idx, fill_color=BLUE_D))
            # dots.next_to(vg, direction=DOWN)
            vocab += [vg, dots]
        vocab = vocab[:-1]
        arr_and_dots = arr_and_dots[:-1]

        arr_and_dots = VGroup(*arr_and_dots).arrange(direction=DOWN)

        for v in vocab:
            if isinstance(v, TextMobject):
                continue
            else:
                txt, arr, idx = v
                txt.next_to(v[1], direction=LEFT)
                idx.next_to(v[1], direction=RIGHT)

        vocab = VGroup(*vocab)
        vocab.scale(0.5)

        vocab.move_to(1.5*DOWN)

        rect = SurroundingRectangle(vocab, stroke_color=LIGHT_BROWN)

        bert_vocab = TextMobject("Vocabulary", fill_color=RED_E)
        bert_vocab.next_to(rect, direction=LEFT)

        indices_to_move_orr = []
        indices_to_move_target = []
        for v in vocab:
            if isinstance(v, TextMobject):
                continue
            else:
                txt, arr, idx = v
                print(indices.tex_strings, idx.tex_string)
                target_idx = list(filter(lambda s: s[1] == idx.tex_string, enumerate(indices.tex_strings)))
                if len(target_idx) == 1:
                    idx_orr: Mobject = idx.deepcopy()
                    indices_to_move_orr.append(idx_orr)
                    indices_to_move_target.append(indices[target_idx[0][0]])
                elif len(target_idx) == 2:
                    idx_orr = idx.deepcopy()
                    idx_orr_2 = idx.deepcopy()
                    indices_to_move_orr += [idx_orr, idx_orr_2]
                    indices_to_move_target += indices[target_idx[0][0]], indices[target_idx[1][0]]
                else:
                    print("nothing for", idx.tex_string)
                    continue

        indices_to_move_orr = VGroup(*indices_to_move_orr)
        indices_to_move_target = VGroup(*indices_to_move_target)

        height = max(t.get_height() for t in indices_to_move_target) + SMALL_BUFF
        indices_to_move_ordered = sorted(indices_to_move_target, key=lambda i: i.get_left()[0])
        fb1 = []
        fbi = []
        for i, t in enumerate(indices_to_move_ordered):
            r = Rectangle(width=t.get_width() + SMALL_BUFF, height = height, color=BLUE_E)
            r.align_to(t.get_top() + 0.5*SMALL_BUFF, direction=UP)
            r.align_to(t.get_right() + 0.5*SMALL_BUFF, direction=RIGHT)
            # fb1.append(r)
            n = TextMobject(str(i + 1))
            n.next_to(r, direction=DOWN)
            fb1.append(VGroup(r, n))
            fbi.append(n)

        vg = VGroup(*fb1)
        vgi = VGroup(*fbi)

        self.add(alltoks, bull)

        self.play(ShowCreation(vocab))
        self.play(ShowCreation(rect), Write(bert_vocab))
        self.wait(2)

        self.play(Transform(indices_to_move_orr, indices_to_move_target))

        self.wait(2)
        self.play(ShowCreation(vg))

        self.wait(2)

        model_inputs = []
        for t, fr in zip(vg, indices_to_move_ordered):
            model_inputs.append(VGroup(t, fr))
        model_inputs = VGroup(*model_inputs)

        self.play(FadeOut(vocab),
                  FadeOut(alltoks),
                  FadeOut(bull),
                  FadeOut(rect),
                  FadeOut(bert_vocab))

        self.play(FadeOut(indices_to_move_orr), ApplyMethod(model_inputs.arrange))

        self.wait(2)

class ForthSentence(Scene):
    #Adding text on the screen
    def construct(self):
        tok1 = Title("2. Transformer")

        tok2 = TextMobject("2. Transformer")
        tok2.to_corner(LEFT+UP)

        bull = BulletedList("word embeddings", "position embeddings", "first hidden-state")
        bull.scale(0.75)
        bull.next_to(tok2, direction=DOWN, aligned_edge=LEFT)
        bull.shift((RIGHT + DOWN)* MED_SMALL_BUFF)

        indices = TextMobject("101", "14393","5242","1116","2493","1485","1103","2493", "102", fill_color=BLUE_D)
        indices.scale(0.75)

        down_amount = BOTTOM + MED_SMALL_BUFF*UP

        height = max(t.get_height() for t in indices) + SMALL_BUFF
        fb1 = []
        fbi = []
        for i, t in enumerate(indices):
            r = Rectangle(width=t.get_width() + SMALL_BUFF, height = height, color=BLUE_E)
            r.align_to(t.get_top() + 0.5*SMALL_BUFF, direction=UP)
            r.align_to(t.get_right() + 0.5*SMALL_BUFF, direction=RIGHT)
            n = TextMobject(str(i + 1))
            n.next_to(r, direction=DOWN)
            fb1.append(r)
            fbi.append(n)

        vg = VGroup(*fb1)
        vgi = VGroup(*fbi)

        model_inputs = []
        for t, fr in zip(vg, indices):
            model_inputs.append(VGroup(t, fr))
        model_inputs = VGroup(*model_inputs)

        model_inputs.arrange()
        for m, i in zip(model_inputs, fbi):
            i.next_to(m, direction=DOWN)

        vector1 = ["1.2", "0.7", "0.2", "-1.2", "-0.1", "1.8"]
        vector2 = ["0.3", "1.8", "0.2", "0.7", "-1.2", "-0.1"]
        vector3 = ["2.1", "-0.1", "0.7", "0.2", "-1.2", "1.8"]
        vector4 = ["-1.1", "0.2", "-1.2", "-0.1", "1.8", "0.7"]
        vector5 = ["-0.3", "-1.2", "-0.1", "1.8", "0.7", "0.2"]
        vector6 = ["1.4", "-1.2", "-0.1", "0.2", "1.8", "0.7"]

        def build_vector(vect, inner_color=PURPLE_E, outer_color=LIGHT_PINK, text_color=BLUE_A):
            vects = list(TextMobject(v, color=text_color) for v in vect)
            rects = list(Rectangle(width=LARGE_BUFF, height=LARGE_BUFF,
                                color=outer_color, fill_color=inner_color, fill_opacity=1.)
                        for _ in range(6))
            vs = VGroup(*vects)
            hs = VGroup(*rects)
            hs.arrange(buff=0)
            for h, v in zip(hs, vs):
                v.move_to(h)
            return VGroup(hs, vs)

        hsa = build_vector(vector1)

        def create_mapping(voc1, voc2, dot_only_last=False, inner_color=PURPLE_E, outer_color=LIGHT_PINK, text_color=BLUE_A):
            vocab = []
            arr_and_dots = []
            for txt, vec in zip(voc1, voc2):
                arr = Arrow()
                hs = build_vector(vec, inner_color=inner_color, outer_color=outer_color, text_color=text_color)
                hs.scale(0.75)
                if dot_only_last:
                    arr_and_dots += [arr]
                else:
                    dots = TextMobject("...")
                    arr_and_dots += [arr, dots]
                vg = VGroup(TextMobject(txt, fill_color=BLUE_D),
                            arr,
                            hs)
                # dots.next_to(vg, direction=DOWN)
                if dot_only_last:
                    vocab += [vg]
                else:
                    vocab += [vg, dots]
            if dot_only_last:
                dots = TextMobject("...")
                vocab = vocab[:-1] + [dots, vocab[-1]]
                arr_and_dots = arr_and_dots[:-1] + [dots, arr_and_dots[-1]]
            else:
                vocab = vocab[:-1]
                arr_and_dots = arr_and_dots[:-1]

            arr_and_dots = VGroup(*arr_and_dots)
            arr_and_dots.arrange(direction=DOWN,
                                 buff=(MED_LARGE_BUFF if dot_only_last else MED_SMALL_BUFF))

            for v in vocab:
                if isinstance(v, TextMobject):
                    continue
                else:
                    txt, arr, idx = v
                    txt.next_to(v[1], direction=LEFT)
                    idx.next_to(v[1], direction=RIGHT)

            return arr_and_dots, vocab

        def create_init_target(vocab, indices):
            vector_init = []
            vector_target = []
            for v in vocab:
                if isinstance(v, TextMobject):
                    continue
                else:
                    txt, arr, vect = v
                    print(txt.tex_string)
                    if isinstance(indices, TextMobject):
                        target_idx = list(filter(lambda s: s[1] == txt.tex_string, enumerate(indices.tex_strings)))
                    else:
                        target_idx = list(filter(lambda s: s[1].tex_string == txt.tex_string, enumerate(indices)))
                    if len(target_idx) == 1:
                        idx_orr: Mobject = vect
                        idx_target = idx_orr.deepcopy()
                        idx_target.rotate(-np.pi/2)
                        idx_target.next_to(indices[target_idx[0][0]], direction=UP)
                        vector_init.append(idx_orr)
                        vector_target.append(idx_target)
                    elif len(target_idx) == 2:
                        idx_orr = vect
                        idx_target = idx_orr.deepcopy()
                        idx_target.rotate(-np.pi/2)
                        idx_target.next_to(indices[target_idx[0][0]], direction=UP)

                        idx_orr_2 = vect.deepcopy()
                        idx_target_2 = idx_orr_2.deepcopy()
                        idx_target_2.rotate(-np.pi/2)
                        idx_target_2.next_to(indices[target_idx[1][0]], direction=UP)

                        vector_init += [idx_orr, idx_orr_2]
                        vector_target += [idx_target, idx_target_2]
                    else:
                        print("nothing for", txt.tex_string)
                        continue

            vector_init = VGroup(*vector_init)
            vector_target = VGroup(*vector_target)
            return vector_init, vector_target

        voc1 = ["0", "101", "102", "1103", "1116", "1485", "2493", "5242", "14393", "28995"]
        voc2 = [vector1, vector5, vector2, vector3, vector4, vector5, vector6, vector3, vector2, vector1]

        arr_and_dots, vocab = create_mapping(voc1, voc2, inner_color=PURPLE_E, outer_color=LIGHT_PINK, text_color=BLUE_A)

        vocabg = VGroup(*vocab)
        vocabg.scale(0.6)
        vocabg.center()
        vocabg.shift(UP)

        rect = SurroundingRectangle(vocabg, stroke_color=LIGHT_BROWN)

        vector_init, vector_target = create_init_target(vocab, indices)
        vector_target.move_to(down_amount + 2*UP)

        vi = list(v[0] for v in vocab if not isinstance(v, TextMobject))
        vi = VGroup(*vi)

        voc_p1 = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "512"]
        voc_p2 = [vector5, vector6, vector3, vector2, vector1, vector5, vector2, vector1, vector3, vector4]

        parr_and_dots, pvocab = create_mapping(voc_p1, voc_p2, dot_only_last=True, inner_color=TEAL_E, outer_color=TEAL_A, text_color=DARK_BLUE)

        pvocabg = VGroup(*pvocab)
        pvocabg.scale(0.6)
        pvocabg.center()
        pvocabg.shift(UP)

        prect = SurroundingRectangle(pvocabg, stroke_color=LIGHT_BROWN)

        pvector_init, pvector_target = create_init_target(pvocab, fbi)
        pvector_target.move_to(down_amount + 2*UP)

        pvi = list(v[0] for v in pvocab if not isinstance(v, TextMobject))
        pvi = VGroup(*pvi)

        self.add(model_inputs, vgi)

        self.play(GrowFromCenter(tok1))

        self.wait(2)

        self.play(Transform(tok1, tok2))

        self.wait(2)

        self.play(FadeIn(bull[0]), ApplyMethod(vgi.move_to, down_amount+DOWN), ApplyMethod(model_inputs.move_to, down_amount))

        self.wait(2)

        self.play(GrowFromCenter(hsa))

        self.wait(2)

        first_v = vocab[0][2]
        vocab[0].remove(first_v)

        self.play(Transform(hsa, first_v))

        self.wait(2)

        bert_vocab = TextMobject("Word Embeddings", fill_color=RED_E)
        bert_vocab.next_to(rect, direction=LEFT)

        self.play(ShowCreation(vocabg))
        self.play(ShowCreation(rect))
        self.play(Write(bert_vocab))

        self.wait(2)

        self.play(FadeOut(arr_and_dots),
                  Transform(vector_init, vector_target))

        self.play(FadeOut(rect),
                  FadeOut(bert_vocab),
                  FadeOut(hsa),
                  FadeOut(vi),
                  FadeOut(vocab[-1][2]))

        self.wait(2)

        self.play(FadeIn(bull[1]))

        self.wait(2)

        self.play(ApplyMethod(vgi.shift, UP + MED_SMALL_BUFF*UP),
                  ApplyMethod(model_inputs.shift, UP),
                  ApplyMethod(vector_init.shift, UP))

        self.wait(2)

        wi = VGroup(model_inputs, vector_init)
        wt2 = wi.deepcopy()
        wt = wi.deepcopy()
        wt.move_to(TOP + DOWN + RIGHT_SIDE + 2*LEFT)
        wt.scale(0.4)

        self.play(Transform(wi, wt))

        pbert_vocab = TextMobject("Positional", "Embeddings", fill_color=RED_E)
        pbert_vocab.arrange(direction=DOWN)
        pbert_vocab.next_to(prect, direction=LEFT)
        pbert_vocab.shift(0.5*DOWN)

        self.play(ShowCreation(pvocabg))
        self.play(ShowCreation(prect))
        self.play(Write(pbert_vocab))

        self.wait(2)

        self.play(FadeOut(parr_and_dots),
                  Transform(pvector_init, pvector_target))

        self.play(FadeOut(prect),
                  FadeOut(pbert_vocab),
                  FadeOut(pvi),
                  FadeOut(pvocab[-1][2]))

        self.wait(2)

        self.play(ApplyMethod(pvector_init.shift, 2*RIGHT),
                  ApplyMethod(vgi.shift, 2*RIGHT))

        wt2[0].next_to(wt2[1], direction=UP)
        wt2.shift(2*RIGHT + 2.5*UP)
        self.play(Transform(wi, wt2))

        plus = list(TexMobject("+") for _ in range(9))
        for p, v in zip(plus, vgi):
            p.next_to(v, direction=UP)
            p.shift(3*UP - UP*SMALL_BUFF)
        plus = VGroup(*plus)

        self.play(ShowCreation(plus))

        self.wait(2)

        self.play(FadeIn(bull[2]))

        def make_final(vector_init):
            vector_final = vector_init.deepcopy()
            for v in vector_final:
                for r in v[0]:
                    assert isinstance(r, Rectangle)
                    r.set_fill(GOLD_D)
                    r.set_stroke(GREY_BROWN)
                for r in v[1]:
                    assert isinstance(r, TexMobject)
                    r.set_fill(BLACK)
            vector_final.center()
            vector_final.shift(2*RIGHT)
            return vector_final

        vector_final = make_final(vector_init)
        vector_final_2 = make_final(pvector_init)

        self.play(FadeOut(plus),
                  FadeOut(wi[0]),
                  FadeOut(vgi),
                  ApplyMethod(wi[1].shift, -wi[1].get_center() + 2*RIGHT + RIGHT*MED_LARGE_BUFF),
                  ApplyMethod(pvector_init.shift, -pvector_init.get_center() + 2*RIGHT),
                  )
        
        self.play(
                  Transform(wi[1], vector_final),
                  Transform(pvector_init, vector_final_2))

        self.wait(2)

        self.remove(wi[1])
