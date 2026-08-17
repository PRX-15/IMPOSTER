from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from .common import COLORS, NeonLabel, RoundedButton
class VoteSummaryScreen(Screen):
    def __init__(self,state,**kwargs): super().__init__(**kwargs); self.state=state; self.root=BoxLayout(orientation="vertical", padding=[dp(24),dp(34)], spacing=dp(10)); self.add_widget(self.root)
    def on_pre_enter(self):
        self.root.clear_widgets(); totals=self.state.vote_totals()
        self.root.add_widget(NeonLabel(text="VOTE SUMMARY", font_size="30sp", bold=True, size_hint_y=.14))
        self.root.add_widget(NeonLabel(text="PLAYER                         VOTES RECEIVED", font_size="14sp", color=COLORS["muted"], size_hint_y=.08))
        for i,name in enumerate(self.state.players): self.root.add_widget(NeonLabel(text=f"{name:<20}  {totals[i]}", font_size="20sp", size_hint_y=.1))
        tie = "Tie detected — the final reveal will explain the outcome." if self.state.is_tie() else f"Top vote: {self.state.players[self.state.leaders()[0]]}"
        self.root.add_widget(NeonLabel(text=tie, font_size="16sp", color=COLORS["muted"], size_hint_y=.16))
        b=RoundedButton(text="REVEAL", size_hint_y=None, height=dp(64), bg_color=COLORS["primary"]); b.bind(on_release=lambda *_: setattr(self.manager,'current','results')); self.root.add_widget(b)
