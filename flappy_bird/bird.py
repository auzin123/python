import arcade
import config

class Bird(arcade.Sprite):
    def __init__(self, view, coords: tuple[int, int]):
        super().__init__()
        self.view = view
        self.textures = [
            arcade.load_texture(config.DIR_IMG / "yellowbird-upflap.png"),
            arcade.load_texture(config.DIR_IMG / "yellowbird-midflap.png"),
            arcade.load_texture(config.DIR_IMG / "yellowbird-downflap.png"),
            arcade.load_texture(config.DIR_IMG / "yellowbird-midflap.png"),
        ]
        self.texture_idx = 0
        self.texture = self.textures[self.texture_idx]
        self.proportion = self.texture.width / self.texture.height

        self.coords_initial = coords
        self.vel_min = -400.0
        self.gravity = 900.0
        self.vel_jump = 300.0

        self.animation_timer = 0.0
        self.animation_frame_duration = 0.12

        self.rotation_speed = 200.0
        self.angle_top = -25
        self.angle_bottom = 90

        self.sound_jump = arcade.load_sound(config.DIR_SOUND / "wing.ogg")
        self.sound_die = arcade.load_sound(config.DIR_SOUND / "die.ogg")
        self.sound_hit = arcade.load_sound(config.DIR_SOUND / "hit.ogg")
        self.sound_point = arcade.load_sound(config.DIR_SOUND / "point.ogg")

    def setup(self):
        self.center_x, self.center_y = self.coords_initial
        self.vel_y = 0.0
        self.angle = 0
        self.is_active = True

    def update(self, delta_time):
        if not self.is_active:
            return
        self.vel_y = max(self.vel_y - self.gravity * delta_time, self.vel_min)
        self.center_y += self.vel_y * delta_time
        
        if self.top > self.view.height:
            self.top = self.view.height
            
        self.animate(delta_time)
        self.rotate(delta_time)

    def jump(self):
        self.vel_y = self.vel_jump
        arcade.play_sound(self.sound_jump, volume=0.05)

    def animate(self, delta_time):
        self.animation_timer += delta_time
        if self.animation_timer >= self.animation_frame_duration:
            self.animation_timer = 0
            self.texture_idx = (self.texture_idx + 1) % len(self.textures)
            self.texture = self.textures[self.texture_idx]

    def rotate(self, delta_time):
        if self.vel_y > 0:
            self.angle = self.angle_top
        else:
            angle_delta = self.angle_bottom - self.angle
            step = self.rotation_speed * delta_time
            if abs(angle_delta) < step:
                self.angle = self.angle_bottom
            else:
                self.angle += step