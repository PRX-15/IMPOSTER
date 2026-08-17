from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from .common import COLORS, NeonLabel, RoundedButton
class ReadyVoteScreen(Screen):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs); self.state=state
        box=BoxLayout(orientation="vertical", padding=[dp(26), dp(44)], spacing=dp(18)); self.add_widget(box)
        box.add_widget(NeonLabel(text="DISCUSS IRL", font_size="32sp", bold=True, size_hint_y=.18))
        msg="The secret words have been revealed.\n\nPut the phone down and discuss your clues IRL. Talk it out, make accusations, defend yourself, and decide who the Imposter is.\n\nWhen everyone is ready, pick up the phone and continue."
        box.add_widget(NeonLabel(text=msg, font_size="18sp", color=COLORS["muted"]))
        btn=RoundedButton(text="READY TO VOTE?", size_hint_y=None, height=dp(64), bg_color=COLORS["primary"]); btn.bind(on_release=self.go); box.add_widget(btn)
    def go(self,*_): self.state.current_vote_index=0; self.manager.current="voting"
