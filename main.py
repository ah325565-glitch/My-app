from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
import os
from datetime import datetime

class TouchStackLayout(StackLayout):
    def __init__(self, app_ref, **kwargs):
        super().__init__(**kwargs)
        self.app_ref = app_ref

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not touch.is_mouse_scrolling:
                self.app_ref.move_cursor_to_touch(touch)
        return super().on_touch_down(touch)

class MyKeyboardApp(App):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical', padding=5, spacing=5)
        with self.main_layout.canvas.before:
            Color(1, 1, 1, 1)
            self.bg_rect = Rectangle(size=Window.size, pos=(0,0))
        self.main_layout.bind(size=self._update_bg, pos=self._update_bg)
       
        self.scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False, scroll_type=['bars', 'content'], bar_width=10)
        with self.scroll.canvas.before:
            Color(1, 1, 1, 1)
            self.rect = Rectangle(size=self.scroll.size, pos=self.scroll.pos)
        self.scroll.bind(size=self._update_rect, pos=self._update_rect)
       
        self.display_area = TouchStackLayout(app_ref=self, orientation='rl-tb', padding=10, spacing=5, size_hint_y=None)
        self.display_area.bind(minimum_height=self.display_area.setter('height'))
       
        with self.display_area.canvas.before:
            Color(1, 1, 1, 1)
            self.area_bg = Rectangle(size=self.display_area.size, pos=self.display_area.pos)
        self.display_area.bind(size=self._update_area_bg, pos=self._update_area_bg)
       
        self.cursor = Button(size_hint=(None, None), size=(2, 60), background_color=(0, 0, 0, 1), disabled=True)
        self.display_area.add_widget(self.cursor)
        Clock.schedule_interval(self.blink_cursor, 0.5)
       
        self.scroll.add_widget(self.display_area)
        self.main_layout.add_widget(self.scroll)
       
        control_container = BoxLayout(size_hint_y=None, height=62, padding=2)
        with control_container.canvas.before: 
            Color(0, 0, 0, 1)
            self.ctrl_bg = Rectangle(size=control_container.size, pos=control_container.pos)
        control_container.bind(size=self._update_ctrl_bg, pos=self._update_ctrl_bg)
       
        control_layout = GridLayout(cols=5, spacing=2)
        for t, c, f in [("SPACE", (0, 0.3, 0.7, 1), self.add_space), ("DASH (-)", (0.5, 0.2, 0, 1), self.add_dash),
                        ("ENTER", (0, 0.4, 0, 1), self.add_enter), ("SAVE", (0.7, 0.5, 0, 1), self.save_as_image),
                        ("CLEAR", (0.5, 0, 0, 1), self.clear_all)]:
            btn = Button(text=t, background_color=c)
            btn.bind(on_release=f)
            control_layout.add_widget(btn)
        control_container.add_widget(control_layout)
        self.main_layout.add_widget(control_container)
       
        keyboard_container = BoxLayout(size_hint=(1, None), height=450, padding=2)
        with keyboard_container.canvas.before: 
            Color(0, 0, 0, 1)
            self.kb_bg = Rectangle(size=keyboard_container.size, pos=keyboard_container.pos)
        keyboard_container.bind(size=self._update_kb_bg, pos=self._update_kb_bg)
       
        buttons_grid = GridLayout(cols=7, spacing=2, size_hint_y=None)
        buttons_grid.bind(minimum_height=buttons_grid.setter('height'))
       
        base_path = "/storage/emulated/0/Pictures/"
        for i in range(1, 38):
            img_path = os.path.join(base_path, f"{i}.png")
            btn = Button(background_normal=img_path if os.path.exists(img_path) else "", 
                         text="" if os.path.exists(img_path) else str(i), size_hint_y=None, height=80)
            btn.bind(on_release=lambda inst, p=img_path: self.add_symbol(p))
            buttons_grid.add_widget(btn)

        # تمت إضافة النقطة (.) هنا في القائمة
        text_items = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "(", ")", "/", ":", "[", "]", "#", "'", ";", "."]
        for item in text_items:
            btn = Button(text=item, font_size=35, size_hint_y=None, height=80, background_color=(0.1, 0.4, 0.4, 1))
            btn.bind(on_release=lambda inst, val=item: self.add_text_label(val))
            buttons_grid.add_widget(btn)
       
        buttons_scroll = ScrollView(do_scroll_x=False, scroll_type=['bars', 'content'], bar_width=5)
        buttons_scroll.add_widget(buttons_grid)
        keyboard_container.add_widget(buttons_scroll)
        self.main_layout.add_widget(keyboard_container)
       
        self.btn_del = Button(text="BACKSPACE", size_hint_y=None, height=80, background_color=(0.6, 0, 0, 1))
        self.btn_del.bind(on_press=self.start_delete_clock)
        self.btn_del.bind(on_release=self.stop_delete_clock)
        self.main_layout.add_widget(self.btn_del)
       
        return self.main_layout

    def add_text_label(self, text):
        lbl = Label(text=text, color=(0,0,0,1), size_hint=(None, None), size=(45, 60), font_size=50)
        idx = self.display_area.children.index(self.cursor)
        self.display_area.add_widget(lbl, index=idx + 1)

    def move_cursor_to_touch(self, touch):
        local_touch = self.display_area.to_local(*touch.pos)
        best_index = 0
        min_dist = float('inf')
        for i, child in enumerate(self.display_area.children):
            if child == self.cursor: continue
            dist = ((child.center_x - local_touch[0])**2 + (child.center_y - local_touch[1])**2)**0.5
            if dist < min_dist:
                min_dist = dist
                best_index = i
        self.display_area.remove_widget(self.cursor)
        self.display_area.add_widget(self.cursor, index=best_index)

    def add_symbol(self, path):
        img = Image(source=path, size_hint=(None, None), size=(60, 60))
        idx = self.display_area.children.index(self.cursor)
        self.display_area.add_widget(img, index=idx + 1)

    def add_dash(self, instance): self.add_text_label("-")
    def add_space(self, instance):
        idx = self.display_area.children.index(self.cursor)
        self.display_area.add_widget(Label(text="", size_hint=(None, None), size=(30, 60)), index=idx + 1)
    def add_enter(self, instance):
        idx = self.display_area.children.index(self.cursor)
        self.display_area.add_widget(BoxLayout(size_hint=(1, None), height=1), index=idx + 1)
    def delete_item(self, dt):
        idx = self.display_area.children.index(self.cursor)
        if idx + 1 < len(self.display_area.children): self.display_area.remove_widget(self.display_area.children[idx + 1])
    def save_as_image(self, instance):
        try:
            self.cursor.opacity = 0
            file_path = f"/storage/emulated/0/Pictures/Page_{datetime.now().strftime('%H%M%S')}.png"
            self.display_area.export_to_png(file_path)
            instance.text = "SAVED!"
            Clock.schedule_once(lambda dt: setattr(instance, 'text', 'SAVE'), 2)
        except: instance.text = "ERROR"
        self.cursor.opacity = 1

    def blink_cursor(self, dt):
        if self.cursor.opacity == 1: self.cursor.background_color[3] = 0 if self.cursor.background_color[3] == 1 else 1
    def start_delete_clock(self, instance): self.delete_item(None); self.delete_event = Clock.schedule_interval(self.delete_item, 0.15)
    def stop_delete_clock(self, instance):
        if hasattr(self, 'delete_event'): Clock.unschedule(self.delete_event)
    def clear_all(self, instance): self.display_area.clear_widgets(); self.display_area.add_widget(self.cursor)
    
    def _update_bg(self, i, v): self.bg_rect.pos = i.pos; self.bg_rect.size = i.size
    def _update_rect(self, i, v): self.rect.pos = i.pos; self.rect.size = i.size
    def _update_area_bg(self, i, v): self.area_bg.pos = i.pos; self.area_bg.size = i.size
    def _update_ctrl_bg(self, i, v): self.ctrl_bg.pos = i.pos; self.ctrl_bg.size = i.size
    def _update_kb_bg(self, i, v): self.kb_bg.pos = i.pos; self.kb_bg.size = i.size

if __name__ == '__main__':
    MyKeyboardApp().run()
