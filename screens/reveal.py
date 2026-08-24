from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stencilview import StencilView
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle, Line
from .common import COLORS, NeonLabel, RoundedButton, hindi_markup


class RevealScreen(Screen):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.secret_visible = False
        self.hide_event = None
        self.curtain_animation = None
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

    def _update_secret_text_bounds(self, *_):
        if not hasattr(self, "secret_label"):
            return
        self.secret_label.text_size = (
            max(dp(1), self.card_area.width - dp(40)),
            max(dp(1), self.card_area.height - dp(36)),
        )

    def _draw_card(self, *_):
        if not hasattr(self, "card_shell"):
            return
        self.card_shell_bg.pos = self.card_shell.pos
        self.card_shell_bg.size = self.card_shell.size
        self.card_shell_border.rounded_rectangle = [
            self.card_shell.x,
            self.card_shell.y,
            self.card_shell.width,
            self.card_shell.height,
            dp(28),
        ]

    def _stop_curtain_animation(self):
        if self.curtain_animation:
            self.curtain_animation.cancel(self.curtain)
            self.curtain_animation = None

    def _slide_curtain_up(self):
        self._stop_curtain_animation()
        self.curtain_animation = Animation(
            y=self.card_area.height,
            duration=0.32,
            t="out_cubic",
        )
        self.curtain_animation.bind(on_complete=self._clear_curtain_animation)
        self.curtain_animation.start(self.curtain)

    def _slide_curtain_down(self):
        self._stop_curtain_animation()
        self.curtain_animation = Animation(
            y=dp(1.5),
            duration=0.32,
            t="out_cubic",
        )
        self.curtain_animation.bind(on_complete=self._clear_curtain_animation)
        self.curtain_animation.start(self.curtain)

    def _clear_curtain_animation(self, *_):
        self.curtain_animation = None

    def build_turn(self):
        self._stop_curtain_animation()
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

        # This is the one fixed card area. Everything involved in the reveal
        # stays inside it; only the cover/curtain moves.
        self.card_area = StencilView(size_hint_y=.52)
        self.root.add_widget(self.card_area)

        self.card_shell = Widget(size_hint=(1, 1))
        with self.card_shell.canvas.before:
            Color(*COLORS["card"])
            self.card_shell_bg = RoundedRectangle(
                pos=self.card_shell.pos,
                size=self.card_shell.size,
                radius=[dp(28)],
            )
            Color(*COLORS["accent"])
            self.card_shell_border = Line(
                rounded_rectangle=[
                    self.card_shell.x,
                    self.card_shell.y,
                    self.card_shell.width,
                    self.card_shell.height,
                    dp(28),
                ],
                width=dp(1.2),
            )
        self.card_shell.bind(pos=self._draw_card, size=self._draw_card)
        self.card_area.add_widget(self.card_shell)

        self.secret_label = NeonLabel(
            text="",
            markup=True,
            size_hint=(1, 1),
            font_size="20sp",
            color=COLORS["text"],
        )
        self.card_area.add_widget(self.secret_label)

        # The actual reveal button is the curtain. It is clipped to the fixed
        # card area, so sliding it up never changes the position of the card,
        # next button, footer, or any surrounding layout.
        self.curtain = RoundedButton(
            text="TAP HERE TO\nREVEAL YOUR ROLE",
            font_size="23sp",
            size_hint=(None, None),
            size=(dp(1), dp(1)),
            pos=(dp(1.5), dp(1.5)),
            bg_color=COLORS["card"],
            border_color=(0, 0, 0, 0),
            radius=26.5,
            padding=[dp(20), dp(18)],
        )
        self.curtain.bind(on_release=self.reveal)
        self.card_area.add_widget(self.curtain)

        def sync_card_geometry(*_):
            inset = dp(1.5)
            self.curtain.pos = (inset, inset)
            self.curtain.size = (
                max(dp(1), self.card_area.width - inset * 2),
                max(dp(1), self.card_area.height - inset * 2),
            )
            self._draw_card()
            self._update_secret_text_bounds()

        self.card_area.bind(size=sync_card_geometry)
        Clock.schedule_once(sync_card_geometry, 0)

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
        self.secret_label.markup = True

        category_size = self._adaptive_size(
            info["category"], normal=30, compact=26, minimum=20, compact_at=14, minimum_at=30
        )
        category_hi_size = self._adaptive_size(
            info["category_hi"], normal=20, compact=18, minimum=15, compact_at=12, minimum_at=26
        )

        if info["is_imposter"]:
            self.secret_label.text = (
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
            self.secret_label.text = (
                "[size=15sp]WORD[/size]\n"
                f"[size={word_size}sp][b]{info['word']}[/b][/size]\n"
                f"[size={word_hi_size}sp]{hindi_markup(info['word_hi'])}[/size]\n\n"
                "[size=15sp]CATEGORY[/size]\n"
                f"[size={category_size}sp][b]{info['category']}[/b][/size]\n"
                f"[size={category_hi_size}sp]{hindi_markup(info['category_hi'])}[/size]"
            )

        self._slide_curtain_up()

        self.next_btn.text = (
            "FINISH REVEAL"
            if self.state.current_reveal_index == len(self.state.players) - 1
            else f"PASS THE PHONE TO {self.state.players[self.state.current_reveal_index + 1].upper()}"
        )
        self.next_btn.opacity = 1
        self.next_btn.disabled = False
        self.hide_event = Clock.schedule_once(lambda dt: self.hide_secret(), 5)

    def hide_secret(self):
        if not self.secret_visible:
            return
        self.secret_visible = False
        self._stop_curtain_animation()
        self.secret_label.markup = True
        self.secret_label.text = "[size=22sp][b]SECRET HIDDEN[/b][/size]"
        self._slide_curtain_down()
        self.next_btn.opacity = 1
        self.next_btn.disabled = False

    def next_player(self, *_):
        if self.hide_event:
            self.hide_event.cancel()
            self.hide_event = None
        self._stop_curtain_animation()
        self.secret_label.text = ""
        self.next_btn.disabled = True
        if self.state.current_reveal_index >= len(self.state.players) - 1:
            self.manager.current = "ready_vote"
        else:
            self.state.current_reveal_index += 1
            self.build_turn()
