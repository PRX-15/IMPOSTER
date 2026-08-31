"""Shared Kivy widgets and styling helpers."""
from pathlib import Path
from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.graphics import Color, RoundedRectangle, Line

ROOT_DIR = Path(__file__).resolve().parents[1]
ASSET_DIR = ROOT_DIR / "assets"

# Android ROMs can ship different Noto Devanagari filenames.
# IMPORTANT: this font must NOT be assigned globally, because it may not
# contain Latin glyphs. English UI keeps Kivy's normal font; Hindi-only text
# explicitly opts into this font.
_DEVANAGARI_CANDIDATES = (
    Path("/system/fonts/NotoSansDevanagari-Regular.ttf"),
    Path("/system/fonts/NotoSansDevanagari-VF.ttf"),
    Path("/system/fonts/NotoSansDevanagari-Regular.otf"),
    Path("/system/fonts/NotoSansDevanagari-VF.otf"),
)
DEVANAGARI_FONT = next((str(p) for p in _DEVANAGARI_CANDIDATES if p.exists()), "")


def hindi_markup(text: str) -> str:
    """Render a Hindi string with the Android Devanagari font in Kivy markup."""
    if not DEVANAGARI_FONT:
        return text
    return f"[font={DEVANAGARI_FONT}]{text}[/font]"


COLORS = {
    "bg": (0.035, 0.015, 0.075, 1),
    "card": (0.13, 0.06, 0.22, 0.92),
    "card2": (0.20, 0.08, 0.32, 0.95),
    "accent": (0.68, 0.25, 1, 1),
    "primary": (1.0, 0.12, 0.38, 1),
    "text": (0.96, 0.92, 1, 1),
    "muted": (0.72, 0.62, 0.85, 1),
}


def asset_path(*parts: str) -> str:
    return str(ASSET_DIR.joinpath(*parts))


class NeonLabel(Label):
    def __init__(self, **kwargs):
        kwargs.setdefault("color", COLORS["text"])
        kwargs.setdefault("halign", "center")
        kwargs.setdefault("valign", "middle")
        super().__init__(**kwargs)
        self.bind(size=lambda *_: setattr(self, "text_size", self.size))


class RoundedButton(Button):
    # These must be Kivy properties. The morph animation changes radius and
    # colours every frame, and plain Python attributes would not redraw the
    # canvas while Animation is running.
    bg_color = ListProperty(COLORS["card2"])
    border_color = ListProperty(COLORS["accent"])
    radius = NumericProperty(dp(22))

    def __init__(self, bg_color=None, border_color=None, radius=22, **kwargs):
        kwargs.setdefault("background_normal", "")
        kwargs.setdefault("background_down", "")
        kwargs.setdefault("background_color", (0, 0, 0, 0))
        kwargs.setdefault("color", COLORS["text"])
        kwargs.setdefault("bold", True)
        kwargs.setdefault("font_size", "18sp")
        super().__init__(**kwargs)

        self.bg_color = bg_color or COLORS["card2"]
        self.border_color = border_color or COLORS["accent"]
        self.radius = dp(radius)
        self.bind(
            pos=self._draw,
            size=self._draw,
            state=self._draw,
            bg_color=self._draw,
            border_color=self._draw,
            radius=self._draw,
        )
        self._draw()

    def _draw(self, *_):
        self.canvas.before.clear()
        color = self.bg_color if self.state == "normal" else COLORS["accent"]
        with self.canvas.before:
            Color(*color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[self.radius])
            Color(*self.border_color)
            Line(
                rounded_rectangle=[self.x, self.y, self.width, self.height, self.radius],
                width=dp(1.2),
            )
