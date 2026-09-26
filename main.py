from math import sqrt

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition

try:
    from plyer import accelerometer
    SENSOR_AVAILABLE = True
except Exception:
    SENSOR_AVAILABLE = False

Window.clearcolor = (0.05, 0.05, 0.07, 1)


class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        root = BoxLayout(orientation="vertical", padding=18, spacing=12)
        root.add_widget(Label(text="FITZONE", font_size="30sp", bold=True,
                              size_hint_y=None, height=70))
        root.add_widget(Label(
            text="🔥 Bugünkü hareket hedefin\\nHazırsan başlayalım!",
            font_size="20sp"
        ))
        self.status = Label(
            text="📱 Telefonu sallayınca Yürüyüş açılır.", font_size="17sp"
        )
        root.add_widget(self.status)
        start = Button(text="🏃 Egzersizlere Başla", size_hint_y=None,
                       height=65, font_size="19sp")
        start.bind(on_release=lambda *_: self.go("exercise"))
        root.add_widget(start)
        root.add_widget(Label(text=""))
        self.add_widget(root)

    def go(self, screen):
        self.manager.current = screen


class ExerciseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation="vertical", padding=20, spacing=15)
        box.add_widget(Label(text="🏋️ Egzersizler", font_size="28sp"))
        for name in ["Squat", "Plank", "Jumping Jack", "Esneme"]:
            button = Button(text=name, font_size="19sp", size_hint_y=None, height=60)
            button.bind(on_release=lambda btn: self.select(btn.text))
            box.add_widget(button)
        self.info = Label(text="Bir hareket seç.")
        box.add_widget(self.info)
        self.add_widget(box)

    def select(self, name):
        self.info.text = f"✅ {name} seçildi!"


class WalkScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation="vertical", padding=20, spacing=18)
        box.add_widget(Label(text="🚶 Yürüyüş", font_size="30sp"))
        self.state = Label(text="Yürüyüş henüz başlamadı.", font_size="21sp")
        box.add_widget(self.state)
        self.steps = 0
        self.step_label = Label(text="Adım: 0", font_size="24sp")
        box.add_widget(self.step_label)
        start = Button(text="Yürüyüşü Başlat", font_size="18sp",
                       size_hint_y=None, height=65)
        start.bind(on_release=self.start_walk)
        box.add_widget(start)
        self.add_widget(box)

    def start_walk(self, *_):
        self.state.text = "🟢 Yürüyüş aktif!"
        self.steps += 1
        self.step_label.text = f"Adım: {self.steps}"


class ProgressScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = BoxLayout(orientation="vertical", padding=20, spacing=15)
        box.add_widget(Label(text="📊 İlerleme", font_size="30sp"))
        box.add_widget(Label(
            text="Bugün\\n\\n🔥 Aktivite: 70%\\n🚶 Yürüyüş: 0 adım\\n💧 Su: 0 bardak",
            font_size="21sp"
        ))
        self.add_widget(box)


class BottomNav(BoxLayout):
    def __init__(self, manager, **kwargs):
        super().__init__(**kwargs)
        self.manager = manager
        self.orientation = "horizontal"
        self.size_hint_y = None
        self.height = 72
        self.spacing = 4
        for text, screen in [
            ("🏠\\nAna", "home"),
            ("🏋️\\nSpor", "exercise"),
            ("🚶\\nYürüyüş", "walk"),
            ("📊\\nİlerleme", "progress"),
        ]:
            button = Button(text=text, font_size="15sp")
            button.bind(on_release=lambda _, s=screen: self.switch(s))
            self.add_widget(button)

    def switch(self, screen):
        self.manager.current = screen


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.content = ScreenManager(transition=FadeTransition())
        self.content.add_widget(HomeScreen(name="home"))
        self.content.add_widget(ExerciseScreen(name="exercise"))
        self.content.add_widget(WalkScreen(name="walk"))
        self.content.add_widget(ProgressScreen(name="progress"))
        self.add_widget(self.content)
        self.add_widget(BottomNav(self.content))


class FitnessApp(App):
    title = "Fitzone"

    def build(self):
        self.main = MainLayout()
        if SENSOR_AVAILABLE:
            try:
                accelerometer.enable()
                Clock.schedule_interval(self.check_shake, 0.15)
            except Exception:
                pass
        return self.main

    def check_shake(self, _dt):
        if not SENSOR_AVAILABLE:
            return
        try:
            values = accelerometer.acceleration
            if not values or None in values:
                return
            x, y, z = values
            magnitude = sqrt(x * x + y * y + z * z)
            if magnitude > 19:
                self.main.content.current = "walk"
                walk = self.main.content.get_screen("walk")
                walk.state.text = "🟢 Telefon hareketi algılandı — yürüyüş açıldı!"
        except Exception:
            pass

    def on_stop(self):
        if SENSOR_AVAILABLE:
            try:
                accelerometer.disable()
            except Exception:
                pass


if __name__ == "__main__":
    FitnessApp().run()
