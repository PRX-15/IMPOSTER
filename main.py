"""IMPOSTER Kivy app entry point."""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, NoTransition
from kivy.animation import Animation

from game.game_logic import GameState
from screens.main_menu import MainMenuScreen
from screens.game_history import GameHistoryScreen
from screens.reveal import RevealScreen
from screens.ready_vote import ReadyVoteScreen
from screens.voting import VotingScreen
from screens.vote_summary import VoteSummaryScreen
from screens.results import ResultsScreen
from screens.common import COLORS


class SwipeScreenManager(ScreenManager):
    """Screen manager with a finger-following horizontal menu/history swipe."""
    SWIPE_THRESHOLD = .20
    SWIPE_TRIGGER = 18

    def __init__(self, **kwargs):
        super().__init__(transition=NoTransition(), **kwargs)
        self._gesture_touch = None
        self._gesture_start = None
        self._dragging = False

    def _menu_history(self):
        return self.get_screen("menu"), self.get_screen("history")

    def on_touch_down(self, touch):
        if self.current in ("menu", "history"):
            self._gesture_touch = touch
            self._gesture_start = touch.pos
            self._dragging = False
        return super().on_touch_down(touch)

    def on_touch_move(self, touch):
        if touch is self._gesture_touch and self._gesture_start:
            dx = touch.x - self._gesture_start[0]
            dy = touch.y - self._gesture_start[1]
            if not self._dragging and abs(dx) > self.SWIPE_TRIGGER and abs(dx) > abs(dy) * 1.15:
                if (self.current == "menu" and dx < 0) or (self.current == "history" and dx > 0):
                    self._dragging = True
            if self._dragging:
                menu, history = self._menu_history()
                if self.current == "menu":
                    menu.x = dx
                    history.x = self.width + dx
                else:
                    history.x = dx
                    menu.x = -self.width + dx
                touch.ud["swipe_progress"] = max(0, min(1, abs(dx) / max(1, self.width)))
                return True
        return super().on_touch_move(touch)

    def on_touch_up(self, touch):
        if touch is self._gesture_touch:
            was_dragging = self._dragging
            dx = touch.x - self._gesture_start[0] if self._gesture_start else 0
            self._gesture_touch = None
            self._gesture_start = None
            self._dragging = False
            if was_dragging:
                if self.current == "menu":
                    target = "history" if abs(dx) >= self.width * self.SWIPE_THRESHOLD else "menu"
                else:
                    target = "menu" if abs(dx) >= self.width * self.SWIPE_THRESHOLD else "history"
                self._finish_drag(target, from_gesture=True)
                return True
        return super().on_touch_up(touch)

    def _finish_drag(self, target, from_gesture=False):
        menu, history = self._menu_history()
        current = menu if self.current == "menu" else history
        incoming = history if target == "history" else menu
        if not from_gesture:
            incoming.x = self.width if target == "history" else -self.width
        target_current_x = -self.width if target == "history" else self.width
        Animation.cancel_all(current, "x")
        Animation.cancel_all(incoming, "x")
        Animation(x=target_current_x, duration=.20, t="out_cubic").start(current)
        final = Animation(x=0, duration=.20, t="out_cubic")
        final.bind(on_complete=lambda *_: self._commit_menu_history(target))
        final.start(incoming)

    def _commit_menu_history(self, target):
        self.current = target
        menu, history = self._menu_history()
        menu.x = 0 if target == "menu" else -self.width
        history.x = 0 if target == "history" else self.width
        if target == "menu": menu.nav.set_active("home", animate=True)
        else: history.nav.set_active("history", animate=True)

    def show_home(self):
        if self.current == "menu":
            self.get_screen("menu").nav.set_active("home", animate=True)
        else:
            self._finish_drag("menu")

    def show_history(self):
        if self.current == "history":
            self.get_screen("history").nav.set_active("history", animate=True)
        else:
            self._finish_drag("history")


class ImposterApp(App):
    title = "IMPOSTER"

    def build(self):
        Window.clearcolor = COLORS["bg"]
        self.state = GameState()
        manager = SwipeScreenManager()
        for screen in (
            MainMenuScreen(self.state, name="menu"),
            GameHistoryScreen(name="history"),
            RevealScreen(self.state, name="reveal"),
            ReadyVoteScreen(self.state, name="ready_vote"),
            VotingScreen(self.state, name="voting"),
            VoteSummaryScreen(self.state, name="vote_summary"),
            ResultsScreen(self.state, name="results"),
        ):
            manager.add_widget(screen)
        return manager


if __name__ == "__main__":
    ImposterApp().run()
