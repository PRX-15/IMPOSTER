from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from .common import COLORS, NeonLabel, RoundedButton, hindi_markup


class RevealScreen(Screen):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.secret_visible = False
        self.hide_event = None
        self.card_animation = None
        self.card_original_y = 0
        self.root = BoxLayout(
            orientation="vertical",
            padding=[dp(24), dp(30)],
            spacing=dp(12),
        )
        self.add_widget(self.root)

    def on_pre_enter(self):
        self.build_turn()

    @staticmethod
    def _adaptive_size(text, normal, compact, minimum, compact_at=12, minimum_at=22):
        """Shrink unusually long reveal words without changing normal entries."""
        longest_line = max((len(line) for line in str(text).splitlines()), default=0)
        if longest_line <= compact_at:
            return normal
        if longest_line >= minimum_at:
            return minimum
        progress = (longest_line - compact_at) / (minimum_at - compact_at)
        return int(normal - (normal - compact) * progress)

    def _update_card_text_bounds(self, *_):
        """Keep reveal text inside the card instead of letting long words overflow."""
        if not hasattr(self, "card"):
            return
        self.card.text_size = (
            max(dp(1), self.card.width - dp(40)),
            max(dp(1), self.card.height - dp(36)),
        )

    def _stop_card_animation(self):
        if self.card_animation:
            self.card_animation.cancel(self.card)
            self.card_animation = None

    def _slide_card_up(self):
        self._stop_card_animation()
        self.card_original_y = self.card.y
        self.card_animation = Animation(
            y=self.card_original_y + dp(90),
            duration=0.32,
            t="out_cubic",
        )
        self.card_animation.bind(on_complete=self._clear_card_animation)
        self.card_animation.start(self.card)

    def _slide_card_down(self):
        self._stop_card_animation()
        self.card_animation = Animation(
            y=self.card_original_y,
            duration=0.32,
            t="out_cubic",
        )
        self.card_animation.bind(on_complete=self._clear_card_animation)
        self.card_animation.start(self.card)

    def _clear_card_animation(self, *_):
        self.card_animation = None

    def build_turn(self):
        self.secret_visible = False
        if self.hide_event:
            self.hide_event.cancel()
            self.hide_event = None
        self.root.clear_widgets()

        i = self.state.current_reveal_index
        self.root.add_widget(
            NeonLabel(
                text=self.state.players[i].upper(),
                font_size="30sp",
                bold=True,
                size_hint_y=.14,
            )
        )
        self.root.add_widget(
            NeonLabel(
                text="It's your turn.",
                font_size="18sp",
                color=COLORS["muted"],
                size_hint_y=.07,
            )
        )

        self.card_area = FloatLayout(size_hint_y=.52)
        self.root.add_widget(self.card_area)

        self.card = RoundedButton(
            text="TAP HERE TO\nREVEAL YOUR ROLE",
            font_size="23sp",
            size_hint=(1, 1),
            pos=(0, 0),
            bg_color=COLORS["card"],
            padding=[dp(20), dp(18)],
        )
        self.card.bind(size=self._update_card_text_bounds)
        self._update_card_text_bounds()
        self.card.bind(on_release=self.reveal)
        self.card_area.add_widget(self.card)
        self.card_original_y = self.card.y

        self.next_btn = RoundedButton(
            text="",
            size_hint_y=None,
            height=dp(60),
            bg_color=COLORS["primary"],
            disabled=True,
            opacity=0,
        )
        self.next_btn.bind(on_release=self.next_player)
        self.root.add_widget(self.next_btn)
        self.root.add_widget(
            NeonLabel(
                text="Keep the screen private, then pass the phone.",
                font_size="14sp",
                color=COLORS["muted"],
                size_hint_y=.15,
            )
        )

    def reveal(self, *_):
        if self.secret_visible:
            return

        info = self.state.get_secret_for_player(self.state.current_reveal_index)
        self.secret_visible = True
        self.card.markup = True
        self._slide_card_up()
        self._update_card_text_bounds()

        category_size = self._adaptive_size(
            info["category"], normal=30, compact=26, minimum=20, compact_at=14, minimum_at=30
        )
        category_hi_size = self._adaptive_size(
            info["category_hi"], normal=20, compact=18, minimum=15, compact_at=12, minimum_at=26
        )

        if info["is_imposter"]:
            self.card.text = (
                "[size=22sp][b]YOU ARE THE IMPOSTER[/b][/size]\n\n"
                "[size=15sp]YOUR CATEGORY[/size]\n"
                f"[size={category_size}sp][b]{info['category']}[/b][/size]\n"
                f"[size={category_hi_size}sp]{hindi_markup(info['category_hi'])}[/size]"
            )
        else:
            word_size = self._adaptive_size(
                info["word"], normal=34, compact=29, minimum=20, compact_at=12, minimum_at=28
            )
            word_hi_size = self._adaptive_size(
                info["word_hi"], normal=21, compact=18, minimum=15, compact_at=12, minimum_at=26
            )
            self.card.text = (
                "[size=15sp]WORD[/size]\n"
                f"[size={word_size}sp][b]{info['word']}[/b][/size]\n"
                f"[size={word_hi_size}sp]{hindi_markup(info['word_hi'])}[/size]\n\n"
                "[size=15sp]CATEGORY[/size]\n"
                f"[size={category_size}sp][b]{info['category']}[/b][/size]\n"
                f"[size={category_hi_size}sp]{hindi_markup(info['category_hi'])}[/size]"
            )

        # Do not animate pos_hint inside a BoxLayout. Changing it can make the
        # reveal card appear to jump or leave text visually offset on some devices.
        self.next_btn.text = (
            "FINISH REVEAL"
            if self.state.current_reveal_index == len(self.state.players) - 1
            else f"PASS THE PHONE TO {self.state.players[self.state.current_reveal_index + 1].upper()}"
        )
        self.next_btn.opacity = 1
        self.next_btn.disabled = False
        self.hide_event = Clock.schedule_once(lambda dt: self.hide_secret(), 5)

    def hide_secret(self):
        self.card.markup = False
        self.card.text = "SECRET HIDDEN"
        self.secret_visible = False
        self._slide_card_down()
        self._update_card_text_bounds()
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
