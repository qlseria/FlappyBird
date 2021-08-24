from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from background import Background
from gameover import GameOver
from bird import Bird

from pipe import Pipe

from random import randint

# START ADD: Game Sound Imports
from kivy.core.audio import SoundLoader
death = SoundLoader.load('assets/audio/death.wav')
death_music = SoundLoader.load('assets/audio/death_music.wav')
point = SoundLoader.load('assets/audio/point.wav')
# END ADD

class MainApp(App):
    pipes = []
    GRAVITY = 300
    was_colliding = False

    #def on_start(self):
    #    Clock.schedule_interval(self.root.ids.background.scroll_textures, 1/60.)

    def move_bird(self, time_passed):
        if self.root.ids.bird.movable:
            bird = self.root.ids.bird
            bird.y = bird.y + bird.velocity * time_passed
            bird.velocity = bird.velocity - self.GRAVITY * time_passed
            self.check_collision()

    def check_collision(self):
        bird = self.root.ids.bird
        # Go through each pipe and check if it collides
        is_colliding = False
        for pipe in self.pipes:
            if pipe.collide_widget(bird):
                is_colliding = True
                # Check if bird is between the gap
                if bird.y < (pipe.pipe_center - pipe.GAP_SIZE/2.0):
                    self.game_over()
                if bird.top > (pipe.pipe_center + pipe.GAP_SIZE/2.0):
                    self.game_over()
        if bird.y < 96:
            self.game_over()
        if bird.top > Window.height:
            self.game_over()

        if self.was_colliding and not is_colliding:
            point.play()
            self.root.ids.score.text = str(int(self.root.ids.score.text)+1)
        self.was_colliding = is_colliding

    def game_over(self):
        death.play()
        death_music.play()
        self.root.ids.bird.source = 'assets/image/dead.png'

        self.root.ids.bird.movable = False

        for pipe in self.pipes:
            self.root.remove_widget(pipe)

        self.frames.cancel()

        self.root.ids.start_button.disabled = False
        self.root.ids.start_button.opacity = 1

        self.root.ids.game_over.pos = (0,0)
        self.root.ids.game_over_label.pos = (self.root.center_x-50, self.root.center_y+45)
        self.root.ids.game_over_button.pos = (self.root.center_x-50, self.root.center_y-100)

        self.root.ids.game_over.size_hint_y = 1
        self.root.ids.game_over.opacity = 1
        self.root.ids.game_over.disabled = False

    def game_reset(self):
        self.root.ids.bird.pos = (20, (self.root.height - 96) / 2.0)
        self.root.ids.bird.source = "assets/image/idle.png"
        self.root.ids.game_over.pos = (5000, 5000)
        self.root.ids.game_over_label.pos = (5000, 5000)
        self.root.ids.game_over_button.pos = (5000, 5000)

        self.root.ids.bird.movable = True


    def next_frame(self, time_passed):
        self.move_bird(time_passed)
        self.move_pipes(time_passed)
        self.root.ids.background.scroll_textures(time_passed)

    def start_game(self):
        if self.root.ids.bird.movable:
            self.root.ids.score.text = "0"
            self.was_colliding = False
            self.pipes = []
            #Clock.schedule_interval(self.move_bird, 1/60.)
            self.frames = Clock.schedule_interval(self.next_frame, 1/60.)

            # Create the pipes
            num_pipes = 5
            distance_between_pipes = Window.width / (num_pipes - 1)
            for i in range(num_pipes):
                pipe = Pipe()
                pipe.pipe_center = randint(96 + 100, self.root.height - 100)
                pipe.size_hint = (None, None)
                pipe.pos = (Window.width + i*distance_between_pipes, 96)
                pipe.size = (64, self.root.height - 96)

                self.pipes.append(pipe)
                self.root.add_widget(pipe)

            # Move the pipes
            #Clock.schedule_interval(self.move_pipes, 1/60.)

    def move_pipes(self, time_passed):
        # Move pipes
        for pipe in self.pipes:
            pipe.x -= time_passed * 100

        # Check if we need to reposition the pipe at the right side
        num_pipes = 5
        distance_between_pipes = Window.width / (num_pipes - 1)
        pipe_xs = list(map(lambda pipe: pipe.x, self.pipes))
        right_most_x = max(pipe_xs)
        if right_most_x <= Window.width - distance_between_pipes:
            most_left_pipe = self.pipes[pipe_xs.index(min(pipe_xs))]
            most_left_pipe.x = Window.width











MainApp().run()
