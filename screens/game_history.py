from datetime import datetime
import os

from kivy.app import App
from kivy.metrics import dp
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.graphics import Color, RoundedRectangle, Line

from game.history import HistoryDB
from .common import COLORS, NeonLabel, RoundedButton, hindi_markup
from .main_menu import GlassNavBar


class GlassCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.padding = kwargs.get("padding", [dp(16), dp(12)])
        self.spacing = kwargs.get("spacing", dp(7))
        with self.canvas.before:
            Color(COLORS["card"][0], COLORS["card"][1], COLORS["card"][2], .72); self.bg = RoundedRectangle(radius=[dp(20)])
            Color(COLORS["accent"][0], COLORS["accent"][1], COLORS["accent"][2], .55); self.border = Line(width=dp(1.0))
        self.bind(pos=self._draw, size=self._draw)
    def _draw(self, *_):
        self.bg.pos,self.bg.size=self.pos,self.size;self.border.rounded_rectangle=[self.x,self.y,self.width,self.height,dp(20)]


class GameHistoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs);self.db=None;self.detail_game_id=None;self.root=FloatLayout();self.add_widget(self.root)
    def _get_db(self):
        if self.db is None:self.db=HistoryDB(os.path.join(App.get_running_app().user_data_dir,"game_data.db"))
        return self.db
    def on_pre_enter(self):
        if self.detail_game_id is None:self.build_list()
    def on_enter(self):
        if self.detail_game_id is None:self.build_list()
    def _background(self):
        root=FloatLayout()
        with root.canvas.before:
            Color(*COLORS["bg"]);bg=RoundedRectangle(pos=root.pos,size=root.size);Color(.30,.04,.52,.38);orb=RoundedRectangle(radius=[dp(90)])
        def draw(*_):bg.pos,bg.size=root.pos,root.size;orb.pos=(root.width-dp(150),root.height-dp(130));orb.size=(dp(180),dp(180))
        root.bind(pos=draw,size=draw);draw();return root
    def _add_nav(self,root):
        self.nav=GlassNavBar(self.go_home,self.go_history,active="history",pos_hint={"center_x":.5,"y":.025});root.add_widget(self.nav)
    def build_list(self):
        self.detail_game_id=None;self.root.clear_widgets();bg=self._background();self.root.add_widget(bg)
        content_host=BoxLayout(orientation="vertical",padding=[dp(20),dp(24),dp(20),dp(105)],spacing=dp(10));content_host.add_widget(NeonLabel(text="GAME HISTORY",font_size="28sp",bold=True,size_hint_y=None,height=dp(52)))
        scroll=ScrollView(do_scroll_x=False,bar_width=dp(3));content=BoxLayout(orientation="vertical",spacing=dp(10),size_hint_y=None,padding=[0,0,0,dp(12)]);content.bind(minimum_height=content.setter("height"))
        games=self._get_db().list_games()
        if not games:content.add_widget(NeonLabel(text="NO GAMES PLAYED YET",font_size="17sp",color=COLORS["muted"],size_hint_y=None,height=dp(80)))
        else:
            for game in games:content.add_widget(self._game_card(game))
        scroll.add_widget(content);content_host.add_widget(scroll);self.root.add_widget(content_host);self._add_nav(self.root)
    def _game_card(self,game):
        card=GlassCard(orientation="vertical",size_hint_y=None,height=dp(112),padding=[dp(16),dp(11)]);names=", ".join(p["name"] for p in game["players"]);names=names if len(names)<=52 else names[:49]+"..."
        try:when=datetime.fromisoformat(game["played_at"]).astimezone().strftime("%d %b %Y • %I:%M %p")
        except ValueError:when=game["played_at"]
        card.add_widget(NeonLabel(text=names,font_size="16sp",bold=True,halign="left",size_hint_y=None,height=dp(28)))
        card.add_widget(NeonLabel(text=f"{game['rounds']} round{'s' if game['rounds']!=1 else ''}  •  {when}",font_size="12sp",color=COLORS["muted"],halign="left",size_hint_y=None,height=dp(22)))
        btn=RoundedButton(text="VIEW GAME",font_size="12sp",height=dp(38),size_hint_y=None,bg_color=COLORS["card2"],press_feedback=False);btn.bind(on_release=lambda *_:self.show_detail(game["id"]));card.add_widget(btn);return card
    def show_detail(self,game_id):
        self.detail_game_id=game_id;game=self._get_db().get_game(game_id)
        if not game:return self.build_list()
        self.root.clear_widgets();bg=self._background();self.root.add_widget(bg);outer=BoxLayout(orientation="vertical",padding=[dp(20),dp(18),dp(20),dp(105)],spacing=dp(9))
        back=RoundedButton(text="‹  HISTORY",size_hint_y=None,height=dp(42),font_size="13sp",bg_color=COLORS["card2"]);back.bind(on_release=lambda *_:self.build_list());outer.add_widget(back);outer.add_widget(NeonLabel(text="GAME DETAILS",font_size="25sp",bold=True,size_hint_y=None,height=dp(44)))
        scroll=ScrollView(do_scroll_x=False,bar_width=dp(3));content=BoxLayout(orientation="vertical",spacing=dp(10),size_hint_y=None,padding=[0,0,0,dp(12)]);content.bind(minimum_height=content.setter("height"))
        rounds_card=GlassCard(orientation="vertical",size_hint_y=None,padding=[dp(14),dp(12)],spacing=dp(6));rounds_card.add_widget(NeonLabel(text=f"ROUNDS  •  {game['rounds']}",font_size="14sp",bold=True,color=COLORS["muted"],halign="left",size_hint_y=None,height=dp(24)))
        for item in game["round_words"]:
            row=BoxLayout(orientation="vertical",size_hint_y=None,height=dp(54));row.add_widget(NeonLabel(text=f"Round {item['round_number']}  •  {item['word']}",font_size="16sp",bold=True,halign="left",size_hint_y=.55));row.add_widget(NeonLabel(markup=True,text=hindi_markup(item["word_hi"]),font_size="13sp",color=COLORS["muted"],halign="left",size_hint_y=.45));rounds_card.add_widget(row)
        rounds_card.height=dp(42)+max(1,len(game["round_words"]))*dp(54)+dp(20);content.add_widget(rounds_card)
        score_card=GlassCard(orientation="vertical",size_hint_y=None,padding=[dp(14),dp(12)],spacing=dp(5));score_card.add_widget(NeonLabel(text="SCORES",font_size="14sp",bold=True,color=COLORS["muted"],halign="left",size_hint_y=None,height=dp(24)))
        for player in game["players"]:
            row=BoxLayout(orientation="horizontal",size_hint_y=None,height=dp(34));row.add_widget(NeonLabel(text=player["name"],font_size="15sp",halign="left",size_hint_x=.72));row.add_widget(NeonLabel(text=str(player["score"]),font_size="16sp",bold=True,size_hint_x=.28));score_card.add_widget(row)
        score_card.height=dp(44)+len(game["players"])*dp(34)+dp(18);content.add_widget(score_card);scroll.add_widget(content);outer.add_widget(scroll);self.root.add_widget(outer);self._add_nav(self.root)
    def go_home(self):self.manager.show_home()
    def go_history(self):self.manager.show_history()
