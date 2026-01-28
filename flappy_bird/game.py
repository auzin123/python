import arcade
import random
import config
from bird import Bird
from pipe import Pipe
from layers import ScrollingLayer

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.bird = Bird(self, (0, 0))
        self.sprites = arcade.SpriteList()
        self.pipes = arcade.SpriteList()
        self.bg = ScrollingLayer(self.window.width, self.window.height, "background-day.png", 1, 100)
        self.ground_height = self.window.height * 0.2
        self.ground = ScrollingLayer(self.window.width, self.window.height, "base.png", 0.2, 100)
        self.music = arcade.load_sound(config.DIR_SOUND / "music.mp3")
        arcade.play_sound(self.music, loop=True, volume=0.05)

        self.pipes_spawn_interval = 4
        self.pipes_spawn_timer = 4
        self.sprites.append(self.bird)

        self.score = 0
        self.score_textures = [arcade.load_texture(config.DIR_IMG / f"{i}.png") for i in range(10)]
        self.score_sprites = arcade.SpriteList()

        self.game_state = "start"
        self.message_texture = arcade.load_texture(config.DIR_IMG / "message.png")
        self.gameover_texture = arcade.load_texture(config.DIR_IMG / "gameover.png")

    def setup(self):
        self.pipes.clear()
        self.bird.coords_initial = (int(self.window.width // 2), int(self.window.height // 2))
        self.bird.height = self.window.height * 0.05
        self.bird.width = self.bird.height * self.bird.proportion
        self.bird.setup()
        self.score = 0
        self.update_score_display()

    def update_score_display(self):
        self.score_sprites.clear()
        score_str = str(self.score)
        digit_width = 60
        total_width = len(score_str) * 70
        x_start = (self.window.width - total_width) / 2 + 30
        for i, digit in enumerate(score_str):
            sprite = arcade.Sprite(self.score_textures[int(digit)])
            sprite.center_x = x_start + i * 70
            sprite.center_y = self.window.height * 0.8
            sprite.width = sprite.height = digit_width
            self.score_sprites.append(sprite)

    def on_draw(self):
        self.clear()
        self.bg.draw()
        self.ground.draw()
        if self.game_state == "playing":
            self.pipes.draw()
            self.sprites.draw()
            self.score_sprites.draw()
        
        if self.game_state == "start":
            arcade.draw_texture_rect(self.message_texture, arcade.LBWH((self.window.width - 184)/2, (self.window.height - 267)/2, 184, 267))
        elif self.game_state == "game_over":
            arcade.draw_texture_rect(self.gameover_texture, arcade.LBWH((self.window.width - 192)/2, (self.window.height - 42)/2, 192, 42))

    def on_update(self, delta_time):
        if self.game_state != "playing":
            return

        if arcade.check_for_collision_with_list(self.bird, self.pipes) or self.bird.bottom <= self.ground_height:
            self.game_state = "game_over"
            arcade.play_sound(self.bird.sound_hit, volume=0.05)
            return

        self.bg.update(delta_time)
        self.ground.update(delta_time)
        self.bird.update(delta_time)
        self.pipes.update(delta_time)

        for pipe in self.pipes:
            if pipe.is_lower and not pipe.passed and self.bird.center_x > pipe.center_x:
                pipe.passed = True
                self.score += 1
                arcade.play_sound(self.bird.sound_point, volume=0.05)
                self.update_score_display()

        self.pipes_spawn_timer += delta_time
        if self.pipes_spawn_timer >= self.pipes_spawn_interval:
            self.spawn_pipes()
            self.pipes_spawn_timer = 0

    def spawn_pipes(self):
        gap = self.bird.height * 3
        shift = random.randint(-100, 100)
        for flipped in [False, True]:
            p = Pipe(is_flipped=flipped)
            p.height = self.window.height * 0.8
            p.width = p.height * p.proportion
            p.left = self.window.width
            if flipped:
                p.bottom = self.window.height * 0.5 + gap / 2 + shift
            else:
                p.top = self.window.height * 0.5 - gap / 2 + shift
            self.pipes.append(p)

    def on_key_press(self, symbol, _):
        if symbol == arcade.key.SPACE:
            if self.game_state == "start":
                self.game_state = "playing"
                self.setup()
            elif self.game_state == "game_over":
                self.game_state = "start"
            else:
                self.bird.jump()