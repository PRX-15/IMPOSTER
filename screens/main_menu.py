from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line

from animations.screen_morph import ScreenMorph
from game.game_logic import MAX_PLAYERS
from .common import COLORS, NeonLabel, RoundedButton, asset_path

try:
    from jnius import autoclass
except ImportError:
    autoclass = None


class PlayerListCard(BoxLayout):
    """Rounded card containing the editable player list and its scroll area."""

    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=[dp(12), dp(12)], **kwargs)
        with self.canvas.before:
            Color(*COLORS["card"])
            self.bg = RoundedRectangle(radius=[dp(24)])
            Color(*COLORS["accent"])
            self.border = Line(width=dp(1.2))
        self.bind(pos=self._draw, size=self._draw)

    def _draw(self, *_):
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.border.rounded_rectangle = [self.x, self.y, self.width, self.height, dp(24)]


class PlayerRow(BoxLayout):
    def __init__(self, number, delete_callback=None, **kwargs):
        super().__init__(orientation="horizontal", spacing=dp(8), padding=[dp(18), dp(6)], size_hint_y=None, height=dp(58), **kwargs)
        self.delete_callback = delete_callback
        with self.canvas.before:
            Color(*COLORS["card2"])
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


class TitleBadge(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, height=dp(76), **kwargs)
        with self.canvas.before:
            Color(COLORS["accent"][0], COLORS["accent"][1], COLORS["accent"][2], 0.12)
            self.fill = RoundedRectangle(radius=[dp(26)])
            Color(COLORS["accent"][0], COLORS["accent"][1], COLORS["accent"][2], 0.92)
            self.border = Line(width=dp(1.7))
        self.title = NeonLabel(text="IMPOSTER", font_size="40sp", bold=True, size_hint=(None, None))
        self.add_widget(self.title)
        self.bind(pos=self._draw, size=self._draw)
        self._draw()

    def _draw(self, *_):
        self.fill.pos = self.pos
        self.fill.size = self.size
        self.border.rounded_rectangle = [self.x, self.y, self.width, self.height, dp(26)]
        self.title.size = self.size
        self.title.pos = self.pos
        self.title.text_size = self.size


class MainMenuScreen(Screen):
    MAX_PLAYER_MESSAGES = [
        "You can only add up to 10 players.",
        "Only 10 players can play bro.",
        "10 10 10",
        "Keep trying🤣",
        "Bro, the 11th player is NOT happening 😭",
    ]

    def __init__(self, state, **kwargs):
        super().__init__(**kwargs)
        self.state = state
        self.rows = []
        self.max_player_message_index = 0
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
        stack.add_widget(TitleBadge())
        stack.add_widget(NeonLabel(text="ONE WORD. ONE FAKE. FIND THEM.", font_size="11sp", bold=True, color=COLORS["muted"], size_hint_y=None, height=dp(24)))

        self.player_card = PlayerListCard(size_hint_y=1)
        self.player_scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, bar_width=dp(4))
        self.player_box = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None, padding=[0, 0, 0, dp(2)])
        self.player_box.bind(minimum_height=self.player_box.setter("height"))
        self.player_scroll.add_widget(self.player_box)
        self.player_card.add_widget(self.player_scroll)
        stack.add_widget(self.player_card)

        self.add_btn = RoundedButton(text="+ ADD PLAYER", size_hint_y=None, height=dp(52), bg_color=COLORS["card"])
        self.add_btn.bind(on_release=self.add_player)
        stack.add_widget(self.add_btn)
        self.play_btn = RoundedButton(text="PLAY", size_hint_y=None, height=dp(60), bg_color=COLORS["primary"], border_color=(1, .38, .65, 1))
        self.play_btn.bind(on_release=self.play)
        stack.add_widget(self.play_btn)
        stack.add_widget(NeonLabel(text="Pass the phone. Find the fake.", font_size="14sp", color=COLORS["muted"], size_hint_y=None, height=dp(32)))
        root.add_widget(stack)
        self.add_widget(root)
        self.morph = ScreenMorph(self)
        for _ in range(3):
            self.add_player()

    def _draw_bg(self, root, *_):
        self.bg.pos, self.bg.size = root.pos, root.size
        self.orb1.pos = (root.width - dp(115), root.height - dp(120))
        self.orb2.pos = (-dp(35), dp(70))

    def _show_max_players_message(self):
        message = self.MAX_PLAYER_MESSAGES[self.max_player_message_index]
        self.max_player_message_index = (self.max_player_message_index + 1) % len(self.MAX_PLAYER_MESSAGES)
        if autoclass is None:
            return
        try:
            Toast = autoclass("android.widget.Toast")
            PythonActivity = autoclass("org.kivy.android.PythonActivity")
            Toast.makeText(PythonActivity.mActivity, message, Toast.LENGTH_SHORT).show()
        except Exception:
            pass

    def add_player(self, *_):
        if len(self.rows) >= MAX_PLAYERS:
            self._show_max_players_message()
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
        if at_max:
            self.add_btn.opacity = 1
            self.add_btn.disabled = False
            self.add_btn.bg_color = COLORS["card2"]
            self.add_btn.border_color = COLORS["muted"]
        else:
            self.add_btn.opacity = 1
            self.add_btn.disabled = False
            self.add_btn.bg_color = COLORS["card"]
            self.add_btn.border_color = COLORS["accent"]
        can_delete = count > 3
        for row in self.rows:
            row.delete_btn.disabled = not can_delete
            row.delete_btn.opacity = 1 if can_delete else 0

    def play(self, *_):
        if self.morph.running:
            return
        self.state.start_round([row.player_name for row in self.rows])
        reveal = self.manager.get_screen("reveal")
        reveal.build_turn()
        self.morph.start(self.play_btn, reveal, on_handoff=lambda: Clock.schedule_once(lambda _dt: reveal.start_entrance_animation(), 0))
