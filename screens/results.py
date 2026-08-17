from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from .common import COLORS, NeonLabel, RoundedButton, hindi_markup


class ResultsScreen(Screen):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.root = BoxLayout(orientation="vertical", padding=[dp(22), dp(28)], spacing=dp(8))
        self.add_widget(self.root)

    def on_pre_enter(self):
        self.build()

    def build(self):
        self.root.clear_widgets()
        s = self.state
        totals = s.vote_totals()
        leaders = s.leaders()
        imp = s.players[s.imposter_index]
        outcome = "IMPOSTER CAUGHT" if s.imposter_caught() else "IMPOSTER NOT CAUGHT"
        voted = "TIE: " + ", ".join(s.players[i] for i in leaders) if s.is_tie() else s.players[leaders[0]]

        self.root.add_widget(NeonLabel(text=outcome, font_size="30sp", bold=True, color=COLORS["primary"], size_hint_y=.12))
        self.root.add_widget(NeonLabel(text=f"THE IMPOSTER WAS\n{imp.upper()}", font_size="25sp", bold=True, size_hint_y=.18))
        self.root.add_widget(NeonLabel(text=f"MOST VOTES\n{voted}", font_size="19sp", color=COLORS["muted"], size_hint_y=.13))

        # Keep the normal Kivy font for English UI and apply the Android
        # Devanagari font only to the Hindi strings.
        self.root.add_widget(NeonLabel(
            markup=True,
            text=(
                "THE SECRET WORD WAS\n"
                f"{s.selected_word.word}\n"
                f"{hindi_markup(s.selected_word.word_hi)}\n\n"
                "CATEGORY\n"
                f"{s.selected_word.category}\n"
                f"{hindi_markup(s.selected_word.category_hi)}"
            ),
            font_size="20sp",
            size_hint_y=.25,
        ))
        lines = "\n".join(f"{name}: {totals[i]}" for i, name in enumerate(s.players))
        self.root.add_widget(NeonLabel(text="COMPLETE VOTE RESULTS\n" + lines, font_size="16sp", color=COLORS["muted"], size_hint_y=.2))
        again = RoundedButton(text="PLAY AGAIN", size_hint_y=None, height=dp(58), bg_color=COLORS["primary"])
        again.bind(on_release=self.again)
        self.root.add_widget(again)
        menu = RoundedButton(text="MAIN MENU", size_hint_y=None, height=dp(52), bg_color=COLORS["card"])
        menu.bind(on_release=self.menu)
        self.root.add_widget(menu)

    def again(self, *_):
        self.state.start_round(self.state.players)
        self.manager.current = "reveal"

    def menu(self, *_):
        self.state.reset_to_menu()
        self.manager.current = "menu"
