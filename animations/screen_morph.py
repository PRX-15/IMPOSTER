"""Reusable button-to-screen morph transition.

This module only handles the source button morph and ScreenManager handoff.
It intentionally contains no target-screen-specific entrance, curtain, fade,
or slide animation logic.
"""

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.screenmanager import NoTransition

from screens.common import COLORS, RoundedButton


MORPH_BORDER_COLOR = (0.35, 0.65, 1.0, 1)


class ScreenMorph:
    """Morph a source button into a fullscreen cover, then change screens."""

    def __init__(self, screen, duration=0.45, transition="out_cubic"):
        self.screen = screen
        self.duration = duration
        self.transition = transition
        self._running = False
        self.layer = FloatLayout(size_hint=(1, 1))
        screen.add_widget(self.layer)

    @property
    def running(self):
        return self._running

    def start(self, source_button, target_screen, on_handoff=None):
        """Run the morph and hand off to ``target_screen`` when it finishes.

        The fullscreen overlay stays mounted for one render tick after the
        ScreenManager switches screens. This prevents the old source screen
        from flashing for a frame during the handoff. Target-screen-specific
        entrance behaviour remains outside this generic animation module.
        """
        if self._running or not source_button or not source_button.parent:
            return False

        self._running = True
        start_x, start_y = self.layer.to_widget(*source_button.to_window(0, 0))
        radius = getattr(source_button, "radius", dp(28))

        overlay = RoundedButton(
            text="",
            size_hint=(None, None),
            size=source_button.size,
            pos=(start_x, start_y),
            bg_color=COLORS["bg"],
            border_color=MORPH_BORDER_COLOR,
            radius=radius,
            disabled=True,
        )
        self.layer.add_widget(overlay)
        source_button.opacity = 0
        source_button.disabled = True

        morph = Animation(
            pos=(0, 0),
            size=self.layer.size,
            radius=0,
            duration=self.duration,
            t=self.transition,
        )

        def finish(*_):
            manager = self.screen.manager
            previous_transition = manager.transition
            manager.transition = NoTransition()
            manager.current = target_screen.name
            manager.transition = previous_transition

            def cleanup(_dt):
                if overlay.parent is self.layer:
                    self.layer.remove_widget(overlay)
                source_button.opacity = 1
                source_button.disabled = False
                self._running = False
                if on_handoff:
                    on_handoff()

            Clock.schedule_once(cleanup, 0)

        morph.bind(on_complete=finish)
        morph.start(overlay)
        return True
