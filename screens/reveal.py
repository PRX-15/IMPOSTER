from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from .common import COLORS, NeonLabel, RoundedButton


class RevealScreen(Screen):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.secret_visible = False
        self.hide_event = None
        self.root = BoxLayout(orientation="vertical", padding=[dp(24), dp(30)], spacing=dp(12))
        self.add_widget(self.root)

    def on_pre_enter(self):
        self.build_turn()

    def build_turn(self):
        self.secret_visible = False
        if self.hide_event:
            self.hide_event.cancel()
            self.hide_event = None
        self.root.clear_widgets()
        i = self.state.current_reveal_index
        self.root.add_widget(NeonLabel(text=self.state.players[i].upper(), font_size="30sp", bold=True, size_hint_y=.14))
        self.root.add_widget(NeonLabel(text="It's your turn.", font_size="18sp", color=COLORS["muted"], size_hint_y=.07))
        self.card = RoundedButton(text="TAP HERE TO\nREVEAL YOUR ROLE", font_size="23sp", size_hint_y=.52, bg_color=COLORS["card"])
        self.card.bind(on_release=self.reveal)
        self.root.add_widget(self.card)
        self.next_btn = RoundedButton(text="", size_hint_y=None, height=dp(60), bg_color=COLORS["primary"], disabled=True, opacity=0)
        self.next_btn.bind(on_release=self.next_player)
        self.root.add_widget(self.next_btn)
        self.root.add_widget(NeonLabel(text="Keep the screen private, then pass the phone.", font_size="14sp", color=COLORS["muted"], size_hint_y=.15))

    def reveal(self, *_):
        if self.secret_visible:
            return
        info = self.state.get_secret_for_player(self.state.current_reveal_index)
        self.secret_visible = True
        self.card.markup = True
        if info["is_imposter"]:
            # The imposter does not see the secret word. Category is enough.
            self.card.text = (
                "[size=22sp][b]YOU ARE THE IMPOSTER[/b][/size]\n\n"
                "[size=15sp]YOUR CATEGORY[/size]\n"
                f"[size=30sp][b]{info['category']}[/b][/size]\n"
                f"[size=20sp]{info['category_hi']}[/size]"
            )
        else:
            self.card.text = (
                "[size=15sp]WORD[/size]\n"
                f"[size=34sp][b]{info['word']}[/b][/size]\n"
                f"[size=21sp]{info['word_hi']}[/size]\n\n"
                "[size=15sp]CATEGORY[/size]\n"
                f"[size=30sp][b]{info['category']}[/b][/size]\n"
                f"[size=20sp]{info['category_hi']}[/size]"
            )
        Animation(pos_hint={"center_y": .58}, duration=.22, t="out_quad").start(self.card)
        final = self.state.current_reveal_index == len(self.state.players) - 1
        self.next_btn.text = "FINISH REVEAL" if final else f"PASS THE PHONE TO {self.state.players[self.state.current_reveal_index + 1].upper()}"
        self.next_btn.opacity = 1
        self.next_btn.disabled = False
        self.hide_event = Clock.schedule_once(lambda dt: self.hide_secret(), 5)

    def hide_secret(self):
        self.card.markup = False
        self.card.text = "SECRET HIDDEN"
        self.secret_visible = False
        Animation(pos_hint={"center_y": .5}, duration=.18, t="out_quad").start(self.card)
        self.next_btn.opacity = 1
        self.next_btn.disabled = False

    def next_player(self, *_):
        if self.hide_event:
            self.hide_event.cancel()
            self.hide_event = None
        self.card.text = ""
        self.next_btn.disabled = True
        if self.state.current_reveal_index >= len(self.state.players) - 1:
            self.manager.current = "ready_vote"
        else:
            self.state.current_reveal_index += 1
            self.build_turn()
