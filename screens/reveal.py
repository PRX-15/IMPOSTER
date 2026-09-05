from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, RoundedRectangle, Line, StencilPush, StencilUse, StencilUnUse, StencilPop, PushMatrix, PopMatrix, Translate
from .common import COLORS, NeonLabel, RoundedButton, hindi_markup


class EntranceLabel(NeonLabel):
    entrance_offset = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            PushMatrix(); self._entrance_translate = Translate(0, 0, 0)
        with self.canvas.after: PopMatrix()
        self.bind(entrance_offset=self._sync_entrance_offset)
    def _sync_entrance_offset(self, *_): self._entrance_translate.y = self.entrance_offset


class RoundedStencilView(Widget):
    def __init__(self, radius=24, **kwargs):
        self.clip_radius = dp(radius); super().__init__(**kwargs)
        with self.canvas.before:
            StencilPush(); self._stencil_mask = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.clip_radius]); StencilUse()
        with self.canvas.after:
            StencilUnUse(); self._stencil_clear = RoundedRectangle(pos=self.pos, size=self.size, radius=[self.clip_radius]); StencilPop()
        self.bind(pos=self._sync_stencil, size=self._sync_stencil)
    def _sync_stencil(self, *_):
        self._stencil_mask.pos=self.pos; self._stencil_mask.size=self.size; self._stencil_mask.radius=[self.clip_radius]
        self._stencil_clear.pos=self.pos; self._stencil_clear.size=self.size; self._stencil_clear.radius=[self.clip_radius]


class PlainCurtain(Button):
    def __init__(self, **kwargs):
        kwargs.setdefault("background_normal", ""); kwargs.setdefault("background_down", ""); kwargs.setdefault("background_color", (0,0,0,0)); kwargs.setdefault("color", COLORS["text"]); kwargs.setdefault("bold", True); kwargs.setdefault("halign", "center"); kwargs.setdefault("valign", "middle")
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*COLORS["card"]); self._background=Rectangle(pos=self.pos,size=self.size)
        self.bind(pos=self._sync_background,size=self._sync_background,size=self._sync_text)
        self._sync_text()
    def _sync_background(self,*_): self._background.pos=self.pos; self._background.size=self.size
    def _sync_text(self,*_): self.text_size=self.size


