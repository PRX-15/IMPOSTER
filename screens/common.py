"""Shared Kivy widgets and styling helpers."""
from pathlib import Path
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import NumericProperty, ListProperty, BooleanProperty
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.text import LabelBase
from kivy.graphics import Color, RoundedRectangle, Line

ROOT_DIR=Path(__file__).resolve().parents[1]
ASSET_DIR=ROOT_DIR/"assets"
GAME_FONT=str(ASSET_DIR/"fonts"/"Matcha Mint.otf")
if Path(GAME_FONT).exists(): LabelBase.register(name="GameFont",fn_regular=GAME_FONT)
_DEVANAGARI_CANDIDATES=(Path("/system/fonts/NotoSansDevanagari-Regular.ttf"),Path("/system/fonts/NotoSansDevanagari-VF.ttf"),Path("/system/fonts/NotoSansDevanagari-Regular.otf"),Path("/system/fonts/NotoSansDevanagari-VF.otf"))
DEVANAGARI_FONT=next((str(p) for p in _DEVANAGARI_CANDIDATES if p.exists()),"")

def hindi_markup(text: str)->str:
    if not DEVANAGARI_FONT:return text
    return f"[font={DEVANAGARI_FONT}]{text}[/font]"

COLORS={"bg":(0.035,0.015,0.075,1),"card":(0.13,0.06,0.22,0.92),"card2":(0.20,0.08,0.32,0.95),"accent":(0.68,0.25,1,1),"primary":(1.0,0.12,0.38,1),"text":(0.96,0.92,1,1),"muted":(0.72,0.62,0.85,1)}

def asset_path(*parts:str)->str:return str(ASSET_DIR.joinpath(*parts))

class NeonLabel(Label):
    def __init__(self,**kwargs):
        kwargs.setdefault("color",COLORS["text"]);kwargs.setdefault("halign","center");kwargs.setdefault("valign","middle");super().__init__(**kwargs);self.bind(size=lambda *_:setattr(self,"text_size",self.size))

class RoundedButton(Button):
    """Rounded Kivy button with press-in, hold, release and matching border glow."""
    bg_color=ListProperty(COLORS["card2"]);border_color=ListProperty(COLORS["accent"]);radius=NumericProperty(dp(22));glow_opacity=NumericProperty(0.0);press_scale=NumericProperty(1.0);press_feedback=BooleanProperty(True)
    PRESS_IN_SCALE=.965;PRESS_DURATION=.09;RELEASE_DURATION=.14;GLOW_MAX=.82
    def __init__(self,bg_color=None,border_color=None,radius=22,press_feedback=True,**kwargs):
        kwargs.setdefault("background_normal","");kwargs.setdefault("background_down","");kwargs.setdefault("background_color",(0,0,0,0));kwargs.setdefault("color",COLORS["text"]);kwargs.setdefault("bold",True);kwargs.setdefault("font_size","18sp");super().__init__(**kwargs)
        self.bg_color=bg_color or COLORS["card2"];self.border_color=border_color or COLORS["accent"];self.radius=dp(radius);self.press_feedback=press_feedback
        self.bind(pos=self._draw,size=self._draw,state=self._draw,bg_color=self._draw,border_color=self._draw,radius=self._draw,glow_opacity=self._draw,press_scale=self._draw)
        self._base_pos=None;self._base_size=None;self._draw()
    def _draw(self,*_):
        if self._base_pos is None or self.state=="normal":self._base_pos=tuple(self.pos);self._base_size=tuple(self.size)
        base_x,base_y=self._base_pos;base_w,base_h=self._base_size;scale=self.press_scale;draw_w=base_w*scale;draw_h=base_h*scale;draw_x=base_x+(base_w-draw_w)/2;draw_y=base_y+(base_h-draw_h)/2
        self.canvas.before.clear()
        with self.canvas.before:
            if self.glow_opacity>0:
                r,g,b,a=self.border_color
                for spread,alpha_mul,width in ((dp(8),.10,dp(3.8)),(dp(5),.18,dp(3.0)),(dp(2),.32,dp(2.2))):
                    Color(r,g,b,a*self.glow_opacity*alpha_mul);Line(rounded_rectangle=[draw_x-spread/2,draw_y-spread/2,draw_w+spread,draw_h+spread,self.radius+spread/2],width=width)
            Color(*self.bg_color);RoundedRectangle(pos=(draw_x,draw_y),size=(draw_w,draw_h),radius=[self.radius]);Color(*self.border_color);Line(rounded_rectangle=[draw_x,draw_y,draw_w,draw_h,self.radius],width=dp(1.2)+dp(1.2)*self.glow_opacity)
    def on_touch_down(self,touch):
        if self.press_feedback and not self.disabled and self.collide_point(*touch.pos):
            Animation.cancel_all(self,"press_scale","glow_opacity");Animation(press_scale=self.PRESS_IN_SCALE,glow_opacity=self.GLOW_MAX,duration=self.PRESS_DURATION,t="out_quad").start(self)
        return super().on_touch_down(touch)
    def on_touch_up(self,touch):
        handled=super().on_touch_up(touch)
        if self.press_feedback and not self.disabled:
            Animation.cancel_all(self,"press_scale","glow_opacity");Animation(press_scale=1.0,glow_opacity=0.0,duration=self.RELEASE_DURATION,t="out_quad").start(self)
        return handled
