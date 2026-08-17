"""IMPOSTER Kivy app entry point."""
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from game.game_logic import GameState
from screens.main_menu import MainMenuScreen
from screens.reveal import RevealScreen
from screens.ready_vote import ReadyVoteScreen
from screens.voting import VotingScreen
from screens.vote_summary import VoteSummaryScreen
from screens.results import ResultsScreen
from screens.common import COLORS


class ImposterApp(App):
    title = "IMPOSTER"

    def build(self):
        Window.clearcolor = COLORS["bg"]
        self.state = GameState()
        manager = ScreenManager(transition=FadeTransition(duration=0.18))
        for screen in (
            MainMenuScreen(self.state, name="menu"),
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
