from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle, Ellipse, Line

from animations.screen_morph import ScreenMorph
from game.game_logic import MAX_PLAYERS
from .common import COLORS, NeonLabel, RoundedButton, asset_path


class PlayerListCard(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation="vertical", padding=[dp(12), dp(12)], **kwargs)
        with self.canvas.before:
            Color(*COLORS["card"]); self.bg = RoundedRectangle(radius=[dp(20)])
            Color(*COLORS["accent"]); self.border = Line(width=dp(1.2))
        self.bind(pos=self._draw, size=self._draw)
    def _draw(self, *_):
        self.bg.pos, self.bg.size = self.pos, self.size
        self.border.rounded_rectangle = [self.x, self.y, self.width, self.height, dp(20)]


class PlayerRow(BoxLayout):
    CONTROL_ANIMATION = 0.24
    def __init__(self, number, delete_callback=None, **kwargs):
        super().__init__(orientation="horizontal", spacing=dp(8), padding=[dp(18), dp(6)], size_hint_y=None, height=dp(58), **kwargs)
        self.delete_callback = delete_callback
        with self.canvas.before:
            Color(*COLORS["card2"]); self.bg = RoundedRectangle(radius=[dp(24)])
        self.bind(pos=self._draw, size=self._draw)
        self.add_widget(Image(source=asset_path("main-menu", "player-icon.png"), size_hint_x=None, width=dp(34)))
        self.input = TextInput(text="", hint_text="Enter a name", multiline=False, background_color=(0,0,0,0), foreground_color=COLORS["text"], hint_text_color=COLORS["muted"], cursor_color=COLORS["primary"], font_size="18sp", padding=[0,dp(14),0,0])
        self.add_widget(self.input)
        self.add_widget(Image(source=asset_path("main-menu", "pencil-icon.png"), size_hint_x=None, width=dp(26)))
        self.delete_btn = RoundedButton(text="−", font_size="22sp", size_hint_x=None, width=0, height=dp(28), radius=10, bg_color=COLORS.get("danger", (0.85,0.08,0.28,1)))
        self.delete_btn.bind(on_release=self._delete); self.add_widget(self.delete_btn)
        self.number = number; self._layout_controls(False, animate=False)
    def _draw(self, *_): self.bg.pos, self.bg.size = self.pos, self.size
    def _delete(self, *_):
        if self.delete_callback: self.delete_callback(self)
    def set_number(self, number): self.number = number
    @property
    def player_name(self): return self.input.text.strip() or f"Player {self.number}"
    def _layout_controls(self, can_delete, animate=True):
        w, o = (dp(42), 1) if can_delete else (0, 0); self.delete_btn.disabled = not can_delete
        if animate: Animation(width=w, opacity=o, duration=self.CONTROL_ANIMATION, t="out_quad").start(self.delete_btn)
        else: self.delete_btn.width, self.delete_btn.opacity = w, o
    def set_delete_state(self, can_delete, animate=True): self._layout_controls(can_delete, animate)


