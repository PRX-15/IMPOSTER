from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Line

from animations.screen_morph import ScreenMorph
from .common import COLORS, NeonLabel, RoundedButton, hindi_markup


class RoundedCard(BoxLayout):
    """Simple rounded container used to keep the results screen structured."""

    bg_color = ListProperty(COLORS["card"])
    border_color = ListProperty(COLORS["accent"])
    radius = dp(22)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = kwargs.get("padding", [dp(16), dp(12)])
        self.spacing = kwargs.get("spacing", dp(8))
        with self.canvas.before:
            Color(*self.bg_color)
            self.background = RoundedRectangle(radius=[self.radius])
            Color(*self.border_color)
            self.border = Line(width=dp(1.0))
        self.bind(pos=self._draw, size=self._draw)
        self._draw()

    def _draw(self, *_):
        self.background.pos = self.pos
        self.background.size = self.size
        self.border.rounded_rectangle = [self.x, self.y, self.width, self.height, self.radius]


class VoteRow(BoxLayout):
    def __init__(self, name, votes, maximum_votes, highlighted=False, **kwargs):
        super().__init__(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(34), **kwargs)
        self.name = NeonLabel(text=name, font_size="13sp", halign="left", color=COLORS["text"], size_hint_x=.30)
        self.bar_host = FloatLayout(size_hint_x=.54)
        self.votes_label = NeonLabel(text=str(votes), font_size="13sp", size_hint_x=.16)
        self.add_widget(self.name)
        self.add_widget(self.bar_host)
        self.add_widget(self.votes_label)

        with self.bar_host.canvas.before:
            Color(*(COLORS["card2"]))
            self.track = RoundedRectangle(radius=[dp(7)])
            Color(*(COLORS["primary"] if highlighted else COLORS["accent"]))
            self.fill = RoundedRectangle(radius=[dp(7)])
        self.bar_host.bind(pos=self._draw, size=self._draw)
        self.votes = votes
        self.maximum_votes = maximum_votes
        self.highlighted = highlighted
        self._draw()

    def _draw(self, *_):
        self.track.pos = (self.bar_host.x, self.bar_host.y + dp(9))
        self.track.size = (self.bar_host.width, dp(12))
        ratio = 0 if self.maximum_votes <= 0 else self.votes / self.maximum_votes
        self.fill.pos = self.track.pos
        self.fill.size = (self.bar_host.width * ratio, dp(12))


