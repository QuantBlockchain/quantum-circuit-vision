"""QCV v5b — 加统一过渡帧 + 居中修复"""
from manim import *

BG = "#1a1a2e"
C_BLUE = "#4A90D9"
C_YELLOW = "#F5C842"
C_RED = "#E74C3C"
C_GREEN = "#2ECC71"
C_ORANGE = "#F39C12"
C_PURPLE = "#9B59B6"
C_GREY = "#7f8c8d"
C_LIGHT = "#ecf0f1"

TITLE_SIZE = 36
SUBTITLE_SIZE = 22
BODY_SIZE = 20
SMALL_SIZE = 14
LABEL_SIZE = 12

class QCVv5b(Scene):
    def construct(self):
        self.camera.background_color = BG

        def transition(text_en, text_cn):
            """统一过渡帧：正中间，停留1秒"""
            t1 = Text(text_en, font_size=26, color=C_GREEN, weight=BOLD)
            t2 = Text(text_cn, font_size=SUBTITLE_SIZE, color=C_YELLOW)
            g = VGroup(t1, t2).arrange(DOWN, buff=0.2)
            self.play(FadeIn(g, shift=UP*0.2), run_time=0.5)
            self.wait(0.8)
            self.play(FadeOut(g), run_time=0.3)

        # ═══ Scene 0: 100 Years of Computation ══════════════════════
        t0 = Text("100 Years of Computation", font_size=TITLE_SIZE, color=C_LIGHT, weight=BOLD)
        t0cn = Text("百年计算史", font_size=SUBTITLE_SIZE, color=C_YELLOW)
        VGroup(t0, t0cn).arrange(DOWN, buff=0.15).move_to(UP*2.5)
        self.play(Write(t0), FadeIn(t0cn), run_time=0.8)

        # 时间线
        timeline = Line(LEFT*5, RIGHT*5, color=C_GREY, stroke_width=2).move_to(UP*0.3)
        self.play(Create(timeline), run_time=0.8)

        # 三个节点
        nodes = [
            (LEFT*3.5, "1947", "Transistor", "Electrons", C_BLUE),
            (ORIGIN, "1971", "Microchip", "Electrons", C_BLUE),
            (RIGHT*3.5, "2019", "Qubit", "Quantum", C_GREEN),
        ]
        for pos, yr, name, era, color in nodes:
            dot = Dot(point=pos + UP*0.3, radius=0.12, color=color)
            yr_t = Text(yr, font_size=18, color=color, weight=BOLD).next_to(dot, UP, buff=0.2)
            name_t = Text(name, font_size=16, color=C_LIGHT).next_to(dot, DOWN, buff=0.2)
            era_t = Text(era, font_size=LABEL_SIZE, color=C_GREY, font="Arial").next_to(name_t, DOWN, buff=0.08)
            self.play(GrowFromCenter(dot), FadeIn(yr_t), FadeIn(name_t), FadeIn(era_t), run_time=0.5)

        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # 过渡
        t_en = Text("Same question, new physics:", font_size=24, color=C_GREEN)
        t_en2 = Text("How do you go from diagram to machine?", font_size=24, color=C_GREEN, weight=BOLD)
        t_cn = Text("同一个问题，新的物理：怎么从图纸变成机器？", font_size=SUBTITLE_SIZE, color=C_YELLOW)
        g = VGroup(t_en, t_en2, t_cn).arrange(DOWN, buff=0.2)
        self.play(FadeIn(g, shift=UP*0.2), run_time=0.5)
        self.wait(1)
        self.play(FadeOut(g), run_time=0.3)

        # ═══ Scene 1: 量子时代 ═══════════════════════════════════════
        year = Text("2025", font_size=100, color=C_BLUE, weight=BOLD)
        sub1 = Text("The Quantum Inflection Point", font_size=26, color=C_LIGHT)
        sub2 = Text("量子拐点之年", font_size=SUBTITLE_SIZE, color=C_YELLOW)
        VGroup(year, sub1, sub2).arrange(DOWN, buff=0.2).move_to(UP*1.5)

        self.play(Write(year), run_time=1)
        self.play(FadeIn(sub1), FadeIn(sub2), run_time=0.5)

        milestones = VGroup()
        for letter, line1, line2 in [("N", "Nobel Prize", "诺贝尔物理学奖"), ("T", "Turing Award", "图灵奖"), ("UN", "UN Quantum Year", "联合国量子年")]:
            c = Circle(radius=0.55, color=C_BLUE, fill_opacity=0.25, stroke_width=2)
            l = Text(letter, font_size=22, color=WHITE, weight=BOLD).move_to(c)
            t1 = Text(line1, font_size=SMALL_SIZE, color=C_LIGHT).next_to(c, DOWN, buff=0.15)
            t2 = Text(line2, font_size=LABEL_SIZE, color=C_GREY, font="Arial").next_to(t1, DOWN, buff=0.05)
            milestones.add(VGroup(c, l, t1, t2))
        milestones.arrange(RIGHT, buff=1.5).move_to(DOWN*1.5)
        for m in milestones:
            self.play(GrowFromCenter(m[0]), FadeIn(m[1]), FadeIn(m[2]), FadeIn(m[3]), run_time=0.4)
        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # 过渡
        transition("Quantum computing is real. But...", "量子计算已成现实。但是...")

        # ═══ Scene 2: 量子电路 = 软件 (类比) ══════════════════════
        t2a = Text("Think of it this way", font_size=TITLE_SIZE, color=C_LIGHT, weight=BOLD)
        t2acn = Text("这样理解", font_size=SUBTITLE_SIZE, color=C_YELLOW)
        VGroup(t2a, t2acn).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.5)
        self.play(Write(t2a), FadeIn(t2acn), run_time=0.5)

        rows = [
            ("CPU", "Quantum Processor"),
            ("Code (Python)", "Quantum Circuit"),
            ("Circuit Diagram", "QC Diagram"),
        ]
        left_header = Text("Classical", font_size=18, color=C_BLUE, weight=BOLD).move_to(LEFT*3.5 + UP*1.2)
        right_header = Text("Quantum", font_size=18, color=C_GREEN, weight=BOLD).move_to(RIGHT*2.5 + UP*1.2)
        self.play(FadeIn(left_header), FadeIn(right_header), run_time=0.3)

        for i, (left, right) in enumerate(rows):
            y = 0.3 - i * 1.0
            lt = Text(left, font_size=20, color=C_BLUE).move_to(LEFT*3.5 + UP*y)
            eq = Text("=", font_size=24, color=C_GREY).move_to(LEFT*0.5 + UP*y)
            rt = Text(right, font_size=20, color=C_GREEN).move_to(RIGHT*2.5 + UP*y)
            self.play(FadeIn(lt), FadeIn(eq), FadeIn(rt), run_time=0.45)

        punchline = Text("Quantum circuits ARE the software of quantum computers", font_size=18, color=C_YELLOW, weight=BOLD).move_to(DOWN*2.3)
        punchline_cn = Text("量子电路就是量子计算机的软件", font_size=16, color=C_YELLOW).next_to(punchline, DOWN, buff=0.15)
        self.play(FadeIn(punchline), FadeIn(punchline_cn), run_time=0.7)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # 过渡
        transition("A $450 billion market is waiting", "一个4500亿美元的市场在等待")

        # ═══ Scene 3: $450B 独立冲击页 ══════════════════════════════
        big_money = Text("$450B", font_size=140, color=C_ORANGE, weight=BOLD)
        money_sub = Text("quantum computing market by 2040", font_size=22, color=C_LIGHT)
        money_cn = Text("2040年量子计算市场规模", font_size=18, color=C_YELLOW)
        VGroup(big_money, money_sub, money_cn).arrange(DOWN, buff=0.25)
        self.play(Write(big_money), run_time=1.2)
        self.play(FadeIn(money_sub), FadeIn(money_cn), run_time=0.5)
        self.wait(0.8)

        but_line = Text("But no one can write the software fast enough", font_size=20, color=C_RED).to_edge(DOWN, buff=0.6)
        but_cn = Text("但没人能快速编写这些软件", font_size=16, color=C_RED).next_to(but_line, DOWN, buff=0.1)
        self.play(FadeIn(but_line), FadeIn(but_cn), run_time=0.6)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # 过渡
        transition("Here's why", "原因在这里")

        # ═══ Scene 4: The Gap (精简版) ══════════════════════════════
        title2 = Text("The Gap", font_size=TITLE_SIZE, color=C_RED, weight=BOLD)
        title2cn = Text("鸿沟", font_size=SUBTITLE_SIZE, color=C_YELLOW)
        VGroup(title2, title2cn).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.5)
        self.play(Write(title2), FadeIn(title2cn), run_time=0.5)

        n1 = Text("100,000", font_size=60, color=C_BLUE, weight=BOLD).move_to(LEFT*3 + UP*0.5)
        n1_sub = Text("circuits published / year", font_size=SMALL_SIZE, color=C_GREY, font="Arial").next_to(n1, DOWN, buff=0.1)
        self.play(FadeIn(n1, shift=LEFT*0.5), FadeIn(n1_sub), run_time=0.6)

        n2 = Text("1-4 hrs", font_size=60, color=C_RED, weight=BOLD).move_to(RIGHT*3 + UP*0.5)
        n2_sub = Text("to translate each manually", font_size=SMALL_SIZE, color=C_GREY, font="Arial").next_to(n2, DOWN, buff=0.1)
        self.play(FadeIn(n2, shift=RIGHT*0.5), FadeIn(n2_sub), run_time=0.6)

        zero = Text("0", font_size=100, color=C_RED, weight=BOLD).move_to(DOWN*1.5)
        zero_sub = Text("automated tools exist", font_size=18, color=C_RED).next_to(zero, DOWN, buff=0.1)
        self.play(Write(zero), run_time=0.8)
        self.play(FadeIn(zero_sub), run_time=0.4)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # 过渡
        transition("What if machines could see what physicists see?", "如果机器能看到物理学家看到的东西呢？")

        # ═══ Scene 3: QCV 野心 ══════════════════════════════════════
        q1 = Text("Can AI read quantum circuits?", font_size=TITLE_SIZE, color=C_LIGHT)
        q2 = Text("Can AI design NEW ones?", font_size=TITLE_SIZE, color=C_YELLOW, weight=BOLD)
        VGroup(q1, q2).arrange(DOWN, buff=0.35).move_to(UP*1.2)
        self.play(Write(q1), run_time=0.9)
        self.play(Write(q2), run_time=0.9)

        sep = Line(LEFT*5.5, RIGHT*5.5, color=C_GREY, stroke_width=1, stroke_opacity=0.3).move_to(DOWN*0.3)
        self.play(Create(sep), run_time=0.2)
        af = Text("AlphaFold:", font_size=16, color=C_GREY).move_to(LEFT*5+DOWN*1.0)
        af_f = Text("Sequence --> Structure", font_size=16, color=C_GREY).next_to(af, RIGHT, buff=0.2)
        qcv_l = Text("QCV:", font_size=16, color=C_BLUE, weight=BOLD).move_to(LEFT*5+DOWN*1.8)
        qcv_f = Text("Diagram --> Code --> ", font_size=16, color=C_BLUE).next_to(qcv_l, RIGHT, buff=0.2)
        qcv_n = Text("NEW Circuits", font_size=16, color=C_YELLOW, weight=BOLD).next_to(qcv_f, RIGHT, buff=0)
        self.play(FadeIn(af), FadeIn(af_f), run_time=0.5)
        self.play(FadeIn(qcv_l), FadeIn(qcv_f), FadeIn(qcv_n), run_time=0.6)
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # 过渡
        transition("We started by teaching AI to read", "我们从教 AI 阅读开始")

        # ═══ Scene 4: 数据集 ════════════════════════════════════════
        t4 = Text("QCV-Dataset", font_size=38, color=C_ORANGE, weight=BOLD)
        t4s = Text("132 circuits  x  7 modalities", font_size=BODY_SIZE, color=C_LIGHT)
        VGroup(t4, t4s).arrange(DOWN, buff=0.12).to_edge(UP, buff=0.4)
        self.play(Write(t4), FadeIn(t4s), run_time=0.6)

        mods = ["Images", "Braket", "Qiskit", "Results", "Annot.", "Targets", "Equiv."]
        mod_colors = [C_BLUE, C_GREEN, C_GREEN, C_ORANGE, C_YELLOW, C_PURPLE, C_GREY]
        mod_group = VGroup()
        for name, col in zip(mods, mod_colors):
            r = RoundedRectangle(width=1.25, height=0.65, corner_radius=0.06, color=col, fill_opacity=0.3, stroke_width=1.5)
            t = Text(name, font_size=LABEL_SIZE, color=WHITE).move_to(r)
            mod_group.add(VGroup(r, t))
        mod_group.arrange(RIGHT, buff=0.1).move_to(UP*1.2)
        self.play(*[GrowFromCenter(g[0]) for g in mod_group], *[FadeIn(g[1]) for g in mod_group], run_time=0.6)

        pipe_data = [("Image", C_BLUE), ("AI (BV/TV)", C_PURPLE), ("Code", C_GREEN), ("Verify", C_YELLOW)]
        pipe_group = VGroup()
        for name, col in pipe_data:
            r = RoundedRectangle(width=2.0, height=0.75, corner_radius=0.08, color=col, fill_opacity=0.25, stroke_width=1.5)
            t = Text(name, font_size=15, color=col, weight=BOLD).move_to(r)
            pipe_group.add(VGroup(r, t))
        pipe_group.arrange(RIGHT, buff=0.35).move_to(DOWN*1.2)
        self.play(FadeIn(pipe_group), run_time=0.5)
        for i in range(3):
            a = Arrow(pipe_group[i].get_right(), pipe_group[i+1].get_left(), buff=0.04, color=WHITE, stroke_width=1.5, max_tip_length_to_length_ratio=0.15)
            self.play(Create(a), run_time=0.12)

        conns = [(0, 0, "input"), (3, 3, "verify"), (5, 1, "context")]
        for mi, pi, label in conns:
            dl = DashedLine(mod_group[mi].get_bottom(), pipe_group[pi].get_top(), color=mod_colors[mi], dash_length=0.08, stroke_width=1.5, stroke_opacity=0.5)
            lt = Text(label, font_size=10, color=mod_colors[mi]).move_to(dl.get_center()+RIGHT*0.4)
            self.play(Create(dl), FadeIn(lt), run_time=0.25)
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # 过渡
        transition("The results surprised us", "结果出乎我们意料")

        # ═══ Scene 5: 97% ═══════════════════════════════════════════
        big = Text("97%", font_size=140, color=C_GREEN, weight=BOLD)
        big_sub = Text("AI reads quantum circuits correctly", font_size=22, color=C_LIGHT)
        big_cn = Text("AI 正确理解量子电路", font_size=18, color=C_YELLOW)
        VGroup(big, big_sub, big_cn).arrange(DOWN, buff=0.25)
        self.play(Write(big), run_time=1.2)
        self.play(FadeIn(big_sub), FadeIn(big_cn), run_time=0.5)
        comp = Text("Opus 97%   Sonnet 88%   Haiku 46%", font_size=16, color=C_GREY).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(comp), run_time=0.4)
        self.wait(1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # 过渡
        transition("But the real discovery was deeper", "但真正的发现更深层")

        # ═══ Scene 6: CoT Window ════════════════════════════════════
        t6 = Text("CoT Sensitivity Window", font_size=TITLE_SIZE, color=C_BLUE, weight=BOLD)
        t6cn = Text("链式思维敏感度窗口", font_size=SUBTITLE_SIZE, color=C_YELLOW)
        VGroup(t6, t6cn).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.4)
        self.play(Write(t6), FadeIn(t6cn), run_time=0.5)

        for txt, x in [("Easy", -3.5), ("Medium", 0), ("Hard", 3.5)]:
            self.add(Text(txt, font_size=LABEL_SIZE, color=C_GREY, font="Arial").move_to(RIGHT*x + UP*1.6))

        bar_left = -4.0
        bar_width = 8.0
        x_start = RIGHT*(bar_left + bar_width/2)
        models = [
            ("Haiku", C_ORANGE, 0.6, [(0, 0.55, C_GREEN), (0.65, 0.35, C_RED)]),
            ("Opus", C_BLUE, -0.3, [(0.3, 0.25, C_GREEN), (0.65, 0.2, C_RED)]),
            ("Sonnet", C_PURPLE, -1.2, []),
        ]
        for name, color, y, segments in models:
            nm = Text(name, font_size=15, color=color, weight=BOLD).move_to(LEFT*5.5 + UP*y)
            bg = Rectangle(width=bar_width, height=0.4, color=color, fill_opacity=0.06, stroke_width=0.5).move_to(x_start + UP*y)
            self.play(FadeIn(nm), FadeIn(bg), run_time=0.2)
            for start_frac, width_frac, seg_color in segments:
                seg = Rectangle(width=bar_width*width_frac, height=0.4, color=seg_color, fill_opacity=0.45, stroke_width=0)
                seg_x = bar_left + bar_width*start_frac + bar_width*width_frac/2
                seg.move_to(RIGHT*seg_x + UP*y)
                self.play(FadeIn(seg), run_time=0.2)
            lbl = {"Haiku": "wide window", "Opus": "narrow", "Sonnet": "no effect"}[name]
            self.play(FadeIn(Text(lbl, font_size=11, color=color).move_to(RIGHT*(bar_left+bar_width+0.8)+UP*y)), run_time=0.12)

        conc = Text("CoT only helps near the capability boundary", font_size=BODY_SIZE, color=C_YELLOW, weight=BOLD).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(conc), run_time=0.6)
        self.wait(1.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # 过渡
        transition("And it has real-world consequences", "而且它有现实世界的影响")

        # ═══ Scene 7: Blockchain ════════════════════════════════════
        t7 = Text("Quantum-Safe Blockchain", font_size=TITLE_SIZE, color=C_RED, weight=BOLD)
        t7cn = Text("量子安全区块链", font_size=SUBTITLE_SIZE, color=C_YELLOW)
        VGroup(t7, t7cn).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.4)
        self.play(Write(t7), FadeIn(t7cn), run_time=0.5)

        for pos, title, color, content in [(LEFT*3.5,"ATTACK",C_RED,"Shor vs ECDSA\nGrover vs SHA-256"),(ORIGIN,"DEFENSE",C_GREEN,"Kyber / Dilithium\nSPHINCS+"),(RIGHT*3.5,"INFRA",C_BLUE,"QKD Network\nRandom Beacon")]:
            c = RoundedRectangle(width=3.0, height=2.2, corner_radius=0.15, color=color, fill_opacity=0.12, stroke_width=1.5).move_to(pos+DOWN*0.8)
            tt = Text(title, font_size=15, color=color, weight=BOLD).move_to(c.get_center()+UP*0.5)
            ct = Text(content, font_size=13, color=C_LIGHT).move_to(c.get_center()+DOWN*0.3)
            self.play(FadeIn(c), FadeIn(tt), FadeIn(ct), run_time=0.4)
        self.wait(1)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # 过渡
        transition("This is just the beginning", "这只是开始")

        # ═══ Scene 8: Hybrid Agent (水平流 + 底部回路) ══════════════
        t8 = Text("Autonomous Circuit Design", font_size=TITLE_SIZE, color=C_GREEN, weight=BOLD)
        t8cn = Text("AI 自主设计量子电路", font_size=SUBTITLE_SIZE, color=C_YELLOW)
        VGroup(t8, t8cn).arrange(DOWN, buff=0.1).to_edge(UP, buff=0.4)
        self.play(Write(t8), FadeIn(t8cn), run_time=0.5)

        # 水平四个步骤
        h_steps = [
            ("Target", C_ORANGE), ("RAG", C_BLUE),
            ("Generate", C_PURPLE), ("Verify", C_GREEN),
        ]
        h_boxes = VGroup()
        for name, color in h_steps:
            r = RoundedRectangle(width=2.0, height=0.9, corner_radius=0.1, color=color, fill_opacity=0.25, stroke_width=1.5)
            t = Text(name, font_size=16, color=color, weight=BOLD).move_to(r)
            h_boxes.add(VGroup(r, t))
        h_boxes.arrange(RIGHT, buff=0.5).move_to(UP*0.5)

        for i, hb in enumerate(h_boxes):
            self.play(FadeIn(hb), run_time=0.3)
            if i < len(h_boxes) - 1:
                a = Arrow(hb.get_right(), h_boxes[i+1].get_left(), buff=0.05, color=WHITE, stroke_width=1.5, max_tip_length_to_length_ratio=0.15)
                self.play(Create(a), run_time=0.15)

        # Fail 回路: Verify 底部 → 向下 → 向左 → Generate 底部
        fail_down = Line(h_boxes[3].get_bottom(), h_boxes[3].get_bottom() + DOWN*0.6, color=C_RED, stroke_width=1.5)
        fail_left = Line(h_boxes[3].get_bottom() + DOWN*0.6, h_boxes[2].get_bottom() + DOWN*0.6, color=C_RED, stroke_width=1.5)
        fail_up = Arrow(h_boxes[2].get_bottom() + DOWN*0.6, h_boxes[2].get_bottom(), buff=0.05, color=C_RED, stroke_width=1.5, max_tip_length_to_length_ratio=0.2)
        fail_label = Text("Fail", font_size=SMALL_SIZE, color=C_RED).next_to(fail_left, DOWN, buff=0.08)

        self.play(Create(fail_down), Create(fail_left), Create(fail_up), FadeIn(fail_label), run_time=0.6)

        # Pass 路径: Verify 底部 → Output
        pass_arrow = Arrow(h_boxes[3].get_bottom() + DOWN*0.05, h_boxes[3].get_bottom() + DOWN*1.5, buff=0, color=C_GREEN, stroke_width=2, max_tip_length_to_length_ratio=0.12)
        pass_label = Text("Pass", font_size=SMALL_SIZE, color=C_GREEN).next_to(pass_arrow, LEFT, buff=0.1)
        output_box = RoundedRectangle(width=3.5, height=0.7, corner_radius=0.1, color=C_GREEN, fill_opacity=0.3, stroke_width=1.5).next_to(pass_arrow, DOWN, buff=0.1)
        output_text = Text("New Verified Circuit", font_size=15, color=C_GREEN, weight=BOLD).move_to(output_box)

        self.play(Create(pass_arrow), FadeIn(pass_label), run_time=0.3)
        self.play(FadeIn(output_box), FadeIn(output_text), run_time=0.4)
        self.wait(2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.4)

        # ═══ Scene 9: 结尾 ══════════════════════════════════════════
        f1 = Text("QCV", font_size=80, color=C_BLUE, weight=BOLD)
        f2 = Text("When AI Reads Quantum", font_size=30, color=C_LIGHT)
        f3 = Text("Toward Autonomous Quantum Circuit Design", font_size=22, color=C_YELLOW)
        f4 = Text("132 Circuits  |  7 Modalities  |  Open Source", font_size=16, color=C_GREY)
        f5 = Text("github.com/QuantBlockchain/quantum-circuit-vision", font_size=14, color=C_BLUE)
        VGroup(f1, f2, f3, f4, f5).arrange(DOWN, buff=0.3)
        self.play(Write(f1), run_time=0.7)
        self.play(FadeIn(f2), run_time=0.4)
        self.play(FadeIn(f3), run_time=0.4)
        self.play(FadeIn(f4), FadeIn(f5), run_time=0.4)
        self.wait(2.5)

        # 过渡到作者页
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

        # ═══ Scene Final: Authors ═══════════════════════════════════
        presented = Text("A story presented by", font_size=24, color=C_GREY, font="Arial")
        presented.to_edge(UP, buff=1.2)
        self.play(FadeIn(presented), run_time=0.5)

        authors = VGroup()
        author_data = [
            ("Dongping Liu", "CEO, Tenorshare", C_BLUE),
            ("Aoyu Zhang", "Applied Scientist, AWS", C_GREEN),
            ("Luyao Zhang", "Professor, Duke Kunshan", C_PURPLE),
        ]
        for name, role, color in author_data:
            n = Text(name, font_size=26, color=color, weight=BOLD, font="Arial")
            r = Text(role, font_size=16, color=C_GREY, font="Arial")
            authors.add(VGroup(n, r).arrange(DOWN, buff=0.1))
        authors.arrange(RIGHT, buff=1.5).move_to(UP*0.2)

        for a in authors:
            self.play(FadeIn(a, shift=UP*0.2), run_time=0.5)

        # Sponsor line
        sponsor = Text("This research is sponsored by Lijian Research Lab, AFS Group",
                      font_size=16, color=C_GREY, font="Arial")
        sponsor.to_edge(DOWN, buff=0.8)
        self.play(FadeIn(sponsor), run_time=0.5)

        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.7)
