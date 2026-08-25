from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget

from animations.screen_morph import ScreenMorph
from .common import COLORS, NeonLabel, RoundedButton, hindi_markup


class ResultsScreen(Screen):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.root = BoxLayout(orientation="vertical", padding=[dp(22), dp(28)], spacing=dp(8))
        self.add_widget(self.root)
        self.morph = ScreenMorph(self)

    def on_pre_enter(self):
        self.build()

    def _result_label(self, name, votes):
        return NeonLabel(text=f"{name}: {votes}", font_size="16sp", color=COLORS["muted"], size_hint_y=1)

    def _build_vote_results(self, players, totals):
        player_count = len(players)
        results_area = BoxLayout(orientation="vertical", spacing=dp(2), size_hint_y=.2)
        results_area.add_widget(NeonLabel(text="COMPLETE VOTE RESULTS", font_size="16sp", color=COLORS["muted"], size_hint_y=None, height=dp(24)))
        player_results = BoxLayout(orientation="vertical", spacing=dp(2), size_hint_y=1)
        if player_count <= 5:
            for idx, name in enumerate(players):
                player_results.add_widget(self._result_label(name, totals[idx]))
        else:
            paired_count = player_count if player_count % 2 == 0 else player_count - 1
            rows = paired_count // 2
            has_centered_player = player_count % 2 == 1
            columns = BoxLayout(orientation="horizontal", spacing=dp(10), size_hint_y=rows / (rows + 1) if has_centered_player else 1)
            left_column = BoxLayout(orientation="vertical", spacing=dp(2))
            right_column = BoxLayout(orientation="vertical", spacing=dp(2))
            columns.add_widget(left_column)
            columns.add_widget(right_column)
            for idx in range(rows):
                left_column.add_widget(self._result_label(players[idx], totals[idx]))
            for idx in range(rows):
                player_idx = rows + idx
                right_column.add_widget(self._result_label(players[player_idx], totals[player_idx]))
            player_results.add_widget(columns)
            if has_centered_player:
                final_row = BoxLayout(orientation="horizontal", size_hint_y=1 / (rows + 1))
                final_row.add_widget(Widget(size_hint_x=.25))
                final_row.add_widget(self._result_label(players[-1], totals[player_count - 1]))
                final_row.add_widget(Widget(size_hint_x=.25))
                player_results.add_widget(final_row)
        results_area.add_widget(player_results)
        return results_area

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
        self.root.add_widget(NeonLabel(markup=True, text=("THE SECRET WORD WAS\n" f"{s.selected_word.word}\n" f"{hindi_markup(s.selected_word.word_hi)}\n\n" "CATEGORY\n" f"{s.selected_word.category}\n" f"{hindi_markup(s.selected_word.category_hi)}"), font_size="20sp", size_hint_y=.25))
        self.root.add_widget(self._build_vote_results(s.players, totals))
        self.again_btn = RoundedButton(text="PLAY AGAIN", size_hint_y=None, height=dp(58), bg_color=COLORS["primary"])
        self.again_btn.bind(on_release=self.again)
        self.root.add_widget(self.again_btn)
        menu = RoundedButton(text="MAIN MENU", size_hint_y=None, height=dp(52), bg_color=COLORS["card"])
        menu.bind(on_release=self.menu)
        self.root.add_widget(menu)

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
