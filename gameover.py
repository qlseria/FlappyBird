from kivy.uix.widget import Widget

class GameOver(Widget):
    def __init__(self, **kwargs):
        self.pos = (5000, 5000)
        super().__init__(**kwargs)