class RevealScreen(Screen):
    def __init__(self,state,**kwargs):
        super().__init__(**kwargs); self.state=state; self.secret_visible=False; self.hide_event=None; self.curtain_animation=None; self.entrance_widgets=[]
        self.root=BoxLayout(orientation="vertical",padding=[dp(24),dp(30)],spacing=dp(12)); self.add_widget(self.root)
    def on_pre_enter(self): self.build_turn()
    @staticmethod
    def _adaptive_size(text,normal,compact,minimum,compact_at=12,minimum_at=22):
        longest_line=max((len(line) for line in str(text).splitlines()),default=0)
        if longest_line<=compact_at:return normal
        if longest_line>=minimum_at:return minimum
        progress=(longest_line-compact_at)/(minimum_at-compact_at); return int(normal-(normal-compact)*progress)
    def _prepare_entrance_widget(self,widget): widget.opacity=0; widget.entrance_offset=dp(28); self.entrance_widgets.append(widget); return widget
    def start_entrance_animation(self):
        for widget in self.entrance_widgets:
            Animation.cancel_all(widget,"opacity","entrance_offset"); Animation(opacity=1,entrance_offset=0,duration=.38,t="out_cubic").start(widget)
        if hasattr(self,"card_area"): Animation.cancel_all(self.card_area,"opacity"); Animation(opacity=1,duration=.48,t="out_cubic").start(self.card_area)
    def _update_secret_text_bounds(self,*_):
        if not hasattr(self,"secret_label"):return
        self.secret_label.text_size=(max(dp(1),self.card_area.width-dp(40)),max(dp(1),self.card_area.height-dp(36)))
    def _draw_card_border(self,*_): self.card_border.rounded_rectangle=[self.card_area.x,self.card_area.y,self.card_area.width,self.card_area.height,dp(24)]
    def _stop_curtain_animation(self):
        if self.curtain_animation:self.curtain_animation.cancel(self.curtain);self.curtain_animation=None
    def _slide_curtain_up(self):
        self._stop_curtain_animation();self.curtain_animation=Animation(y=self.card_area.top,duration=.34,t="out_cubic");self.curtain_animation.bind(on_complete=self._clear_curtain_animation);self.curtain_animation.start(self.curtain)
    def _slide_curtain_down(self):
        self._stop_curtain_animation();self.curtain_animation=Animation(y=self.card_area.y,duration=.30,t="out_cubic");self.curtain_animation.bind(on_complete=self._clear_curtain_animation);self.curtain_animation.start(self.curtain)
    def _clear_curtain_animation(self,*_): self.curtain_animation=None
    def build_turn(self):
        self._stop_curtain_animation();self.secret_visible=False
        if self.hide_event:self.hide_event.cancel();self.hide_event=None
        self.root.clear_widgets();self.entrance_widgets=[];i=self.state.current_reveal_index
        self.player_label=self._prepare_entrance_widget(EntranceLabel(text=self.state.players[i].upper(),font_size="30sp",bold=True,size_hint_y=.14));self.root.add_widget(self.player_label)
        self.turn_label=self._prepare_entrance_widget(EntranceLabel(text="It's your turn.",font_size="18sp",color=COLORS["muted"],size_hint_y=.07));self.root.add_widget(self.turn_label)
        self.card_area=RoundedStencilView(radius=24,size_hint_y=.52,opacity=0);self.root.add_widget(self.card_area)
        self.card_background=Widget(size_hint=(None,None))
        with self.card_background.canvas.before:
            Color(*COLORS["card"]);self.card_background_rect=Rectangle(pos=self.card_background.pos,size=self.card_background.size)
        self.card_background.bind(pos=self._sync_card_background,size=self._sync_card_background);self.card_area.add_widget(self.card_background)
        self.secret_label=NeonLabel(text="",markup=True,size_hint=(None,None),font_size="20sp",color=COLORS["text"]);self.card_area.add_widget(self.secret_label)
        self.curtain=PlainCurtain(text="TAP HERE TO\nREVEAL YOUR ROLE",font_size="23sp",size_hint=(None,None));self.curtain.bind(on_release=self.reveal);self.card_area.add_widget(self.curtain)
        self.card_border_overlay=Widget(size_hint=(None,None))
        with self.card_border_overlay.canvas: Color(*COLORS["accent"]);self.card_border=Line(width=dp(1.2))
        self.card_border_overlay.bind(pos=self._draw_card_border,size=self._draw_card_border);self.card_area.add_widget(self.card_border_overlay)
        self.card_area.bind(pos=self._sync_card_geometry,size=self._sync_card_geometry);Clock.schedule_once(self._sync_card_geometry,0)
        self.next_btn=RoundedButton(text="",size_hint_y=None,height=dp(60),bg_color=COLORS["primary"],disabled=True,opacity=0);self.next_btn.bind(on_release=self.next_player);self.root.add_widget(self.next_btn)
        self.privacy_label=self._prepare_entrance_widget(EntranceLabel(text="Keep the screen private, then pass the phone.",font_size="14sp",color=COLORS["muted"],size_hint_y=.15));self.root.add_widget(self.privacy_label)
    def _sync_card_background(self,*_): self.card_background_rect.pos=self.card_background.pos;self.card_background_rect.size=self.card_background.size
    def _sync_card_geometry(self,*_):
        x,y=self.card_area.pos;width,height=self.card_area.size;self.card_background.pos=(x,y);self.card_background.size=(width,height);self.secret_label.pos=(x,y);self.secret_label.size=(width,height);self.curtain.pos=(x,y if not self.secret_visible else self.curtain.y);self.curtain.size=(width,height);self.card_border_overlay.pos=(x,y);self.card_border_overlay.size=(width,height);self._draw_card_border();self._update_secret_text_bounds()
    def reveal(self,*_):
        if self.secret_visible:return
        info=self.state.get_secret_for_player(self.state.current_reveal_index);self.secret_visible=True;self.secret_label.markup=True
        category_size=self._adaptive_size(info["category"],30,26,20,14,30);category_hi_size=self._adaptive_size(info["category_hi"],20,18,15,12,26)
        if info["is_imposter"]:
            self.secret_label.text="[size=22sp][b]YOU ARE THE IMPOSTER[/b][/size]\n\n[size=15sp]YOUR CATEGORY[/size]\n"+f"[size={category_size}sp][b]{info['category']}[/b][/size]\n"+f"[size={category_hi_size}sp]{hindi_markup(info['category_hi'])}[/size]"
        else:
            word_size=self._adaptive_size(info["word"],34,29,20,12,28);word_hi_size=self._adaptive_size(info["word_hi"],21,18,15,12,26)
            self.secret_label.text="[size=15sp]WORD[/size]\n"+f"[size={word_size}sp][b]{info['word']}[/b][/size]\n"+f"[size={word_hi_size}sp]{hindi_markup(info['word_hi'])}[/size]\n\n[size=15sp]CATEGORY[/size]\n"+f"[size={category_size}sp][b]{info['category']}[/b][/size]\n"+f"[size={category_hi_size}sp]{hindi_markup(info['category_hi'])}[/size]"
        self._slide_curtain_up();self.next_btn.text="FINISH REVEAL" if self.state.current_reveal_index==len(self.state.players)-1 else f"PASS THE PHONE TO {self.state.players[self.state.current_reveal_index+1].upper()}";self.next_btn.opacity=0;self.next_btn.disabled=False;Animation(opacity=1,duration=.28,t="out_cubic").start(self.next_btn);self.hide_event=Clock.schedule_once(lambda dt:self.hide_secret(),5)
    def hide_secret(self):
        if not self.secret_visible:return
        self.secret_visible=False;self._stop_curtain_animation();self.secret_label.text="";self.curtain.text="SECRET HIDDEN";self._slide_curtain_down();self.next_btn.opacity=1;self.next_btn.disabled=False
    def next_player(self,*_):
        if self.hide_event:self.hide_event.cancel();self.hide_event=None
        self._stop_curtain_animation();self.secret_label.text="";self.next_btn.disabled=True
        if self.state.current_reveal_index>=len(self.state.players)-1:self.manager.current="ready_vote"
        else:self.state.current_reveal_index+=1;self.build_turn();self.start_entrance_animation()
