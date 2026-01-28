import arcade
import config

class Pipe(arcade.Sprite):
    def __init__(self, is_flipped=False):
        super().__init__()
        self.texture = arcade.load_texture(config.DIR_IMG / "pipe-green.png")
        if is_flipped:
            self.texture = self.texture.flip_vertically()
        self.proportion = self.texture.width / self.texture.height
        self.vel_x = 200
        self.passed = False
        self.is_lower = not is_flipped

    def update(self, delta_time):
        self.center_x -= self.vel_x * delta_time
        if self.right <= 0:
            self.remove_from_sprite_lists()