class ResultsScreen(Screen):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.root = FloatLayout()
        self.add_widget(self.root)
        self.morph = ScreenMorph(self)

    def on_pre_enter(self):
        self.build()

    def _build_round_info(self, word, word_hi, category, category_hi):
        card = RoundedCard(size_hint_y=None, height=dp(94), padding=[dp(10), dp(10)], spacing=0)

        left = BoxLayout(orientation="vertical", size_hint_x=.48, spacing=0)
        left.add_widget(NeonLabel(text=word, font_size="18sp", bold=True, size_hint_y=.56))
        left.add_widget(NeonLabel(markup=True, text=hindi_markup(word_hi), font_size="14sp", color=COLORS["muted"], size_hint_y=.44))

        divider_host = FloatLayout(size_hint_x=None, width=dp(1))
        with divider_host.canvas.before:
            Color(*COLORS["accent"])
            divider = Line(width=dp(1.0))
        def draw_divider(*_):
            divider.points = [divider_host.center_x, divider_host.y + dp(14), divider_host.center_x, divider_host.top - dp(14)]
        divider_host.bind(pos=draw_divider, size=draw_divider)
        draw_divider()

        right = BoxLayout(orientation="vertical", size_hint_x=.48, spacing=0)
        right.add_widget(NeonLabel(text=category, font_size="18sp", bold=True, size_hint_y=.56))
        right.add_widget(NeonLabel(markup=True, text=hindi_markup(category_hi), font_size="14sp", color=COLORS["muted"], size_hint_y=.44))

        card.add_widget(left)
        card.add_widget(divider_host)
        card.add_widget(right)
        return card

    def _build_vote_card(self, players, totals):
        card = RoundedCard(orientation="vertical", size_hint_y=None, padding=[dp(14), dp(12)], spacing=dp(5))
        card.add_widget(NeonLabel(text="VOTE RESULTS", font_size="15sp", bold=True, color=COLORS["muted"], size_hint_y=None, height=dp(22)))
        maximum_votes = max(totals.values()) if totals else 0
        leaders = [idx for idx, total in totals.items() if total == maximum_votes]
        for idx, name in enumerate(players):
            card.add_widget(VoteRow(name, totals[idx], maximum_votes, highlighted=idx in leaders))
        card.height = dp(38) + len(players) * dp(34) + (len(players) - 1) * dp(5) + dp(24)
        return card

    def _build_score_card(self, players, scores, points):
        card = RoundedCard(orientation="vertical", size_hint_y=None, padding=[dp(14), dp(12)], spacing=dp(4))

        header = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(23))
        header.add_widget(NeonLabel(text="PLAYER", font_size="13sp", color=COLORS["muted"], halign="left", size_hint_x=.52))
        header.add_widget(NeonLabel(text="ROUND", font_size="13sp", color=COLORS["muted"], size_hint_x=.24))
        header.add_widget(NeonLabel(text="TOTAL", font_size="13sp", color=COLORS["muted"], size_hint_x=.24))
        card.add_widget(header)

        for idx, name in enumerate(players):
            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=dp(30))
            row.add_widget(NeonLabel(text=name, font_size="13sp", halign="left", size_hint_x=.52))
            change = points[idx]
            sign = "+" if change > 0 else ""
            change_text = f"{sign}{change}"
            change_color = (0.35, 0.85, 0.40, 1) if change > 0 else ((1.0, 0.35, 0.40, 1) if change < 0 else COLORS["muted"])
            row.add_widget(NeonLabel(text=change_text, font_size="14sp", bold=True, color=change_color, size_hint_x=.24))
            row.add_widget(NeonLabel(text=str(scores[idx]), font_size="14sp", bold=True, size_hint_x=.24))
            card.add_widget(row)

        card.height = dp(35) + dp(30) * len(players) + dp(24)
        return card

    def build(self):
        self.root.clear_widgets()
        s = self.state
        totals = s.vote_totals()
        leaders = s.leaders()
        imp = s.players[s.imposter_index]
        caught = s.imposter_caught()
        points = s.calculate_round_points()
        outcome = "IMPOSTER CAUGHT" if caught else "IMPOSTER NOT CAUGHT"
        outcome_color = (0.35, 0.85, 0.40, 1) if caught else COLORS["primary"]
        voted = "Tie: " + ", ".join(s.players[i] for i in leaders) if s.is_tie() else s.players[leaders[0]]

        top = BoxLayout(orientation="vertical", size_hint=(1, None), height=dp(126), padding=[dp(20), 0], spacing=0, pos_hint={"top": 1})
        top.add_widget(NeonLabel(text=outcome, font_size="30sp", bold=True, color=outcome_color, size_hint_y=.52))
        top.add_widget(NeonLabel(text=imp, font_size="22sp", bold=True, size_hint_y=.28))
        top.add_widget(NeonLabel(text=f"Most votes: {voted}", font_size="14sp", color=COLORS["muted"], size_hint_y=.20))
        self.root.add_widget(top)

        scroll = ScrollView(size_hint=(1, None), size=(self.width, self.height - dp(206)), pos_hint={"x": 0, "y": 0.13}, do_scroll_x=False, bar_width=dp(3))
        content = BoxLayout(orientation="vertical", spacing=dp(10), padding=[dp(20), dp(8), dp(20), dp(8)], size_hint_y=None)
        content.bind(minimum_height=content.setter("height"))
        content.add_widget(self._build_round_info(s.selected_word.word, s.selected_word.word_hi, s.selected_word.category, s.selected_word.category_hi))
        content.add_widget(self._build_vote_card(s.players, totals))
        content.add_widget(self._build_score_card(s.players, s.scores, points))
        scroll.add_widget(content)
        self.root.add_widget(scroll)

        buttons = BoxLayout(orientation="vertical", spacing=dp(8), padding=[dp(20), dp(8)], size_hint=(1, None), height=dp(110), pos_hint={"x": 0, "y": 0})
        self.again_btn = RoundedButton(text="PLAY AGAIN", size_hint_y=None, height=dp(50), bg_color=COLORS["primary"])
        self.again_btn.bind(on_release=self.again)
        menu = RoundedButton(text="MAIN MENU", size_hint_y=None, height=dp(46), bg_color=COLORS["card"])
        menu.bind(on_release=self.menu)
        buttons.add_widget(self.again_btn)
        buttons.add_widget(menu)
        self.root.add_widget(buttons)

    def again(self, *_):
        if self.morph.running:
            return
        self.state.start_round(self.state.players)
        reveal = self.manager.get_screen("reveal")
        reveal.build_turn()
        self.morph.start(
            self.again_btn,
            reveal,
            on_handoff=lambda: Clock.schedule_once(lambda _dt: reveal.start_entrance_animation(), 0),
        )

    def menu(self, *_):
        self.state.reset_to_menu()
        self.manager.current = "menu"
