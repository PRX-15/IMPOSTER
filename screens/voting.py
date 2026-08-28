from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from .common import COLORS, NeonLabel, RoundedButton


class VotingScreen(Screen):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.selected = None
        self.root = BoxLayout(
            orientation="vertical",
            padding=[dp(18), dp(20)],
            spacing=dp(8),
        )
        self.add_widget(self.root)

    def on_pre_enter(self):
        self.build_vote()

    def _make_vote_button(self, idx, name, height=None):
        button = RoundedButton(
            text=name.upper(),
            size_hint_y=None if height is not None else 1,
            height=dp(height) if height is not None else 100,
            bg_color=COLORS["card"],
            font_size="14sp",
        )
        button.bind(on_release=lambda _button, player_idx=idx: self.select(player_idx))
        self.vote_buttons[idx] = button
        return button

    def _pulse_selected(self, button):
        Animation.cancel_all(button, "opacity")
        pulse = Animation(opacity=.72, duration=.08, t="out_quad") + Animation(
            opacity=1, duration=.14, t="out_quad"
        )
        pulse.start(button)

    def build_vote(self):
        self.selected = None
        self.root.clear_widgets()
        i = self.state.current_vote_index
        player_count = len(self.state.players)

        self.root.add_widget(
            NeonLabel(
                text=f"{self.state.players[i].upper()} — VOTE",
                font_size="24sp",
                bold=True,
                size_hint_y=None,
                height=dp(44),
            )
        )
        self.root.add_widget(
            NeonLabel(
                text="Who do you think is the Imposter?",
                font_size="15sp",
                color=COLORS["muted"],
                size_hint_y=None,
                height=dp(30),
            )
        )

        self.vote_buttons = {}
        thin_vote_buttons = player_count <= 5
        vote_button_height = 46 if thin_vote_buttons else None
        players_area = BoxLayout(
            orientation="vertical",
            spacing=dp(8),
            size_hint_y=None if thin_vote_buttons else 1,
            height=dp(player_count * vote_button_height + max(player_count - 1, 0) * 8)
            if thin_vote_buttons else 100,
        )

        if player_count <= 5:
            for idx, name in enumerate(self.state.players):
                players_area.add_widget(
                    self._make_vote_button(idx, name, height=vote_button_height)
                )
        else:
            paired_count = player_count if player_count % 2 == 0 else player_count - 1
            rows = paired_count // 2
            columns = BoxLayout(
                orientation="horizontal",
                spacing=dp(10),
                size_hint_y=rows / (rows + 1) if player_count % 2 else 1,
            )
            left_column = BoxLayout(orientation="vertical", spacing=dp(8))
            right_column = BoxLayout(orientation="vertical", spacing=dp(8))
            columns.add_widget(left_column)
            columns.add_widget(right_column)

            for idx in range(rows):
                left_column.add_widget(
                    self._make_vote_button(idx, self.state.players[idx])
                )

            for idx in range(rows):
                player_idx = rows + idx
                right_column.add_widget(
                    self._make_vote_button(player_idx, self.state.players[player_idx])
                )

            players_area.add_widget(columns)

            if player_count % 2:
                final_row = BoxLayout(
                    orientation="horizontal",
                    spacing=0,
                    size_hint_y=1 / (rows + 1),
                )
                final_row.add_widget(Widget(size_hint_x=.25))
                final_row.add_widget(
                    self._make_vote_button(player_count - 1, self.state.players[-1])
                )
                final_row.add_widget(Widget(size_hint_x=.25))
                players_area.add_widget(final_row)

        self.root.add_widget(players_area)

        self.confirm = RoundedButton(
            text="CONFIRM VOTE",
            size_hint_y=None,
            height=dp(50),
            bg_color=COLORS["primary"],
            disabled=True,
            opacity=.45,
        )
        self.confirm.bind(on_release=self.confirm_vote)
        self.root.add_widget(self.confirm)

        self.notice = NeonLabel(
            text="Your vote stays private between turns.",
            font_size="12sp",
            color=COLORS["muted"],
            size_hint_y=None,
            height=dp(28),
        )
        self.root.add_widget(self.notice)

    def select(self, idx):
        self.selected = idx
        for button in self.vote_buttons.values():
            button.bg_color = COLORS["card"]
            button.opacity = 1
            button._draw()

        selected_button = self.vote_buttons[idx]
        selected_button.bg_color = COLORS["primary"]
        selected_button._draw()
        self._pulse_selected(selected_button)

        self.confirm.disabled = False
        self.confirm.opacity = 0.45
        Animation(opacity=1, duration=0.18, t="out_cubic").start(self.confirm)
        self.notice.text = f"Selected: {self.state.players[idx]}"

    def confirm_vote(self, *_):
        if self.selected is None:
            return
        self.state.cast_vote(self.state.current_vote_index, self.selected)
        self.selected = None
        self.root.clear_widgets()

        final = self.state.current_vote_index == len(self.state.players) - 1
        self.root.add_widget(
            NeonLabel(text="VOTE LOCKED", font_size="26sp", bold=True)
        )
        text = (
            "SHOW VOTE SUMMARY"
            if final
            else f"PASS THE PHONE TO {self.state.players[self.state.current_vote_index + 1].upper()}"
        )
        button = RoundedButton(
            text=text,
            size_hint_y=None,
            height=dp(54),
            bg_color=COLORS["primary"],
            font_size="15sp",
            opacity=0,
        )
        button.bind(on_release=self.next)
        self.root.add_widget(button)
        Animation(opacity=1, duration=0.24, t="out_cubic").start(button)

    def next(self, *_):
        if self.state.current_vote_index >= len(self.state.players) - 1:
            self.manager.current = "vote_summary"
        else:
            self.state.current_vote_index += 1
            self.build_vote()