class TitleBadge(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(size_hint_y=None, height=dp(76), **kwargs)
        with self.canvas.before:
            Color(COLORS["accent"][0],COLORS["accent"][1],COLORS["accent"][2],.12); self.fill=RoundedRectangle(radius=[dp(26)])
            Color(COLORS["accent"][0],COLORS["accent"][1],COLORS["accent"][2],.92); self.border=Line(width=dp(1.7))
        self.title=NeonLabel(text="IMPOSTER",font_name="GameFont",font_size="40sp",bold=True,size_hint=(None,None));self.add_widget(self.title);self.bind(pos=self._draw,size=self._draw);self._draw()
    def _draw(self,*_):
        self.fill.pos,self.fill.size=self.pos,self.size;self.border.rounded_rectangle=[self.x,self.y,self.width,self.height,dp(26)];self.title.pos,self.title.size=self.pos,self.size;self.title.text_size=self.size


class NavTab(ButtonBehavior, FloatLayout):
    def __init__(self, icon, text, callback, **kwargs):
        super().__init__(**kwargs); self.callback=callback
        self.add_widget(Image(source=icon,size_hint=(None,None),size=(dp(25),dp(25)),pos_hint={"center_x":.5,"center_y":.63}))
        self.add_widget(NeonLabel(text=text,font_size="10sp",color=COLORS["muted"],size_hint=(1,None),height=dp(20),pos_hint={"x":0,"y":.04}))
    def on_release(self):
        if self.callback: self.callback()


class GlassNavBar(BoxLayout):
    indicator_x=NumericProperty(0)
    def __init__(self,on_home,on_history,active="home",**kwargs):
        super().__init__(orientation="horizontal",spacing=dp(5),padding=[dp(6),dp(6)],size_hint=(None,None),width=dp(190),height=dp(72),**kwargs)
        self.on_home=on_home;self.on_history=on_history
        with self.canvas.before:
            Color(1,1,1,.055);self.bg=RoundedRectangle(radius=[dp(30)])
            Color(1,1,1,.72);self.border=Line(width=dp(1.05))
            Color(COLORS["primary"][0],COLORS["primary"][1],COLORS["primary"][2],.34);self.indicator=RoundedRectangle(radius=[dp(25)])
        self.add_widget(NavTab(asset_path("main-menu","home-icon.png"),"HOME",self._home,size_hint_x=1))
        self.add_widget(NavTab(asset_path("main-menu","history-icon.png"),"HISTORY",self._history,size_hint_x=1))
        self.bind(pos=self._draw,size=self._draw);Clock.schedule_once(lambda *_: self.set_active(active,False),0)
    def _draw(self,*_):
        self.bg.pos,self.bg.size=self.pos,self.size;self.border.rounded_rectangle=[self.x,self.y,self.width,self.height,dp(30)];self.indicator.pos=(self.indicator_x,self.y+dp(6));self.indicator.size=(self.width/2-dp(8),self.height-dp(12))
    def set_active(self,active,animate=True):
        target=self.x+dp(6) if active=="home" else self.x+self.width/2+dp(1)
        if animate: Animation(indicator_x=target,duration=.22,t="out_cubic").start(self)
        else: self.indicator_x=target
        self._draw()
    def _home(self): self.set_active("home");self.on_home()
    def _history(self): self.set_active("history");self.on_history()


class MainMenuScreen(Screen):
    def __init__(self,state,**kwargs):
        super().__init__(**kwargs);self.state=state;self.rows=[];root=FloatLayout()
        with root.canvas.before:
            Color(*COLORS["bg"]);self.bg=RoundedRectangle(pos=root.pos,size=root.size);Color(.30,.04,.52,.38);self.orb1=Ellipse(size=(dp(180),dp(180)));Color(1,.06,.35,.18);self.orb2=Ellipse(size=(dp(120),dp(120)))
        root.bind(pos=self._draw_bg,size=self._draw_bg)
        stack=BoxLayout(orientation="vertical",spacing=dp(12),padding=[dp(26),dp(20),dp(26),dp(105)],size_hint=(1,1))
        stack.add_widget(TitleBadge());stack.add_widget(NeonLabel(text="ONE WORD. ONE FAKE. FIND THEM.",font_size="11sp",bold=True,color=COLORS["muted"],size_hint_y=None,height=dp(24)))
        self.player_card=PlayerListCard(size_hint_y=1);self.player_scroll=ScrollView(size_hint=(1,1),do_scroll_x=False,bar_width=dp(4),scroll_timeout=250);self.player_box=BoxLayout(orientation="vertical",spacing=dp(10),size_hint_y=None,height=dp(3*58+2*10),padding=[0,0,0,dp(2)]);self.player_box.bind(minimum_height=self.player_box.setter("height"));self.player_scroll.add_widget(self.player_box);self.player_card.add_widget(self.player_scroll);stack.add_widget(self.player_card)
        self.add_btn=RoundedButton(text="+ ADD PLAYER",size_hint_y=None,height=dp(52),bg_color=COLORS["card"]);self.add_btn.bind(on_release=self.add_player);stack.add_widget(self.add_btn)
        self.play_btn=RoundedButton(text="PLAY",size_hint_y=None,height=dp(60),bg_color=COLORS["primary"],border_color=(1,.38,.65,1));self.play_btn.bind(on_release=self.play);stack.add_widget(self.play_btn)
        stack.add_widget(NeonLabel(text="Pass the phone. Find the fake.",font_size="14sp",color=COLORS["muted"],size_hint_y=None,height=dp(28)));root.add_widget(stack)
        self.nav=GlassNavBar(self.go_home,self.go_history,active="home",pos_hint={"center_x":.5,"y":.025});root.add_widget(self.nav);self.add_widget(root);self.morph=ScreenMorph(self)
        for _ in range(3):self.add_player()
    def _draw_bg(self,root,*_):self.bg.pos,self.bg.size=root.pos,root.size;self.orb1.pos=(root.width-dp(115),root.height-dp(120));self.orb2.pos=(-dp(35),dp(70))
    def add_player(self,*_):
        if len(self.rows)>=MAX_PLAYERS:return
        was_three=len(self.rows)==3;row=PlayerRow(len(self.rows)+1,delete_callback=self.remove_player);self.rows.append(row);self.player_box.add_widget(row);self._refresh_player_controls(was_three);self._update_player_scroll()
    def remove_player(self,row):
        if len(self.rows)<=3:return
        if row in self.rows:self.rows.remove(row);self.player_box.remove_widget(row)
        for i,r in enumerate(self.rows,1):r.set_number(i)
        self._refresh_player_controls();self._update_player_scroll()
    def _update_player_scroll(self):self.player_scroll.do_scroll_y=len(self.rows)>5;self.player_scroll.scroll_y=1
    def _refresh_player_controls(self,animate=True):
        count=len(self.rows)
        if count>=MAX_PLAYERS:self.add_btn.opacity=1;self.add_btn.disabled=True;self.add_btn.bg_color=(.12,.12,.16,1);self.add_btn.border_color=(.38,.38,.44,1)
        else:self.add_btn.opacity=1;self.add_btn.disabled=False;self.add_btn.bg_color=COLORS["card"];self.add_btn.border_color=COLORS["accent"]
        for row in self.rows:row.set_delete_state(count>3,animate)
    def go_home(self):self.manager.show_home()
    def go_history(self):self.manager.show_history()
    def play(self,*_):
        if self.morph.running:return
        self.state.begin_new_game([row.player_name for row in self.rows]);self.state.start_round();reveal=self.manager.get_screen("reveal");reveal.build_turn();self.morph.start(self.play_btn,reveal,on_handoff=lambda:Clock.schedule_once(lambda _dt:reveal.start_entrance_animation(),0))
