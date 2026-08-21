from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Ellipse

from game.game_logic import MAX_PLAYERS
from screens.transitions import ContainerTransformTransition
from .common import COLORS, NeonLabel, RoundedButton, asset_path


class PlayerRow(BoxLayout):
    def __init__(self, number, delete_callback=None, **kwargs):
        super().__init__(orientation="horizontal", spacing=dp(8), padding=[dp(18), dp(6)], size_hint_y=None, height=dp(58), **kwargs)
        self.delete_callback = delete_callback
        with self.canvas.before:
            Color(*COLORS["card"])
            self.bg = RoundedRectangle(radius=[dp(29)])
        self.bind(pos=self._draw, size=self._draw)
        self.add_widget(Image(source=asset_path("main-menu", "player-icon.png"), size_hint_x=None, width=dp(34)))
        self.input = TextInput(text="", hint_text="Enter a name", multiline=False, background_color=(0, 0, 0, 0), foreground_color=COLORS["text"], hint_text_color=COLORS["muted"], cursor_color=COLORS["primary"], font_size="18sp", padding=[0, dp(14), 0, 0])
        self.add_widget(self.input)
        self.add_widget(Image(source=asset_path("main-menu", "pencil-icon.png"), size_hint_x=None, width=dp(26)))
        self.delete_btn = RoundedButton(text="DELETE", font_size="11sp", size_hint_x=None, width=dp(64), height=dp(34), bg_color=COLORS.get("danger", (0.85, 0.08, 0.28, 1)))
        self.delete_btn.bind(on_release=self._delete)
        self.add_widget(self.delete_btn)
        self.number = number

    def _draw(self, *_):
        self.bg.pos = self.pos
        self.bg.size = self.size

    def _delete(self, *_):
        if self.delete_callback:
            self.delete_callback(self)

    def set_number(self, number):
        self.number = number

    @property
    def player_name(self):
        return self.input.text.strip() or f"Player {self.number}"


class MainMenuScreen(Screen):
    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.rows = []
        root = FloatLayout()
        with root.canvas.before:
            Color(*COLORS["bg"])
            self.bg = RoundedRectangle(pos=root.pos, size=root.size)
            Color(0.30, 0.04, 0.52, 0.38)
            self.orb1 = Ellipse(size=(dp(180), dp(180)))
            Color(1, 0.06, 0.35, 0.18)
            self.orb2 = Ellipse(size=(dp(120), dp(120)))
        root.bind(pos=self._draw_bg, size=self._draw_bg)

        stack = BoxLayout(orientation="vertical", spacing=dp(12), padding=[dp(26), dp(24)], size_hint=(1, 1))
        stack.add_widget(NeonLabel(text="IMPOSTER", font_size="42sp", bold=True, size_hint_y=None, height=dp(72)))

        self.player_scroll = ScrollView(size_hint_y=1, do_scroll_x=False, bar_width=dp(4))
        self.player_box = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None, padding=[0, 0, 0, dp(2)])
        self.player_box.bind(minimum_height=self.player_box.setter("height"))
        self.player_scroll.add_widget(self.player_box)
        stack.add_widget(self.player_scroll)

        self.add_btn = RoundedButton(text="+ ADD PLAYER", size_hint_y=None, height=dp(52), bg_color=COLORS["card"])
        self.add_btn.bind(on_release=self.add_player)
        stack.add_widget(self.add_btn)
        self.play_btn = RoundedButton(text="PLAY", size_hint_y=None, height=dp(60), bg_color=COLORS["primary"], border_color=(1, .38, .65, 1))
        self.play_btn.bind(on_release=self.play)
        stack.add_widget(self.play_btn)
        stack.add_widget(NeonLabel(text="Pass the phone. Find the fake.", font_size="14sp", color=COLORS["muted"], size_hint_y=None, height=dp(32)))
        root.add_widget(stack)
        self.add_widget(root)
        for _ in range(3):
            self.add_player()

    def _draw_bg(self, root, *_):
        self.bg.pos, self.bg.size = root.pos, root.size
        self.orb1.pos = (root.width - dp(115), root.height - dp(120))
        self.orb2.pos = (-dp(35), dp(70))

    def add_player(self, *_):
        if len(self.rows) >= MAX_PLAYERS:
            return
        row = PlayerRow(len(self.rows) + 1, delete_callback=self.remove_player)
        self.rows.append(row)
        self.player_box.add_widget(row)
        self._refresh_player_controls()
        self.player_scroll.scroll_y = 0

    def remove_player(self, row):
        if len(self.rows) <= 3:
            return
        if row in self.rows:
            self.rows.remove(row)
            self.player_box.remove_widget(row)
        for index, player_row in enumerate(self.rows, start=1):
            player_row.set_number(index)
        self._refresh_player_controls()

    def _refresh_player_controls(self):
        count = len(self.rows)
        at_max = count >= MAX_PLAYERS
        self.add_btn.opacity = 0 if at_max else 1
        self.add_btn.disabled = at_max
        can_delete = count > 3
        for row in self.rows:
            row.delete_btn.disabled = not can_delete
            row.delete_btn.opacity = 1 if can_delete else 0

    def play(self, *_):
        self.state.start_round([row.player_name for row in self.rows])
        reveal = self.manager.get_screen("reveal")
        self.manager.transition = ContainerTransformTransition(source_widget=self.play_btn, duration=0.35)
        self.manager.current = reveal.name
