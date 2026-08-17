from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from .common import COLORS, NeonLabel, RoundedButton


class VotingScreen(Screen):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.selected = None
        self.root = BoxLayout(orientation="vertical", padding=[dp(24), dp(34)], spacing=dp(12))
        self.add_widget(self.root)

    def on_pre_enter(self):
        self.build_vote()

    def build_vote(self):
        self.selected = None
        self.root.clear_widgets()
        i = self.state.current_vote_index
        self.root.add_widget(NeonLabel(text=f"{self.state.players[i].upper()} — VOTE", font_size="28sp", bold=True, size_hint_y=.15))
        self.root.add_widget(NeonLabel(text="Who do you think is the Imposter?", font_size="18sp", color=COLORS["muted"], size_hint_y=.1))

        self.vote_buttons = []
        for idx, name in enumerate(self.state.players):
            # Self-voting is intentionally allowed.
            b = RoundedButton(text=name.upper(), size_hint_y=None, height=dp(56), bg_color=COLORS["card"])
            b.bind(on_release=lambda btn, n=idx: self.select(n))
            self.vote_buttons.append(b)
            self.root.add_widget(b)

        self.confirm = RoundedButton(text="CONFIRM VOTE", size_hint_y=None, height=dp(62), bg_color=COLORS["primary"], disabled=True, opacity=.45)
        self.confirm.bind(on_release=self.confirm_vote)
        self.root.add_widget(self.confirm)

        self.notice = NeonLabel(text="Your vote stays private between turns.", font_size="14sp", color=COLORS["muted"], size_hint_y=.18)
        self.root.add_widget(self.notice)

    def select(self, idx):
        self.selected = idx
        for button in self.vote_buttons:
            button.bg_color = COLORS["card"]
            button._draw()

        selected_button = self.vote_buttons[idx]
        selected_button.bg_color = COLORS["primary"]
        selected_button._draw()

        self.confirm.disabled = False
        self.confirm.opacity = 1
        self.notice.text = f"Selected: {self.state.players[idx]}"

    def confirm_vote(self, *_):
        self.state.cast_vote(self.state.current_vote_index, self.selected)
        self.selected = None
        self.root.clear_widgets()
        final = self.state.current_vote_index == len(self.state.players) - 1
        self.root.add_widget(NeonLabel(text="VOTE LOCKED", font_size="30sp", bold=True))
        text = "SHOW VOTE SUMMARY" if final else f"PASS THE PHONE TO {self.state.players[self.state.current_vote_index + 1].upper()}"
        b = RoundedButton(text=text, size_hint_y=None, height=dp(64), bg_color=COLORS["primary"])
        b.bind(on_release=self.next)
        self.root.add_widget(b)

    def next(self, *_):
        if self.state.current_vote_index >= len(self.state.players) - 1:
            self.manager.current = "vote_summary"
        else:
            self.state.current_vote_index += 1
            self.build_vote()
