from kivy.core.audio import SoundLoader
from kivy.uix.image import Image
from kivy.properties import NumericProperty

bird_flap = SoundLoader.load('assets/audio/flap.wav')


class Bird(Image):
    velocity = NumericProperty(0)
    movable = True

    def on_touch_down(self, touch):
        if self.movable:
            self.source = "assets/image/flap.png"
            self.velocity = 150
            super().on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.movable:
            self.source = "assets/image/idle.png"
            bird_flap.play()
            print("touched!")
            super().on_touch_up(touch)