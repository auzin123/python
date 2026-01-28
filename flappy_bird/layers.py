import arcade
import config

class ScrollingLayer(arcade.SpriteList):
    def __init__(self, window_width, window_height, texture_name, window_portion, speed):
        super().__init__()
        texture = arcade.load_texture(config.DIR_IMG / texture_name)
        proportion = texture.width / texture.height
        height = window_height * window_portion
        width = height * proportion
        self.sprite_width = width
        self.speed = speed
        
        for i in range(int(window_width / width) + 2):
            sprite = arcade.Sprite(texture)
            sprite.width = width
            sprite.height = height
            sprite.left = i * width
            sprite.bottom = 0
            self.append(sprite)

    def update(self, delta_time):
        for sprite in self:
            sprite.center_x -= self.speed * delta_time
            if sprite.right < 0:
                sprite.left = max(s.left for s in self if s != sprite) + self.sprite_width